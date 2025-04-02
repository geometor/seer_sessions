import numpy as np

"""
Transforms a 1D grid by finding a specific pattern and modifying it.
The pattern consists of a contiguous block of a non-white, non-blue color (source_block), 
followed immediately by a contiguous block of white pixels (gap_block), 
followed immediately by a single blue pixel (boundary_pixel).
The transformation replaces the white pixels in the gap_block with the color 
of the source_block. All other pixels remain unchanged.
"""

def transform(input_grid):
    """
    Applies the described transformation to a 1D input grid.

    Args:
        input_grid (list): A list of integers representing the 1D grid.

    Returns:
        list: The transformed 1D grid as a list of integers.
    """

    # Convert input list to a numpy array for easier manipulation
    # Assuming input is always a flat list based on examples
    grid = np.array(input_grid, dtype=int)
    
    # Create a copy of the grid to modify and return
    output_grid = grid.copy()

    # 1. Find the index of the blue pixel (1)
    # np.where returns a tuple of arrays, get the first array for indices
    blue_indices = np.where(grid == 1)[0] 
    
    # If no blue pixel is found, or it's the first element, no transformation is possible
    if len(blue_indices) == 0:
        return input_grid # Return original list
    
    # Assume only one blue pixel based on examples
    blue_idx = blue_indices[0] 
    
    if blue_idx == 0:
         return input_grid # Cannot have blocks before it

    # 2. & 3. Identify the contiguous block of white pixels (0) 
    #          immediately preceding the blue pixel.
    # Start searching leftwards from the pixel just before the blue one.
    gap_end_idx = blue_idx - 1
    current_idx = gap_end_idx
    
    # Scan left while the pixel is white (0) and we are within grid bounds
    while current_idx >= 0 and grid[current_idx] == 0:
        current_idx -= 1
        
    # The actual start index of the white gap is one position to the right 
    # of the last non-white pixel encountered (or index 0 if the gap starts there).
    gap_start_idx = current_idx + 1
    
    # Calculate the number of white pixels (length of the gap)
    gap_length = blue_idx - gap_start_idx

    # 4. If a gap exists (gap_length > 0), identify the color of the pixel 
    #    immediately preceding the white gap.
    if gap_length > 0:
        # Check if there's a pixel before the gap starts
        if gap_start_idx > 0:
            source_color_idx = gap_start_idx - 1
            source_color = grid[source_color_idx]
            
            # Check if this color meets the criteria (non-white, non-blue)
            # Although the NL description implies a block, we only need the color
            # from the pixel immediately preceding the gap based on the examples.
            if source_color != 0 and source_color != 1:
                # 5. Modify the output grid: Change the color of the N white pixels
                #    identified in step 3 to the source_color.
                # Slicing range is [start, end), so use gap_start_idx and blue_idx
                output_grid[gap_start_idx:blue_idx] = source_color
        # Else: The white gap starts at the beginning of the grid (index 0).
        # There is no preceding source block, so no change is made.

    # 6. Leave all other pixels unchanged (already handled by copying).
    
    # 7. Return the modified grid as a list.
    return output_grid.tolist()