
Previous Code:
```python
import numpy as np

"""
Reflects objects across a central blue line (axis), swaps specific color pairs, 
and then either removes the original objects (if the axis is horizontal) or 
swaps the colors of the original objects in place (if the axis is vertical).

1. Initialize the output grid as a copy of the input grid.
2. Find the single blue axis line (color 1), its orientation (horizontal/vertical), and index.
3. Define color swap pairs: Red(2)<->Green(3), Yellow(4)<->Azure(8), Gray(5)<->Magenta(6).
4. Identify and store the coordinates and original colors of all non-background (0), non-axis (1) pixels.
5. Iterate through the identified original object pixels:
   a. Calculate the reflection coordinate across the axis.
   b. Determine the swapped color based on the defined pairs.
   c. If the reflection coordinate is within grid bounds, update the output grid at that coordinate with the swapped color.
6. Check the axis orientation:
   a. If horizontal: Iterate through the stored original object pixel coordinates and set the corresponding locations in the output grid to the background color (0).
   b. If vertical: Iterate through the stored original object pixels. For each, determine its swapped color and update the output grid at the *original* coordinate with this swapped color.
7. Return the modified output grid.
"""

def find_blue_axis(grid):
    """
    Finds the blue line axis (row/col index) and its orientation ('horizontal'/'vertical').
    
    Args:
        grid (np.array): The input grid.
        
    Returns:
        tuple: (orientation, index) where orientation is 'horizontal' or 'vertical',
               and index is the row or column index of the axis. Returns (None, None) 
               if no single blue line axis is found.
    """
    rows, cols = grid.shape
    
    # Check for horizontal line (all elements in a row are 1)
    horizontal_lines = [r for r in range(rows) if np.all(grid[r, :] == 1)]
    
    # Check for vertical line (all elements in a column are 1)
    vertical_lines = [c for c in range(cols) if np.all(grid[:, c] == 1)]

    # Check validity based on examples: exactly one line, not both
    is_single_horizontal = len(horizontal_lines) == 1 and len(vertical_lines) == 0
    is_single_vertical = len(vertical_lines) == 1 and len(horizontal_lines) == 0

    if is_single_horizontal:
        return 'horizontal', horizontal_lines[0]
    elif is_single_vertical:
        return 'vertical', vertical_lines[0]
    else:
        # No single line found or both found, inconsistent with examples
        return None, None


def transform(input_grid):
    """
    Applies the reflection, color swap, and conditional original object handling.
    
    Args:
        input_grid (np.array): The input grid as a NumPy array.
        
    Returns:
        np.array: The transformed output grid.
    """
    
    # 1. Initialize output_grid as a copy
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 2. Find the blue axis
    orientation, index = find_blue_axis(input_grid)

    # If no single blue line is found per the examples' pattern, return the original grid copy
    if orientation is None:
        # print("Warning: No single horizontal or vertical blue axis found.")
        return output_grid

    # 3. Define the color swap map 
    color_swap_map = {
        2: 3, 3: 2,  # Red <-> Green
        4: 8, 8: 4,  # Yellow <-> Azure
        5: 6, 6: 5   # Gray <-> Magenta
    }
    # Include identity mapping for colors not in pairs (or default behavior)
    for i in range(10):
        if i not in color_swap_map:
             color_swap_map[i] = i # Maps color to itself if not in a swap pair

    # 4. Identify and store original object pixels (coord + color)
    original_object_pixels = [] 
    for r in range(rows):
        for c in range(cols):
            color = input_grid[r, c]
            # Skip background (0) and axis (1) pixels
            if color != 0 and color != 1:
                original_object_pixels.append({'r': r, 'c': c, 'color': color})

    # 5. Perform reflection and place swapped colors
    for pixel_info in original_object_pixels:
        r, c, color = pixel_info['r'], pixel_info['c'], pixel_info['color']
        
        # Calculate reflected coordinates
        nr, nc = -1, -1
        if orientation == 'horizontal':
            axis_row_idx = index
            nr = axis_row_idx + (axis_row_idx - r)
            nc = c
        elif orientation == 'vertical':
            axis_col_idx = index
            nr = r
            nc = axis_col_idx + (axis_col_idx - c)

        # Get swapped color
        swapped_color = color_swap_map.get(color, color) # Use .get for safety, though map includes all 0-9 now

        # Place the swapped color onto the output grid IF the reflected coordinate is within bounds
        if 0 <= nr < rows and 0 <= nc < cols:
            output_grid[nr, nc] = swapped_color
        # Else: Reflection is outside the grid, do nothing.

    # 6. Handle original pixels based on axis orientation
    if orientation == 'horizontal':
        # a. Remove original objects by setting them to background color
        for pixel_info in original_object_pixels:
            r, c = pixel_info['r'], pixel_info['c']
            # Check coordinate validity just in case, though should always be valid
            if 0 <= r < rows and 0 <= c < cols:
                 output_grid[r, c] = 0 # Set to background color (white)
                 
    elif orientation == 'vertical':
        # b. Swap colors of the original objects in place
        for pixel_info in original_object_pixels:
            r, c, color = pixel_info['r'], pixel_info['c'], pixel_info['color']
            swapped_color = color_swap_map.get(color, color)
            # Check coordinate validity just in case
            if 0 <= r < rows and 0 <= c < cols:
                output_grid[r, c] = swapped_color

    # 7. Return the modified grid
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 8 0 8 0
0 0 0 0 0 0 1 0 0 8 4 0
0 0 0 0 0 0 1 0 8 8 8 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 8 0 8 0 1 0 4 0 4 0
0 0 4 8 0 0 1 0 0 4 8 0
0 0 8 8 8 0 1 0 4 4 4 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 4 0 4 0 1 0 4 0 4 0
0 0 8 4 0 0 1 0 0 4 8 0
0 0 4 4 4 0 1 0 4 4 4 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 1 0 0 0 0 0
```
Match: False
Pixels Off: 7
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 10.606060606060595

