
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
Okay, let's analyze the provided information and strategize for improving the natural language program and subsequently the code.

**General Assessment and Strategy**

The initial code was based on observations from the first training example, and it's clear that it doesn't generalize well to the second example. The core issue is that the replication logic is too simplistic. It replicates objects to the right and bottom based on available space, but it doesn't correctly handle:

1.  **Conditional Replication:** The replication seems to depend on more than just available space. There's a pattern related to the shape and arrangement of the original objects.
2.  **Single Cell Object Expansion:** The `expand_single_cell_objects` function has hardcoded logic for colors 3 and 6, and its expansion logic isn't universally correct based on the second example. It expands some single cell objects, others it replicates with its shape.
3. **Object Selection for Copy:** It appears that all objects are being copied, including mixed color objects.

**Strategy:**

1.  **Re-examine Object Definition:** Ensure the `find_objects` function correctly identifies contiguous regions of the *same* color as single objects.
2.  **Analyze Replication Conditions:** Carefully examine both examples to discern *when* replication occurs. Is it based on object shape, size, color, position relative to other objects, or a combination of these?
3.  **Refine Single Cell Handling:** Determine the precise rule for expanding single-cell objects. Does it apply to all colors, or only specific ones? Is the expansion always in the same direction/amount? Is it replicating or expanding.
4. **Object interaction**: Establish weather objects interact based on color, adjacency and other factors.

**Gather Metrics and Evidence**

Let's use `tool_code` to gather more detailed information about the objects in each example. I will build a comprehensive object report, then use this as the basis for the yaml.



*code_execution:*
```python
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
    if not object_coords:
        return 0
    r,c = object_coords[0]
    return grid[r,c]

def get_object_bounds(object_coords):

    min_row = min(r for r, _ in object_coords)
    max_row = max(r for r, _ in object_coords)
    min_col = min(c for _, c in object_coords)
    max_col = max(c for _, c in object_coords)

    return min_row, max_row, min_col, max_col

def analyze_example(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    input_objects = find_objects(input_grid)
    output_objects = find_objects(output_grid)

    input_object_data = []
    for obj in input_objects:
      color = get_object_color(input_grid, obj)
      min_row, max_row, min_col, max_col = get_object_bounds(obj)
      width = max_col - min_col + 1
      height = max_row - min_row + 1
      size = len(obj)
      input_object_data.append({
          'color': color,
          'min_row': min_row,
          'max_row': max_row,
          'min_col': min_col,
          'max_col': max_col,
          'width': width,
          'height': height,
          'size': size
      })

    output_object_data = []
    for obj in output_objects:
      color = get_object_color(output_grid, obj)
      min_row, max_row, min_col, max_col = get_object_bounds(obj)
      width = max_col - min_col + 1
      height = max_row - min_row + 1
      size = len(obj)
      output_object_data.append({
          'color': color,
          'min_row': min_row,
          'max_row': max_row,
          'min_col': min_col,
          'max_col': max_col,
          'width': width,
          'height': height,
          'size': size
      })

    return input_object_data, output_object_data



input_grid1 = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 4, 4, 4, 4, 4, 0, 0, 0, 4, 0, 0, 0, 0, 0, 0, 0, 4, 0, 0, 0, 0],
[0, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 4, 4, 4, 4, 4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0]
]
output_grid1 = [
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 4, 4, 4, 4, 4, 0, 0, 0, 4, 4, 4, 4, 4, 0, 0, 0, 4, 4, 4, 4, 4],
[0, 4, 4, 4, 4, 4, 0, 0, 0, 4, 4, 4, 4, 4, 0, 0, 0, 4, 4, 4, 4, 4],
[0, 4, 4, 4, 4, 4, 0, 0, 0, 4, 4, 4, 4, 4, 0, 0, 0, 4, 4, 4, 4, 4],
[0, 4, 4, 4, 4, 4, 0, 0, 0, 4, 4, 4, 4, 4, 0, 0, 0, 4, 4, 4, 4, 4],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0],
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 3, 0, 0, 0, 0, 0]
]

input_grid2 = [
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
[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
]
output_grid2 = [
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
[0, 0, 0, 0, 0, 0, 0, 3, 3, 3, 3, 0, 0, 0]
]

input_data1, output_data1 = analyze_example(input_grid1, output_grid1)
input_data2, output_data2 = analyze_example(input_grid2, output_grid2)

print("Example 1 Input Objects:")
print(input_data1)
print("Example 1 Output Objects:")
print(output_data1)
print("\nExample 2 Input Objects:")
print(input_data2)
print("Example 2 Output Objects:")
print(output_data2)

```

