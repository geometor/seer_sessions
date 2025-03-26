import numpy as np

"""
1. Given an input grid of height H and width W.
2. Create a new output grid with height H+2 and width W+2.
3. Construct the first row (row 0) of the output grid: Take the first row of the input grid, place a white pixel (0) before it, and place a white pixel (0) after it.
4. Construct the last row (row H+1) of the output grid: Take the last row (row H-1) of the input grid, place a white pixel (0) before it, and place a white pixel (0) after it.
5. For each row `i` from 0 to H-1 in the input grid:
    a. Identify the pixel value at the start (first column) of input row `i`.
    b. Identify the pixel value at the end (last column) of input row `i`.
    c. Construct the corresponding row `i+1` in the output grid by taking the input row `i`, placing the identified starting pixel value before it, and placing the identified ending pixel value after it.
6. The assembled output grid is the result.
"""

def transform(input_grid):
    """
    Adds padding to an input grid. The top and bottom rows are padded with white (0) 
    pixels, using the first and last rows of the input respectively. The middle rows 
    are constructed by taking each corresponding input row and padding it on the left 
    with its first pixel and on the right with its last pixel.
    """
    input_grid_np = np.array(input_grid)
    input_height, input_width = input_grid_np.shape

    # Calculate output dimensions
    output_height = input_height + 2
    output_width = input_width + 2

    # Initialize output_grid with white (0) pixels
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Construct the top border row (Row 0)
    top_row_content = input_grid_np[0, :]
    output_grid[0, 1:-1] = top_row_content
    # Left and right borders are already 0 from initialization

    # Construct the bottom border row (Row H+1)
    bottom_row_content = input_grid_np[input_height - 1, :]
    output_grid[output_height - 1, 1:-1] = bottom_row_content
    # Left and right borders are already 0 from initialization

    # Construct intermediate rows (Rows 1 to H)
    for i in range(input_height):
        input_row = input_grid_np[i, :]
        first_pixel = input_row[0]
        last_pixel = input_row[input_width - 1]
        
        # Construct the output row: [first_pixel] + input_row + [last_pixel]
        output_row = np.concatenate(([first_pixel], input_row, [last_pixel]))
        
        # Assign to the corresponding row in the output grid
        output_grid[i + 1, :] = output_row

    return output_grid.tolist() # Convert back to list of lists for ARC standard
