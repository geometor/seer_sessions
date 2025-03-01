"""
The transformation rule involves a simple substitution of digits. Each digit in the input grid is mapped to a different, specific digit in the output grid.

1. Iterate through each cell of the input grid.
2. Replace the value '3' with '4'.
3. Replace the value '1' with '5'.
4. Replace the value '2' with '6'.
5. The resulting output is the new grid.
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