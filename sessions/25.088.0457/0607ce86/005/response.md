```python
import numpy as np
from scipy.ndimage import label, find_objects
from collections import Counter

"""
Identifies repeating block patterns in an input grid, potentially obscured by noise pixels (green=3). 
It first identifies all connected components of non-background (white=0) pixels, including noise pixels. 
It determines the most frequent bounding box size among these components. Then, it extracts full block 
instances (including any noise pixels within them) from the original grid at the locations corresponding 
to the common-sized components. A "canonical" pattern for this block size is derived by finding the most 
frequent non-noise, non-background color at each position across all instances. If only noise and/or 
background pixels are present at a position, noise becomes the canonical color if it was present, otherwise 
background. Finally, it constructs an output grid containing only these block instances, placed at their 
original locations. Within each placed block, pixels that were noise (green=3) in the input are replaced 
by the corresponding canonical pixel, but only if the canonical pixel itself is not noise (green=3). 
All pixels outside the placed blocks are set to background (white=0).
"""

def _find_blocks_and_derive_pattern(grid, background_color=0, noise_color=3):
    """
    Finds potential pattern blocks (including noise), determines the most 
    common bounding box size, extracts full block instances of that size from 
    the original grid, and infers the canonical pattern.

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
    # 1. Identify Potential Pattern Blocks: Create a mask for all non-background pixels
    component_mask = (grid != background_color)
    
    # Label connected components of these potential structures
    labeled_grid, num_labels = label(component_mask)
    
    # 2. Determine bounding boxes for components
    objects_slices = find_objects(labeled_grid)

    if not objects_slices: # Handle cases with no components
        return None, None, [], []

    # Calculate sizes and locations based on component bounding boxes
    sizes = []
    locations = [] # Store top-left corner (r_start, c_start)
    component_indices = [] # Store index corresponding to size/location
    
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
            component_indices.append(i) # Keep track of which original component this is

    if not sizes:
        return None, None, [], []

    # 3. Find Dominant Block Size
    size_counts = Counter(sizes)
    if not size_counts:
         return None, None, [], []
    # Find the most common size based on components
    # If there's a tie, Counter picks one arbitrarily, which is acceptable here.
    most_common_size = size_counts.most_common(1)[0][0]
    common_height, common_width = most_common_size

    # 4. Extract Valid Instances from *original grid* based on common size and locations
    valid_instances = []
    valid_locations = []
    grid_height, grid_width = grid.shape
    
    processed_locations = set() # Avoid processing overlapping components leading to same instance extraction

    for i, size in enumerate(sizes):
        if size == most_common_size:
            r_start, c_start = locations[i]
            
            # Ensure the instance extraction uses the *determined common size*, not necessarily the 
            # component's exact bounding box if it was slightly off but classified as common.
            # Also check if the block fits within the grid using the common size.
            if r_start + common_height <= grid_height and c_start + common_width <= grid_width:
                 # Check if this location has essentially been processed already 
                 # (e.g., if two components are within the same target block area)
                 # We only store one instance per top-left corner of the common size block
                 if (r_start, c_start) not in processed_locations:
                    instance = grid[r_start : r_start + common_height, c_start : c_start + common_width]
                    # Double check extracted shape just in case (should match common_size)
                    if instance.shape == most_common_size:
                        valid_instances.append(instance)
                        valid_locations.append((r_start, c_start))
                        processed_locations.add((r_start, c_start))
            # else: # Optional: log if a potential block is cut off by grid edge
                # print(f"Component at {locations[i]} suggests block size {most_common_size}, but instance doesn't fit grid.")


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
            
            if core_color_counts:
                # 4.c: If non-noise, non-background colors exist, find the most frequent among them
                most_frequent_core_color = max(core_color_counts, key=core_color_counts.get)
                canonical_pattern[r, c] = most_frequent_core_color
            elif noise_color in color_counts:
                 # 4.d: If only noise and/or background are present, and noise is present, canonical is noise
                 canonical_pattern[r, c] = noise_color
            # 4.e: Otherwise (only background was present), it remains background (due to initialization)


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

    # Steps 1-5: Find components, common size, extract instances, derive canonical pattern
    canonical_pattern, common_size, block_locations, block_instances = \
        _find_blocks_and_derive_pattern(input_np, background_color, noise_color)

    # 5.a: Initialize output grid with background color
    output_grid = np.full((height, width), background_color, dtype=int)

    # If no consistent blocks were found, return the empty background grid
    if canonical_pattern is None or not block_locations:
        return output_grid.tolist()

    block_height, block_width = common_size

    # 5.b: Iterate through the stored valid instances and locations
    for idx, (r_start, c_start) in enumerate(block_locations):
        # 5.c: Process each instance
        instance = block_instances[idx] # Get the original block instance content
        
        # 5.c.i: Create a temporary block to store the repaired version
        repaired_block = np.copy(instance)

        # 5.c.ii: Iterate through each pixel of the instance to apply repair logic
        for r in range(block_height):
            for c in range(block_width):
                # 5.c.iii: Get original and canonical pixel values
                original_pixel = instance[r, c]
                canonical_pixel = canonical_pattern[r, c]

                # 5.c.v: Repair Rule: Replace input pixel if it's noise AND canonical is NOT noise
                if original_pixel == noise_color and canonical_pixel != noise_color:
                    repaired_block[r, c] = canonical_pixel
                # Otherwise, repaired_block[r, c] retains the value from the copied instance

        # 5.c.vi: Place the (potentially) repaired block onto the output grid
        # Ensure placement doesn't exceed output grid bounds (shouldn't happen if extraction was correct)
        end_row = min(r_start + block_height, height)
        end_col = min(c_start + block_width, width)
        output_grid[r_start : end_row, c_start : end_col] = repaired_block[0:(end_row-r_start), 0:(end_col-c_start)]


    # Step 6: Return the final grid as a list of lists
    return output_grid.tolist()
```