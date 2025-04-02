import numpy as np

"""
Transforms the input grid by processing each row independently.
If a row contains exactly two non-white pixels of the same color,
it fills the horizontal space between them (exclusive of the endpoints) with that color.
Otherwise, the row remains unchanged.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert input to a numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    # Create a copy of the input grid to modify and return as the output
    output_np = np.copy(input_np)
    # Get the dimensions of the grid
    height, width = input_np.shape

    # Iterate through each row of the grid
    for r in range(height):
        # Get the current row
        row = input_np[r, :]

        # Find the column indices of all non-white (non-zero) pixels in this row
        non_white_indices = np.where(row != 0)[0]

        # Check if there are exactly two non-white pixels in this row
        if len(non_white_indices) == 2:
            # Get the colors of the two non-white pixels
            color1 = row[non_white_indices[0]]
            color2 = row[non_white_indices[1]]

            # Check if the two non-white pixels have the same color
            if color1 == color2:
                # The color to fill with is the color of the pair
                fill_color = color1
                # Get the column indices of the two pixels
                col1, col2 = non_white_indices[0], non_white_indices[1]
                
                # Determine the start and end columns for filling
                # The fill range is between the two columns, exclusive of the endpoints
                col_start = min(col1, col2) + 1
                col_end = max(col1, col2) # Slicing is exclusive at the end index

                # Fill the pixels between the two points in the output grid
                # Only fill if there's space between them (col_start < col_end)
                if col_start < col_end:
                    output_np[r, col_start:col_end] = fill_color
        
        # If the conditions (exactly two non-white pixels of the same color) are not met,
        # the row in the output grid remains unchanged (as it was copied initially).

    # Convert the final numpy array back to a list of lists before returning
    return output_np.tolist()