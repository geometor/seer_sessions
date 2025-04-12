import copy

"""
Transformation Rule:
Iterate through each cell of the input grid. If a cell's color is not white (0) AND its column index is odd, change the cell's color to yellow (4) in the output grid. Otherwise, the cell retains its original color.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on the rule:
    Change non-white pixels to yellow (4) if their column index is odd.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Initialize output_grid as a deep copy of input_grid to avoid modifying the original
    output_grid = copy.deepcopy(input_grid)
    
    # Get grid dimensions
    height = len(input_grid)
    if height == 0:
        return []
    width = len(input_grid[0])
    if width == 0:
        return [[] for _ in range(height)]

    # Iterate through each cell of the grid
    for r in range(height):
        for c in range(width):
            # Get the color of the current cell
            current_color = input_grid[r][c]

            # Check if the color is not white (0)
            if current_color != 0:
                # Check if the column index 'c' is odd
                if c % 2 == 1:
                    # Change the color to yellow (4) in the output grid
                    output_grid[r][c] = 4
            
            # No action needed if the color is white or the column index is even,
            # as the output_grid was initialized as a copy of the input_grid.

    return output_grid
