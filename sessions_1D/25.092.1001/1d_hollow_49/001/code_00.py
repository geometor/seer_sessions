import numpy as np

"""
Transforms a 1D grid (represented as a 1xN list of lists) by identifying a 
single contiguous horizontal block of a non-white color. In the output grid, 
only the first and last pixels of this block retain their original color, while 
all pixels *between* them are turned white (0). Pixels outside the original 
block (originally white) remain unchanged. If the block has length 1 or 2, or 
if no non-white block exists, the grid remains unchanged.
"""

def find_colored_block_indices(grid_row):
    """
    Finds the start and end indices of the contiguous block of non-white pixels.
    Assumes at most one such contiguous block exists based on examples.
    
    Args:
        grid_row (list or np.array): A 1D list or array representing a row.
        
    Returns:
        tuple: (start_index, end_index) of the block, or (None, None) if no 
               non-white pixels are found.
    """
    # Find all indices that contain a non-white color (not 0)
    non_white_indices = [i for i, color in enumerate(grid_row) if color != 0]
    
    # If the list is empty, no non-white pixels were found
    if not non_white_indices:
        return None, None
        
    # The start of the block is the minimum index found
    start_index = min(non_white_indices)
    # The end of the block is the maximum index found
    end_index = max(non_white_indices)
    
    # Note: This implicitly assumes the non-white pixels form a single 
    # contiguous block, as seen in the examples. If there were gaps 
    # (e.g., [0, 5, 0, 5, 0]), this would still return the min and max index 
    # covering the gap. However, the transformation logic correctly handles
    # this by only modifying pixels *between* start and end.

    return start_index, end_index

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): A 2D list representing the input grid. 
                                     Expected to be 1xN based on examples.

    Returns:
        list of lists: The transformed grid.
    """
    # Convert input to a numpy array for easier manipulation
    input_array = np.array(input_grid, dtype=int)
    
    # Ensure the input grid is effectively 1D (has only one row)
    # This aligns with the structure observed in the training examples.
    if input_array.shape[0] != 1:
        # If the grid structure is different, return the input unchanged
        # or raise an error, depending on desired behavior for unexpected inputs.
        # Returning unchanged seems safer for ARC general tasks.
        return input_grid 
        
    # Create a copy of the input array to modify, ensuring the original is untouched
    output_array = np.copy(input_array)
    
    # Extract the single row from the grid
    grid_row = input_array[0] 

    # Find the start and end indices of the colored block in the row
    start_index, end_index = find_colored_block_indices(grid_row)

    # Proceed only if a block was found and it has a length greater than 2
    # (i.e., there are interior pixels to change)
    # A block of length 1 has start_index == end_index
    # A block of length 2 has end_index == start_index + 1
    # Changes are needed only if end_index > start_index + 1
    if start_index is not None and end_index > start_index + 1:
        
        # Iterate through the column indices strictly *between* the start and end indices
        for i in range(start_index + 1, end_index):
            # Set the color of these interior pixels to white (0) in the output array
            output_array[0, i] = 0
            
    # Convert the modified numpy array back to a list of lists format
    return output_array.tolist()