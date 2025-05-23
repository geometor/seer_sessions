# 0a938d79 • 012 • refine_coder

---
```python
"""
The transformation identifies all unique non-zero colors in the input grid. It then creates a sequence where each unique color is followed by two zeros. This sequence is repeated horizontally across each row of the output grid. The output grid has the same dimensions as the input grid.
"""

import numpy as np

def find_non_zero_pixels(grid):
    # Find coordinates and colors of non-zero pixels
    coords = np.transpose(np.nonzero(grid))
    colors = [grid[y, x] for y, x in coords]
    return coords, colors

def construct_base_pattern(colors):
     # Construct a base pattern using the unique non-zero input colors
    unique_colors = sorted(list(set(colors)))
    pattern = []
    for color in unique_colors:
        pattern.append(color)
        pattern.extend([0, 0])
    return pattern[:-2]


def transform(input_grid):
    """
    Transforms the input grid by replicating a base pattern horizontally.
    """
    # Initialize output grid with the same dimensions as the input grid
    output_grid = np.zeros((input_grid.shape[0], input_grid.shape[1]), dtype=int)

    # Find non-zero pixels in the input grid
    _, colors = find_non_zero_pixels(input_grid)

    # construct base pattern
    base_pattern = construct_base_pattern(colors)


    # Construct each row of the output grid
    for i in range(output_grid.shape[0]):
        # repeat base pattern
        row = np.tile(base_pattern, output_grid.shape[1] // len(base_pattern) + 1)[:output_grid.shape[1]]
        output_grid[i] = row

    return output_grid
```