*code_execution_result:*
outcome: 1
```
Example 1 Input Objects:
[{'color': np.int64(4), 'min_row': 1, 'max_row': 4, 'min_col': 1, 'max_col': 5, 'width': 5, 'height': 4, 'size': 20}, {'color': np.int64(4), 'min_row': 1, 'max_row': 1, 'min_col': 9, 'max_col': 9, 'width': 1, 'height': 1, 'size': 1}, {'color': np.int64(4), 'min_row': 1, 'max_row': 1, 'min_col': 17, 'max_col': 17, 'width': 1, 'height': 1, 'size': 1}, {'color': np.int64(3), 'min_row': 6, 'max_row': 8, 'min_col': 12, 'max_col': 16, 'width': 5, 'height': 3, 'size': 15}]
Example 1 Output Objects:
[{'color': np.int64(4), 'min_row': 1, 'max_row': 4, 'min_col': 1, 'max_col': 5, 'width': 5, 'height': 4, 'size': 20}, {'color': np.int64(4), 'min_row': 1, 'max_row': 4, 'min_col': 9, 'max_col': 13, 'width': 5, 'height': 4, 'size': 20}, {'color': np.int64(4), 'min_row': 1, 'max_row': 4, 'min_col': 17, 'max_col': 21, 'width': 5, 'height': 4, 'size': 20}, {'color': np.int64(3), 'min_row': 6, 'max_row': 8, 'min_col': 12, 'max_col': 16, 'width': 5, 'height': 3, 'size': 15}]

Example 2 Input Objects:
[{'color': np.int64(6), 'min_row': 0, 'max_row': 1, 'min_col': 3, 'max_col': 5, 'width': 3, 'height': 2, 'size': 6}, {'color': np.int64(6), 'min_row': 2, 'max_row': 6, 'min_col': 8, 'max_col': 13, 'width': 6, 'height': 5, 'size': 30}, {'color': np.int64(3), 'min_row': 3, 'max_row': 6, 'min_col': 1, 'max_col': 4, 'width': 4, 'height': 4, 'size': 12}, {'color': np.int64(4), 'min_row': 4, 'max_row': 5, 'min_col': 2, 'max_col': 3, 'width': 2, 'height': 2, 'size': 4}, {'color': np.int64(3), 'min_row': 9, 'max_row': 9, 'min_col': 2, 'max_col': 2, 'width': 1, 'height': 1, 'size': 1}, {'color': np.int64(6), 'min_row': 10, 'max_row': 12, 'min_col': 12, 'max_col': 13, 'width': 2, 'height': 3, 'size': 6}, {'color': np.int64(3), 'min_row': 12, 'max_row': 12, 'min_col': 7, 'max_col': 7, 'width': 1, 'height': 1, 'size': 1}]
Example 2 Output Objects:
[{'color': np.int64(6), 'min_row': 0, 'max_row': 1, 'min_col': 3, 'max_col': 5, 'width': 3, 'height': 2, 'size': 6}, {'color': np.int64(6), 'min_row': 2, 'max_row': 6, 'min_col': 8, 'max_col': 13, 'width': 6, 'height': 5, 'size': 30}, {'color': np.int64(3), 'min_row': 3, 'max_row': 6, 'min_col': 1, 'max_col': 4, 'width': 4, 'height': 4, 'size': 12}, {'color': np.int64(4), 'min_row': 4, 'max_row': 5, 'min_col': 2, 'max_col': 3, 'width': 2, 'height': 2, 'size': 4}, {'color': np.int64(3), 'min_row': 9, 'max_row': 12, 'min_col': 2, 'max_col': 5, 'width': 4, 'height': 4, 'size': 12}, {'color': np.int64(4), 'min_row': 10, 'max_row': 11, 'min_col': 3, 'max_col': 4, 'width': 2, 'height': 2, 'size': 4}, {'color': np.int64(6), 'min_row': 10, 'max_row': 12, 'min_col': 12, 'max_col': 13, 'width': 2, 'height': 3, 'size': 6}, {'color': np.int64(3), 'min_row': 12, 'max_row': 15, 'min_col': 7, 'max_col': 10, 'width': 4, 'height': 4, 'size': 12}, {'color': np.int64(4), 'min_row': 13, 'max_row': 14, 'min_col': 8, 'max_col': 9, 'width': 2, 'height': 2, 'size': 4}]

```
**YAML Fact Base**


