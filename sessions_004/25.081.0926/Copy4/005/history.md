
Previous Code:
```python
"""
Replicates single-color objects in the output grid, adding extra copies beside any
existing copies of these single-color objects in the input.
"""

import numpy as np

def find_objects(grid):
    """
    Finds all contiguous objects in a grid.
    Returns a list of objects, where each object is a list of (row, col) tuples.
    """
    objects = []
    visited = set()
    rows, cols = grid.shape

    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    def dfs(r, c, color, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        for dr, dc in [(0, 1), (1, 0), (0, -1), (-1, 0)]:
            dfs(r + dr, c + dc, color, current_object)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r,c] != 0:
                current_object = []
                dfs(r, c, grid[r, c], current_object)
                objects.append(current_object)
    return objects

def get_object_color(grid, object_coords):
    """
    Gets color of object
    """
    if not object_coords:
        return 0
    r,c = object_coords[0]
    return grid[r,c]

def get_object_bounds(object_coords):
    """
    Gets boundaries of the object
    """

    min_row = min(r for r, _ in object_coords)
    max_row = max(r for r, _ in object_coords)
    min_col = min(c for _, c in object_coords)
    max_col = max(c for _, c in object_coords)

    return min_row, max_row, min_col, max_col

def expand_single_cell_objects(input_grid, output_grid, objects):
    """
    Expands single cell colored objects that are not part of multi-colored objects
    """

    rows, cols = input_grid.shape
    output_rows, output_cols = output_grid.shape
    
    for obj in objects:
      color = get_object_color(input_grid, obj)
      if len(obj) == 1:
        r,c = obj[0]
        if color == 3:
          if c+3 < cols and input_grid[r, c+1] == 0 and input_grid[r, c+2] == 0 and input_grid[r, c+3] == 0:
              output_grid[r,c+1] = 3
              output_grid[r,c+2] = 3
              output_grid[r,c+3] = 3
        if color == 6:
          if r+1 < rows and input_grid[r+1, c] == 0:
            output_grid[r+1, c] = 6



def transform(input_grid):
    # Initialize output_grid as a copy of the input grid, then modify
    input_grid = np.array(input_grid)
    output_grid = np.copy(input_grid)

    objects = find_objects(input_grid)

    # Replicate objects and add extra copies
    for obj in objects:
        color = get_object_color(input_grid, obj)
        min_row, max_row, min_col, max_col = get_object_bounds(obj)

        # Place object in the output
        for r,c in obj:
          output_grid[r,c] = input_grid[r,c]

        # Check for adjacent objects of same color
        object_width = max_col - min_col + 1
        object_height = max_row - min_row + 1

        # Check to the right
        if max_col + object_width < output_grid.shape[1]:
            is_right_clear = True
            for r in range(min_row, max_row + 1):
                for c in range(max_col+1, max_col+1+object_width):
                  if output_grid[r,c] != 0:
                    is_right_clear = False

            if is_right_clear:
              for r_offset in range(object_height):
                for c_offset in range(object_width):
                    output_grid[min_row + r_offset, max_col + 1+ c_offset] = color

        # Check bottom
        if max_row + object_height < output_grid.shape[0]:
          is_bottom_clear = True
          for r in range(max_row + 1, max_row + 1 + object_height):
            for c in range(min_col, max_col+1):
              if output_grid[r,c] != 0:
                is_bottom_clear = False

          if is_bottom_clear:
            for r_offset in range(object_height):
                for c_offset in range(object_width):
                  output_grid[max_row + 1 + r_offset, min_col+c_offset] = color

    expand_single_cell_objects(input_grid, output_grid, objects)
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 4 0 0 0 0 0 0 0 4 0 0 0 0
0 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 4 4 4 4 4 0 0 0 4 4 4 4 4
0 4 4 4 4 4 0 0 0 4 4 4 4 4 0 0 0 4 4 4 4 4
0 4 4 4 4 4 0 0 0 4 4 4 4 4 0 0 0 4 4 4 4 4
0 4 4 4 4 4 0 0 0 4 4 4 4 4 0 0 0 4 4 4 4 4
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 3 3 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 4 4 0 0 0 0 0 0 4 4 0 0 0
0 4 4 4 4 4 0 0 0 4 0 0 0 0 0 0 0 4 0 0 0 0
0 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3
0 4 4 4 4 4 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3
0 4 4 4 4 4 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 3
```
![Transformed Image](Copy4-1.png)
match: False
pixels_off: 69
size_correct: True
color_palette_correct: True
correct_pixel_counts: None

