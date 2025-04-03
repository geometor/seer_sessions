import numpy as np
import collections

"""
Transforms an input grid represented as a 2D NumPy array of shape (1, N).
The transformation identifies a contiguous block of non-white pixels within the single row.
This block must contain exactly two distinct non-white colors: one appearing once (singleton) 
and the other appearing multiple times (sequence). The singleton must be located at either 
the start or the end of the block.
The transformation moves the singleton pixel to the opposite end of the block, 
preserving the relative order of the sequence pixels. Pixels outside this block 
(i.e., white background pixels) remain unchanged.
"""

def find_non_white_block(grid_1d):
    """
    Finds the start and end indices of the first contiguous non-white block in a 1D list.
    Args:
        grid_1d: A list representing the 1D grid row.
    Returns:
        A tuple (start_index, end_index) or (None, None) if no block is found or block is empty.
    """
    start_index = -1
    end_index = -1
    for i, pixel in enumerate(grid_1d):
        if pixel != 0: # Assuming 0 is the background/white color
            if start_index == -1:
                start_index = i
            end_index = i
        elif start_index != -1:
            # Found the end of the first block
            break
    # Handle case where the block extends to the end of the row
    if start_index != -1:
        return start_index, end_index
    else:
        return None, None

def analyze_block(block):
    """
    Analyzes a block (list of pixels) to find the singleton and sequence colors/properties.
    Args:
        block: A list representing the non-white block.
    Returns:
        A tuple (singleton_color, sequence_color, singleton_index_in_block)
        or (None, None, None) if the block doesn't fit the required pattern 
        (not exactly 2 colors, no singleton, singleton not at ends).
    """
    if not block or len(block) < 2:
        return None, None, None # Block must exist and have at least 2 pixels

    counts = collections.Counter(block)

    # Expect exactly two distinct non-white colors
    if len(counts) != 2:
        return None, None, None

    singleton_color = None
    sequence_color = None
    singleton_count = 0
    
    for color, count in counts.items():
        if count == 1:
            singleton_color = color
            singleton_count += 1
        else:
            sequence_color = color # Assume the other is the sequence

    # Check if we found exactly one singleton color and one sequence color
    if singleton_count != 1 or sequence_color is None:
        return None, None, None

    # Find the index of the singleton within the block
    try:
        # Find first occurrence, which is sufficient since count is 1
        singleton_index_in_block = block.index(singleton_color) 
    except ValueError:
         # Should not happen if counts were correct, but handle defensively
         return None, None, None

    # Verify singleton is at one of the ends of the block
    if singleton_index_in_block != 0 and singleton_index_in_block != len(block) - 1:
        # Singleton is not at an end, which violates the observed pattern
        return None, None, None

    return singleton_color, sequence_color, singleton_index_in_block


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    Args:
        input_grid: A numpy array representing the input grid, expected shape (1, N).
    Returns:
        A numpy array representing the transformed grid, shape (1, N).
    """
    
    # Validate input format
    if not isinstance(input_grid, np.ndarray) or input_grid.ndim != 2 or input_grid.shape[0] != 1:
        print("Warning: Input grid is not a 2D NumPy array with shape (1, N). Returning input.")
        return input_grid

    # Extract the single row as a Python list
    input_row_list = input_grid[0].tolist()
    
    # Initialize output row as a copy of the input row
    output_row_list = list(input_row_list)

    # 1. Find the contiguous block of non-white pixels in the row
    start_index, end_index = find_non_white_block(output_row_list)

    # If no block found or block is invalid, return the original grid unchanged
    if start_index is None:
        return input_grid # Return original NumPy array

    # Extract the block from the row list
    block = output_row_list[start_index : end_index + 1]

    # 2. Analyze the block to find singleton and sequence properties
    analysis_result = analyze_block(block)

    # If block doesn't match the expected pattern, return original grid
    if analysis_result == (None, None, None):
        return input_grid # Return original NumPy array
        
    singleton_color, sequence_color, singleton_index_in_block = analysis_result

    # 3. Construct the new block based on the singleton's original position
    new_block = []
    # Extract sequence pixels maintaining their order
    sequence_pixels = [p for p in block if p == sequence_color] 
        
    if singleton_index_in_block == 0:
        # Singleton was at the start, move it to the end
        new_block = sequence_pixels + [singleton_color]
    elif singleton_index_in_block == len(block) - 1:
        # Singleton was at the end, move it to the start
        # The original examples only showed start->end, but applying symmetry
        new_block = [singleton_color] + sequence_pixels
    # No else needed because analyze_block already verified it's at an end

    # Ensure the new block has the same length as the old one (sanity check)
    if len(new_block) != len(block):
        print(f"Warning: Reconstruction error. New block length ({len(new_block)}) doesn't match old block length ({len(block)}). Returning input.")
        return input_grid # Return original grid on error

    # 4. Reconstruct the output row by replacing the original block part
    output_row_list[start_index : end_index + 1] = new_block

    # 5. Convert the transformed list back into a 2D NumPy array with the original shape and dtype
    output_grid = np.array([output_row_list], dtype=input_grid.dtype)

    return output_grid