## Example 2:
Input:
```
0 0 0 2 0 2 0 0 0
0 0 2 3 2 2 0 0 0
0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 3 0 3 0 0 0
0 0 3 2 3 3 0 0 0
0 0 0 0 3 0 0 0 0
0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 0
0 0 2 3 2 2 0 0 0
0 0 0 2 0 2 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0
0 0 3 2 3 3 0 0 0
0 0 0 3 0 3 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 14
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 25.925925925925924

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0
0 0 5 6 6 5 0 0 0 0 0
0 0 6 6 6 6 0 0 0 0 0
0 0 6 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 0 6 0 0 0 0 0
0 0 6 6 6 6 0 0 0 0 0
0 0 5 6 6 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0
0 0 6 5 5 6 0 0 0 0 0
0 0 5 5 5 5 0 0 0 0 0
0 0 5 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 5 0 0 5 0 0 0 0 0
0 0 5 5 5 5 0 0 0 0 0
0 0 6 5 5 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 20
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 25.974025974025977
**General Assessment**

The previous code correctly identified the blue axis, the reflection mechanism, and the color swap pairs (Red<->Green, Yellow<->Azure, Gray<->Magenta). However, it incorrectly assumed that the handling of the original object pixels depended on the axis orientation (removing originals for horizontal axes, swapping colors in place for vertical axes).

Reviewing the failed examples reveals a consistent pattern:
1.  **Example 1 (Vertical Axis):** The code correctly reflected the objects and applied the color swap (Azure<->Yellow) to the reflected pixels. However, it failed because the *original* object pixels also needed their colors swapped in place. The expected output shows swapped colors on *both* sides of the axis.
2.  **Example 2 & 3 (Horizontal Axis):** The code correctly reflected the objects and applied the color swaps (Red<->Green and Gray<->Magenta, respectively) to the reflected pixels. However, it failed because it erased the original object pixels (setting them to background color 0). The expected output shows that the original object pixels should also have their colors swapped in place, similar to the vertical axis case.

The core error is the conditional logic based on axis orientation for handling the original pixels. The correct rule appears to be consistent across both orientations: **swap the colors of the original pixels in place *and* place the swapped colors at the reflected positions.**

**Strategy:**
1.  Modify the code to remove the conditional logic (if horizontal vs. if vertical) that handles the original pixels differently.
2.  Implement the unified logic: iterate through the original object pixels, swap their color according to the map, update the output grid at the *original* position with the swapped color, calculate the reflected position, and if valid, update the output grid at the *reflected* position with the same swapped color.

**Gather Metrics**


*code_execution:*
```python
import numpy as np

# Data from Example 1
expected_1 = np.array([
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 8, 0, 8, 0, 1, 0, 4, 0, 4, 0],
    [0, 0, 4, 8, 0, 0, 1, 0, 0, 4, 8, 0],
    [0, 0, 8, 8, 8, 0, 1, 0, 4, 4, 4, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
])
transformed_1 = np.array([
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 4, 0, 4, 0, 1, 0, 4, 0, 4, 0],
    [0, 0, 8, 4, 0, 0, 1, 0, 0, 4, 8, 0],
    [0, 0, 4, 4, 4, 0, 1, 0, 4, 4, 4, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 1, 0, 0, 0, 0, 0]
])
diff_1 = np.sum(expected_1 != transformed_1)
print(f"Example 1 Pixels Off: {diff_1}")