```yaml
example_1:
  input:
    objects:
      - color: 4  # Yellow
        shape: rectangle
        width: 5
        height: 4
        count: 1
        replication: horizontal
        copies: 3
      - color: 4
        shape: single_cell
        width: 1
        height: 1
        count: 2
        replication: horizontal
        copies: 3
      - color: 3  # Green
        shape: rectangle
        width: 5
        height: 3
        count: 1
        replication: none
        copies: 1

  output:
     grid_changes:
       - object_color: 4
         change_type: replicate
         direction: horizontal
         final_count: 3
       - object_color: 3
         change_type: none

example_2:
  input:
    objects:
      - color: 6  # Magenta
        shape: rectangle
        width: 3
        height: 2
        count: 1
        replication: none
        copies: 1
      - color: 6  # Magenta
        shape: rectangle
        width: 6
        height: 5
        count: 1
        replication: none
        copies: 1
      - color: 3  # Green
        shape: rectangle
        width: 4
        height: 4
        count: 1
        notes: contains_object
        contains:
          - color: 4
            shape: rectangle
            width: 2
            height: 2
        replication: horizontal
        copies: 2
      - color: 4 #yellow
        shape: rectangle
        width: 2
        height: 2
        count: 1
        contained_by:
          - color: 3
        replication: horizontal
        copies: 2
      - color: 3  # Green
        shape: single_cell
        width: 1
        height: 1
        count: 1
        replication: horizontal, expand
        copies: 4, square
      - color: 6 # Magenta
        shape: rectangle
        width: 2
        height: 3
        count: 1
        replication: none
      - color: 3 # Green
        shape: single_cell
        width: 1
        height: 1
        count: 1
        replication: vertical, expand
        copies: 4, square

  output:
    grid_changes:
       - object_color: 3
         change_type: replicate_if_contains_other_objects
         direction: horizontal
       - object_color: 3
         change_type: expand
         direction: both
       - object_color: 6
         change_type: none

```


**Natural Language Program**

1.  **Identify Objects:** Find all contiguous regions (objects) of the same non-zero color in the input grid.
2.  **Object Replication - Containing Objects**:
    *   If an object of color 3 contains an object of color 4, then make one additional copy to the right. The contained object is also copied.
3.  **Object Replication - Single Cell**:
    *   If the input grid includes a single cell of color 3 and does *not* contain any other objects, replicate the object, making a 4x4 square, copying horizontally and vertically.
    *    If the input grid includes a single cell of color 3 and does *not* contain any other objects, replicate the object, making a 4x4 square, copying horizontally and vertically.
4.  **No Other Replication:** Objects of other colors, or objects not meeting the above criteria, are not replicated. Their initial representation in the input grid is simply copied to the output grid.
5. **Mixed Color Objects**
    * Mixed color objects are treated as distinct, individual, single-color objects and do not impact processing.


