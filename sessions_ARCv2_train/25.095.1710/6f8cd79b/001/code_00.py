import copy

"""
Transforms an input grid of zeros by creating a border of eights around it.

1. Determines the height and width of the input grid.
2. Creates a new output grid with the same dimensions, initially a copy of the input.
3. Iterates through each cell of the grid using row and column indices.
4. If a cell is located on the first row, last row, first column, or last column, 
   its value in the output grid is set to 8.
5. Interior cells retain their original value (which is 0 in this case).
6. Returns the modified grid with the border.
"""


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies a border of '8's to an input grid of '0's.

    Args:
        input_grid: A list of lists representing the input grid, containing only 0s.

    Returns:
        A list of lists representing the output grid with an '8' border.
    """

    # Determine the dimensions of the input grid
    if not input_grid:
        return []
    height = len(input_grid)
    if height == 0 or not input_grid[0]:
         # Handle empty grid or grid with empty rows
         # Create a copy to avoid modifying the original potentially empty structure
         return [row[:] for row in input_grid]
    width = len(input_grid[0])

    # Create a deep copy of the input grid to serve as the initial output grid
    # This ensures interior cells remain 0 without extra logic
    output_grid = [row[:] for row in input_grid]

    # Iterate through each cell by row and column index
    for r in range(height):
        for c in range(width):
            # Check if the cell is on the border
            is_border = (r == 0) or (r == height - 1) or \
                        (c == 0) or (c == width - 1)

            # If the cell is on the border, set its value to 8
            if is_border:
                output_grid[r][c] = 8
            # No 'else' needed as interior cells already have the correct value (0)
            # from the initial copy.

    return output_grid
