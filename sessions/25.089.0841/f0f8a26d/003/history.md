
## train_1

**input:**
```
7 5 7 7 7 7 7 7 7
7 5 7 7 7 5 7 7 7
7 5 7 5 7 7 7 7 7
7 7 7 5 7 7 5 7 7
7 7 7 5 7 7 5 7 7
7 7 7 7 7 7 5 7 7
5 5 5 5 5 7 5 7 7
7 7 7 7 7 7 5 7 7
7 7 7 7 7 7 7 7 7
```


**output:**
```
7 7 7 7 7 7 7 7 7
5 5 5 7 7 5 7 7 7
7 7 7 7 7 7 7 7 7
7 7 5 5 5 7 7 7 7
7 7 5 7 7 7 7 7 7
7 7 5 7 5 5 5 5 5
7 7 5 7 7 7 7 7 7
7 7 5 7 7 7 7 7 7
7 7 5 7 7 7 7 7 7
```


## train_2

**input:**
```
7 7 7 7 7 7 7 7 7
7 7 2 2 2 7 2 7 7
7 7 7 7 7 7 2 7 7
7 7 2 7 7 7 2 7 7
7 7 2 7 7 7 7 7 7
7 7 2 7 7 7 7 7 7
7 7 7 7 7 2 2 2 7
7 2 2 2 7 7 7 7 7
7 7 7 7 7 7 7 7 7
```


**output:**
```
7 7 7 2 7 7 7 7 7
7 7 7 2 7 7 7 7 7
7 7 7 2 7 2 2 2 7
7 7 7 7 7 7 7 7 7
7 2 2 2 7 7 7 7 7
7 7 7 7 7 7 2 7 7
7 7 2 7 7 7 2 7 7
7 7 2 7 7 7 2 7 7
7 7 2 7 7 7 7 7 7
```


## train_3

**input:**
```
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7
7 8 7 7 7 8 8 8 8 8 7
7 8 7 8 7 7 7 7 7 7 7
7 8 7 7 7 7 8 7 7 7 7
7 7 7 7 7 7 8 7 8 8 8
7 7 7 7 7 7 8 7 7 7 7
7 7 7 7 7 7 8 7 7 7 7
8 8 8 8 8 7 8 7 7 7 7
7 7 7 7 7 7 8 7 8 8 8
7 7 7 7 7 7 8 7 7 7 7
```


**output:**
```
7 7 7 7 7 7 7 8 7 7 7
7 7 7 7 7 7 7 8 7 7 7
7 7 7 7 7 7 7 8 7 7 7
8 8 8 8 7 7 7 8 7 7 7
7 7 7 7 7 7 7 8 7 8 7
7 7 7 7 7 7 7 7 7 8 7
7 7 8 7 7 7 7 7 7 8 7
7 7 8 8 8 8 8 8 8 8 7
7 7 8 7 7 7 7 7 7 8 7
7 7 8 7 7 7 7 7 7 8 7
7 7 8 7 7 7 7 7 7 8 7
```

Okay, counter-clockwise rotation is not it. Let's try clockwise.


*code_execution:*
```python
import numpy as np

input_1 = np.array([
    [7, 5, 7, 7, 7, 7, 7, 7, 7],
    [7, 5, 7, 7, 7, 5, 7, 7, 7],
    [7, 5, 7, 5, 7, 7, 7, 7, 7],
    [7, 7, 7, 5, 7, 7, 5, 7, 7],
    [7, 7, 7, 5, 7, 7, 5, 7, 7],
    [7, 7, 7, 7, 7, 7, 5, 7, 7],
    [5, 5, 5, 5, 5, 7, 5, 7, 7],
    [7, 7, 7, 7, 7, 7, 5, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7]
])

output_1 = np.array([
    [7, 7, 7, 7, 7, 7, 7, 7, 7],
    [5, 5, 5, 7, 7, 5, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 7, 5, 5, 5, 7, 7, 7, 7],
    [7, 7, 5, 7, 7, 7, 7, 7, 7],
    [7, 7, 5, 7, 5, 5, 5, 5, 5],
    [7, 7, 5, 7, 7, 7, 7, 7, 7],
    [7, 7, 5, 7, 7, 7, 7, 7, 7],
    [7, 7, 5, 7, 7, 7, 7, 7, 7]
])

# Rotate input 90 degrees clockwise
rotated_input_1_cw = np.rot90(input_1, k=-1)
print("Rotated Input 1 (CW):\n", rotated_input_1_cw)

# Compare with output
print("Matches Output 1:", np.array_equal(rotated_input_1_cw, output_1))
```

*code_execution_result:*
outcome: OUTCOME_OK
```
Rotated Input 1 (CW):
 [[7 7 5 7 7 7 7 7 7]
 [7 7 5 7 7 7 5 5 5]
 [7 7 5 7 7 7 7 7 7]
 [7 7 5 7 5 5 5 7 7]
 [7 7 5 7 7 7 7 7 7]
 [7 7 7 7 7 7 7 5 7]
 [7 5 5 5 5 5 7 7 7]
 [7 7 7 7 7 7 7 7 7]
 [7 7 7 7 7 7 7 7 7]]
Matches Output 1: False

```
Okay, simple rotation isn't it either.

Let's re-evaluate example 1.
Input:

```
7 5 7 7 7 7 7 7 7  <- Row 0
7 5 7 7 7 5 7 7 7  <- Row 1
7 5 7 5 7 7 7 7 7  <- Row 2
7 7 7 5 7 7 5 7 7  <- Row 3
7 7 7 5 7 7 5 7 7  <- Row 4
7 7 7 7 7 7 5 7 7  <- Row 5
5 5 5 5 5 7 5 7 7  <- Row 6
7 7 7 7 7 7 5 7 7  <- Row 7
7 7 7 7 7 7 7 7 7  <- Row 8
```

Output:

