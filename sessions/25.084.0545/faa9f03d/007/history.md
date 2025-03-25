
Previous Code:
```python
"""
Transforms the input grid based on example-specific and generalized rules,
handling background identification, object manipulation, and color replacements.
"""

import numpy as np
from collections import deque

def find_objects(grid):
    """
    Identifies contiguous regions of the same color as objects.
    Returns a dictionary where keys are colors and values are lists of (row, col) tuples.
    """
    objects = {}
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, color, obj):
        if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r, c] != color:
            return
        visited.add((r, c))
        obj.append((r, c))
        dfs(r + 1, c, color, obj)
        dfs(r - 1, c, color, obj)
        dfs(r, c + 1, color, obj)
        dfs(r, c - 1, color, obj)

    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                color = grid[r, c]
                if color not in objects:
                    objects[color] = []
                dfs(r, c, color, objects[color])
    return objects

def get_neighbors(grid, r, c):
    """Returns the valid neighbors (including diagonals) of a cell."""
    rows, cols = grid.shape
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
    return neighbors

def flood_fill(grid, start_r, start_c, target_color, replacement_color):
    """Performs a flood fill on the grid."""
    rows, cols = grid.shape
    q = deque([(start_r, start_c)])
    visited = set()

    if grid[start_r, start_c] != target_color:
      return #start at the correct color

    while q:
        r, c = q.popleft()
        if (r,c) in visited:
          continue
        visited.add((r,c))

        if grid[r, c] == target_color:
            grid[r, c] = replacement_color
            for nr, nc in get_neighbors(grid, r, c):
                q.append((nr, nc))



def transform(input_grid):
    """
    Transforms the input grid according to the observed rules.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    objects = find_objects(input_grid)
    background_color = 0  # Identified as background

    # Example 1 context
    if 2 in objects:  # Red exists, apply Example 1 rules
        for r, c in objects.get(2, []):
            output_grid[r, c] = 3  # Replace red with green

        #fill adjacent greens
        for r in range(rows):
          for c in range(cols):
            if input_grid[r,c] == 3:
              for nr, nc in get_neighbors(input_grid,r,c):
                if input_grid[nr,nc] == 2:
                  output_grid[r,c] = 1
                  break

    # Example 2 context
    if 4 in objects and 6 not in objects:
        for r,c in objects.get(4, []):
          output_grid[r,c] = 3

    # Example 3 context
    if 6 in objects: # Magenta exists, apply example 3 rules

        #replace yellow with magenta
        for r, c in objects.get(4, []):
          output_grid[r,c] = 6

        # Magenta expansion (flood fill from each magenta pixel)
        magenta_pixels = objects[6]
        for r, c in magenta_pixels:
            flood_fill(output_grid, r, c, background_color, 6)

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 3 0 0
1 1 1 1 0 0 0 0 0 3 0 0
0 0 0 1 0 0 0 0 0 3 0 0
2 3 3 3 2 0 0 0 0 3 0 0
0 0 0 1 3 0 0 0 0 3 0 0
0 0 0 1 3 1 1 0 0 3 0 0
0 0 0 0 3 0 1 0 0 3 0 0
0 0 0 0 3 0 1 0 0 3 0 0
0 0 0 0 2 3 3 3 0 2 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 1 0 1 1 0
0 0 0 0 0 0 0 0 0 0 1 1
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 3 0 0
1 1 1 1 0 0 0 0 0 3 0 0
0 0 0 1 0 0 0 0 0 3 0 0
3 3 3 1 3 0 0 0 0 3 0 0
0 0 0 1 3 0 0 0 0 3 0 0
0 0 0 1 1 1 1 0 0 3 0 0
0 0 0 0 3 0 1 0 0 3 0 0
0 0 0 0 3 0 1 0 0 3 0 0
0 0 0 0 3 3 1 3 3 3 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 1 1
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 3 0 0
1 1 1 1 0 0 0 0 0 3 0 0
0 0 0 1 0 0 0 0 0 3 0 0
3 1 3 1 3 0 0 0 0 3 0 0
0 0 0 1 1 0 0 0 0 3 0 0
0 0 0 1 3 1 1 0 0 3 0 0
0 0 0 0 3 0 1 0 0 3 0 0
0 0 0 0 1 0 1 0 0 1 0 0
0 0 0 0 3 1 3 3 0 3 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 1 0 1 1 0
0 0 0 0 0 0 0 0 0 0 1 1
```
Match: False
Pixels Off: 9
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 12.5

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 7 0
7 7 7 7 0 0 0 0 0 0 7 0
3 3 3 3 3 0 3 3 3 4 7 0
0 0 0 7 0 0 0 0 3 0 7 0
0 0 0 0 0 0 0 0 0 0 7 0
0 0 0 7 7 7 7 0 3 0 0 0
0 0 0 0 0 0 7 0 3 0 7 0
0 0 7 7 7 7 7 0 3 0 7 0
0 0 7 0 0 0 0 0 3 0 7 0
3 3 0 3 3 3 3 3 3 0 7 0
0 0 7 7 7 7 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 7 0
7 7 7 7 0 0 0 0 0 0 7 0
0 0 0 7 0 0 0 0 3 3 3 3
0 0 0 7 0 0 0 0 3 0 7 0
0 0 0 7 0 0 0 0 3 0 7 0
0 0 0 7 7 7 7 0 3 0 7 0
0 0 0 0 0 0 7 0 3 0 7 0
0 0 7 7 7 7 7 0 3 0 7 0
0 0 7 0 0 0 0 0 3 0 7 0
3 3 3 3 3 3 3 3 3 0 7 0
0 0 7 7 7 7 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 7 0
7 7 7 7 0 0 0 0 0 0 7 0
3 3 3 3 3 0 3 3 3 3 7 0
0 0 0 7 0 0 0 0 3 0 7 0
0 0 0 0 0 0 0 0 0 0 7 0
0 0 0 7 7 7 7 0 3 0 0 0
0 0 0 0 0 0 7 0 3 0 7 0
0 0 7 7 7 7 7 0 3 0 7 0
0 0 7 0 0 0 0 0 3 0 7 0
3 3 0 3 3 3 3 3 3 0 7 0
0 0 7 7 7 7 7 7 7 7 7 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 13
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 18.05555555555557

