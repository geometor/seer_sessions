
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 4 4 4 4 4 4 0 0 0
0 0 0 0 3 3 3 3 3 3 3 3 0 0 0
0 0 0 0 3 0 0 0 0 0 0 3 0 0 0
0 0 0 0 3 0 0 0 0 0 0 3 0 0 0
0 0 0 0 3 0 0 0 0 0 0 3 0 0 0
0 0 0 0 3 3 3 3 3 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 3 3 3 3 3 0 0 0
0 0 0 0 3 0 0 0 0 0 0 3 0 0 0
0 0 0 0 3 0 0 0 0 0 0 3 0 0 0
0 0 0 0 3 0 0 0 0 0 0 3 0 0 0
0 0 0 0 3 3 3 3 3 3 3 3 0 0 0
0 0 0 0 4 4 4 4 4 4 4 4 0 0 0
```


## train_2

**input:**
```
0 0 0 8 8 0 0 0 0 0 0 0
0 0 8 8 8 8 0 0 0 8 0 0
0 8 8 8 8 8 8 0 8 8 8 0
0 2 2 2 2 2 2 0 2 2 2 0
0 2 0 0 0 0 2 0 2 0 2 0
0 2 0 0 0 0 2 0 2 0 2 0
0 2 0 0 0 0 2 0 2 0 2 0
0 2 0 0 0 0 2 0 2 2 2 0
0 2 2 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 2 0 2 2 2 0
0 2 0 0 0 0 2 0 2 0 2 0
0 2 0 0 0 0 2 0 2 0 2 0
0 2 0 0 0 0 2 0 2 0 2 0
0 2 0 0 0 0 2 0 2 2 2 0
0 2 2 2 2 2 2 0 0 8 0 0
0 0 0 8 8 0 0 0 8 8 8 0
0 0 8 8 8 8 0 0 0 0 0 0
0 8 8 8 8 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the provided examples to understand the transformation.

**Perception of Elements:**

*   The input and output are 2D grids of integers.
*   The integer `0` represents the background.
*   Non-zero integers represent distinct "colors" or types of objects.
*   In each example, there are exactly two distinct non-zero colors present in the input.
*   These non-zero colors form contiguous or semi-contiguous shapes/objects within the grid.
*   One object is positioned vertically above the other object in the input grid.
*   The transformation involves changing the vertical positions of these two objects relative to each other.

**Analysis of Transformation (Example 1):**

*   Object 1: Color 4, occupies row 3.
*   Object 2: Color 3, occupies rows 4 through 8.
*   Object 1 (color 4) is above Object 2 (color 3).
*   In the output, Object 2 (color 3) remains in rows 4 through 8.
*   Object 1 (color 4) moves to row 9, which is immediately below the original position of Object 2.

**Analysis of Transformation (Example 2):**

*   Object 1: Color 8, occupies rows 0 through 2 (min_row=0, max_row=2).
*   Object 2: Color 2, occupies rows 3 through 8 (min_row=3, max_row=8).
*   Object 1 (color 8) is above Object 2 (color 2).
*   In the output, Object 2 (color 2) remains in rows 3 through 8.
*   Object 1 (color 8) moves to rows 9 through 11. The new top row (9) is immediately below the original bottom row of Object 2 (row 8). The relative shape of object 1 is preserved.

**Conclusion on Transformation:**

The transformation identifies the two distinct non-zero colored objects in the grid. It determines which object is vertically higher (top object) and which is lower (bottom object). The bottom object remains in its original position in the output. The top object is moved vertically downwards so that its new top edge is positioned one row below the original bottom edge of the bottom object. The internal structure and horizontal positions of both objects are preserved.

**YAML Facts:**


```yaml
Grid:
  Type: 2D array
  Element: Integer
Background:
  Value: 0
Objects:
  Identification: Contiguous regions of identical non-zero integers
  Count_Per_Grid: 2
  Properties:
    - Color: The non-zero integer value
    - Pixels: Set of (row, column) coordinates
    - BoundingBox: min_row, max_row, min_col, max_col
Relationships:
  - Spatial: One object ('Top Object') is located vertically above the other ('Bottom Object') based on min_row comparison.
Action:
  Name: Reposition Top Object
  Rule: Move 'Top Object' vertically downwards.
  Target_Position: The new min_row of 'Top Object' becomes 'Bottom Object'.max_row + 1.
  Invariant: 'Bottom Object' position remains unchanged.
  Invariant: Internal shape and horizontal position of both objects are preserved.
Output_Grid:
  Construction: Start with a background grid, place the 'Bottom Object' at its original location, place the 'Top Object' at its new calculated location.
```


**Natural Language Program:**

