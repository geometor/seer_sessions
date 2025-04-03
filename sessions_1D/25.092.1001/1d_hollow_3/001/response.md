```python
import numpy as np

"""
Identify the contiguous block of a single non-white color in the input row.
Create an output row of the same size, initially all white (0).
Place the color of the block at the start and end indices of the original block in the output row.
All other positions in the output row remain white.
"""

def find_non_white_block_endpoints(row):
    """
    Finds the start index, end index, and color of the first contiguous non-white block.

    Args:
        row (np.array): A 1D numpy array representing the input row.

    Returns:
        tuple: (start_index, end_index, color) or (None, None, None) if no non-white block is found.
    """
    start_index = -1
    end_index = -1
    color = 0  # Default to white
    
    # Find the first non-white pixel
    for i, pixel in enumerate(row):
        if pixel != 0:
            start_index = i
            color = pixel
            break
            
    # If no non-white pixel was found, return None
    if start_index == -1:
        return None, None, None
        
    # Find the last non-white pixel (assuming only one block per row as per examples)
    # Iterate backwards is more efficient, but iterating forwards ensures we get the end of the *first* block if multiple existed.
    # Since examples show only one block, iterating backwards is safe and potentially clearer.
    for i in range(len(row) - 1, start_index -1 , -1):
         if row[i] == color: # check if it's part of the same block color
             end_index = i
             break
    # If somehow end_index wasn't found after finding start_index (shouldn't happen with contiguous blocks)
    if end_index == -1:
        end_index = start_index # Handle single pixel block case correctly

    # Correction: Let's find the *last* occurrence of the *first found color*
    last_occurrence_index = -1
    for i in range(len(row) -1, -1, -1):
        if row[i] == color:
            last_occurrence_index = i
            break
    
    # Ensure the block is contiguous - find the first and last index OF THAT COLOR
    indices_of_color = np.where(row == color)[0]
    if len(indices_of_color) > 0:
        start_index = indices_of_color[0]
        end_index = indices_of_color[-1]
        # Verify contiguity (optional based on problem constraints, but good practice)
        # is_contiguous = np.all(row[start_index : end_index + 1] == color)
        # if not is_contiguous:
             # Handle error or unexpected input if necessary
             # For this specific problem, examples imply contiguity
        return start_index, end_index, color
    else: # Should not happen if start_index was found initially
        return None, None, None


def transform(input_grid):
    """
    Transforms the input grid by keeping only the start and end pixels of the non-white block.

    Args:
        input_grid (list or np.array): A 2D list or numpy array representing the input grid (expected to have only 1 row).

    Returns:
        np.array: A numpy array representing the transformed grid.
    """
    # Convert input to numpy array for easier handling
    input_array = np.array(input_grid, dtype=int)
    
    # Assuming the input grid always has at least one row
    # And for this specific task, it seems to always be exactly one row
    if input_array.shape[0] != 1:
        # Handle unexpected input dimensions if necessary
        # For now, assume it's always 1 row based on examples
        pass
        
    input_row = input_array[0]
    height, width = 1, input_row.shape[0] # Get dimensions

    # Initialize output grid with the same dimensions, filled with white (0)
    output_grid = np.zeros((height, width), dtype=int)
    output_row = output_grid[0] # Get a reference to the row we'll modify

    # Find the endpoints and color of the non-white block
    start_index, end_index, color = find_non_white_block_endpoints(input_row)

    # If a block was found, place its color at the start and end indices
    if start_index is not None:
        output_row[start_index] = color
        # Check if start and end are different before setting end_index
        # This correctly handles blocks of length 1
        if start_index != end_index:
             output_row[end_index] = color # Place color at the end index

    return output_grid
```