"""
Transforms a 3x3 input grid into a 9x9 output grid.
The transformation identifies the location of the top-leftmost non-zero cell 
in the input grid. Let this location be (min_r, min_c).
It then initializes a 9x9 output grid with zeros.
Two 4x4 squares filled with the value 3 are drawn onto the output grid.
The first square's top-left corner is at (min_r, min_c).
The second square's top-left corner is at (min_r + 4, min_c + 4).
If the input grid contains only zeros, the output grid remains all zeros.
"""

import numpy as np

def find_top_left_non_zero(grid: np.ndarray) -> tuple[int, int] | None:
    """
    Finds the coordinates (row, col) of the top-leftmost non-zero cell.
    Returns None if the grid contains only zeros.
    """
    non_zero_coords = np.argwhere(grid != 0)
    if non_zero_coords.size == 0:
        return None
    min_r = non_zero_coords[:, 0].min()
    # Find columns corresponding to the minimum row
    cols_at_min_r = non_zero_coords[non_zero_coords[:, 0] == min_r][:, 1]
    min_c = cols_at_min_r.min()
    return int(min_r), int(min_c)

def draw_square(grid: np.ndarray, top_left_row: int, top_left_col: int, size: int, color: int):
    """
    Draws a square of a given size and color onto the grid.
    Handles boundary conditions implicitly via numpy slicing.
    """
    # Define the boundaries of the square
    end_row = top_left_row + size
    end_col = top_left_col + size
    
    # Draw the square using slicing
    # Ensure the indices stay within the grid bounds (numpy slicing handles this)
    grid[top_left_row:end_row, top_left_col:end_col] = color


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.
    """
    input_np = np.array(input_grid, dtype=int)
    output_rows, output_cols = 9, 9
    output_grid_np = np.zeros((output_rows, output_cols), dtype=int)

    # Find the top-leftmost non-zero cell in the input grid
    top_left_coord = find_top_left_non_zero(input_np)

    # If no non-zero cells are found, return the zero-filled output grid
    if top_left_coord is None:
        return output_grid_np.tolist()

    min_r, min_c = top_left_coord
    square_size = 4
    square_color = 3

    # Draw the first square at (min_r, min_c)
    draw_square(output_grid_np, min_r, min_c, square_size, square_color)

    # Calculate the position for the second square
    second_square_r = min_r + 4
    second_square_c = min_c + 4

    # Draw the second square at (min_r + 4, min_c + 4)
    # Check if the second square's top-left position is within bounds
    # (Drawing itself handles slicing correctly even if part goes out of bounds)
    draw_square(output_grid_np, second_square_r, second_square_c, square_size, square_color)

    # Convert the numpy array back to a list of lists for the return value
    return output_grid_np.tolist()