```
7 7 7 7 7 7 7 7 7  <- Row 0
5 5 5 7 7 5 7 7 7  <- Row 1
7 7 7 7 7 7 7 7 7  <- Row 2
7 7 5 5 5 7 7 7 7  <- Row 3
7 7 5 7 7 7 7 7 7  <- Row 4
7 7 5 7 5 5 5 5 5  <- Row 5
7 7 5 7 7 7 7 7 7  <- Row 6
7 7 5 7 7 7 7 7 7  <- Row 7
7 7 5 7 7 7 7 7 7  <- Row 8
```

There seems to be a dominant background color (orange, 7). The other color (gray, 5) forms objects/pixels.
Let's consider the transformation as:
1. Rotate the grid 90 degrees counter-clockwise.
2. Apply gravity to the non-background pixels (gray) in each column, making them fall downwards.
3. Rotate the resulting grid back 90 degrees clockwise.

Let's try this on Example 1.
Step 1: Rotate Input 1 CCW (already calculated):

```
7 7 7 7 7 7 7 7 7
7 7 5 5 5 7 5 7 7
7 7 7 7 7 7 5 7 7
7 7 7 5 7 7 5 7 7
7 7 7 5 7 7 5 7 7
7 5 7 7 7 5 7 7 7
7 5 7 5 7 7 7 7 7
7 5 7 7 7 7 7 7 7
5 7 7 7 7 7 7 7 7
```

Step 2: Apply gravity (gray=5 falls in orange=7 background).
*   Col 0: 5 falls to row 8.
*   Col 1: 5s at rows 5, 6, 7 fall to 6, 7, 8.
*   Col 2: 5 at row 1 falls to row 8.
*   Col 3: 5s at rows 1, 3, 4, 6 fall to 5, 6, 7, 8.
*   Col 4: 5 at row 1 falls to row 8.
*   Col 5: 5 at row 5 falls to row 8.
*   Col 6: 5s at rows 1, 2, 3, 4, 6 fall to 4, 5, 6, 7, 8.
*   Col 7: No 5s.
*   Col 8: No 5s.

Intermediate grid after gravity:

```
7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 5 7 7
7 7 7 5 7 7 5 7 7
7 5 7 5 7 7 5 7 7
7 5 7 5 7 7 5 7 7
5 5 5 5 5 5 5 7 7
```

Step 3: Rotate Intermediate grid 90 degrees clockwise (k=-1).


*code_execution:*
```python
import numpy as np

intermediate_1 = np.array([
    [7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 5, 7, 7],
    [7, 7, 7, 5, 7, 7, 5, 7, 7],
    [7, 5, 7, 5, 7, 7, 5, 7, 7],
    [7, 5, 7, 5, 7, 7, 5, 7, 7],
    [5, 5, 5, 5, 5, 5, 5, 7, 7]
])

output_1_expected = np.array([
    [7, 7, 7, 7, 7, 7, 7, 7, 7],
    [5, 5, 5, 7, 7, 5, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 7, 5, 5, 5, 7, 7, 7, 7],
    [7, 7, 5, 7, 7, 7, 7, 7, 7],
    [7, 7, 5, 7, 5, 5, 5, 5, 5],
    [7, 7, 5, 7, 7, 7, 7, 7, 7],
    [7, 7, 5, 7, 7, 7, 7, 7, 7],
    [7, 7, 5, 7, 7, 7, 7, 7, 7]
])


# Rotate intermediate 90 degrees clockwise
final_1 = np.rot90(intermediate_1, k=-1)
print("Final Grid 1:\n", final_1)

# Compare with expected output
print("Matches Output 1:", np.array_equal(final_1, output_1_expected))
```

*code_execution_result:*
outcome: OUTCOME_OK
```
Final Grid 1:
 [[5 7 7 7 7 7 7 7 7]
 [5 5 5 7 7 7 7 7 7]
 [5 7 7 7 7 7 7 7 7]
 [5 5 5 5 7 7 7 7 7]
 [5 7 7 7 7 7 7 7 7]
 [5 7 7 7 7 7 7 7 7]
 [5 5 5 5 5 7 7 7 7]
 [7 7 7 7 7 7 7 7 7]
 [7 7 7 7 7 7 7 7 7]]
Matches Output 1: False

```
Okay, that didn't work either. The rotation + gravity hypothesis seems incorrect, or at least my implementation of it.

Let's re-think "gravity". Maybe it's not about falling down. What if it's about consolidating pixels towards one side?

Look at Example 1 again.
Input has gray pixels (5) scattered. Output has them concentrated vertically, mostly along column 2, and a horizontal line segment in row 1 and row 5.
It almost looks like the gray pixels are pulled towards the left edge.

Let's try "gravity towards the left".
For each row, move all gray pixels as far left as possible, maintaining their relative order within the row, and filling the rest with orange.

Example 1:
Row 0: `7 5 7 7 7 7 7 7 7` -> `5 7 7 7 7 7 7 7 7`
Row 1: `7 5 7 7 7 5 7 7 7` -> `5 5 7 7 7 7 7 7 7`
Row 2: `7 5 7 5 7 7 7 7 7` -> `5 5 7 7 7 7 7 7 7`
Row 3: `7 7 7 5 7 7 5 7 7` -> `5 5 7 7 7 7 7 7 7`
Row 4: `7 7 7 5 7 7 5 7 7` -> `5 5 7 7 7 7 7 7 7`
Row 5: `7 7 7 7 7 7 5 7 7` -> `5 7 7 7 7 7 7 7 7`
Row 6: `5 5 5 5 5 7 5 7 7` -> `5 5 5 5 5 5 7 7 7`
Row 7: `7 7 7 7 7 7 5 7 7` -> `5 7 7 7 7 7 7 7 7`
Row 8: `7 7 7 7 7 7 7 7 7` -> `7 7 7 7 7 7 7 7 7`

Resulting grid (Left Gravity):

```
5 7 7 7 7 7 7 7 7
5 5 7 7 7 7 7 7 7
5 5 7 7 7 7 7 7 7
5 5 7 7 7 7 7 7 7
5 5 7 7 7 7 7 7 7
5 7 7 7 7 7 7 7 7
5 5 5 5 5 5 7 7 7
5 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7
```

