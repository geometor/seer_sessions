```python
"""
Rotates the input grid 90 degrees counter-clockwise.
The pixel value at input grid position (row r, column c) is moved to the
output grid position (row W-1-c, column r), where W is the width of the input grid.
"""

# No external libraries needed for this basic rotation

def transform(input_grid):
    """
    Rotates the input grid 90 degrees counter-clockwise.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A new 2D list representing the rotated grid.
    """
    # Determine input grid dimensions
    input_height = len(input_grid)
    if input_height == 0:
        # Handle empty grid: [] -> []
        return []

    # Assuming a rectangular grid, get width from the first row
    input_width = len(input_grid[0])
    if input_width == 0:
        # Handle grid with empty rows: [[], [], ...] -> []
        # Output dimensions should be W x H = 0 x H, resulting in an empty grid.
        return []

    # Calculate output grid dimensions after 90-degree rotation (W x H)
    output_height = input_width
    output_width = input_height

    # Initialize the output grid with a default value (e.g., 0)
    # It will have output_height rows and output_width columns
    output_grid = [[0 for _ in range(output_width)] for _ in range(output_height)]

    # Iterate through each pixel of the input grid using row and column indices
    for r in range(input_height): # r iterates from 0 to H-1
        for c in range(input_width): # c iterates from 0 to W-1

            # Get the color value of the pixel at input position (r, c)
            value = input_grid[r][c]

            # Calculate the target coordinates in the output grid
            # corresponding to a 90-degree counter-clockwise rotation:
            # New row index: r_new = W - 1 - c
            # New column index: c_new = r
            new_r = input_width - 1 - c
            new_c = r

            # Place the retrieved color value at the calculated position (new_r, new_c)
            # in the output grid
            output_grid[new_r][new_c] = value

    # Return the newly created and populated rotated grid
    return output_grid
```