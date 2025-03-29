import numpy as np

"""
Transforms the input grid based on 'marker' pixels and a 4x4 grid structure. 
Specifically, for each pixel in the input grid that is not white (0) or azure (8) (a 'marker pixel'), it identifies the 4x4 grid cell containing that marker. It then fills all pixels that were originally white (0) within that 4x4 cell in the output grid with the color of the marker pixel. The output grid is initialized as a copy of the input grid.
"""

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.ndarray): The input grid.

    Returns:
        np.ndarray: The transformed output grid.
    """
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Iterate through each pixel of the input grid to find markers
    for r in range(height):
        for c in range(width):
            marker_color = input_grid[r, c]

            # Check if the current pixel is a marker (not white 0 and not azure 8)
            if marker_color != 0 and marker_color != 8:
                
                # Determine the top-left corner of the 4x4 cell containing the marker
                # Integer division // finds the index of the cell (0, 1, 2, ...)
                # Multiplying by 4 gives the starting row/column index of that cell
                cell_start_r = (r // 4) * 4
                cell_start_c = (c // 4) * 4

                # Iterate through the pixels within this 4x4 cell
                # The cell ranges from cell_start_r to cell_start_r + 3 (inclusive)
                # and cell_start_c to cell_start_c + 3 (inclusive)
                for i in range(cell_start_r, cell_start_r + 4):
                    # Ensure the row index is within the grid bounds
                    if 0 <= i < height:
                        for j in range(cell_start_c, cell_start_c + 4):
                            # Ensure the column index is within the grid bounds
                            if 0 <= j < width:
                                # Check if the pixel in the *original* input grid was white (0)
                                if input_grid[i, j] == 0:
                                    # If it was white, change its color in the output grid
                                    # to the marker's color
                                    output_grid[i, j] = marker_color

    # Return the modified output grid
    return output_grid