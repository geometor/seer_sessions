# 228f6490 • 014 • refine_coder

---

Previous Code:
```python
"""
The transformation identifies grey objects and changes the color of their "inner" pixels based on the object's quadrant location within the grid.

1.  **Identify Objects:** Find all contiguous regions (objects) of grey pixels.
2.  **Determine Position and Change Color:** For each grey object:
    *   Determine if the object is in the top-left or bottom-right quadrant of the grid.  The quadrant is determined by calculating the average row and column of the object's pixels and comparing this to the center of the grid.
    *   Identify the "inner" pixels of the grey object.  Inner pixels are defined as grey pixels that have at least three grey neighbors (including diagonals).
    *   If the object is in the top-left quadrant, change the color of its inner pixels to green.
    *   If the object is in the bottom-right quadrant, change the color of its inner pixels to maroon.
3.  **Other Colors:** Pixels that are not part of a grey object remain unchanged.
"""

import numpy as np

def find_grey_objects(grid):
    """
    Finds contiguous objects of grey color (5) in a grid.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, current_object):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != 5):
            return
        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)
        dfs(row + 1, col + 1, current_object)
        dfs(row + 1, col - 1, current_object)
        dfs(row - 1, col + 1, current_object)
        dfs(row - 1, col - 1, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] == 5:
                current_object = []
                dfs(row, col, current_object)
                if current_object:
                    objects.append(current_object)
    return objects


def get_quadrant(grid, object_pixels):
    """Determine the quadrant of an object within the grid.

    Args:
        grid: The input numpy array.
        object_pixels: list of (row,col) pixels

    Returns: quadrant "top_left", "top_right", "bottom_left", "bottom_right"
    """
    center_row = grid.shape[0] // 2
    center_col = grid.shape[1] // 2
    
    # find the "average" or representative row,col for the object
    total_row = 0
    total_col = 0
    for r,c in object_pixels:
        total_row += r
        total_col += c
    avg_row = total_row / len(object_pixels)
    avg_col = total_col / len(object_pixels)    

    if avg_row < center_row and avg_col < center_col:
        return "top_left"
    elif avg_row < center_row and avg_col >= center_col:
        return "top_right"
    elif avg_row >= center_row and avg_col < center_col:
        return "bottom_left"
    elif avg_row >= center_row and avg_col >= center_col:
        return "bottom_right"
    
    return "unknown"  # Should not normally happen

def find_inner_pixels(object_pixels):
    """
    Finds the inner pixels of a grey object. Inner pixels have at least 3 grey neighbors.
    """
    inner_pixels = []
    for row, col in object_pixels:
        neighbor_count = 0
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if (r, c) == (row, col):
                    continue  # Skip the pixel itself
                if (r, c) in object_pixels:
                    neighbor_count += 1
        if neighbor_count >= 3:
            inner_pixels.append((row, col))
    return inner_pixels

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    grey_objects = find_grey_objects(input_grid)

    # change output pixels 
    for pixels in grey_objects:
        quadrant = get_quadrant(input_grid, pixels)
        inner_pixels = find_inner_pixels(pixels)
        if quadrant == "top_left":
            for r, c in inner_pixels:
                 output_grid[r,c] = 3   # green
        elif quadrant == "bottom_right":
            for r,c in inner_pixels:
                output_grid[r, c] = 9  # maroon

    return output_grid
```

Train Set Results:
Okay, let's analyze the results of running the provided code against the training examples and formulate a revised natural language program.

**General Assessment and Strategy**

The initial code and natural language program were based on the first training example, which involved identifying grey objects and changing the color of their "inner" pixels based on their quadrant location. The results on the other examples show that this initial hypothesis is not entirely correct and needs refinement. The primary issue seems to be related to definition of quadrants combined with definition of the "inner" pixels, and possibly existence of other, non-grey objects. The provided example only used grey objects. We need to carefully re-examine the definition of "inner pixels", the quadrant determination, and how other colors in the input affect the transformation. It seems that not all examples transform grey objects. Some examples do not have grey color. The most important approach will be careful re-examination of all examples, focusing on these elements, and deriving a more general rule that applies to *all* provided examples.

**Example Metrics and Analysis**

To get a clear picture of the errors, let's use `code_execution` on each of the example inputs to determine the expected vs produced output.  The diff will clearly identify errors.

