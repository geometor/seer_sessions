import numpy as np
from scipy.ndimage import label, find_objects
from collections import Counter

"""
The transformation identifies repeating rectangular patterns (blocks) within the input grid, which may be corrupted by noise pixels (green=3). It cleans these blocks based on a derived 'canonical' pattern and removes any elements outside these blocks.

1.  **Identify Core Structures:** Find connected components of pixels that are *neither* background (white=0) *nor* noise (green=3). These represent the stable parts of the patterns.
2.  **Determine Common Block Size:** Calculate the bounding box size for each core structure. Identify the most frequently occurring size. This is assumed to be the size of the repeating pattern block.
3.  **Locate Pattern Instances:** Find the top-left corner coordinates of all core structures whose bounding box matches the common size.
4.  **Extract Noisy Instances:** Using the locations from step 3 and the common block size, extract the corresponding rectangular regions from the *original input grid*. These are the potentially noisy instances of the pattern.
5.  **Derive Canonical Pattern:** Create a template pattern of the common block size. For each position (row, col) within the block:
    a.  Collect the colors found at that position across all extracted noisy instances.
    b.  Count the occurrences of each color.
    c.  Determine the canonical color for this position:
        i.  Find the most frequent color that is *not* noise (3) and *not* background (0). If such a color exists, it becomes the canonical color.
        ii. If only noise and/or background colors were found, the canonical color becomes noise (3) if noise was present at least once.
        iii. Otherwise (only background was present), the canonical color is background (0).
6.  **Reconstruct Output Grid:**
    a.  Initialize an output grid of the same size as the input, filled with the background color (0).
    b.  For each located pattern instance (using the locations from step 3):
        i.  Get the corresponding noisy instance extracted in step 4.
        ii. Create a 'repaired' block, initially a copy of the noisy instance.
        iii. Iterate through each pixel (row, col) within this block.
        iv. If the pixel in the noisy instance is noise (3) *and* the corresponding pixel in the canonical pattern is *not* noise (3), replace the pixel in the 'repaired' block with the canonical pixel value.
        v.  Place this 'repaired' block onto the output grid at its original location.
7.  Return the final output grid. Pixels outside the identified and repaired blocks remain background.
"""