# Data from Example 2
expected_2 = np.array([
    [0, 0, 0, 3, 0, 3, 0, 0, 0],
    [0, 0, 3, 2, 3, 3, 0, 0, 0],
    [0, 0, 0, 0, 3, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 0, 0, 0, 0],
    [0, 0, 2, 3, 2, 2, 0, 0, 0],
    [0, 0, 0, 2, 0, 2, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
])
transformed_2 = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 3, 0, 0, 0, 0],
    [0, 0, 3, 2, 3, 3, 0, 0, 0],
    [0, 0, 0, 3, 0, 3, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0]
])
diff_2 = np.sum(expected_2 != transformed_2)
print(f"Example 2 Pixels Off: {diff_2}")

# Data from Example 3
expected_3 = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 6, 0, 0, 6, 0, 0, 0, 0, 0],
    [0, 0, 6, 6, 6, 6, 0, 0, 0, 0, 0],
    [0, 0, 5, 6, 6, 5, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 6, 5, 5, 6, 0, 0, 0, 0, 0],
    [0, 0, 5, 5, 5, 5, 0, 0, 0, 0, 0],
    [0, 0, 5, 0, 0, 5, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])
transformed_3 = np.array([
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 5, 0, 0, 5, 0, 0, 0, 0, 0],
    [0, 0, 5, 5, 5, 5, 0, 0, 0, 0, 0],
    [0, 0, 6, 5, 5, 6, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
])
diff_3 = np.sum(expected_3 != transformed_3)
print(f"Example 3 Pixels Off: {diff_3}")
```

*code_execution_result:*
outcome: OUTCOME_OK
```
Example 1 Pixels Off: 7
Example 2 Pixels Off: 14
Example 3 Pixels Off: 20

```
The pixel difference counts match the report, confirming the locations of the errors discussed above.

**Facts**


```yaml
task_description: Reflect objects across a blue axis, swapping specific colors on both the original and reflected sides.

definitions:
  grid: A 2D array of integers 0-9 representing colors.
  background: Color 0 (white).
  axis: A single continuous line (row or column) of color 1 (blue).
  object_pixel: Any pixel that is not background (0) and not part of the axis (1).
  color_swap_map:
    Red (2): Green (3)
    Green (3): Red (2)
    Yellow (4): Azure (8)
    Azure (8): Yellow (4)
    Gray (5): Magenta (6)
    Magenta (6): Gray (5)
    Other colors: Map to themselves (e.g., 0->0, 1->1, 7->7, 9->9).

transformation_steps:
  - description: Identify the blue axis.
    properties:
      - color: 1 (blue)
      - shape: A single full row or a single full column.
      - location: Store its orientation (horizontal/vertical) and index (row/column number).
  - description: Initialize the output grid as a copy of the input grid.
  - description: Identify all object pixels in the input grid.
    properties:
      - color: Not 0 and not 1.
      - location: Store their row and column coordinates (r, c).
  - description: Iterate through each identified object pixel.
    actions:
      - name: Determine the swapped color.
        input: Original color of the object pixel.
        using: color_swap_map.
        output: swapped_color.
      - name: Update the original pixel location.
        location: The original coordinates (r, c) of the object pixel.
        value: Set the pixel in the output grid at (r, c) to swapped_color.
      - name: Calculate the reflected coordinate.
        input: Original coordinates (r, c), axis orientation, axis index.
        output: Reflected coordinates (nr, nc).
        details:
          if horizontal axis at index `ax`: nr = ax + (ax - r), nc = c
          if vertical axis at index `ax`: nr = r, nc = ax + (ax - c)
      - name: Update the reflected pixel location.
        condition: The reflected coordinates (nr, nc) are within the grid bounds.
        location: The reflected coordinates (nr, nc).
        value: Set the pixel in the output grid at (nr, nc) to swapped_color.
  - description: Return the final output grid.
```


**Natural Language Program**

1.  Create a copy of the input grid, which will become the output grid.
2.  Locate the single blue line (color 1) that spans the entire grid either horizontally or vertically. Record its orientation (horizontal or vertical) and its index (row or column number). If no such single line exists, return the original grid copy.
3.  Define the color swapping rules: Red (2) swaps with Green (3), Yellow (4) swaps with Azure (8), and Gray (5) swaps with Magenta (6). All other colors remain unchanged.
4.  Identify all pixels in the input grid that are *not* background (color 0) and *not* part of the blue axis (color 1). These are the "object pixels". Store their original coordinates (row `r`, column `c`) and original color.
5.  For each identified object pixel:
    a.  Look up its original color in the color swapping rules to find its `swapped_color`.
    b.  Update the output grid at the object pixel's original coordinates (`r`, `c`) by setting it to the `swapped_color`.
    c.  Calculate the reflection coordinates (`nr`, `nc`) across the blue axis based on the original coordinates (`r`, `c`), the axis orientation, and the axis index.
    d.  Check if the calculated reflection coordinates (`nr`, `nc`) are within the bounds of the grid.
    e.  If the reflection coordinates are valid (within the grid), update the output grid at these coordinates (`nr`, `nc`) by setting it to the same `swapped_color`.
6.  Return the modified output grid.