## Example 2:
Input:
```
0 0 0 6 6 6 0 0 0 0 0 0 0 0
0 0 0 6 6 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 6 6 6 6 6
0 3 3 3 3 0 0 0 6 6 6 6 6 6
0 3 4 4 3 0 0 0 6 6 6 6 6 6
0 3 4 4 3 0 0 0 6 6 6 6 6 6
0 3 3 3 3 0 0 0 6 6 6 6 6 6
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 6 6
0 0 0 0 0 0 0 0 0 0 0 0 6 6
0 0 0 0 0 0 0 3 0 0 0 0 6 6
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 6 6 6 0 0 0 0 0 0 0 0
0 0 0 6 6 6 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 6 6 6 6 6
0 3 3 3 3 0 0 0 6 6 6 6 6 6
0 3 4 4 3 0 0 0 6 6 6 6 6 6
0 3 4 4 3 0 0 0 6 6 6 6 6 6
0 3 3 3 3 0 0 0 6 6 6 6 6 6
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 0 0 0 0 0 0 0 0
0 0 3 4 4 3 0 0 0 0 0 0 6 6
0 0 3 4 4 3 0 0 0 0 0 0 6 6
0 0 3 3 3 3 0 3 3 3 3 0 6 6
0 0 0 0 0 0 0 3 4 4 3 0 0 0
0 0 0 0 0 0 0 3 4 4 3 0 0 0
0 0 0 0 0 0 0 3 3 3 3 0 0 0
```
Transformed Output:
```
0 0 0 6 6 6 6 6 6 0 0 0 0 0
0 0 0 6 6 6 6 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 6 6 6 6 6 6
0 3 3 3 3 0 0 0 6 6 6 6 6 6
0 3 4 4 3 0 0 0 6 6 6 6 6 6
0 3 4 4 3 0 0 0 6 6 6 6 6 6
0 3 3 3 3 0 0 0 6 6 6 6 6 6
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 3 3 3 3 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0 0 6 6
0 0 0 0 0 0 0 0 0 0 0 0 6 6
0 0 0 0 0 0 0 3 3 3 3 0 6 6
0 0 0 0 0 0 0 3 0 0 0 0 6 6
0 0 0 0 0 0 0 0 0 0 0 0 6 6
0 0 0 0 0 0 0 0 0 0 0 0 6 6
```
![Transformed Image](Copy4-2.png)
match: False
pixels_off: 34
size_correct: True
color_palette_correct: True
correct_pixel_counts: None
Okay, let's analyze the provided information and develop a refined natural language program.

**General Assessment and Strategy**

The initial code was designed with the concept of replicating objects, primarily focusing on horizontal and vertical replication. It also included special handling for single-cell objects of colors 3 (green) and 6 (magenta). However, the test results on the second example show that the replication logic and single-cell handling are not entirely correct and need adjustments. The first example failed because it added extra copies to all the objects. The second example failed as it did not replicate all objects as needed, specifically, single cell objects of color 3, and it also seems that some replications missed by one position.

The strategy will involve:

1.  **Refine Object Replication:** Correct the existing logic to accurately replicate objects to adjacent empty spaces in the input data, both horizontally and vertically.
2.  **Adjust Single-Cell Object Handling**: Revisit the `expand_single_cell_objects` to ensure correct expansion, considering the specific rules and variations in the examples.
3.  **Unified approach.** Consider objects of single cells as no different to other objects - ie. all objects are treated the same
4.  **Eliminate Hardcoding:** Where possible, remove the special cases for color and shape.

**Metrics Gathering and Analysis (using code execution where needed)**

Let's perform some more analysis of the errors and determine the properties of the task.

First, an overall summary, then metrics for each task