This doesn't match the output either.

What if it's gravity towards the top?
For each column, move gray pixels upwards.

Example 1:
Col 0: `7 7 7 7 7 7 5 7 7` -> `5 7 7 7 7 7 7 7 7`
Col 1: `5 5 5 7 7 7 5 7 7` -> `5 5 5 5 7 7 7 7 7`
Col 2: `7 7 7 7 7 7 5 7 7` -> `5 7 7 7 7 7 7 7 7`
Col 3: `7 7 5 5 5 7 5 7 7` -> `5 5 5 5 7 7 7 7 7`
Col 4: `7 7 7 7 7 7 5 7 7` -> `5 7 7 7 7 7 7 7 7`
Col 5: `7 5 7 7 7 7 7 7 7` -> `5 7 7 7 7 7 7 7 7`
Col 6: `7 7 7 5 5 5 5 5 7` -> `5 5 5 5 5 7 7 7 7`
Col 7: `7 7 7 7 7 7 7 7 7` -> `7 7 7 7 7 7 7 7 7`
Col 8: `7 7 7 7 7 7 7 7 7` -> `7 7 7 7 7 7 7 7 7`

Resulting Grid (Up Gravity):

```
5 5 5 5 5 5 5 7 7
7 5 7 5 7 7 5 7 7
7 5 7 5 7 7 5 7 7
7 5 7 5 7 7 5 7 7
7 7 7 5 7 7 5 7 7
7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7
```

Still not matching.

Okay, let's analyze all three examples together.

**Commonalities:**
*   All examples involve a background color (orange, 7).
*   All examples involve one other "active" color (gray 5, red 2, azure 8).
*   The transformation seems to rearrange the pixels of the active color within the background.
*   The dimensions of the grid remain the same.

**Hypothesis: Gravity combined with rotation.**
Let's revisit the first idea: Rotate CCW, apply gravity down, rotate CW.

Example 2:
Input:

```
7 7 7 7 7 7 7 7 7
7 7 2 2 2 7 2 7 7
7 7 7 7 7 7 2 7 7
7 7 2 7 7 7 2 7 7
7 7 2 7 7 7 7 7 7
7 7 2 7 7 7 7 7 7
7 7 7 7 7 2 2 2 7
7 2 2 2 7 7 7 7 7
7 7 7 7 7 7 7 7 7
```

Output:

```
7 7 7 2 7 7 7 7 7
7 7 7 2 7 7 7 7 7
7 7 7 2 7 2 2 2 7
7 7 7 7 7 7 7 7 7
7 2 2 2 7 7 7 7 7
7 7 7 7 7 7 2 7 7
7 7 2 7 7 7 2 7 7
7 7 2 7 7 7 2 7 7
7 7 2 7 7 7 7 7 7
```

Active color: red (2). Background: orange (7).

Step 1: Rotate Input 2 CCW.


*code_execution:*
```python
import numpy as np

input_2 = np.array([
    [7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 7, 2, 2, 2, 7, 2, 7, 7],
    [7, 7, 7, 7, 7, 7, 2, 7, 7],
    [7, 7, 2, 7, 7, 7, 2, 7, 7],
    [7, 7, 2, 7, 7, 7, 7, 7, 7],
    [7, 7, 2, 7, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 2, 2, 2, 7],
    [7, 2, 2, 2, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7]
])

rotated_input_2_ccw = np.rot90(input_2, k=1)
print("Rotated Input 2 (CCW):\n", rotated_input_2_ccw)
```

*code_execution_result:*
outcome: OUTCOME_OK
```
Rotated Input 2 (CCW):
 [[7 7 7 7 7 7 7 7 7]
 [7 7 7 7 7 7 2 7 7]
 [7 2 2 2 7 7 2 7 7]
 [7 7 7 7 7 7 2 7 7]
 [7 2 7 7 7 7 7 7 7]
 [7 2 7 7 7 7 7 2 7]
 [7 2 7 2 2 2 7 2 7]
 [7 7 7 7 7 7 7 2 7]
 [7 7 7 7 7 7 7 7 7]]

```
```python
import numpy as np

"""
The transformation consists of three steps:
1. Rotate the input grid 90 degrees counter-clockwise.
2. Apply downward gravity to the non-background pixels within each column of the rotated grid. The most frequent color is considered the background. Non-background pixels in a column fall to the lowest possible positions in that column, maintaining their original vertical order relative to each other.
3. Rotate the resulting grid 90 degrees clockwise to produce the output grid.
"""

def apply_gravity_down(grid, background_color):
    """
    Applies downward gravity to non-background pixels in each column.
    """
    rows, cols = grid.shape
    output_grid = np.full((rows, cols), background_color, dtype=int)

    for j in range(cols):
        # Extract non-background pixels from the column
        column = grid[:, j]
        non_background_pixels = [p for p in column if p != background_color]

        # Place non-background pixels at the bottom of the output column
        num_non_background = len(non_background_pixels)
        if num_non_background > 0:
            output_grid[rows - num_non_background:, j] = non_background_pixels

    return output_grid

def find_background_color(grid):
    """
    Finds the most frequent color in the grid, assuming it's the background.
    Defaults to 0 (black/white depending on map) if grid is empty or uniform.
    """
    unique, counts = np.unique(grid, return_counts=True)
    if len(counts) == 0:
        return 0 # Default background
    background_color = unique[np.argmax(counts)]
    return background_color

def transform(input_grid):
    """
    Applies a counter-clockwise rotation, downward gravity, and clockwise rotation.
    """
    # Find the background color (most frequent pixel value)
    background_color = find_background_color(input_grid)

    # 1. Rotate the input grid 90 degrees counter-clockwise
    rotated_ccw_grid = np.rot90(input_grid, k=1)

    # 2. Apply downward gravity to non-background pixels
    gravity_applied_grid = apply_gravity_down(rotated_ccw_grid, background_color)

    # 3. Rotate the resulting grid 90 degrees clockwise
    output_grid = np.rot90(gravity_applied_grid, k=-1) # k=-1 for clockwise

    return output_grid
```

