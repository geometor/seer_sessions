import numpy as np
from scipy.ndimage import label, find_objects
from collections import Counter

"""
Identifies repeating block structures in the input grid, ignoring scattered
noise pixels (green=3). It determines the most common block size and infers
a 'canonical' pattern for blocks of this size by finding the most frequent
non-noise color at each position across all instances. It then constructs
an output grid containing only these blocks, where any green pixels within
a block instance that deviate from the inferred canonical pattern are
replaced by the canonical color at that position. All other pixels (background,
scattered noise, blocks of non-standard size) are set to background (white=0).
"""

def _find_blocks_and_derive_pattern(grid, background_color=0, noise_color=3):
    """
    Finds non-background connected components, determines the most common
    bounding box size, extracts blocks of that size, and infers the
    canonical pattern.

    Args:
        grid (np.array): Input grid.
        background_color (int): Color representing the background.
        noise_color (int): Color representing noise pixels to be potentially repaired.

    Returns:
        tuple: (canonical_pattern, common_size, valid_locations, valid_blocks)
               - canonical_pattern (np.array or None): The inferred pattern.
               - common_size (tuple or None): The (height, width) of common blocks.
               - valid_locations (list): List of (row, col) top-left corners.
               - valid_blocks (list): List of original np.array subgrids corresponding
                                      to valid_locations.
               Returns (None, None, [], []) if no common blocks are found.
    """
    # Label connected components of non-background pixels
    labeled_grid, num_labels = label(grid != background_color)
    # Find the bounding box slices for each labeled component
    objects_slices = find_objects(labeled_grid)

    blocks = []
    locations = []
    sizes = []

    if not objects_slices: # Handle empty or all-background grids
        return None, None, [], []

    # Extract blocks based on bounding boxes and record sizes/locations
    for i, slc in enumerate(objects_slices):
        if slc is None: # Might happen with empty labels
             continue
        r_start, r_stop = slc[0].start, slc[0].stop
        c_start, c_stop = slc[1].start, slc[1].stop
        height = r_stop - r_start
        width = c_stop - c_start

        # Extract the subgrid defined by the bounding box
        subgrid_bbox = grid[r_start:r_stop, c_start:c_stop]

        # Only store if the extracted subgrid is not empty
        if subgrid_bbox.size > 0:
            blocks.append(subgrid_bbox)
            locations.append((r_start, c_start))
            sizes.append((height, width))

    if not sizes:
        return None, None, [], []

    # Find the most common block size (dimensions)
    size_counts = Counter(sizes)
    if not size_counts:
         return None, None, [], []
    most_common_size = size_counts.most_common(1)[0][0]
    block_height, block_width = most_common_size

    # Filter blocks and locations to keep only those matching the most common size
    valid_blocks = []
    valid_locations = []
    for i, size in enumerate(sizes):
        if size == most_common_size:
            # Double check the shape of the extracted block
            if blocks[i].shape == most_common_size:
                 valid_blocks.append(blocks[i])
                 valid_locations.append(locations[i])

    if not valid_blocks:
        # If no blocks match the most common size after shape check (unlikely but possible)
        return None, None, [], []

    # Infer the canonical pattern from the valid blocks
    canonical_pattern = np.full((block_height, block_width), background_color, dtype=int)
    num_valid_blocks = len(valid_blocks)

    for r in range(block_height):
        for c in range(block_width):
            # Collect colors at this position (r, c) from all valid blocks
            pixel_colors = [block[r, c] for block in valid_blocks if r < block.shape[0] and c < block.shape[1]] # Safety check
            if not pixel_colors: continue # Should not happen with current logic

            color_counts = Counter(pixel_colors)

            # Separate counts for noise vs non-noise colors
            non_noise_counts = {color: count for color, count in color_counts.items() if color != noise_color}

            if non_noise_counts:
                # If non-noise colors exist, find the most frequent among them
                most_frequent_non_noise = max(non_noise_counts, key=non_noise_counts.get)
                canonical_pattern[r, c] = most_frequent_non_noise
            elif color_counts:
                # If only noise or background colors are present, take the most frequent overall
                most_frequent_overall = color_counts.most_common(1)[0][0]
                canonical_pattern[r, c] = most_frequent_overall
            # else: # If color_counts is somehow empty, it defaults to background_color

    return canonical_pattern, most_common_size, valid_locations, valid_blocks


def transform(input_grid):
    """
    Identifies repeating block structures, infers a canonical pattern, repairs
    noise pixels within blocks based on this pattern, and constructs the output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    background_color = 0
    noise_color = 3

    # Step 1: Find blocks, determine the common size, extract instances, and infer the canonical pattern
    canonical_pattern, common_size, block_locations, original_blocks = \
        _find_blocks_and_derive_pattern(input_np, background_color, noise_color)

    # Step 2: Initialize the output grid with the background color
    output_grid = np.full((height, width), background_color, dtype=int)

    # Step 3: If no consistent blocks were found, return the empty background grid
    if canonical_pattern is None or not block_locations:
        return output_grid.tolist()

    block_height, block_width = common_size

    # Step 4: Iterate through each identified block instance
    for idx, (r, c) in enumerate(block_locations):
        input_subgrid = original_blocks[idx] # Get the original block content

        # Basic sanity check (should already be filtered by the helper function)
        if input_subgrid.shape != (block_height, block_width):
             continue

        # Create a copy of the input subgrid to modify for the output
        repaired_subgrid = np.copy(input_subgrid)

        # Step 5: Repair the subgrid based on the canonical pattern
        for i in range(block_height):
            for j in range(block_width):
                input_pixel = input_subgrid[i, j]
                canonical_pixel = canonical_pattern[i, j]

                # The core repair rule:
                # If the pixel in the input block is the noise color (3)
                # AND it differs from the corresponding pixel in the canonical pattern,
                # then replace it with the canonical pattern's pixel.
                if input_pixel == noise_color and input_pixel != canonical_pixel:
                    repaired_subgrid[i, j] = canonical_pixel
                # Otherwise, the pixel remains as it was in the input_subgrid (already copied to repaired_subgrid)

        # Step 6: Place the (potentially) repaired subgrid onto the output grid
        # Ensure placement doesn't go out of bounds (shouldn't happen if locations are correct)
        end_r, end_c = r + block_height, c + block_width
        if end_r <= height and end_c <= width:
             output_grid[r:end_r, c:end_c] = repaired_subgrid
        # else: # Log error if placement is out of bounds
             # print(f"Warning: Block placement at ({r},{c}) with size {common_size} exceeds grid bounds ({height},{width})")


    # Step 7: Return the final grid as a list of lists
    return output_grid.tolist()