*code_execution:*
```python
import numpy as np

def analyze_results(examples):
    """Analyzes the results of the transformation, focusing on incorrect pixels."""
    analysis = []
    for example in examples:
        input_grid = np.array(example['input'])
        expected_output = np.array(example['expected_output'])
        transformed_output = np.array(example['transformed_output'])

        diff = expected_output != transformed_output
        incorrect_pixels = np.sum(diff)

        # Object analysis (simplified for demonstration)
        unique_expected, counts_expected = np.unique(expected_output, return_counts=True)
        unique_transformed, counts_transformed = np.unique(transformed_output, return_counts=True)

        analysis.append({
            'incorrect_pixels': int(incorrect_pixels),
            'expected_colors': dict(zip(unique_expected, counts_expected)),
            'transformed_colors': dict(zip(unique_transformed, counts_transformed)),
        })
    return analysis

examples = [
    {
        'input': [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 4, 4, 4, 4, 4, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0],
            [0, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0],
        ],
        'expected_output': [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 4, 4, 4, 4, 4, 0, 0, 0, 4, 4, 4, 4, 4, 0, 0, 0, 4, 4, 4, 4, 4],
            [0, 4, 4, 4, 4, 4, 0, 0, 0, 4, 4, 4, 4, 4, 0, 0, 0, 4, 4, 4, 4, 4],
            [0, 4, 4, 4, 4, 4, 0, 0, 0, 4, 4, 4, 4, 4, 0, 0, 0, 4, 4, 4, 4, 4],
            [0, 4, 4, 4, 4, 4, 0, 0, 0, 4, 4, 4, 4, 4, 0, 0, 0, 4, 4, 4, 4, 4],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0],
        ],
        'transformed_output': [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 4, 4, 4, 4, 4, 0, 0, 0, 4, 4, 0, 0, 0, 0, 0, 0, 4, 4, 0, 0, 0],
            [0, 4, 4, 4, 4, 4, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0],
            [0, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [0, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [0, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        ]
    },
    {
        'input': [
            [0, 0, 0, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 6],
            [0, 3, 3, 3, 3, 0, 0, 0, 6, 6, 6, 6, 6, 6],
            [0, 3, 4, 4, 3, 0, 0, 0, 6, 6, 6, 6, 6, 6],
            [0, 3, 4, 4, 3, 0, 0, 0, 6, 6, 6, 6, 6, 6],
            [0, 3, 3, 3, 3, 0, 0, 0, 6, 6, 6, 6, 6, 6],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6],
            [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 6, 6],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ],
        'expected_output': [
            [0, 0, 0, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 6, 6, 6, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 6],
            [0, 3, 3, 3, 3, 0, 0, 0, 6, 6, 6, 6, 6, 6],
            [0, 3, 4, 4, 3, 0, 0, 0, 6, 6, 6, 6, 6, 6],
            [0, 3, 4, 4, 3, 0, 0, 0, 6, 6, 6, 6, 6, 6],
            [0, 3, 3, 3, 3, 0, 0, 0, 6, 6, 6, 6, 6, 6],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 3, 4, 4, 3, 0, 0, 0, 0, 0, 0, 6, 6],
            [0, 0, 3, 4, 4, 3, 0, 0, 0, 0, 0, 0, 6, 6],
            [0, 0, 3, 3, 3, 3, 0, 3, 3, 3, 3, 0, 6, 6],
            [0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 3, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 3, 4, 4, 3, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 0, 0, 0],
        ],
        'transformed_output': [
            [0, 0, 0, 6, 6, 6, 6, 6, 6, 0, 0, 0, 0, 0],
            [0, 0, 0, 6, 6, 6, 6, 6, 6, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 6, 6, 6, 6, 6, 6],
            [0, 3, 3, 3, 3, 0, 0, 0, 6, 6, 6, 6, 6, 6],
            [0, 3, 4, 4, 3, 0, 0, 0, 6, 6, 6, 6, 6, 6],
            [0, 3, 4, 4, 3, 0, 0, 0, 6, 6, 6, 6, 6, 6],
            [0, 3, 3, 3, 3, 0, 0, 0, 6, 6, 6, 6, 6, 6],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 3, 3, 3, 3, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 3, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6],
            [0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 0, 6, 6],
            [0, 0, 0, 0, 0, 0, 0, 3, 0, 0, 0, 0, 6, 6],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 6, 6],
        ]
    }
]

analysis = analyze_results(examples)
print(analysis)


```

*code_execution_result:*
outcome: 1
```
[{'incorrect_pixels': 69, 'expected_colors': {np.int64(0): np.int64(123), np.int64(3): np.int64(15), np.int64(4): np.int64(60)}, 'transformed_colors': {np.int64(0): np.int64(122), np.int64(3): np.int64(30), np.int64(4): np.int64(46)}}, {'incorrect_pixels': 34, 'expected_colors': {np.int64(0): np.int64(134), np.int64(3): np.int64(36), np.int64(4): np.int64(12), np.int64(6): np.int64(42)}, 'transformed_colors': {np.int64(0): np.int64(144), np.int64(3): np.int64(22), np.int64(4): np.int64(4), np.int64(6): np.int64(54)}}]

```
**YAML Fact Documentation**


```yaml
observations:
  - task: Copy and expand objects
  - example_1:
      input_objects:
        - color: 4
          shape: rectangle
          dimensions: [5, 5] # height, width
          count: 3
        - color: 3
          shape: rectangle
          dimensions: [3, 5]
          count: 1
      transformations:
        - action: replicate
          details: "Replicate existing objects next to original, maintaining shape, size and color. If object adjacent, do not replicate"
      notes: |
        The first object (color 4) should be replicated horizontally because there is space.
        The second object (color 3) should not be replicated, since there is no adjacent space.
        Single-color objects are treated as any other object, expanding where there's adjacent blank space.

  - example_2:
      input_objects:
        - color: 6
          shape: rectangle
          dimensions: [2, 3]
          count: 1
        - color: 6
          shape: rectangle
          dimensions: [4, 6]
          count: 1
        - color: 3
          shape: rectangle
          dimensions: [1,1]
          count: 1
        - color: 3
          shape: rectangle
          dimensions: [2,1]
          count: 1
        - color: 4
          shape: rectangle
          dimensions: [2,2]
          count: 1
      transformations:
        - action: replicate
          details: "Replicate single-color objects horizontally and/or vertically if adjacent space exists. No color changes"
      notes:
        Single cell object of color 3 at [9,2] replicates to occupy 4 cells in a rectangle with color 4 inside.
        single cell object of color 3 at [12,7] expands into a 4x4 object.
        Object of color 6 at 10,12 expands vertically.

```


**Natural Language Program**

1.  **Identify Objects:** Find all contiguous objects in the input grid. An object is defined as a group of one or more pixels of the same color that are connected (up, down, left, or right - not diagonally).
2.  **Replicate objects:** For each identified object, replicate adjacent to the original object, if space is available.
3.  **Termination:** Do not replicate an object where it would overlap with another.

This natural language program captures the core transformation rule, emphasizing the replication of all the objects and the adjacency rule.