Previous Code:
```python
import numpy as np

"""
The transformation consists of three steps:
1. Rotate the input grid 90 degrees counter-clockwise.
2. Apply downward gravity to the non-background pixels within each column of the rotated grid. The most frequent color is considered the background. Non-background pixels in a column fall to the lowest possible positions in that column, maintaining their original vertical order relative to each other.
3. Rotate the resulting grid 90 degrees clockwise to produce the output grid.
"""

def apply_gravity_down(grid, background_color):
    """
    Applies downward gravity to non-background pixels in each column.
    """
    rows, cols = grid.shape
    output_grid = np.full((rows, cols), background_color, dtype=int)

    for j in range(cols):
        # Extract non-background pixels from the column
        column = grid[:, j]
        non_background_pixels = [p for p in column if p != background_color]

        # Place non-background pixels at the bottom of the output column
        num_non_background = len(non_background_pixels)
        if num_non_background > 0:
            output_grid[rows - num_non_background:, j] = non_background_pixels

    return output_grid

def find_background_color(grid):
    """
    Finds the most frequent color in the grid, assuming it's the background.
    Defaults to 0 (black/white depending on map) if grid is empty or uniform.
    """
    unique, counts = np.unique(grid, return_counts=True)
    if len(counts) == 0:
        return 0 # Default background
    background_color = unique[np.argmax(counts)]
    return background_color

def transform(input_grid):
    """
    Applies a counter-clockwise rotation, downward gravity, and clockwise rotation.
    """
    # Find the background color (most frequent pixel value)
    background_color = find_background_color(input_grid)

    # 1. Rotate the input grid 90 degrees counter-clockwise
    rotated_ccw_grid = np.rot90(input_grid, k=1)

    # 2. Apply downward gravity to non-background pixels
    gravity_applied_grid = apply_gravity_down(rotated_ccw_grid, background_color)

    # 3. Rotate the resulting grid 90 degrees clockwise
    output_grid = np.rot90(gravity_applied_grid, k=-1) # k=-1 for clockwise

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
7 5 7 7 7 7 7 7 7
7 5 7 7 7 5 7 7 7
7 5 7 5 7 7 7 7 7
7 7 7 5 7 7 5 7 7
7 7 7 5 7 7 5 7 7
7 7 7 7 7 7 5 7 7
5 5 5 5 5 7 5 7 7
7 7 7 7 7 7 5 7 7
7 7 7 7 7 7 7 7 7
```
Expected Output:
```
7 7 7 7 7 7 7 7 7
5 5 5 7 7 5 7 7 7
7 7 7 7 7 7 7 7 7
7 7 5 5 5 7 7 7 7
7 7 5 7 7 7 7 7 7
7 7 5 7 5 5 5 5 5
7 7 5 7 7 7 7 7 7
7 7 5 7 7 7 7 7 7
7 7 5 7 7 7 7 7 7
```
Transformed Output:
```
5 7 7 7 7 7 7 7 7
5 5 7 7 7 7 7 7 7
5 5 7 7 7 7 7 7 7
5 5 7 7 7 7 7 7 7
5 5 7 7 7 7 7 7 7
5 7 7 7 7 7 7 7 7
5 5 5 5 5 5 7 7 7
5 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7
```
Match: False
Pixels Off: 28
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 34.5679012345679

## Example 2:
Input:
```
7 7 7 7 7 7 7 7 7
7 7 2 2 2 7 2 7 7
7 7 7 7 7 7 2 7 7
7 7 2 7 7 7 2 7 7
7 7 2 7 7 7 7 7 7
7 7 2 7 7 7 7 7 7
7 7 7 7 7 2 2 2 7
7 2 2 2 7 7 7 7 7
7 7 7 7 7 7 7 7 7
```
Expected Output:
```
7 7 7 2 7 7 7 7 7
7 7 7 2 7 7 7 7 7
7 7 7 2 7 2 2 2 7
7 7 7 7 7 7 7 7 7
7 2 2 2 7 7 7 7 7
7 7 7 7 7 7 2 7 7
7 7 2 7 7 7 2 7 7
7 7 2 7 7 7 2 7 7
7 7 2 7 7 7 7 7 7
```
Transformed Output:
```
7 7 7 7 7 7 7 7 7
2 2 2 2 7 7 7 7 7
2 7 7 7 7 7 7 7 7
2 2 7 7 7 7 7 7 7
2 7 7 7 7 7 7 7 7
2 7 7 7 7 7 7 7 7
2 2 2 7 7 7 7 7 7
2 2 2 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7
```
Match: False
Pixels Off: 24
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 29.629629629629633

## Example 3:
Input:
```
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7
7 8 7 7 7 8 8 8 8 8 7
7 8 7 8 7 7 7 7 7 7 7
7 8 7 7 7 7 8 7 7 7 7
7 7 7 7 7 7 8 7 8 8 8
7 7 7 7 7 7 8 7 7 7 7
7 7 7 7 7 7 8 7 7 7 7
8 8 8 8 8 7 8 7 7 7 7
7 7 7 7 7 7 8 7 8 8 8
7 7 7 7 7 7 8 7 7 7 7
```
Expected Output:
```
7 7 7 7 7 7 7 8 7 7 7
7 7 7 7 7 7 7 8 7 7 7
7 7 7 7 7 7 7 8 7 7 7
8 8 8 8 7 7 7 8 7 7 7
7 7 7 7 7 7 7 8 7 8 7
7 7 7 7 7 7 7 7 7 8 7
7 7 8 7 7 7 7 7 7 8 7
7 7 8 8 8 8 8 8 8 8 7
7 7 8 7 7 7 7 7 7 8 7
7 7 8 7 7 7 7 7 7 8 7
7 7 8 7 7 7 7 7 7 8 7
```
Transformed Output:
```
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7
8 8 8 8 8 8 7 7 7 7 7
8 8 7 7 7 7 7 7 7 7 7
8 8 7 7 7 7 7 7 7 7 7
8 8 8 8 7 7 7 7 7 7 7
8 7 7 7 7 7 7 7 7 7 7
8 7 7 7 7 7 7 7 7 7 7
8 8 8 8 8 8 7 7 7 7 7
8 8 8 8 7 7 7 7 7 7 7
8 7 7 7 7 7 7 7 7 7 7
```
Match: False
Pixels Off: 46
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 38.01652892561983
Okay, `Rotate CW -> Gravity Down -> Rotate CCW` is also incorrect.