def _find_blocks_and_derive_pattern(grid, background_color=0, noise_color=3):
    """
    Finds potential pattern blocks based on non-noise/non-background pixels, 
    determines the most common bounding box size, extracts full block instances 
    (including noise) of that size from the original grid, and infers the 
    canonical pattern.

    Args:
        grid (np.array): Input grid.
        background_color (int): Color representing the background.
        noise_color (int): Color representing noise pixels.

    Returns:
        tuple: (canonical_pattern, common_size, valid_locations, valid_instances)
               - canonical_pattern (np.array or None): The inferred pattern.
               - common_size (tuple or None): The (height, width) of common blocks.
               - valid_locations (list): List of (row, col) top-left corners.
               - valid_instances (list): List of original np.array subgrids corresponding
                                        to valid_locations.
               Returns (None, None, [], []) if no common blocks are found.
    """
    grid_height, grid_width = grid.shape
    
    # 1. Identify Core Structures: Mask for non-background and non-noise pixels
    core_mask = (grid != background_color) & (grid != noise_color)
    
    # Label connected components of these core structures
    labeled_grid, num_labels = label(core_mask)
    
    # 2. Determine bounding boxes for core components
    objects_slices = find_objects(labeled_grid)

    if not objects_slices: # Handle cases with no core components
        return None, None, [], []

    # Calculate sizes and locations based on core component bounding boxes
    sizes = []
    locations = [] # Store top-left corner (r_start, c_start)
    
    for i, slc in enumerate(objects_slices):
        if slc is None: 
            continue
        # Ensure the slices are valid tuples of slice objects
        if not (isinstance(slc, tuple) and len(slc) == 2 and 
                isinstance(slc[0], slice) and isinstance(slc[1], slice)):
             continue # Skip invalid slice formats

        r_start, r_stop = slc[0].start, slc[0].stop
        c_start, c_stop = slc[1].start, slc[1].stop
        height = r_stop - r_start
        width = c_stop - c_start
        
        # Store size and location if the slice is valid
        if height > 0 and width > 0:
            sizes.append((height, width))
            locations.append((r_start, c_start))

    if not sizes:
        return None, None, [], []

    # 3. Find Dominant Block Size (based on core components)
    size_counts = Counter(sizes)
    if not size_counts:
         return None, None, [], []
    most_common_size = size_counts.most_common(1)[0][0]
    common_height, common_width = most_common_size

    # 4. Extract Valid Noisy Instances from *original grid* based on common size and locations
    valid_instances = []
    valid_locations = []
    
    processed_locations = set() # Avoid storing duplicate instances if core components overlap conceptually

    for i, size in enumerate(sizes):
        if size == most_common_size:
            r_start, c_start = locations[i]
            
            # Check if the block fits within the grid using the *common size*.
            if r_start + common_height <= grid_height and c_start + common_width <= grid_width:
                 # Check if this location has essentially been processed already 
                 # We only store one instance per top-left corner of the common size block
                 if (r_start, c_start) not in processed_locations:
                    # Extract from the ORIGINAL grid to include noise
                    instance = grid[r_start : r_start + common_height, c_start : c_start + common_width]
                    # Double check extracted shape just in case
                    if instance.shape == most_common_size:
                        valid_instances.append(instance)
                        valid_locations.append((r_start, c_start))
                        processed_locations.add((r_start, c_start))

    if not valid_instances:
        # No instances matching the most common size could be extracted
        return None, None, [], []

    # 5. Derive Canonical Pattern
    canonical_pattern = np.full(most_common_size, background_color, dtype=int) # Initialize with background
    num_valid_instances = len(valid_instances)

    for r in range(common_height):
        for c in range(common_width):
            # Collect colors at this position (r, c) from all valid instances
            pixel_colors = [instance[r, c] for instance in valid_instances]
            if not pixel_colors: continue 

            color_counts = Counter(pixel_colors)

            # Separate counts for non-noise, non-background colors
            core_color_counts = {
                color: count for color, count in color_counts.items() 
                if color != noise_color and color != background_color
            }
            
            # 5.c.i: Find most frequent non-noise, non-background color
            if core_color_counts:
                most_frequent_core_color = max(core_color_counts, key=core_color_counts.get)
                canonical_pattern[r, c] = most_frequent_core_color
            # 5.c.ii: If only noise/background, check if noise exists
            elif noise_color in color_counts:
                 canonical_pattern[r, c] = noise_color
            # 5.c.iii: Otherwise, it remains background (due to initialization)


    return canonical_pattern, most_common_size, valid_locations, valid_instances


def transform(input_grid):
    """
    Transforms the input grid by identifying repeating patterns (including noise), 
    deriving a canonical form, repairing noise within pattern instances based on the
    canonical form, and reconstructing the grid with only these repaired instances.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    background_color = 0
    noise_color = 3

    # Steps 1-5: Find core components, common size, extract noisy instances, derive canonical pattern
    canonical_pattern, common_size, block_locations, block_instances = \
        _find_blocks_and_derive_pattern(input_np, background_color, noise_color)

    # 6.a: Initialize output grid with background color
    output_grid = np.full((height, width), background_color, dtype=int)

    # If no consistent blocks were found, return the empty background grid
    if canonical_pattern is None or not block_locations:
        return output_grid.tolist()

    block_height, block_width = common_size

    # 6.b: Iterate through the located instances
    for idx, (r_start, c_start) in enumerate(block_locations):
        # 6.b.i: Get the original noisy block instance content
        instance = block_instances[idx] 
        
        # 6.b.ii: Create a temporary block to store the repaired version
        repaired_block = np.copy(instance)

        # 6.b.iii: Iterate through each pixel of the instance to apply repair logic
        for r in range(block_height):
            for c in range(block_width):
                # Get original and canonical pixel values
                original_pixel = instance[r, c]
                canonical_pixel = canonical_pattern[r, c]

                # 6.b.iv: Repair Rule: Replace input pixel if it's noise AND canonical is NOT noise
                if original_pixel == noise_color and canonical_pixel != noise_color:
                    repaired_block[r, c] = canonical_pixel
                # Otherwise, repaired_block[r, c] retains the value from the copied instance (which was the original noisy pixel)

        # 6.b.v: Place the (potentially) repaired block onto the output grid
        # Ensure placement doesn't exceed output grid bounds 
        end_row = min(r_start + block_height, height)
        end_col = min(c_start + block_width, width)
        # Ensure the slice of the repaired block matches the target area size
        output_grid[r_start : end_row, c_start : end_col] = repaired_block[0:(end_row-r_start), 0:(end_col-c_start)]

    # Step 7: Return the final grid as a list of lists
    return output_grid.tolist()