```python
import numpy as np

def transform(input_grid):
    """
    Processes a grid structured with lines every 3rd row/column, defining 2x2 cells.
    For each row of these 2x2 cells, it propagates the color of non-white blocks
    horizontally to the right, filling subsequent white blocks in that row until
    another non-white block is encountered or the grid edge is reached.
    The grid lines and original non-white blocks remain unchanged.
    """
    
    # Convert input list of lists to a numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    # Create a copy to modify, preserving the original structure and colors initially
    output_grid = input_np.copy()
    height, width = input_np.shape

    # Calculate the number of 2x2 cell rows and columns based on the grid structure
    # The pattern repeats every 3 rows and 3 columns (1 line + 2 cell rows/cols)
    num_cell_rows = height // 3
    num_cell_cols = width // 3

    # Helper function to fill a 2x2 cell area in the grid
    def fill_cell(grid, cell_r, cell_c, color):
        # Calculate the top-left coordinates of the 2x2 cell area
        r, c = cell_r * 3, cell_c * 3
        # Ensure the 2x2 area fits within the grid boundaries before filling
        if r + 1 < height and c + 1 < width:
            grid[r:r+2, c:c+2] = color

    # Iterate through each row of 2x2 cells
    for cell_r in range(num_cell_rows):
        # Initialize the fill color for the current row of cells. 0 represents white (no active fill color).
        current_fill_color = 0  

        # Iterate through each column of 2x2 cells from left to right within the current row
        for cell_c in range(num_cell_cols):
            # Calculate the top-left grid coordinates (r, c) for the current 2x2 cell
            r, c = cell_r * 3, cell_c * 3
            
            # Check if coordinates are valid (should be, given loop bounds, but safety check)
            if r >= height or c >= width:
                continue

            # Determine the color of the block in the input grid. 
            # We check the top-left pixel; the task implies these are solid 2x2 blocks if not white.
            cell_top_left_color = input_np[r, c]

            # Assume it's a white cell initially
            is_non_white_block = False
            # If the top-left pixel is not white, check if it's part of a solid 2x2 block
            if cell_top_left_color != 0:
                 # Verify the entire 2x2 area is the same non-white color
                 if r + 1 < height and c + 1 < width:
                     if (input_np[r:r+2, c:c+2] == cell_top_left_color).all():
                         is_non_white_block = True

            if is_non_white_block:
                # If this cell contains a non-white block, update the active fill color for this row
                current_fill_color = cell_top_left_color
            else:
                # If this cell is white (or not a solid non-white block)
                # and we have an active fill color from a previous block in this row
                if current_fill_color != 0:
                    # Fill this white 2x2 cell area in the output grid with the active fill color
                    fill_cell(output_grid, cell_r, cell_c, current_fill_color)

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()

```