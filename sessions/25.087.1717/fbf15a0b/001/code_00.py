import numpy as np

"""
Identifies the coordinates of the two gray pixels (color 5) in the input grid.
If the gray pixels are vertically aligned (same column), the output grid starts 
at a row index equal to the difference between the gray pixels' row coordinates, 
and its height is half the input grid's height (integer division). All columns are kept.
If the gray pixels are horizontally aligned (same row), the output grid starts 
at a column index equal to the difference between the gray pixels' column coordinates, 
and its width is half the input grid's width (integer division). All rows are kept.
The content of the extracted subgrid is returned.
"""

def transform(input_grid):
    """
    Transforms the input grid based on the position of two gray marker pixels.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    grid = np.array(input_grid, dtype=int)
    input_height, input_width = grid.shape

    # Find the coordinates of the gray pixels (color 5)
    gray_rows, gray_cols = np.where(grid == 5)
    gray_pixels = list(zip(gray_rows, gray_cols))

    # Ensure exactly two gray pixels are found (as per observations)
    if len(gray_pixels) != 2:
        # Handle cases with not exactly two gray pixels if necessary, 
        # though based on examples, this shouldn't happen.
        # For now, let's return the input or raise an error if this occurs.
        # Returning input might be safer for unexpected test cases.
        print("Warning: Expected 2 gray pixels, found {}.".format(len(gray_pixels)))
        return input_grid # Or raise ValueError("Input grid must contain exactly two gray pixels.")

    p1 = gray_pixels[0]
    p2 = gray_pixels[1]

    # Initialize crop parameters
    start_row = 0
    start_col = 0
    output_height = input_height
    output_width = input_width

    # Check if gray pixels are vertically aligned (same column)
    if p1[1] == p2[1]:
        row_coords = [p1[0], p2[0]]
        start_row = max(row_coords) - min(row_coords)
        output_height = input_height // 2
        # start_col and output_width remain as initialized (0 and input_width)
        
    # Check if gray pixels are horizontally aligned (same row)
    elif p1[0] == p2[0]:
        col_coords = [p1[1], p2[1]]
        start_col = max(col_coords) - min(col_coords)
        output_width = input_width // 2
        # start_row and output_height remain as initialized (0 and input_height)
        
    else:
        # Handle cases where pixels are neither vertically nor horizontally aligned
        # Based on training data, this case is not expected.
        print("Warning: Gray pixels are not aligned vertically or horizontally.")
        return input_grid # Or raise ValueError("Gray pixels must be aligned.")

    # Calculate end indices for slicing
    end_row = start_row + output_height
    end_col = start_col + output_width
    
    # Extract the subgrid
    output_grid = grid[start_row:end_row, start_col:end_col]

    return output_grid.tolist()