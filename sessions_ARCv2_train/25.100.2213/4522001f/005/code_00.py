import numpy as np

"""
Transforms a 3x3 input grid into a 9x9 output grid based on the positions of the 
first and last non-zero cells found in the input.

1. Initialize a 9x9 output grid with zeros.
2. Find the coordinates (r1, c1) of the first non-zero cell in the input grid (scanning row-major).
3. Find the coordinates (r2, c2) of the last non-zero cell in the input grid (scanning row-major).
4. If a first non-zero cell (r1, c1) is found, draw a 4x4 block of value 3 in the output grid with its top-left corner at (r1, c1).
5. If a last non-zero cell (r2, c2) is found, draw a 4x4 block of value 3 in the output grid with its top-left corner at (r2 + 3, c2 + 3).
6. If no non-zero cells are found, the output remains all zeros. Overlapping blocks are handled by the drawing sequence (the second block overwrites the first if they overlap).
"""

def find_first_non_zero(grid: list[list[int]]) -> tuple[int, int] | None:
    """Finds the coordinates of the first non-zero cell (row-major scan)."""
    height = len(grid)
    if height == 0:
        return None
    width = len(grid[0])
    for r in range(height):
        for c in range(width):
            if grid[r][c] != 0:
                return r, c
    return None

def find_last_non_zero(grid: list[list[int]]) -> tuple[int, int] | None:
    """Finds the coordinates of the last non-zero cell (row-major scan)."""
    height = len(grid)
    if height == 0:
        return None
    width = len(grid[0])
    last_coord = None
    for r in range(height):
        for c in range(width):
            if grid[r][c] != 0:
                last_coord = (r, c)
    return last_coord

def draw_block(grid: np.ndarray, top_left: tuple[int, int], size: tuple[int, int], value: int):
    """Draws a block of a given size and value onto the grid."""
    r_start, c_start = top_left
    block_height, block_width = size
    grid_height, grid_width = grid.shape

    # Calculate end coordinates, ensuring they don't exceed grid bounds
    r_end = min(r_start + block_height, grid_height)
    c_end = min(c_start + block_width, grid_width)

    # Ensure start coordinates are within bounds
    r_start_clipped = max(r_start, 0)
    c_start_clipped = max(c_start, 0)

    # Assign the value to the block slice
    if r_start_clipped < r_end and c_start_clipped < c_end:
      grid[r_start_clipped:r_end, c_start_clipped:c_end] = value


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: A 3x3 list of lists representing the input grid.

    Returns:
        A 9x9 list of lists representing the transformed output grid.
    """
    # Define output grid dimensions and block properties
    output_height = 9
    output_width = 9
    block_size = (4, 4)
    fill_value = 3

    # Initialize output grid with zeros using numpy
    output_grid_np = np.zeros((output_height, output_width), dtype=int)

    # Find the coordinates of the first non-zero cell
    first_nz = find_first_non_zero(input_grid)

    # Find the coordinates of the last non-zero cell
    last_nz = find_last_non_zero(input_grid)

    # Draw the first block if a non-zero cell was found
    if first_nz:
        r1, c1 = first_nz
        draw_block(output_grid_np, top_left=(r1, c1), size=block_size, value=fill_value)

    # Draw the second block if a non-zero cell was found
    if last_nz:
        r2, c2 = last_nz
        # Apply offset for the second block's position
        second_block_top_left = (r2 + 3, c2 + 3)
        draw_block(output_grid_np, top_left=second_block_top_left, size=block_size, value=fill_value)

    # Convert the numpy array back to a list of lists
    output_grid = output_grid_np.tolist()

    return output_grid