1.  Create an output grid of the same dimensions as the input grid, filled entirely with the background color (0).
2.  Identify the two distinct non-zero colors present in the input grid. Call them `ColorA` and `ColorB`.
3.  Find all coordinates `(r, c)` where the input grid contains `ColorA`. Store these as `CoordsA`.
4.  Find all coordinates `(r, c)` where the input grid contains `ColorB`. Store these as `CoordsB`.
5.  Determine the minimum row (`min_rowA`) and maximum row (`max_rowA`) from `CoordsA`.
6.  Determine the minimum row (`min_rowB`) and maximum row (`max_rowB`) from `CoordsB`.
7.  Identify the "Top Object" and "Bottom Object":
    *   If `min_rowA < min_rowB`, then the Top Object has `ColorA` and `CoordsA`, and the Bottom Object has `ColorB`, `CoordsB`, and its bottom row is `max_rowB`.
    *   Else (`min_rowB < min_rowA`), then the Top Object has `ColorB` and `CoordsB`, and the Bottom Object has `ColorA`, `CoordsA`, and its bottom row is `max_rowA`.
8.  Let `TopColor`, `TopCoords`, `min_rowTop` refer to the properties of the identified Top Object.
9.  Let `BottomColor`, `BottomCoords`, `max_rowBottom` refer to the properties of the identified Bottom Object.
10. Calculate the vertical shift for the Top Object: `shift = (max_rowBottom + 1) - min_rowTop`.
11. Populate the output grid:
    *   For each coordinate `(r, c)` in `BottomCoords`, set `output_grid[r][c] = BottomColor`.
    *   For each coordinate `(r, c)` in `TopCoords`, set `output_grid[r + shift][c] = TopColor`.
12. Return the final output grid.
```python
import numpy as np

"""
Identifies two distinct non-zero colored objects in the input grid. Determines which object is vertically higher (Top Object) and which is lower (Bottom Object) based on their minimum row indices. The Bottom Object remains in its original position in the output grid. The Top Object is moved vertically downwards so that its new top edge is positioned one row below the original bottom edge of the Bottom Object. The internal structure and horizontal positions of both objects are preserved. The output grid is initialized with the background color (0).
"""

def find_object_coords_and_bounds(grid, color):
    """
    Finds all coordinates and the row bounds for a given color in the grid.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the object to find.

    Returns:
        tuple: A tuple containing:
            - list: A list of (row, col) coordinates for the object.
            - int: The minimum row index of the object.
            - int: The maximum row index of the object.
            Returns ([], -1, -1) if the color is not found.
    """
    coords = []
    min_row = -1
    max_row = -1
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color:
                coords.append((r, c))
                if min_row == -1 or r < min_row:
                    min_row = r
                if r > max_row:
                    max_row = r
    return coords, min_row, max_row

def transform(input_grid):
    """
    Transforms the input grid by identifying two objects and swapping their vertical order.

    Args:
        input_grid (list of lists): A 2D list representing the input grid.

    Returns:
        list of lists: A 2D list representing the transformed grid.
    """
    # Convert input to numpy array for easier manipulation
    grid_np = np.array(input_grid)
    rows, cols = grid_np.shape

    # Initialize output_grid with the background color (0)
    output_grid = np.zeros_like(grid_np)

    # Find the unique non-zero colors in the input grid
    unique_colors = np.unique(grid_np[grid_np != 0])

    if len(unique_colors) != 2:
        # Handle cases with not exactly two colors if necessary,
        # for now, assume valid input based on examples
        return input_grid # Or raise an error, or return empty grid

    color_a = unique_colors[0]
    color_b = unique_colors[1]

    # Find coordinates and row bounds for each object
    coords_a, min_row_a, max_row_a = find_object_coords_and_bounds(grid_np, color_a)
    coords_b, min_row_b, max_row_b = find_object_coords_and_bounds(grid_np, color_b)

    # Identify the Top and Bottom objects based on minimum row index
    if min_row_a < min_row_b:
        top_color, top_coords, min_row_top = color_a, coords_a, min_row_a
        bottom_color, bottom_coords, max_row_bottom = color_b, coords_b, max_row_b
    else:
        top_color, top_coords, min_row_top = color_b, coords_b, min_row_b
        bottom_color, bottom_coords, max_row_bottom = color_a, coords_a, max_row_a

    # Calculate the vertical shift needed for the Top Object
    # The new top row of the Top Object should be one row below the max row of the Bottom Object
    shift = (max_row_bottom + 1) - min_row_top

    # Populate the output grid
    # Place the Bottom Object at its original location
    for r, c in bottom_coords:
        output_grid[r, c] = bottom_color

    # Place the Top Object at its new shifted location
    for r, c in top_coords:
        new_r = r + shift
        # Check bounds just in case, though problem description implies shapes fit
        if 0 <= new_r < rows:
             output_grid[new_r, c] = top_color

    # Convert back to list of lists for the required output format
    return output_grid.tolist()
```
