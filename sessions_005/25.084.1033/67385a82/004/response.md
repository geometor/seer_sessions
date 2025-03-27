## Assessment

The previous code correctly identified the core concept of finding connected green components and changing their color based on size. However, it derived an overly specific rule ("2x2 plus tail") from the first example, which caused it to fail on that same example while coincidentally working for the others.

The failure on Example 1, where the code *correctly* identified the "2x2 plus tail" shape but only colored the square part, while the expected output colored the entire shape, indicates that the special rule was incorrect. The success on the other examples suggests the underlying principle of component size is likely correct, but the special shape handling needs removal.

The simplest hypothesis that fits all examples is: Identify all 4-way connected green components. If a component consists of 3 or more pixels, change all pixels in that component to azure.

**Strategy:**
1.  Verify the component sizes for each input using 4-way connectivity.
2.  Confirm that changing all green pixels in components of size >= 3 to azure matches the expected output for all examples.
3.  Update the natural language program and facts based on this simpler, verified rule.

## Metrics Gathering

Let's analyze the green components (value 3) using 4-way connectivity in each training input.


``` python
import numpy as np
from collections import deque

def find_connected_components_4way(grid, target_color):
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == target_color and not visited[r, c]:
                current_component = []
                q = deque([(r, c)])
                visited[r, c] = True
                while q:
                    curr_r, curr_c = q.popleft()
                    current_component.append((curr_r, curr_c))
                    for dr, dc in directions:
                        nr, nc = curr_r + dr, curr_c + dc
                        if 0 <= nr < rows and 0 <= nc < cols:
                            if grid[nr, nc] == target_color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                components.append(current_component)
    return components

# Example Inputs
inputs = [
    np.array([[3, 3, 0, 3], [3, 3, 0, 0], [3, 0, 0, 3], [0, 0, 3, 3]]),
    np.array([[0, 3, 0, 0, 0, 3], [0, 3, 3, 3, 0, 0], [0, 0, 0, 0, 3, 0], [0, 3, 0, 0, 0, 0]]),
    np.array([[3, 3, 0, 0, 0, 0], [0, 3, 0, 0, 3, 0], [3, 0, 0, 0, 0, 0], [0, 3, 3, 0, 0, 0], [0, 3, 3, 0, 0, 3]]),
    np.array([[3, 3, 0], [0, 3, 0], [3, 0, 3]])
]

target_color = 3  # green

# Analyze components for each input
results = {}
for i, input_grid in enumerate(inputs):
    components = find_connected_components_4way(input_grid, target_color)
    component_sizes = [len(comp) for comp in components]
    results[f"Example {i+1}"] = {"component_sizes": component_sizes}

print(results)
```
```
{'Example 1': {'component_sizes': [5, 1, 3]}, 'Example 2': {'component_sizes': [4, 1, 1, 1]}, 'Example 3': {'component_sizes': [3, 1, 1, 4, 1]}, 'Example 4': {'component_sizes': [3, 1, 1]}}

```
## Facts


```yaml
task_description: Identify specific groups of green pixels and change their color based on the group's size.

definitions:
  - object: Green Component
    description: A contiguous group of green (3) pixels connected using 4-way adjacency (up, down, left, right).
    properties:
      - size: The number of pixels in the component.

transformations:
  - action: Identify Green Components
    input: Input grid
    output: A list of Green Components.
    condition: Pixels must be green (3) and connected 4-way.

  - action: Filter Components by Size
    input: List of Green Components
    output: Filtered list of Green Components.
    condition: Component size must be greater than or equal to 3.

  - action: Change Color
    input: Filtered list of Green Components and the original grid.
    output: Modified grid.
    rule: For each pixel coordinate within the filtered components, change its color in the grid from green (3) to azure (8).
    condition: The pixel's original color is green.

constants:
  - input_color: green (3)
  - output_color: azure (8)
  - size_threshold: 3
  - connectivity: 4-way (von Neumann)
```


## Natural Language Program

1.  Identify all distinct groups (components) of connected green (3) pixels within the input grid. Connectivity is defined by 4-way adjacency (pixels sharing an edge, not just a corner).
2.  For each identified green component, count the number of pixels it contains (its size).
3.  Select only those green components whose size is 3 or more.
4.  Create the output grid by copying the input grid.
5.  For every pixel belonging to any of the selected components (those with size >= 3), change its color in the output grid from green (3) to azure (8).
6.  Leave all other pixels (pixels not part of a green component of size >= 3) unchanged from their original color in the input grid.