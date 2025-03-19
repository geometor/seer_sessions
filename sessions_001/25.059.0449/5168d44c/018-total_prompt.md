# 5168d44c • 018 • refine_coder

---

Previous Code:
```python
"""
1.  **Identify Objects:** Find the vertical green line and the red cross-shaped object.
2.  **Rotate Red Cross** Rotate the Red cross by 180 degrees around its center point.
3.  **Copy Green line:** Copy the green line segments below other objects.
4.  **Combine**: combine the altered green segments and the rotated red object into an output grid, maintaining relative positions, filling remaining space with white.
"""

import numpy as np

def find_object(grid, color, shape_type=None):
    objects = []
    visited = set()

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(r, c, current_object):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append([r, c])
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] == color and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                if shape_type == 'line':
                    # Check if it forms a line (vertical or horizontal)
                   if all(x[0] == current_object[0][0] for x in current_object) or all(x[1] == current_object[0][1] for x in current_object):
                        objects.append(current_object)

                elif shape_type == 'cross':
                    # Basic cross shape check (can be refined)
                    if len(current_object) > 1:
                        objects.append(current_object)

                elif shape_type is None:

                    objects.append(current_object)


    return objects


def rotate_object(object_coords, center, degrees):
    """Rotates object coordinates around a center point."""
    rotated_coords = []
    rads = np.radians(degrees)
    for r, c in object_coords:
        # Translate to origin
        r -= center[0]
        c -= center[1]
        # Rotate
        new_r = r * np.cos(rads) - c * np.sin(rads)
        new_c = r * np.sin(rads) + c * np.cos(rads)
        # Translate back
        rotated_coords.append([int(round(new_r + center[0])), int(round(new_c + center[1]))])
    return rotated_coords


def transform(input_grid):
    # initialize output_grid
    grid = np.array(input_grid)
    output_grid = np.zeros_like(grid)

    # Find the green line and red cross
    green_line = find_object(grid, 3, 'line')
    red_cross = find_object(grid, 2, 'cross')
    #print(f'{green_line=}')
    #print(f'{red_cross=}')
    if not green_line or not red_cross:
       return output_grid.tolist()
    
    green_line = green_line[0]
    red_cross = red_cross[0]

    # Find center of the red_cross
    red_cross_center = [int(np.mean([x[0] for x in red_cross])), int(np.mean([x[1] for x in red_cross]))]


    # Rotate the red cross
    rotated_red_cross = rotate_object(red_cross, red_cross_center, 180)
    #print(f'{rotated_red_cross=}')

    # Find position to copy green line to
    max_row = 0
    for coord in rotated_red_cross:
        if coord[0] > max_row:
           max_row = coord[0]
    new_green_line = []

    for i in range(len(green_line)):
       new_green_line.append([max_row-len(green_line)+1 + i, green_line[0][1]])

    # Fill output grid
    for r, c in rotated_red_cross:
        if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
            output_grid[r, c] = 2

    for r, c in new_green_line:
      if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
        output_grid[r, c] = 3

    return output_grid.tolist()
```

Train Set Results:
Okay, let's analyze the results of the code execution on the training examples and refine the natural language program accordingly.

**General Assessment and Strategy**

The initial code and natural language program were a good starting point, correctly identifying the core objects (green line and red cross) and the general operations (rotation and copying). However, the execution results reveal discrepancies, particularly in handling the positioning and interaction of the objects. The strategy to resolve these errors involves:

1.  **Refined Object Identification:** Improve the object identification to be more robust, possibly by considering connectivity and shape more explicitly.
2.  **Precise Spatial Relationships:** More accurately determine the spatial relationship between the green line and the red cross, and how this relationship dictates the placement of the copied green line. The concept of "below" needs to be clarified – does it mean directly below, or simply at a lower row index?
3.  **Conditional Logic:** Consider if there are conditions under which certain operations are applied or skipped.
4. **Size Invariance:** address cases where the output grid has differing dimensions than the input.

**Metrics and Observations (using code_execution where needed):**

I'll need to interleave observations with code execution to confirm details, running the `transform()` function on each input and inspecting both the input, generated output, and expected output grids. Since I cannot directly visualize the grids, I will focus on comparing key properties like dimensions, object locations, and colors.

```tool_code
def check_output(task_index):
    from utils import load_task_json
    task = load_task_json(f'00d62c1b', 'train', task_index)
    input_grid = task['input']
    expected_output_grid = task['output']
    actual_output_grid = transform(input_grid)

    print(f"Example {task_index + 1}:")
    print(f"Input Dimensions: {np.array(input_grid).shape}")
    print(f"Expected Output Dimensions: {np.array(expected_output_grid).shape}")
    print(f"Actual Output Dimensions: {np.array(actual_output_grid).shape}")
    
    # find the green line
    input_green = find_object(np.array(input_grid), 3, 'line')
    output_green = find_object(np.array(expected_output_grid), 3, 'line')
    actual_output_green = find_object(np.array(actual_output_grid), 3, 'line')
    print(f"Input Green Line: {input_green}")
    print(f"Expected Output Green Line: {output_green}")
    print(f"Actual Output Green Line: {actual_output_green}")

    # find the red_cross
    input_red = find_object(np.array(input_grid), 2, 'cross')
    output_red = find_object(np.array(expected_output_grid), 2, 'cross')
    actual_output_red = find_object(np.array(actual_output_grid), 2, 'cross')
    print(f"Input Red Cross: {input_red}")
    print(f"Expected Output Red Cross: {output_red}")
    print(f"Actual Output Red Cross: {actual_output_red}")

    print(f"Correct Output: {actual_output_grid == expected_output_grid}")
    print("\n")

for i in range(3):
    check_output(i)

```
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