## Example 3:
Input:
```
0 1 0 0 0 0 1 0 0 0 6 0
0 1 0 0 0 0 1 0 0 0 6 0
6 1 6 6 6 6 0 6 0 6 6 0
0 1 0 0 0 0 1 0 0 0 4 0
0 0 0 0 0 0 1 0 0 0 0 0
0 1 1 1 0 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 1 0 0 0 0 1 0 0 0 0 0
0 1 0 0 0 0 1 0 0 0 0 0
6 1 6 6 6 6 1 6 6 6 6 0
0 1 0 0 0 0 1 0 0 0 6 0
0 1 0 0 0 0 1 0 0 0 6 0
0 1 1 1 1 1 1 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0 6 0
```
Transformed Output:
```
0 1 0 0 0 0 1 0 0 0 6 0
0 1 0 0 0 0 1 0 0 0 6 0
6 1 6 6 6 6 0 6 0 6 6 0
0 1 0 0 0 0 1 0 0 0 6 0
0 0 0 0 0 0 1 0 0 0 0 0
0 1 1 1 0 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 14
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 19.44444444444443
Here's an analysis of the provided examples, results, and a proposed strategy for improving the natural language program and subsequently the code.

**General Assessment:**

The code performs reasonably well in identifying objects and applying some color transformations. However, it struggles with correctly applying the context-specific rules and propagation of color changes (especially in Examples 1 and 3). The flood fill implementation seems to have a bug, or is being misapplied, as it should be filling the entire grid, which isn't happening. The current strategy of having separate conditional blocks for each example's context is not scalable and misses the underlying general rule. We need to unify the logic. The main errors seem to stem from:

1.  Incorrect or incomplete color replacement rules.
2.  Problems with the flood fill's stopping condition or neighbor selection.
3.  A lack of generalization across the different examples.

**Strategy for Resolving Errors:**

1.  **Unify Rules:** Instead of separate `if` blocks for each example, identify a common pattern. The core pattern seems to be: replace some colors, then apply a flood fill using a specific color, conditional on object adjacencies.
2.  **Improve Flood Fill:** Review the `flood_fill` function. Ensure it correctly uses neighbors (including diagonals) and has the right stopping conditions.
3.  **Refine Color Replacement:** Examine how colors are being replaced. It appears the logic for "adjacent" replacements needs clarification and potentially a more iterative approach.
4.  **Iterative Refinement:** Instead of trying to handle all changes in one go, consider an iterative process where color replacements and flood fills might influence subsequent steps.

**Gather Metrics and Observations (using code):**

Let's collect some information about the grids and objects.



*code_execution:*
```python
import numpy as np
from collections import Counter

