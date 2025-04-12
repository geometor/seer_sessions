
## train_1

**input:**
```
7 7 2 7 7 7 7
7 7 2 2 2 7 7
7 7 7 7 2 7 7
2 2 7 7 2 2 2
7 2 7 7 7 7 7
7 2 2 2 2 7 7
7 7 7 7 2 7 7
```


**output:**
```
3 3 2 5 5 5 5
3 3 2 2 2 5 5
3 3 3 3 2 5 5
2 2 3 3 2 2 2
5 2 3 3 3 3 3
5 2 2 2 2 3 3
5 5 5 5 2 3 3
```


## train_2

**input:**
```
2 7 7 7 7 7 7
2 7 7 7 7 7 7
2 7 7 7 7 7 7
2 2 2 7 7 7 7
7 7 2 7 7 7 7
7 7 2 2 2 7 7
7 7 7 7 2 2 2
```


**output:**
```
2 3 3 3 3 3 3
2 3 3 3 3 3 3
2 3 3 3 3 3 3
2 2 2 3 3 3 3
5 5 2 3 3 3 3
5 5 2 2 2 3 3
5 5 5 5 2 2 2
```


## train_3

**input:**
```
7 7 7 7 7 2 7 7
7 7 7 7 7 2 7 7
2 2 2 2 7 2 7 7
7 7 7 2 7 2 7 7
7 7 7 2 7 2 7 7
2 2 7 2 7 2 2 7
7 2 7 2 7 7 2 2
7 2 7 2 7 7 7 7
```


**output:**
```
5 5 5 5 5 2 3 3
5 5 5 5 5 2 3 3
2 2 2 2 5 2 3 3
3 3 3 2 5 2 3 3
3 3 3 2 5 2 3 3
2 2 3 2 5 2 2 3
5 2 3 2 5 5 2 2
5 2 3 2 5 5 5 5
```

## Perception of Task Elements

The input grids consist primarily of two colors: Red (2) and Orange (7). The Red pixels form distinct shapes or patterns, while the Orange pixels typically fill the remaining space, acting like a background or field.

The output grids retain the original Red (2) pixels in their exact positions. The Orange (7) pixels from the input are replaced by either Green (3) or Gray (5) pixels in the output.

The transformation logic appears to depend on the proximity of the Orange pixels to the Red pixels. Orange pixels that are adjacent (horizontally, vertically, or diagonally) to any Red pixel are changed to Gray (5). Orange pixels that are not adjacent to any Red pixel are changed to Green (3).

## YAML Facts


```yaml
Colors:
  Input:
    - Red: 2
    - Orange: 7
  Output:
    - Red: 2
    - Green: 3
    - Gray: 5
Objects:
  - Type: Pixel cluster
    Color: Red (2)
    Property: Static - position remains unchanged.
  - Type: Pixel
    Color: Orange (7)
    Property: Dynamic - color changes based on relationship to Red pixels.
Relationships:
  - Type: Adjacency
    Description: Checks if an Orange pixel is adjacent (including diagonals) to a Red pixel.
    Source: Orange Pixel (7)
    Target: Red Pixel (2)
Actions:
  - Action: Identify
    Target: All Red (2) pixels.
  - Action: Identify
    Target: All Orange (7) pixels.
  - Action: Conditional Recolor
    Target: Orange (7) pixels.
    Condition:
      - If adjacent (8 directions) to any Red (2) pixel:
          Change color to Gray (5).
      - Else (not adjacent to any Red (2) pixel):
          Change color to Green (3).
Grid:
  Property: The dimensions of the output grid are identical to the input grid.
```


## Natural Language Program

1.  Create a new grid with the same dimensions as the input grid.
2.  Iterate through each cell (pixel) of the input grid using its row and column index.
3.  Get the color of the current pixel in the input grid.
4.  If the input pixel color is Red (2), set the corresponding pixel in the new grid to Red (2).
5.  If the input pixel color is Orange (7):
    a.  Examine the 8 neighboring pixels (up, down, left, right, and the four diagonals) of the current pixel in the *input* grid.
    b.  Check if any of these neighbors have the color Red (2).
    c.  If at least one neighbor is Red (2), set the corresponding pixel in the new grid to Gray (5).
    d.  If none of the neighbors are Red (2), set the corresponding pixel in the new grid to Green (3).
6.  The final new grid is the output.
```python
import numpy as np

"""
This program transforms an input grid based on the color of its pixels.
The input grid primarily contains Red (2) and Orange (7) pixels.
The transformation rules are:
1. Red (2) pixels remain unchanged in the output grid.
2. Orange (7) pixels are transformed based on their adjacency to Red (2) pixels in the input grid:
   - If an Orange (7) pixel is adjacent (horizontally, vertically, or diagonally) to at least one Red (2) pixel, it becomes Gray (5) in the output grid.
   - If an Orange (7) pixel is not adjacent to any Red (2) pixel, it becomes Green (3) in the output grid.
The output grid has the same dimensions as the input grid.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid according to the rules described above.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to a numpy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize the output grid as a copy of the input grid.
    # This handles rule 1 automatically (Red pixels remain Red).
    # We will only modify the cells that were originally Orange.
    output_np = np.copy(input_np)

    # Define the relative coordinates for the 8 neighbors (including diagonals)
    neighbor_deltas = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    # Iterate through each cell of the input grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel in the input grid is Orange (7)
            if input_np[r, c] == 7:
                is_adjacent_to_red = False
                # Examine the 8 neighbors of the current pixel in the *input* grid
                for dr, dc in neighbor_deltas:
                    nr, nc = r + dr, c + dc
                    # Check if the neighbor coordinates are within the grid bounds
                    if 0 <= nr < height and 0 <= nc < width:
                        # Check if the neighbor pixel is Red (2)
                        if input_np[nr, nc] == 2:
                            is_adjacent_to_red = True
                            break  # Found a red neighbor, no need to check further

                # Apply transformation based on adjacency
                if is_adjacent_to_red:
                    # Rule 2a: If adjacent to Red, change to Gray (5)
                    output_np[r, c] = 5
                else:
                    # Rule 2b: If not adjacent to Red, change to Green (3)
                    output_np[r, c] = 3

    # Convert the numpy array back to a list of lists for the final output
    output_grid = output_np.tolist()
    return output_grid

```
