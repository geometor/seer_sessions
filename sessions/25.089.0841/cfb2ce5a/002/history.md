
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 9 0 0 0 0
0 3 3 8 8 7 0 0 0 0
0 3 8 3 8 0 0 0 0 0
0 3 8 8 3 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0
0 0 0 0 1 5 2 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 3 3 3 3 9 9 9 9 0
0 3 3 8 8 7 7 9 9 0
0 3 8 3 8 7 9 7 9 0
0 3 8 8 3 9 7 7 9 0
0 4 1 1 4 2 5 5 2 0
0 4 1 4 1 5 2 5 2 0
0 4 4 1 1 5 5 2 2 0
0 4 4 4 4 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 2 1 2 1 0 0 0 8 0
0 1 1 2 1 0 0 0 0 0
0 2 2 2 1 0 0 0 0 0
0 1 1 1 1 3 0 0 0 0
0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 5 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 2 1 2 1 3 8 3 8 0
0 1 1 2 1 3 8 3 3 0
0 2 2 2 1 3 8 8 8 0
0 1 1 1 1 3 3 3 3 0
0 7 7 7 7 0 0 0 0 0
0 4 4 4 7 0 5 5 5 0
0 7 7 4 7 0 5 0 0 0
0 4 7 4 7 0 5 0 5 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 8 2 8 8 0 0 0 0 0
0 2 2 2 2 6 0 0 0 0
0 8 2 8 8 0 0 0 0 0
0 8 2 8 8 0 1 0 0 0
0 0 5 4 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 8 2 8 8 1 1 6 1 0
0 2 2 2 2 6 6 6 6 0
0 8 2 8 8 1 1 6 1 0
0 8 2 8 8 1 1 6 1 0
0 4 5 4 4 3 3 1 3 0
0 4 5 4 4 3 3 1 3 0
0 5 5 5 5 1 1 1 1 0
0 4 5 4 4 3 3 1 3 0
0 0 0 0 0 0 0 0 0 0
```

```python
import copy

"""
Iterate through each pixel of the input grid. If a pixel has a non-white color (not 0), 
paint a 4x4 square of that color onto the output grid, starting at the pixel's 
coordinates (top-left corner of the 4x4 square). 
Ensure painting stays within the grid boundaries. 
Paints occur in the order pixels are encountered (row by row, column by column), 
so later paints can overwrite earlier ones.
"""

def transform(input_grid):
    """
    Transforms the input grid by painting 4x4 squares for each non-white pixel.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Get the dimensions of the input grid
    height = len(input_grid)
    width = len(input_grid[0])

    # Initialize the output grid with white (0) pixels, same size as input
    # Use deepcopy initially, though we overwrite most pixels. A simple initialization works too.
    # output_grid = [[0 for _ in range(width)] for _ in range(height)]
    # Let's initialize based on input to preserve background 0s correctly.
    # A simpler approach is to just start with a grid of 0s.
    output_grid = [[0 for _ in range(width)] for _ in range(height)]


    # Iterate through each pixel of the input grid
    for r in range(height):
        for c in range(width):
            color = input_grid[r][c]

            # Check if the pixel is non-white
            if color != 0:
                # Paint a 4x4 square of this color starting at (r, c)
                # Iterate through the 4x4 area
                for dr in range(4):
                    for dc in range(4):
                        # Calculate the target coordinates in the output grid
                        nr = r + dr
                        nc = c + dc

                        # Check if the target coordinates are within the grid bounds
                        if 0 <= nr < height and 0 <= nc < width:
                            # Paint the pixel in the output grid
                            output_grid[nr][nc] = color

    return output_grid
```