Let's reconsider the simplest hypothesis: **Gravity applied directly to the input grid.** Which direction?
We tried Down and Left for Example 1, neither worked.

Try **Gravity Right**: Move non-background pixels to the rightmost columns within each row.
Example 1:
Row 0: `7 5 7 7 7 7 7 7 7` -> `7 7 7 7 7 7 7 7 5`
Row 1: `7 5 7 7 7 5 7 7 7` -> `7 7 7 7 7 7 5 5 7` (Error in manual application, should be `7 7 7 7 7 7 7 5 5`)
Row 2: `7 5 7 5 7 7 7 7 7` -> `7 7 7 7 7 7 7 5 5`
Row 3: `7 7 7 5 7 7 5 7 7` -> `7 7 7 7 7 7 5 5 7` (Error -> `7 7 7 7 7 7 7 5 5`)
Row 4: `7 7 7 5 7 7 5 7 7` -> `7 7 7 7 7 7 7 5 5`
Row 5: `7 7 7 7 7 7 5 7 7` -> `7 7 7 7 7 7 7 7 5`
Row 6: `5 5 5 5 5 7 5 7 7` -> `7 7 7 5 5 5 5 5 5`
Row 7: `7 7 7 7 7 7 5 7 7` -> `7 7 7 7 7 7 7 7 5`
Row 8: `7 7 7 7 7 7 7 7 7` -> `7 7 7 7 7 7 7 7 7`

Let's implement this properly with code.



*code_execution:*
```python
import numpy as np

def apply_gravity_right(grid, background_color):
    """
    Applies rightward gravity to non-background pixels in each row.
    """
    rows, cols = grid.shape
    output_grid = np.full((rows, cols), background_color, dtype=int)

    for i in range(rows):
        row = grid[i, :]
        non_background_pixels = [p for p in row if p != background_color]
        num_non_background = len(non_background_pixels)
        if num_non_background > 0:
            output_grid[i, cols - num_non_background:] = non_background_pixels
    return output_grid

def find_background_color(grid):
    """
    Finds the most frequent color in the grid.
    """
    unique, counts = np.unique(grid, return_counts=True)
    if len(counts) == 0: return 0
    background_color = unique[np.argmax(counts)]
    return background_color

input_1 = np.array([
    [7, 5, 7, 7, 7, 7, 7, 7, 7],
    [7, 5, 7, 7, 7, 5, 7, 7, 7],
    [7, 5, 7, 5, 7, 7, 7, 7, 7],
    [7, 7, 7, 5, 7, 7, 5, 7, 7],
    [7, 7, 7, 5, 7, 7, 5, 7, 7],
    [7, 7, 7, 7, 7, 7, 5, 7, 7],
    [5, 5, 5, 5, 5, 7, 5, 7, 7],
    [7, 7, 7, 7, 7, 7, 5, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7]
])

output_1_expected = np.array([
    [7, 7, 7, 7, 7, 7, 7, 7, 7],
    [5, 5, 5, 7, 7, 5, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 7, 5, 5, 5, 7, 7, 7, 7],
    [7, 7, 5, 7, 7, 7, 7, 7, 7],
    [7, 7, 5, 7, 5, 5, 5, 5, 5],
    [7, 7, 5, 7, 7, 7, 7, 7, 7],
    [7, 7, 5, 7, 7, 7, 7, 7, 7],
    [7, 7, 5, 7, 7, 7, 7, 7, 7]
])

bg_color_1 = find_background_color(input_1)
result_1_grav_right = apply_gravity_right(input_1, bg_color_1)
print("Result 1 (Gravity Right):\n", result_1_grav_right)
print("Matches Output 1:", np.array_equal(result_1_grav_right, output_1_expected))

# --- Example 2 ---
input_2 = np.array([
    [7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 7, 2, 2, 2, 7, 2, 7, 7],
    [7, 7, 7, 7, 7, 7, 2, 7, 7],
    [7, 7, 2, 7, 7, 7, 2, 7, 7],
    [7, 7, 2, 7, 7, 7, 7, 7, 7],
    [7, 7, 2, 7, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 2, 2, 2, 7],
    [7, 2, 2, 2, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7]
])
output_2_expected = np.array([
    [7, 7, 7, 2, 7, 7, 7, 7, 7],
    [7, 7, 7, 2, 7, 7, 7, 7, 7],
    [7, 7, 7, 2, 7, 2, 2, 2, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 2, 2, 2, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 2, 7, 7],
    [7, 7, 2, 7, 7, 7, 2, 7, 7],
    [7, 7, 2, 7, 7, 7, 2, 7, 7],
    [7, 7, 2, 7, 7, 7, 7, 7, 7]
])
bg_color_2 = find_background_color(input_2)
result_2_grav_right = apply_gravity_right(input_2, bg_color_2)
print("\nResult 2 (Gravity Right):\n", result_2_grav_right)
print("Matches Output 2:", np.array_equal(result_2_grav_right, output_2_expected))


# --- Example 3 ---
input_3 = np.array([
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 8, 7, 7, 7, 8, 8, 8, 8, 8, 7],
    [7, 8, 7, 8, 7, 7, 7, 7, 7, 7, 7],
    [7, 8, 7, 7, 7, 7, 8, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 8, 7, 8, 8, 8],
    [7, 7, 7, 7, 7, 7, 8, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 8, 7, 7, 7, 7],
    [8, 8, 8, 8, 8, 7, 8, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 8, 7, 8, 8, 8],
    [7, 7, 7, 7, 7, 7, 8, 7, 7, 7, 7]
])
output_3_expected = np.array([
    [7, 7, 7, 7, 7, 7, 7, 8, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 8, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 8, 7, 7, 7],
    [8, 8, 8, 8, 7, 7, 7, 8, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 8, 7, 8, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 7],
    [7, 7, 8, 7, 7, 7, 7, 7, 7, 8, 7],
    [7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 7],
    [7, 7, 8, 7, 7, 7, 7, 7, 7, 8, 7],
    [7, 7, 8, 7, 7, 7, 7, 7, 7, 8, 7],
    [7, 7, 8, 7, 7, 7, 7, 7, 7, 8, 7]
])
bg_color_3 = find_background_color(input_3)
result_3_grav_right = apply_gravity_right(input_3, bg_color_3)
print("\nResult 3 (Gravity Right):\n", result_3_grav_right)
print("Matches Output 3:", np.array_equal(result_3_grav_right, output_3_expected))
```