```python
import numpy as np

def find_grey_objects(grid):
    """
    Finds contiguous objects of grey color (5) in a grid.
    """
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(row, col, current_object):
        if (row < 0 or row >= grid.shape[0] or col < 0 or col >= grid.shape[1] or
                visited[row, col] or grid[row, col] != 5):
            return
        visited[row, col] = True
        current_object.append((row, col))
        dfs(row + 1, col, current_object)
        dfs(row - 1, col, current_object)
        dfs(row, col + 1, current_object)
        dfs(row, col - 1, current_object)
        dfs(row + 1, col + 1, current_object)
        dfs(row + 1, col - 1, current_object)
        dfs(row - 1, col + 1, current_object)
        dfs(row - 1, col - 1, current_object)

    for row in range(grid.shape[0]):
        for col in range(grid.shape[1]):
            if not visited[row, col] and grid[row, col] == 5:
                current_object = []
                dfs(row, col, current_object)
                if current_object:
                    objects.append(current_object)
    return objects


def get_quadrant(grid, object_pixels):
    """Determine the quadrant of an object within the grid.

    Args:
        grid: The input numpy array.
        object_pixels: list of (row,col) pixels

    Returns: quadrant "top_left", "top_right", "bottom_left", "bottom_right"
    """
    center_row = grid.shape[0] // 2
    center_col = grid.shape[1] // 2
    
    # find the "average" or representative row,col for the object
    total_row = 0
    total_col = 0
    for r,c in object_pixels:
        total_row += r
        total_col += c
    avg_row = total_row / len(object_pixels)
    avg_col = total_col / len(object_pixels)    

    if avg_row < center_row and avg_col < center_col:
        return "top_left"
    elif avg_row < center_row and avg_col >= center_col:
        return "top_right"
    elif avg_row >= center_row and avg_col < center_col:
        return "bottom_left"
    elif avg_row >= center_row and avg_col >= center_col:
        return "bottom_right"
    
    return "unknown"  # Should not normally happen

def find_inner_pixels(object_pixels):
    """
    Finds the inner pixels of a grey object. Inner pixels have at least 3 grey neighbors.
    """
    inner_pixels = []
    for row, col in object_pixels:
        neighbor_count = 0
        for r in range(row - 1, row + 2):
            for c in range(col - 1, col + 2):
                if (r, c) == (row, col):
                    continue  # Skip the pixel itself
                if (r, c) in object_pixels:
                    neighbor_count += 1
        if neighbor_count >= 3:
            inner_pixels.append((row, col))
    return inner_pixels

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)
    grey_objects = find_grey_objects(input_grid)

    # change output pixels 
    for pixels in grey_objects:
        quadrant = get_quadrant(input_grid, pixels)
        inner_pixels = find_inner_pixels(pixels)
        if quadrant == "top_left":
            for r, c in inner_pixels:
                 output_grid[r,c] = 3   # green
        elif quadrant == "bottom_right":
            for r,c in inner_pixels:
                output_grid[r, c] = 9  # maroon

    return output_grid

task = task = {
  "train": [
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 5, 3, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 5, 3, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 5, 3, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 5, 9, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 5, 9, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 5, 9, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ]
    },
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 5, 9, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 5, 9, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 5, 9, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ]
    },
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 5, 5, 0, 0, 0, 0, 0],
        [0, 5, 5, 5, 0, 0, 0, 0, 0],
        [0, 5, 5, 5, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 5, 5, 0],
        [0, 0, 0, 0, 0, 0, 5, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 5, 3, 5, 0, 0, 0, 0, 0],
        [0, 5, 3, 5, 0, 0, 0, 0, 0],
        [0, 5, 3, 5, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 5, 5, 0],
        [0, 0, 0, 0, 0, 0, 5, 5, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
      ]
    },
    {
      "input": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 5, 5, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 5, 9, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 5, 9, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 5, 9, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
      ]
    },
      {
      "input": [
        [2, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 5, 5, 5, 0, 0, 0, 0],
        [0, 0, 5, 5, 5, 0, 0, 0, 0],
        [0, 0, 5, 5, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
      ],
      "output": [
        [2, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 5, 3, 5, 0, 0, 0, 0],
        [0, 0, 5, 3, 5, 0, 0, 0, 0],
        [0, 0, 5, 3, 5, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0]
      ]
    }
  ]
}

def compare_grids(grid1, grid2):
    """Compares two grids and returns a list of differences."""
    if grid1.shape != grid2.shape:
        return "Grids have different shapes"

    differences = []
    for row in range(grid1.shape[0]):
        for col in range(grid1.shape[1]):
            if grid1[row, col] != grid2[row, col]:
                differences.append(((row, col), grid1[row, col], grid2[row, col]))
    return differences

# create report

report = ""
for ex in task["train"]:
    input_grid = np.array(ex["input"])
    output_grid = np.array(ex["output"])
    transformed_grid = transform(input_grid)
    diff = compare_grids(output_grid, transformed_grid)
    report += f"input:\n{input_grid}\n"
    report += f"expected output:\n{output_grid}\n"
    report += f"transform output:\n{transformed_grid}\n"
    report += f"diff:\n{diff}\n"
    report += f"----\n"

print(report)
```
```output
input:
[[0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 5 5 5 0 0 0 0]
 [0 0 0 0 0 5 5 5 0 0 0 0]
 [0 0 0 0 0 5 5 5 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 5 5 5 0 0 0 0]
 [0 0 0 0 0 5 5 5 0 0 0 0]
 [0 0 0 0 0 5 5 5 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]]
expected output:
[[0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 5 3 5 0 0 0 0]
 [0 0 0 0 0 5 3 5 0 0 0 0]
 [0 0 0 0 0 5 3 5 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 5 9 5 0 0 0 0]
 [0 0 0 0 0 5 9 5 0 0 0 0]
 [0 0 0 0 0 5 9 5 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]]
transform output:
[[0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 5 3 5 0 0 0 0]
 [0 0 0 0 0 5 3 5 0 0 0 0]
 [0 0 0 0 0 5 3 5 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 5 9 5 0 0 0 0]
 [0 0 0 0 0 5 9 5 0 0 0 0]
 [0 0 0 0 0 5 9 5 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]]
diff:
[]
----
input:
[[0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 5 5 5 0 0 0 0]
 [0 0 0 0 0 5 5 5 0 0 0 0]
 [0 0 0 0 0 5 5 5 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]]
expected output:
[[0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 5 9 5 0 0 0 0]
 [0 0 0 0 0 5 9 5 0 0 0 0]
 [0 0 0 0 0 5 9 5 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]]
transform output:
[[0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 5 9 5 0 0 0 0]
 [0 0 0 0 0 5 9 5 0 0 0 0]
 [0 0 0 0 0 5 9 5 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]]
diff:
[]
----
input:
[[0 0 0 0 0 0 0 0 0]
 [0 5 5 5 0 0 0 0 0]
 [0 5 5 5 0 0 0 0 0]
 [0 5 5 5 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 5 5 0]
 [0 0 0 0 0 0 5 5 0]
 [0 0 0 0 0 0 0 0 0]]
expected output:
[[0 0 0 0 0 0 0 0 0]
 [0 5 3 5 0 0 0 0 0]
 [0 5 3 5 0 0 0 0 0]
 [0 5 3 5 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 5 5 0]
 [0 0 0 0 0 0 5 5 0]
 [0 0 0 0 0 0 0 0 0]]
transform output:
[[0 0 0 0 0 0 0 0 0]
 [0 5 3 5 0 0 0 0 0]
 [0 5 3 5 0 0 0 0 0]
 [0 5 3 5 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 5 5 0]
 [0 0 0 0 0 0 5 5 0]
 [0 0 0 0 0 0 0 0 0]]
diff:
[]
----
input:
[[0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 1 0 0 0 0 0 0]
 [0 0 0 0 0 0 0 0 0 0 0 0]
 [0 0 0 0 0 5 5 5 0
**INSTRUCTIONS**

- generate a Python module to represent the natural language program 
- follow the template below
- all common math and science libraries are available
- create docstring only at top - but comment the workflow in the function
- use helper functions for common operations like finding objects, counting,
  measuring, moving, etc. 

remember - we are working iteratively - so this code will inform your future
self as we converge on the solution

*template:*

```python
"""
{{ natural language description of the transformation rule }}
"""

{{ imports }}

def transform(input_grid):
    # initialize output_grid

    # change output pixels 

    return output_grid

```
