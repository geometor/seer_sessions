"""
Transformation Rule:
Identify the first occurrence (scanning left-to-right) of a specific pattern in the 1D input grid: a single non-white pixel (Color A) immediately followed by a contiguous block of one or more pixels of a different non-white color (Color B). The 'single' characteristic of Pixel A means it must be either at the very beginning of the grid (index 0) or immediately preceded by a white pixel (color 0).

If this pattern is found, perform a positional swap on a copy of the grid:
1.  The contiguous block (Color B) is moved one position to the left, so it starts at the original index of Pixel A.
2.  Pixel A (Color A) is moved to the position immediately following the original end position of Block B. This target index is calculated as `original_index_of_A + length_of_block_B`.

All other pixels (background white pixels, and any pixels not part of the first matched pattern instance) remain unchanged. If the specified pattern is not found anywhere in the grid, the output grid is an identical copy of the input grid.
"""

import copy
# Using numpy is not strictly necessary for this 1D task, 
# but it's often useful in ARC. Let's include it for potential future use
# or if the input format assumes numpy arrays, though the code below uses list indexing.
import numpy as np 

def find_pattern_indices(grid):
    """
    Scans the grid to find the first occurrence of the pattern: 
    a single pixel (A) followed immediately by a block (B).
    'Single' means preceded by 0 or at index 0. A and B must be non-zero and different.

    Args:
        grid: A list of integers representing the 1D grid row.

    Returns:
        A tuple (single_pixel_index, block_start_index, block_end_index) 
        if the pattern is found, otherwise None.
    """
    n = len(grid)
    # Iterate through possible start positions of block B (index i)
    # This means pixel A would be at i-1. The loop range ensures i-1 and i are valid indices.
    for i in range(1, n): 
        color_a = grid[i-1] # Potential single pixel A
        color_b = grid[i]   # Potential start of block B

        # Check primary conditions: A and B are non-white (non-zero) and different
        if color_a != 0 and color_b != 0 and color_a != color_b:
            
            # Check if grid[i-1] (Color A) meets the 'single pixel' condition:
            # It's either at the very start (i-1 == 0, which means i == 1) 
            # or preceded by white (grid[i-2] == 0).
            is_single_pixel_a = (i == 1 or grid[i-2] == 0)
            
            # If all conditions for the pattern start are met
            if is_single_pixel_a:
                single_pixel_index = i - 1
                block_start_index = i
                
                # Find the end of the contiguous block of Color B
                block_end_index = block_start_index
                # Keep extending the end index as long as we are within bounds 
                # and the next pixel has the same color B
                while block_end_index + 1 < n and grid[block_end_index + 1] == color_b:
                    block_end_index += 1
                    
                # Pattern found, return the relevant indices. We only need the first match.
                return single_pixel_index, block_start_index, block_end_index
                
    # If the loop completes without finding the pattern
    return None 

def transform(input_grid):
    """
    Applies the described swap transformation to the input grid row.
    """
    # Initialize output_grid as a deep copy to avoid modifying the input directly
    # and to handle the case where no pattern is found.
    output_grid = copy.deepcopy(input_grid)
    
    # Use the helper function to find the indices of the first matching pattern (if it exists)
    pattern_indices = find_pattern_indices(input_grid)

    # Proceed with transformation only if the pattern was found
    if pattern_indices:
        # Unpack the indices returned by the helper function
        single_pixel_index, block_start_index, block_end_index = pattern_indices
        
        # Extract the actual colors involved in the pattern from the input grid
        color_a = input_grid[single_pixel_index]
        color_b = input_grid[block_start_index]
        
        # Calculate the length of the block B based on its start and end indices
        block_length = block_end_index - block_start_index + 1

        # --- Perform the swap in the output grid ---
        
        # 1. Place the block B starting at the single pixel's original index (single_pixel_index)
        # Iterate 'block_length' times to place each pixel of block B
        for k in range(block_length):
            # Calculate the target index in the output grid for the k-th pixel of block B
            target_index = single_pixel_index + k
            # Assign color B to this target index in the output grid
            output_grid[target_index] = color_b
            
        # 2. Place the single pixel A immediately after the block's new position.
        # The block B now occupies indices from single_pixel_index to single_pixel_index + block_length - 1.
        # Therefore, pixel A goes into the next index in the output grid.
        target_index_a = single_pixel_index + block_length
        # We assume based on the problem structure that this index will be valid within the grid bounds.
        output_grid[target_index_a] = color_a

        # Return the modified grid. Since we only transform the first found pattern, we return now.
        return output_grid

    # If pattern_indices was None (pattern not found), return the unmodified copy of the input grid.
    return output_grid