*code_execution_result:*
outcome: OUTCOME_OK
```
Result 1 (Gravity Right):
 [[7 7 7 7 7 7 7 7 5]
 [7 7 7 7 7 7 7 5 5]
 [7 7 7 7 7 7 7 5 5]
 [7 7 7 7 7 7 7 5 5]
 [7 7 7 7 7 7 7 5 5]
 [7 7 7 7 7 7 7 7 5]
 [7 7 7 5 5 5 5 5 5]
 [7 7 7 7 7 7 7 7 5]
 [7 7 7 7 7 7 7 7 7]]
Matches Output 1: False

Result 2 (Gravity Right):
 [[7 7 7 7 7 7 7 7 7]
 [7 7 7 7 7 2 2 2 2]
 [7 7 7 7 7 7 7 7 2]
 [7 7 7 7 7 7 7 2 2]
 [7 7 7 7 7 7 7 7 2]
 [7 7 7 7 7 7 7 7 2]
 [7 7 7 7 7 7 2 2 2]
 [7 7 7 7 7 7 2 2 2]
 [7 7 7 7 7 7 7 7 7]]
Matches Output 2: False

Result 3 (Gravity Right):
 [[7 7 7 7 7 7 7 7 7 7 7]
 [7 7 7 7 7 7 7 7 7 7 7]
 [7 7 7 7 7 8 8 8 8 8 8]
 [7 7 7 7 7 7 7 7 7 8 8]
 [7 7 7 7 7 7 7 7 7 8 8]
 [7 7 7 7 7 7 7 8 8 8 8]
 [7 7 7 7 7 7 7 7 7 7 8]
 [7 7 7 7 7 7 7 7 7 7 8]
 [7 7 7 7 7 8 8 8 8 8 8]
 [7 7 7 7 7 7 7 8 8 8 8]
 [7 7 7 7 7 7 7 7 7 7 8]]
Matches Output 3: False

```
Gravity Right also fails for all examples.

The only simple gravity direction left is **Gravity Up**. Move non-background pixels to the topmost rows within each column.



*code_execution:*
```python
import numpy as np

def apply_gravity_up(grid, background_color):
    """
    Applies upward gravity to non-background pixels in each column.
    """
    rows, cols = grid.shape
    output_grid = np.full((rows, cols), background_color, dtype=int)

    for j in range(cols):
        column = grid[:, j]
        non_background_pixels = [p for p in column if p != background_color]
        num_non_background = len(non_background_pixels)
        if num_non_background > 0:
            output_grid[:num_non_background, j] = non_background_pixels
    return output_grid

def find_background_color(grid):
    """
    Finds the most frequent color in the grid.
    """
    unique, counts = np.unique(grid, return_counts=True)
    if len(counts) == 0: return 0
    background_color = unique[np.argmax(counts)]
    return background_color

# --- Example 1 ---
input_1 = np.array([
    [7, 5, 7, 7, 7, 7, 7, 7, 7],
    [7, 5, 7, 7, 7, 5, 7, 7, 7],
    [7, 5, 7, 5, 7, 7, 7, 7, 7],
    [7, 7, 7, 5, 7, 7, 5, 7, 7],
    [7, 7, 7, 5, 7, 7, 5, 7, 7],
    [7, 7, 7, 7, 7, 7, 5, 7, 7],
    [5, 5, 5, 5, 5, 7, 5, 7, 7],
    [7, 7, 7, 7, 7, 7, 5, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7]
])
output_1_expected = np.array([
    [7, 7, 7, 7, 7, 7, 7, 7, 7],
    [5, 5, 5, 7, 7, 5, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 7, 5, 5, 5, 7, 7, 7, 7],
    [7, 7, 5, 7, 7, 7, 7, 7, 7],
    [7, 7, 5, 7, 5, 5, 5, 5, 5],
    [7, 7, 5, 7, 7, 7, 7, 7, 7],
    [7, 7, 5, 7, 7, 7, 7, 7, 7],
    [7, 7, 5, 7, 7, 7, 7, 7, 7]
])
bg_color_1 = find_background_color(input_1)
result_1_grav_up = apply_gravity_up(input_1, bg_color_1)
print("Result 1 (Gravity Up):\n", result_1_grav_up)
print("Matches Output 1:", np.array_equal(result_1_grav_up, output_1_expected))

# --- Example 2 ---
input_2 = np.array([
    [7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 7, 2, 2, 2, 7, 2, 7, 7],
    [7, 7, 7, 7, 7, 7, 2, 7, 7],
    [7, 7, 2, 7, 7, 7, 2, 7, 7],
    [7, 7, 2, 7, 7, 7, 7, 7, 7],
    [7, 7, 2, 7, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 2, 2, 2, 7],
    [7, 2, 2, 2, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7]
])
output_2_expected = np.array([
    [7, 7, 7, 2, 7, 7, 7, 7, 7],
    [7, 7, 7, 2, 7, 7, 7, 7, 7],
    [7, 7, 7, 2, 7, 2, 2, 2, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 2, 2, 2, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 2, 7, 7],
    [7, 7, 2, 7, 7, 7, 2, 7, 7],
    [7, 7, 2, 7, 7, 7, 2, 7, 7],
    [7, 7, 2, 7, 7, 7, 7, 7, 7]
])
bg_color_2 = find_background_color(input_2)
result_2_grav_up = apply_gravity_up(input_2, bg_color_2)
print("\nResult 2 (Gravity Up):\n", result_2_grav_up)
print("Matches Output 2:", np.array_equal(result_2_grav_up, output_2_expected))


# --- Example 3 ---
input_3 = np.array([
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 8, 7, 7, 7, 8, 8, 8, 8, 8, 7],
    [7, 8, 7, 8, 7, 7, 7, 7, 7, 7, 7],
    [7, 8, 7, 7, 7, 7, 8, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 8, 7, 8, 8, 8],
    [7, 7, 7, 7, 7, 7, 8, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 8, 7, 7, 7, 7],
    [8, 8, 8, 8, 8, 7, 8, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 8, 7, 8, 8, 8],
    [7, 7, 7, 7, 7, 7, 8, 7, 7, 7, 7]
])
output_3_expected = np.array([
    [7, 7, 7, 7, 7, 7, 7, 8, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 8, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 8, 7, 7, 7],
    [8, 8, 8, 8, 7, 7, 7, 8, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 8, 7, 8, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 7],
    [7, 7, 8, 7, 7, 7, 7, 7, 7, 8, 7],
    [7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 7],
    [7, 7, 8, 7, 7, 7, 7, 7, 7, 8, 7],
    [7, 7, 8, 7, 7, 7, 7, 7, 7, 8, 7],
    [7, 7, 8, 7, 7, 7, 7, 7, 7, 8, 7]
])
bg_color_3 = find_background_color(input_3)
result_3_grav_up = apply_gravity_up(input_3, bg_color_3)
print("\nResult 3 (Gravity Up):\n", result_3_grav_up)
print("Matches Output 3:", np.array_equal(result_3_grav_up, output_3_expected))
```

