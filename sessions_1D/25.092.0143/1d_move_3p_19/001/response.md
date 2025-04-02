```python
import numpy as np

def find_colored_block(grid_row):
    """
    Finds the start index, end index, color, and length of the first 
    contiguous non-white (non-zero) block in a 1D numpy array.

    Args:
        grid_row (np.array): A 1D numpy array representing a row of the grid.

    Returns:
        tuple: (start_index, end_index, block_color, length) if a block is found,
               otherwise None. end_index is exclusive (like Python slices).
    """
    start_index = -1
    block_color = -1
    length = 0
    in_block = False

    for i, pixel in enumerate(grid_row):
        if pixel != 0:  # Found a non-white pixel
            if not in_block:  # Start of a new block
                start_index = i
                block_color = pixel
                length = 1
                in_block = True
            elif pixel == block_color:  # Continuation of the current block
                length += 1
            else: 
                # Found a different non-white color, end the current block
                # Based on the examples, we assume only one block per row.
                break 
        elif in_block:  # Found a white pixel after being in a block
            # End of the block
            break

    if start_index != -1:
        end_index = start_index + length
        return start_index, end_index, block_color, length
    else:
        # No non-white block found in the row
        return None

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Shifts a horizontal block of color three steps to the right within a 
    single row grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.
                                 Expected to have only one row.

    Returns:
        np.ndarray: A 2D numpy array representing the output grid with the 
                    block shifted.
    """
    # Ensure input is a 2D numpy array
    if not isinstance(input_grid, np.ndarray) or input_grid.ndim != 2:
        raise ValueError("Input must be a 2D numpy array.")
        
    # Check if input has only one row as expected from examples
    if input_grid.shape[0] != 1:
         # This case isn't explicitly handled by the examples, 
         # but we'll proceed assuming the logic applies only to the first row
         # or raise an error if strict adherence to 1-row input is needed.
         # For now, let's assume we process the first row if multiple exist,
         # or handle it as an error if that's safer.
         # Given ARC tasks, it's safer to assume the examples define the structure.
         print("Warning: Input grid has more than one row. Processing the first row only.")
         # Or uncomment below to be stricter:
         # raise ValueError("Input grid is expected to have exactly one row.")

    input_row = input_grid[0] # Extract the first (and likely only) row
    height, width = input_grid.shape

    # Initialize the output grid with the background color (white = 0)
    output_grid = np.zeros_like(input_grid)

    # Step 1: Identify the contiguous block of non-white pixels
    block_info = find_colored_block(input_row)

    # If no block is found, return the empty background grid
    if not block_info:
        print("Warning: No non-white block found in the input row.")
        return output_grid # Return grid filled with background

    start_index, end_index, block_color, length = block_info

    # Step 2: Calculate the new starting position
    shift_distance = 3
    new_start_index = start_index + shift_distance
    new_end_index = new_start_index + length # Exclusive end index

    # Step 3 & 4: Create output row and place the block at the new position
    # Ensure the new indices are within the grid boundaries
    # Calculate the portion of the block that actually fits within the grid width
    place_start = max(0, new_start_index)
    place_end = min(width, new_end_index)
    
    # Only place the block if there's overlap with the grid boundaries
    if place_start < place_end:
        # Place the block (using its original color) into the output row
        output_grid[0, place_start:place_end] = block_color

    # Step 6: Return the resulting grid
    return output_grid
```