def analyze_grid(grid):
    """Analyzes a single grid and returns relevant metrics."""
    rows, cols = grid.shape
    unique_colors = np.unique(grid)
    color_counts = Counter(grid.flatten())
    num_objects = 0

    visited = set()
    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                num_objects += 1
                color = grid[r,c]
                dfs(grid, r, c, color, visited)

    return {
        "rows": rows,
        "cols": cols,
        "unique_colors": unique_colors.tolist(),
        "color_counts": dict(color_counts),
        "num_objects": num_objects
    }

def dfs(grid, r, c, color, visited):
    rows, cols = grid.shape
    if (r, c) in visited or r < 0 or r >= rows or c < 0 or c >= cols or grid[r, c] != color:
        return
    visited.add((r, c))
    dfs(grid, r + 1, c, color, visited)
    dfs(grid, r - 1, c, color, visited)
    dfs(grid, r, c + 1, color, visited)
    dfs(grid, r, c - 1, color, visited)

# Example data (replace with actual input grids)
example1_input = np.array([[0,0,0,0,0,0,0,0,0,3,0,0],[1,1,1,1,0,0,0,0,0,3,0,0],[0,0,0,1,0,0,0,0,0,3,0,0],[2,3,3,3,2,0,0,0,0,3,0,0],[0,0,0,1,3,0,0,0,0,3,0,0],[0,0,0,1,3,1,1,0,0,3,0,0],[0,0,0,0,3,0,1,0,0,3,0,0],[0,0,0,0,3,0,1,0,0,3,0,0],[0,0,0,0,2,3,3,3,0,2,0,0],[0,0,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,1,1,0,1,1,0],[0,0,0,0,0,0,0,0,0,0,1,1]])
example1_expected = np.array([[0,0,0,0,0,0,0,0,0,3,0,0],[1,1,1,1,0,0,0,0,0,3,0,0],[0,0,0,1,0,0,0,0,0,3,0,0],[3,3,3,1,3,0,0,0,0,3,0,0],[0,0,0,1,3,0,0,0,0,3,0,0],[0,0,0,1,1,1,1,0,0,3,0,0],[0,0,0,0,3,0,1,0,0,3,0,0],[0,0,0,0,3,0,1,0,0,3,0,0],[0,0,0,0,3,3,1,3,3,3,0,0],[0,0,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,1,1,1,1,1,0],[0,0,0,0,0,0,0,0,0,0,1,1]])
example1_output = np.array([[0,0,0,0,0,0,0,0,0,3,0,0],[1,1,1,1,0,0,0,0,0,3,0,0],[0,0,0,1,0,0,0,0,0,3,0,0],[3,1,3,1,3,0,0,0,0,3,0,0],[0,0,0,1,1,0,0,0,0,3,0,0],[0,0,0,1,3,1,1,0,0,3,0,0],[0,0,0,0,3,0,1,0,0,1,0,0],[0,0,0,0,1,0,1,0,0,1,0,0],[0,0,0,0,3,1,3,3,0,3,0,0],[0,0,0,0,0,0,1,0,0,0,0,0],[0,0,0,0,0,0,1,1,0,1,1,0],[0,0,0,0,0,0,0,0,0,0,1,1]])
example2_input = np.array([[0,0,0,0,0,0,0,0,0,0,7,0],[7,7,7,7,0,0,0,0,0,0,7,0],[3,3,3,3,3,0,3,3,3,4,7,0],[0,0,0,7,0,0,0,0,3,0,7,0],[0,0,0,0,0,0,0,0,0,0,7,0],[0,0,0,7,7,7,7,0,3,0,0,0],[0,0,0,0,0,0,7,0,3,0,7,0],[0,0,7,7,7,7,7,0,3,0,7,0],[0,0,7,0,0,0,0,0,3,0,7,0],[3,3,0,3,3,3,3,3,3,0,7,0],[0,0,7,7,7,7,7,7,7,7,7,0],[0,0,0,0,0,0,0,0,0,0,0,0]])
example2_expected = np.array([[0,0,0,0,0,0,0,0,0,0,7,0],[7,7,7,7,0,0,0,0,0,0,7,0],[0,0,0,7,0,0,0,0,3,3,3,3],[0,0,0,7,0,0,0,0,3,0,7,0],[0,0,0,7,0,0,0,0,3,0,7,0],[0,0,0,7,7,7,7,0,3,0,7,0],[0,0,0,0,0,0,7,0,3,0,7,0],[0,0,7,7,7,7,7,0,3,0,7,0],[0,0,7,0,0,0,0,0,3,0,7,0],[3,3,3,3,3,3,3,3,3,0,7,0],[0,0,7,7,7,7,7,7,7,7,7,0],[0,0,0,0,0,0,0,0,0,0,0,0]])
example2_output = np.array([[0,0,0,0,0,0,0,0,0,0,7,0],[7,7,7,7,0,0,0,0,0,0,7,0],[3,3,3,3,3,0,3,3,3,3,7,0],[0,0,0,7,0,0,0,0,3,0,7,0],[0,0,0,0,0,0,0,0,0,0,7,0],[0,0,0,7,7,7,7,0,3,0,0,0],[0,0,0,0,0,0,7,0,3,0,7,0],[0,0,7,7,7,7,7,0,3,0,7,0],[0,0,7,0,0,0,0,0,3,0,7,0],[3,3,0,3,3,3,3,3,3,0,7,0],[0,0,7,7,7,7,7,7,7,7,7,0],[0,0,0,0,0,0,0,0,0,0,0,0]])
example3_input = np.array([[0,1,0,0,0,0,1,0,0,0,6,0],[0,1,0,0,0,0,1,0,0,0,6,0],[6,1,6,6,6,6,0,6,0,6,6,0],[0,1,0,0,0,0,1,0,0,0,4,0],[0,0,0,0,0,0,1,0,0,0,0,0],[0,1,1,1,0,1,1,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0]])
example3_expected = np.array([[0,1,0,0,0,0,1,0,0,0,0,0],[0,1,0,0,0,0,1,0,0,0,0,0],[6,1,6,6,6,6,1,6,6,6,6,0],[0,1,0,0,0,0,1,0,0,0,6,0],[0,1,0,0,0,0,1,0,0,0,6,0],[0,1,1,1,1,1,1,0,0,0,6,0],[0,0,0,0,0,0,0,0,0,0,6,0],[0,0,0,0,0,0,0,0,0,0,6,0],[0,0,0,0,0,0,0,0,0,0,6,0],[0,0,0,0,0,0,0,0,0,0,6,0],[0,0,0,0,0,0,0,0,0,0,6,0],[0,0,0,0,0,0,0,0,0,0,6,0]])
example3_output = np.array([[0,1,0,0,0,0,1,0,0,0,6,0],[0,1,0,0,0,0,1,0,0,0,6,0],[6,1,6,6,6,6,0,6,0,6,6,0],[0,1,0,0,0,0,1,0,0,0,6,0],[0,0,0,0,0,0,1,0,0,0,0,0],[0,1,1,1,0,1,1,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0]])


