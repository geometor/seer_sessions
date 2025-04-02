import numpy as np

"""
Transforms a 1xN input grid based on the following rule:
1. Identify the first contiguous block of a non-white color (C1) in the row.
2. Identify the very next non-white pixel (C2) that appears after this block ends.
3. If the sequence of pixels strictly between the end of block C1 and the position of pixel C2 
   consists entirely of white pixels (0), this sequence (the "gap") is filled with the color C1.
4. Otherwise, the sequence remains unchanged.
The input and output are NumPy arrays of shape (1, N).
"""

def find_first_non_white_block(row):
    """
    Finds the start index, end index, and color of the first contiguous 
    non-white block in a 1D sequence (list or NumPy array).

    Args:
        row: A list or 1D NumPy array of integers representing pixel colors.

    Returns:
        A tuple (start_index, end_index, color) if a block is found, 
        otherwise (None, None, None). Returns indices relative to the input row.
    """
    start_index = -1
    end_index = -1
    color = -1
    in_block = False
    
    for i, pixel in enumerate(row):
        # Start of a new non-white block
        if pixel != 0 and not in_block:
            start_index = i
            end_index = i 
            color = pixel
            in_block = True
        # Continuation of the current block
        elif pixel == color and in_block:
            end_index = i
        # End of the current block (different color or white encountered)
        elif pixel != color and in_block:
            # We found the first block, stop searching
            break 
            
    if start_index == -1:
        # No non-white block found at all
        return None, None, None
    else:
        # Return the details of the first block found
        return start_index, end_index, color

def find_next_non_white_pixel(row, start_search_index):
    """
    Finds the index and color of the first non-white pixel at or after 
    a given starting index in a 1D sequence (list or NumPy array).

    Args:
        row: A list or 1D NumPy array of integers representing pixel colors.
        start_search_index: The index from which to start searching (inclusive).

    Returns:
        A tuple (index, color) if a non-white pixel is found, 
        otherwise (None, None). Returns index relative to the input row.
    """
    # Ensure start index is within bounds
    if start_search_index >= len(row):
        return None, None
        
    for i in range(start_search_index, len(row)):
        if row[i] != 0:
            return i, row[i] # Found the next non-white pixel
            
    return None, None # No non-white pixel found after the start index

def transform(input_grid):
    """
    Applies the transformation rule to fill the gap between the first non-white 
    block and the next non-white pixel if the gap is white.

    Args:
        input_grid: A 2D NumPy array of shape (1, N) representing the input grid.

    Returns:
        A 2D NumPy array of shape (1, N) representing the transformed grid.
    """
    # 1. Validate input shape (optional but good practice for robustness)
    if not isinstance(input_grid, np.ndarray) or input_grid.ndim != 2 or input_grid.shape[0] != 1:
        # Handle error or return input unchanged, depending on requirements
        # For ARC, inputs usually conform, so returning input might be sufficient
        # print("Warning: Input grid is not a 1xN NumPy array. Returning unchanged.")
        return input_grid

    # 2. Extract the single row from the input grid
    input_row = input_grid[0]
    
    # 3. Create a mutable copy of this 1D pixel sequence
    output_row = list(input_row) # Convert to list for easy modification
    row_len = len(output_row)

    # 4. Find the first non-white block (C1).
    start_C1, end_C1, color_C1 = find_first_non_white_block(output_row)

    # 5. If no non-white block is found, no transformation needed.
    if start_C1 is None:
        # 11 & 12. Return the original grid (already in correct format).
        return input_grid # Return original numpy array

    # 6. Find the next non-white pixel (C2) after the first block.
    search_start_index_C2 = end_C1 + 1
    index_C2, color_C2 = find_next_non_white_pixel(output_row, search_start_index_C2)

    # 7. If no second non-white pixel is found, no transformation needed.
    if index_C2 is None:
        # 11 & 12. Return the original grid.
        return input_grid

    # 8. Define the potential 'gap' region indices.
    gap_start_index = end_C1 + 1
    gap_end_index = index_C2 - 1 # Inclusive end index for checking/filling

    # 9. Check if the gap region exists and if all pixels within it are white (0).
    gap_exists_and_is_white = False
    if gap_start_index <= gap_end_index: # Check if gap indices are valid
        is_gap_white = True
        for i in range(gap_start_index, gap_end_index + 1):
            if output_row[i] != 0:
                is_gap_white = False
                break
        if is_gap_white:
            gap_exists_and_is_white = True

    # 10. If the gap exists and is white, fill it with color C1.
    if gap_exists_and_is_white:
        for i in range(gap_start_index, gap_end_index + 1):
            output_row[i] = color_C1

    # 11. Reshape the final 1D sequence back into a 1xN NumPy array.
    # Convert the modified list back to a NumPy array and reshape.
    output_grid = np.array(output_row).reshape(1, row_len)

    # 12. Return the resulting output grid.
    return output_grid