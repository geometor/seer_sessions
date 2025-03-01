"""
The transformation rule is a color substitution cipher. Every instance of color '3' (green) in the input grid is replaced with color '4' (yellow) in the output grid. Every instance of color '1' (blue) is replaced with color '5' (gray). Every instance of color '2' (red) is replaced with color '6' (magenta). Other colors remain unchanged.
"""

def transform(input_grid):
    # Initialize the output grid with the same dimensions as the input grid.
    output_grid = []
    for row in input_grid:
      output_grid.append(row.copy())

    # Iterate through each cell of the output grid.
    for i in range(len(output_grid)):
        for j in range(len(output_grid[i])):
            # Apply the value mapping.
            if output_grid[i][j] == 3:
                output_grid[i][j] = 4
            elif output_grid[i][j] == 1:
                output_grid[i][j] = 5
            elif output_grid[i][j] == 2:
                output_grid[i][j] = 6

    return output_grid