examples = [
    {"name": "Example 1 Input", "grid": example1_input},
    {"name": "Example 1 Expected", "grid": example1_expected},
    {"name": "Example 1 Output", "grid": example1_output},
    {"name": "Example 2 Input", "grid": example2_input},
    {"name": "Example 2 Expected", "grid": example2_expected},
    {"name": "Example 2 Output", "grid": example2_output},
    {"name": "Example 3 Input", "grid": example3_input},
    {"name": "Example 3 Expected", "grid": example3_expected},
    {"name": "Example 3 Output", "grid": example3_output},
]

results = []
for example in examples:
    results.append({
        "name": example["name"],
        "analysis": analyze_grid(example["grid"])
    })

for result in results:
    print(f"--- {result['name']} ---")
    for key, value in result['analysis'].items():
        print(f"{key}: {value}")

```

*code_execution_result:*
outcome: 1
```
--- Example 1 Input ---
rows: 12
cols: 12
unique_colors: [0, 1, 2, 3]
color_counts: {np.int64(0): 104, np.int64(3): 18, np.int64(1): 18, np.int64(2): 4}
num_objects: 16
--- Example 1 Expected ---
rows: 12
cols: 12
unique_colors: [0, 1, 3]
color_counts: {np.int64(0): 102, np.int64(3): 20, np.int64(1): 22}
num_objects: 10
--- Example 1 Output ---
rows: 12
cols: 12
unique_colors: [0, 1, 3]
color_counts: {np.int64(0): 104, np.int64(3): 15, np.int64(1): 25}
num_objects: 19
--- Example 2 Input ---
rows: 12
cols: 12
unique_colors: [0, 3, 4, 7]
color_counts: {np.int64(0): 88, np.int64(7): 34, np.int64(3): 21, np.int64(4): 1}
num_objects: 12
--- Example 2 Expected ---
rows: 12
cols: 12
unique_colors: [0, 3, 7]
color_counts: {np.int64(0): 89, np.int64(7): 36, np.int64(3): 19}
num_objects: 9
--- Example 2 Output ---
rows: 12
cols: 12
unique_colors: [0, 3, 7]
color_counts: {np.int64(0): 88, np.int64(7): 34, np.int64(3): 22}
num_objects: 11
--- Example 3 Input ---
rows: 12
cols: 12
unique_colors: [0, 1, 4, 6]
color_counts: {np.int64(0): 120, np.int64(1): 13, np.int64(6): 10, np.int64(4): 1}
num_objects: 13
--- Example 3 Expected ---
rows: 12
cols: 12
unique_colors: [0, 1, 6]
color_counts: {np.int64(0): 110, np.int64(1): 16, np.int64(6): 18}
num_objects: 9
--- Example 3 Output ---
rows: 12
cols: 12
unique_colors: [0, 1, 6]
color_counts: {np.int64(0): 120, np.int64(1): 13, np.int64(6): 11}
num_objects: 12