*code_execution_result:*
outcome: OUTCOME_OK
```
Result 1 (Gravity Up):
 [[5 5 5 5 5 5 5 7 7]
 [7 5 7 5 7 7 5 7 7]
 [7 5 7 5 7 7 5 7 7]
 [7 5 7 5 7 7 5 7 7]
 [7 7 7 7 7 7 5 7 7]
 [7 7 7 7 7 7 7 7 7]
 [7 7 7 7 7 7 7 7 7]
 [7 7 7 7 7 7 7 7 7]
 [7 7 7 7 7 7 7 7 7]]
Matches Output 1: False

Result 2 (Gravity Up):
 [[7 2 2 2 2 2 2 2 7]
 [7 7 2 2 7 7 2 7 7]
 [7 7 2 7 7 7 2 7 7]
 [7 7 2 7 7 7 2 7 7]
 [7 7 2 7 7 7 7 7 7]
 [7 7 7 7 7 7 7 7 7]
 [7 7 7 7 7 7 7 7 7]
 [7 7 7 7 7 7 7 7 7]
 [7 7 7 7 7 7 7 7 7]]
Matches Output 2: False

Result 3 (Gravity Up):
 [[8 8 8 8 8 8 8 8 8 8 8]
 [7 8 7 8 7 7 8 7 8 8 8]
 [7 8 7 7 7 7 8 7 8 8 7]
 [7 8 7 7 7 7 8 7 7 7 7]
 [7 7 7 7 7 7 8 7 7 7 7]
 [7 7 7 7 7 7 8 7 7 7 7]
 [7 7 7 7 7 7 8 7 7 7 7]
 [7 7 7 7 7 7 8 7 7 7 7]
 [7 7 7 7 7 7 7 7 7 7 7]
 [7 7 7 7 7 7 7 7 7 7 7]
 [7 7 7 7 7 7 7 7 7 7 7]]
Matches Output 3: False

```
Gravity Up also fails. It seems a simple directional gravity (Up, Down, Left, Right) applied directly or combined with a simple rotation (CCW/CW) is not the correct transformation.

Let's reconsider the description: "Apply downward gravity ... maintaining their original vertical order relative to each other." My `apply_gravity_down` implementation does this. The issue must be elsewhere.

Perhaps the background color identification is wrong?
Example 1: Orange (7) is clearly dominant.
Example 2: Orange (7) is clearly dominant.
Example 3: Orange (7) is clearly dominant.
The background color identification seems correct.

Let's look at the first hypothesis again: `Rotate CCW -> Gravity Down -> Rotate CW`.
Why did it fail? Let's re-run the code explicitly for Example 1 using the functions.



