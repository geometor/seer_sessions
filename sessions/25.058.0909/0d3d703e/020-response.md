# 4-0d3d703e • 020 • example_4 • investigate_coder

---
```python
"""
The transformation is a simple color substitution. Each digit in the input grid is replaced by a corresponding digit in the output grid according to a fixed mapping. The mapping is as follows:

1.  Input color 9 (maroon) is replaced by output color 8 (azure).
2.  Input color 4 (yellow) is replaced by output color 3 (green).
3.  Input color 2 (red) is replaced by output color 6 (magenta).
    All other colors, if any, remain unchanged.
"""

def transform(input_grid):
    """
    Applies a color substitution to the input grid based on a predefined mapping.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = [row[:] for row in input_grid]

    # Define the color mapping.
    color_map = {
        9: 8,
        4: 3,
        2: 6,
    }

    # Iterate through each cell of the grid.
    for i in range(len(output_grid)):
        for j in range(len(output_grid[0])):
            # Check if the current color is in the mapping.
            if output_grid[i][j] in color_map:
                # Apply the color substitution.
                output_grid[i][j] = color_map[output_grid[i][j]]

    return output_grid
```