```
**YAML Facts:**


```yaml
observations:
  - example: 1
    input_objects:
      - color: 2 # Red
        shape: "irregular"
        action: "replace with 3" # Green
      - color: 0 # Black
        shape: "background"
        action: "flood fill with 1 if adjacent to a new 3" # Blue, triggered by red->green
      - color: 3 # Green
        shape: irregular
        action: "change to 1 if adjacent to color 2"  # Blue
      - color: 1 #blue
        shape: irregular
        action: none

    output_objects:
      - color: 3 # Green
        shape: "irregular, expanded"
      - color: 1 #blue
        shape: irregular
        action: none

  - example: 2
    input_objects:
      - color: 4 # Yellow
        shape: "single pixel"
        action: "replace with 3" # Green
      - color: 7 #orange
        shape: irregular
        action: none
      - color: 3 # Green
        shape: irregular
        action: none
      - color: 0
        action: none

    output_objects:
        - color: 3 # Green
          shape: "single pixel then expands along row to meet other 3 object"
        - color: 7 #orange
          shape: irregular
          action: none

  - example: 3
    input_objects:
      - color: 6 # Magenta
        shape: "irregular"
        action: "flood fill background (0)"
      - color: 4 # Yellow
        shape: "single pixel"
        action: "replace with 6" # Magenta
      - color: 1 #blue
        shape: irregular
        action: none
      - color: 0
        action: none
    output_objects:
      - color: 6 # Magenta
        shape: "covers most of grid"
      - color: 1
        shape: irregular
        action: none

general_rule: |
    1.  Identify objects by color.
    2.  Conditional Color Replacement:
        -   If red (2) exists, replace it with green (3).
        -   If yellow (4) exists and magenta (6) does *not* exist, replace yellow (4) with green (3).
        -   If magenta (6) exists, replace yellow (4) with magenta (6).
    3.  Conditional Actions Based on Adjacency and Color:
        - If any green (3) is adjacent to where red (2) *was*, change that green (3) to blue (1).
        - If magenta (6) exists, flood fill the background (0) starting from each magenta pixel, replacing 0 with 6.
    4. No flood filling occurs if Magenta(6) is not present

```


**Natural Language Program:**

1.  **Object Identification:** Find all contiguous regions (objects) of the same color in the input grid.

2.  **Color Replacement Phase:**
    *   If an object of color red (2) is present, replace all pixels of that object with green (3).
    *   If an object of color yellow (4) is present, AND no object of color magenta (6) is present, replace all pixels of the yellow object with green (3).
    *   If an object of color magenta (6) is present, replace all pixels of any yellow (4) objects with magenta (6).

3.  **Conditional Propagation Phase:**
    *    If a green (3) pixel is found adjacent to a location that *was* red (2) in the input grid, change this green pixel to blue (1). Check for these former red locations by storing them before any replacements occur.
    *    If any magenta (6) pixels are present, perform a flood fill operation starting from each magenta pixel. The flood fill replaces connected background pixels (0) with magenta (6).

4. **Termination:** The algorithm terminates after the color replacements, adjacency checks and any triggered flood fills are complete.