*code_execution:*
```python
import numpy as np

def apply_gravity_down(grid, background_color):
    """
    Applies downward gravity to non-background pixels in each column.
    """
    rows, cols = grid.shape
    output_grid = np.full((rows, cols), background_color, dtype=int)
    for j in range(cols):
        column = grid[:, j]
        non_background_pixels = [p for p in column if p != background_color]
        num_non_background = len(non_background_pixels)
        if num_non_background > 0:
            output_grid[rows - num_non_background:, j] = non_background_pixels
    return output_grid

def find_background_color(grid):
    """
    Finds the most frequent color in the grid.
    """
    unique, counts = np.unique(grid, return_counts=True)
    if len(counts) == 0: return 0
    background_color = unique[np.argmax(counts)]
    return background_color

def transform_ccw_grav_cw(input_grid):
    """
    Applies a counter-clockwise rotation, downward gravity, and clockwise rotation.
    """
    background_color = find_background_color(input_grid)
    rotated_ccw_grid = np.rot90(input_grid, k=1)
    gravity_applied_grid = apply_gravity_down(rotated_ccw_grid, background_color)
    output_grid = np.rot90(gravity_applied_grid, k=-1)
    return output_grid

# --- Example 1 ---
input_1 = np.array([
    [7, 5, 7, 7, 7, 7, 7, 7, 7],
    [7, 5, 7, 7, 7, 5, 7, 7, 7],
    [7, 5, 7, 5, 7, 7, 7, 7, 7],
    [7, 7, 7, 5, 7, 7, 5, 7, 7],
    [7, 7, 7, 5, 7, 7, 5, 7, 7],
    [7, 7, 7, 7, 7, 7, 5, 7, 7],
    [5, 5, 5, 5, 5, 7, 5, 7, 7],
    [7, 7, 7, 7, 7, 7, 5, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7]
])
output_1_expected = np.array([
    [7, 7, 7, 7, 7, 7, 7, 7, 7],
    [5, 5, 5, 7, 7, 5, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 7, 5, 5, 5, 7, 7, 7, 7],
    [7, 7, 5, 7, 7, 7, 7, 7, 7],
    [7, 7, 5, 7, 5, 5, 5, 5, 5],
    [7, 7, 5, 7, 7, 7, 7, 7, 7],
    [7, 7, 5, 7, 7, 7, 7, 7, 7],
    [7, 7, 5, 7, 7, 7, 7, 7, 7]
])
result_1_trans = transform_ccw_grav_cw(input_1)
print("Result 1 (CCW -> Grav -> CW):\n", result_1_trans)
print("Matches Output 1:", np.array_equal(result_1_trans, output_1_expected))

# --- Example 2 ---
input_2 = np.array([
    [7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 7, 2, 2, 2, 7, 2, 7, 7],
    [7, 7, 7, 7, 7, 7, 2, 7, 7],
    [7, 7, 2, 7, 7, 7, 2, 7, 7],
    [7, 7, 2, 7, 7, 7, 7, 7, 7],
    [7, 7, 2, 7, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 2, 2, 2, 7],
    [7, 2, 2, 2, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7]
])
output_2_expected = np.array([
    [7, 7, 7, 2, 7, 7, 7, 7, 7],
    [7, 7, 7, 2, 7, 7, 7, 7, 7],
    [7, 7, 7, 2, 7, 2, 2, 2, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 2, 2, 2, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 2, 7, 7],
    [7, 7, 2, 7, 7, 7, 2, 7, 7],
    [7, 7, 2, 7, 7, 7, 2, 7, 7],
    [7, 7, 2, 7, 7, 7, 7, 7, 7]
])
result_2_trans = transform_ccw_grav_cw(input_2)
print("\nResult 2 (CCW -> Grav -> CW):\n", result_2_trans)
print("Matches Output 2:", np.array_equal(result_2_trans, output_2_expected))

# --- Example 3 ---
input_3 = np.array([
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7],
    [7, 8, 7, 7, 7, 8, 8, 8, 8, 8, 7],
    [7, 8, 7, 8, 7, 7, 7, 7, 7, 7, 7],
    [7, 8, 7, 7, 7, 7, 8, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 8, 7, 8, 8, 8],
    [7, 7, 7, 7, 7, 7, 8, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 8, 7, 7, 7, 7],
    [8, 8, 8, 8, 8, 7, 8, 7, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 8, 7, 8, 8, 8],
    [7, 7, 7, 7, 7, 7, 8, 7, 7, 7, 7]
])
output_3_expected = np.array([
    [7, 7, 7, 7, 7, 7, 7, 8, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 8, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 8, 7, 7, 7],
    [8, 8, 8, 8, 7, 7, 7, 8, 7, 7, 7],
    [7, 7, 7, 7, 7, 7, 7, 8, 7, 8, 7],
    [7, 7, 7, 7, 7, 7, 7, 7, 7, 8, 7],
    [7, 7, 8, 7, 7, 7, 7, 7, 7, 8, 7],
    [7, 7, 8, 8, 8, 8, 8, 8, 8, 8, 7],
    [7, 7, 8, 7, 7, 7, 7, 7, 7, 8, 7],
    [7, 7, 8, 7, 7, 7, 7, 7, 7, 8, 7],
    [7, 7, 8, 7, 7, 7, 7, 7, 7, 8, 7]
])
result_3_trans = transform_ccw_grav_cw(input_3)
print("\nResult 3 (CCW -> Grav -> CW):\n", result_3_trans)
print("Matches Output 3:", np.array_equal(result_3_trans, output_3_expected))
```

*code_execution_result:*
outcome: OUTCOME_OK
```
Result 1 (CCW -> Grav -> CW):
 [[5 7 7 7 7 7 7 7 7]
 [5 5 7 7 7 7 7 7 7]
 [5 5 7 7 7 7 7 7 7]
 [5 5 7 7 7 7 7 7 7]
 [5 5 7 7 7 7 7 7 7]
 [5 7 7 7 7 7 7 7 7]
 [5 5 5 5 5 5 7 7 7]
 [5 7 7 7 7 7 7 7 7]
 [7 7 7 7 7 7 7 7 7]]
Matches Output 1: False

Result 2 (CCW -> Grav -> CW):
 [[7 7 7 7 7 7 7 7 7]
 [2 2 2 2 7 7 7 7 7]
 [2 7 7 7 7 7 7 7 7]
 [2 2 7 7 7 7 7 7 7]
 [2 7 7 7 7 7 7 7 7]
 [2 7 7 7 7 7 7 7 7]
 [2 2 2 7 7 7 7 7 7]
 [2 2 2 7 7 7 7 7 7]
 [7 7 7 7 7 7 7 7 7]]
Matches Output 2: False

Result 3 (CCW -> Grav -> CW):
 [[7 7 7 7 7 7 7 7 7 7 7]
 [7 7 7 7 7 7 7 7 7 7 7]
 [8 8 8 8 8 8 7 7 7 7 7]
 [8 8 7 7 7 7 7 7 7 7 7]
 [8 8 7 7 7 7 7 7 7 7 7]
 [8 8 8 8 7 7 7 7 7 7 7]
 [8 7 7 7 7 7 7 7 7 7 7]
 [8 7 7 7 7 7 7 7 7 7 7]
 [8 8 8 8 8 8 7 7 7 7 7]
 [8 8 8 8 7 7 7 7 7 7 7]
 [8 7 7 7 7 7 7 7 7 7 7]]
Matches Output 3: False

```
