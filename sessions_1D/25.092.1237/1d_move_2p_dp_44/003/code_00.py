import numpy as np

"""
Transformation Rule:
1. Determine if the input grid is effectively 1-dimensional (1xN or Nx1). If not, return the input unchanged.
2. Extract the 1D sequence of pixels from the grid.
3. Identify the first contiguous block (one or more adjacent pixels) of non-white (non-zero color) pixels starting from the beginning of the sequence.
4. Identify the contiguous block of white (zero color) pixels that starts immediately after the end of the non-white block found in step 3.
5. If both blocks are successfully identified, construct a new sequence by rearranging the parts:
    a. Any leading white pixels (before the first non-white block).
    b. The identified white block.
    c. The identified non-white block.
    d. Any remaining pixels after the white block.
6. If either block is not found as described, the sequence remains unchanged.
7. Reconstruct the output grid with the same dimensions (shape) as the input grid, using the potentially modified sequence.
"""

def find_first_non_white_block(sequence: np.ndarray) -> tuple[int, int]:
    """
    Finds the start and end indices of the first contiguous block of 
    non-white (non-zero) pixels in a 1D sequence.
    Returns (-1, -1) if no non-white block is found.
    """
    start_index = -1
    n = len(sequence)

    # Find the start index of the first non-zero pixel
    for i in range(n):
        if sequence[i] != 0:
            start_index = i
            break

    # If no non-white pixel is found, return (-1, -1)
    if start_index == -1:
        return -1, -1 

    # Find the end index of this non-white block
    end_index = start_index
    for i in range(start_index + 1, n):
        if sequence[i] != 0:
            end_index = i
        else:
            # Block ends when a zero or the end of sequence is encountered
            break 

    return start_index, end_index

def find_subsequent_white_block(sequence: np.ndarray, start_search_index: int) -> tuple[int, int]:
    """
    Finds the start and end indices of the contiguous block of white (zero) 
    pixels starting exactly at start_search_index in a 1D sequence.
    Returns (-1, -1) if no white block starts at that index or if the index is out of bounds.
    """
    start_index = -1
    n = len(sequence)

    # Check if the search starts within bounds and the pixel is white (0)
    if start_search_index >= n or sequence[start_search_index] != 0:
        return -1, -1 # No white block starts immediately after, or out of bounds

    start_index = start_search_index
    end_index = start_index

    # Find the end index of this white block
    for i in range(start_index + 1, n):
        if sequence[i] == 0:
            end_index = i
        else:
            # Block ends when a non-zero or the end of sequence is encountered
            break 

    return start_index, end_index

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the transformation rule to the input grid.
    Identifies the first non-white block and the immediately following white block
    in the effective 1D sequence, swaps their positions, and reconstructs the grid.
    """
    
    # Make a copy to avoid modifying the original input
    output_grid = input_grid.copy()
    rows, cols = output_grid.shape
    
    sequence = None
    is_row_vector = False
    original_shape = output_grid.shape

    # Check if the grid is effectively 1D (1xN or Nx1) and extract the sequence
    if rows == 1:
        sequence = output_grid[0, :]
        is_row_vector = True
    elif cols == 1:
        sequence = output_grid[:, 0]
        is_row_vector = False
    else:
        # If grid is not 1xN or Nx1, return the original grid unchanged
        return output_grid

    n = len(sequence)

    # --- Identify Blocks ---
    # 1. Find the first contiguous block of non-white pixels.
    nw_start, nw_end = find_first_non_white_block(sequence)

    # If no non-white block is found, return the original grid
    if nw_start == -1:
        return output_grid

    # 2. Find the contiguous block of white pixels immediately following.
    # The search for the white block must start exactly at the index after the non-white block ends.
    w_start_search = nw_end + 1
    w_start, w_end = find_subsequent_white_block(sequence, w_start_search)

    # If no white block starts immediately after, return the original grid
    if w_start == -1:
        return output_grid

    # --- Rearrange Sequence ---
    # 3. Extract the segments using numpy slicing
    # Pixels before the non-white block (must be white or empty)
    leading_pixels = sequence[0:nw_start] 
    # The non-white block itself
    non_white_block = sequence[nw_start : nw_end + 1]
    # The white block itself
    white_block = sequence[w_start : w_end + 1] 
    # Pixels after the white block
    remainder = sequence[w_end + 1 :]

    # 4. Construct the new sequence by swapping the white and non-white blocks
    # Order: leading + white_block + non_white_block + remainder
    output_sequence = np.concatenate((leading_pixels, white_block, non_white_block, remainder))

    # --- Reconstruct Grid ---
    # 5. Reshape the sequence back into the original grid shape
    if is_row_vector:
        # Reshape as 1xN
        output_grid = output_sequence.reshape(1, n) 
    else:
        # Reshape as Nx1
        output_grid = output_sequence.reshape(n, 1) 
        
    # Ensure the shape is exactly the same as the input
    if output_grid.shape != original_shape:
         # This case should theoretically not happen if logic above is correct, but as safeguard:
         print(f"Warning: Output shape {output_grid.shape} differs from input shape {original_shape}. Returning original.")
         return input_grid.copy()


    return output_grid