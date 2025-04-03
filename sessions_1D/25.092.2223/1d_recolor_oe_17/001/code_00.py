import copy
import numpy as np # Although not strictly required by the description, ARC often uses numpy

"""
Recolors contiguous horizontal blocks of yellow (4) pixels based on the block's length parity (odd/even).
- Blocks with odd length are changed to maroon (9).
- Blocks with even length are changed to orange (7).
- All other pixels, including the background white (0), remain unchanged.
"""

def get_horizontal_block_length(row_data, start_col, target_color):
    """
    Calculates the length of a contiguous horizontal block starting at start_col.

    Args:
        row_data (list or np.array): The row of the grid to search within.
        start_col (int): The starting column index for the block.
        target_color (int): The color of the pixels forming the block.

    Returns:
        int: The length of the contiguous block.
    """
    length = 0
    num_cols = len(row_data)
    # Iterate from the starting column to the end of the row
    for c in range(start_col, num_cols):
        # If the pixel matches the target color, increment length
        if row_data[c] == target_color:
            length += 1
        else:
            # Stop counting when a different color or the end of the row is encountered
            break
    return length

def transform(input_grid):
    """
    Transforms the input grid by recoloring horizontal blocks of yellow (4)
    based on their length parity. Odd length -> maroon (9), Even length -> orange (7).

    Args:
        input_grid (list of lists or np.array): The input grid containing pixel values.

    Returns:
        list of lists or np.array: The transformed grid.
    """
    # Ensure we are working with lists of lists for easier modification,
    # or handle numpy arrays appropriately if needed.
    # Using deepcopy ensures the original input_grid is not modified.
    if isinstance(input_grid, np.ndarray):
        output_grid = input_grid.copy() # Use numpy's copy for arrays
        is_numpy = True
    else:
         # Assuming list of lists based on examples
        output_grid = copy.deepcopy(input_grid)
        is_numpy = False

    # Get grid dimensions
    if is_numpy:
        rows, cols = output_grid.shape
    else:
        rows = len(output_grid)
        if rows == 0:
            return output_grid # Handle empty grid
        cols = len(output_grid[0])
        if cols == 0:
             return output_grid # Handle empty rows

    target_color = 4  # Yellow
    odd_color = 9     # Maroon
    even_color = 7    # Orange

    # Iterate through each row
    for r in range(rows):
        c = 0 # Initialize column index for the current row
        while c < cols:
            # Check if the current pixel is the start of a target block
            current_pixel = output_grid[r][c] if is_numpy else output_grid[r][c]

            if current_pixel == target_color:
                # Find the length of the contiguous horizontal block of target_color
                if is_numpy:
                    block_length = get_horizontal_block_length(output_grid[r,:], c, target_color)
                else:
                    block_length = get_horizontal_block_length(output_grid[r], c, target_color)


                # Determine the output color based on block length parity
                output_color = odd_color if block_length % 2 != 0 else even_color

                # Recolor the block in the output grid
                for i in range(block_length):
                    if is_numpy:
                        output_grid[r, c + i] = output_color
                    else:
                        output_grid[r][c + i] = output_color


                # Skip the columns already processed as part of this block
                c += block_length
            else:
                # If not the target color, move to the next column
                c += 1

    # Return the modified grid
    return output_grid
