
## train_1

**input:**
```
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 5 8 8 8 8 8 8 8 8 8 8 8
8 5 8 8 8 8 2 8 8 8 8 8 8
8 5 8 8 8 8 2 7 8 8 8 8 8
8 5 8 8 8 8 2 7 1 8 8 8 8
6 5 6 6 6 6 2 7 1 6 6 6 6
8 5 8 8 8 8 2 7 1 8 8 8 8
8 5 8 8 8 8 2 7 8 8 8 8 8
8 5 8 8 8 8 2 8 8 8 8 8 8
8 5 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
```


**output:**
```
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 1 8 8 8 8
8 8 8 8 8 8 8 7 1 8 8 8 8
8 8 8 8 8 8 2 7 1 8 8 8 8
8 5 8 8 8 8 2 7 1 8 8 8 8
6 5 6 6 6 6 2 7 1 6 6 6 6
8 5 8 8 8 8 2 7 1 8 8 8 8
8 8 8 8 8 8 2 7 1 8 8 8 8
8 8 8 8 8 8 8 7 1 8 8 8 8
8 8 8 8 8 8 8 8 1 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
```


## train_2

**input:**
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 9 8 8
8 8 8 8 7 8 8 8 8 8 8 8 9 8 8
8 8 8 8 7 8 8 8 8 8 8 8 9 8 8
8 8 4 8 7 8 5 8 8 8 8 8 9 8 8
8 8 4 8 7 8 5 8 1 8 8 8 9 8 8
6 6 4 6 7 6 5 6 1 6 6 6 9 6 6
8 8 4 8 7 8 5 8 1 8 8 8 9 8 8
8 8 4 8 7 8 5 8 8 8 8 8 9 8 8
8 8 8 8 7 8 8 8 8 8 8 8 9 8 8
8 8 8 8 7 8 8 8 8 8 8 8 9 8 8
8 8 8 8 8 8 8 8 8 8 8 8 9 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```


**output:**
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 9 8 8
8 8 8 8 8 8 8 8 1 8 8 8 9 8 8
8 8 8 8 8 8 8 8 1 8 8 8 9 8 8
8 8 8 8 7 8 5 8 1 8 8 8 9 8 8
8 8 4 8 7 8 5 8 1 8 8 8 9 8 8
6 6 4 6 7 6 5 6 1 6 6 6 9 6 6
8 8 4 8 7 8 5 8 1 8 8 8 9 8 8
8 8 8 8 7 8 5 8 1 8 8 8 9 8 8
8 8 8 8 8 8 8 8 1 8 8 8 9 8 8
8 8 8 8 8 8 8 8 1 8 8 8 9 8 8
8 8 8 8 8 8 8 8 8 8 8 8 9 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```


## train_3

**input:**
```
8 8 8 8 8 8 8
8 8 1 8 8 8 8
4 8 1 8 1 8 7
4 6 1 6 1 6 7
4 8 1 8 1 8 7
8 8 1 8 8 8 8
8 8 8 8 8 8 8
```


**output:**
```
8 8 8 8 8 8 8
8 8 8 8 8 8 7
4 8 1 8 1 8 7
4 6 1 6 1 6 7
4 8 1 8 1 8 7
8 8 8 8 8 8 7
8 8 8 8 8 8 8
```

**Perception**

The task involves simulating a form of gravity constrained by a specific horizontal line within the grid. The input grids contain a background color (azure, 8), a single horizontal line composed of magenta (6) pixels, and various other colored pixels (objects) primarily located above the magenta line. The transformation moves these objects downwards within their respective columns until they either rest on the magenta line or land on top of another object that has already settled in that column. Objects maintain their original colors and horizontal positions. Pixels below the magenta line, the magenta line itself, and the background pixels that are not replaced by falling objects remain unchanged.

**Facts**


```yaml
Grid:
  Background: Azure (8) is the predominant color.
  Reference Line:
    Exists: True
    Color: Magenta (6)
    Orientation: Horizontal
    Uniqueness: Single instance per grid.
    Behavior: Static, acts as a barrier or floor.
Objects:
  Identification: Contiguous pixels or single pixels of any color other than Azure (8) and Magenta (6).
  Location: Primarily located above the Magenta reference line in the input.
  Behavior:
    Action: Move vertically downwards ("fall").
    Constraint: Movement stops when the object is directly above a Magenta pixel or another non-Azure pixel in the same column.
    Integrity: Objects retain their shape and color during movement.
    Relativity: Objects maintain their horizontal position (column).
Transformation:
  Focus: Applies only to objects located above the Magenta line.
  Mechanism: Simulates gravity within each column independently.
  Outcome: Objects settle at the lowest possible position within their column, bounded below by the Magenta line or previously settled objects.
  Scope: Pixels at or below the Magenta line are unaffected.
```


**Natural Language Program**

1.  Identify the horizontal row composed entirely of magenta (6) pixels. This is the 'floor'.
2.  Identify all non-azure (8) and non-magenta (6) pixels located *above* the magenta floor line. These are the 'falling objects'.
3.  Initialize the output grid as a copy of the input grid.
4.  Iterate through each column of the grid.
5.  For the current column, identify all falling objects (non-azure, non-magenta pixels above the magenta floor line).
6.  If falling objects exist in the column:
    a.  Temporarily remove all falling objects from this column in the output grid, replacing them with the background color (azure, 8).
    b.  For each falling object identified in step 5 (processing them from lowest original row to highest original row is simplest), determine its 'landing spot' in the output grid's column. The landing spot is the highest row index `r` such that `grid[r][col]` is azure (8) and `grid[r+1][col]` is either magenta (6) or another non-azure object.
    c.  Place the falling object's color into the determined landing spot `(r, col)` in the output grid.
7.  After processing all columns, the modified output grid represents the final state.
```python
import numpy as np

"""
Identifies a horizontal line of magenta (6) pixels which acts as a 'floor'. 
All non-azure (8) and non-magenta (6) pixels located above this floor in each column 
are treated as 'falling objects'. These objects 'fall' downwards within their 
respective columns until they rest directly above the magenta floor or another 
previously settled non-azure object in that column. The background color is azure (8). 
Pixels at or below the magenta line, the magenta line itself, and background pixels 
not replaced by falling objects remain unchanged. Objects retain their original color 
and horizontal position.
"""

def find_magenta_line(grid):
    """Finds the row index of the horizontal magenta line."""
    height, width = grid.shape
    for r in range(height):
        # Check if all pixels in the row are magenta (6)
        # We check only the non-background pixels to be robust against cases
        # where the line might be interspersed with background (though examples show solid lines)
        # Let's stick to the stricter definition from examples: full row must be magenta
        # Edit: The examples actually show the magenta line can have other colors INTERSPERSED,
        # but the key is the row *containing* magenta defines the floor level.
        # Re-evaluating based on train_1, train_2, train_3: The line IS solid magenta in the examples,
        # except for the intersection with falling objects in the *output*.
        # The DEFINING feature seems to be the ROW where magenta appears. Let's assume the
        # *lowest* row containing any magenta defines the floor.
        # Edit 2: Looking closely at train_1, the magenta line is NOT solid initially (6 5 6 6...).
        # The description says "a single horizontal line composed of magenta (6) pixels".
        # This implies the defining characteristic is the row where the '6's *predominantly* are,
        # or perhaps any row containing a '6'.
        # Let's assume the row index is defined by the position of the '6's, even if other colors exist on that row.
        # The examples consistently show '6's only on ONE row. Let's find that row.
        if 6 in grid[r, :]:
            return r
    return -1 # Indicate not found (though examples suggest it's always present)


def transform(input_grid):
    """
    Applies gravity to objects above a magenta line within a grid.

    Args:
        input_grid (np.array): The input grid.

    Returns:
        np.array: The transformed grid with objects settled.
    """
    # Initialize output grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape
    background_color = 8
    floor_color = 6

    # Find the row index of the magenta floor line
    magenta_row_index = find_magenta_line(input_grid)

    # If no magenta line is found, return the original grid (as per examples, this shouldn't happen)
    if magenta_row_index == -1:
        return output_grid

    # Process each column independently
    for col in range(width):
        falling_objects = []
        # Collect all non-background, non-floor objects above the magenta line in this column
        for r in range(magenta_row_index):
            color = input_grid[r, col]
            if color != background_color and color != floor_color:
                falling_objects.append(color)
                # Clear the original position of the falling object in the output grid
                output_grid[r, col] = background_color

        # Place the collected objects back into the column, starting from the bottom up
        current_row = magenta_row_index - 1
        # Iterate through the collected objects in reverse order (bottom-most object first)
        for obj_color in reversed(falling_objects):
            # Ensure we don't try to place objects outside the grid boundaries (above the top)
            if current_row >= 0:
                output_grid[current_row, col] = obj_color
                current_row -= 1
            else:
                # This case would mean more objects than available space above the line,
                # which doesn't occur in the examples.
                pass

    return output_grid
```
