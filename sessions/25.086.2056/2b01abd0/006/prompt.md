
Previous Code:
```python
import numpy as np

"""
Reflects objects across a central blue line (axis), swaps specific color pairs 
(Red<->Green, Yellow<->Azure, Gray<->Magenta) on both the original object 
pixels and their reflections.

1. Initialize the output grid as a copy of the input grid.
2. Find the single blue axis line (color 1), its orientation (horizontal/vertical), and index. If no single axis is found, return the copy.
3. Define color swap pairs: Red(2)<->Green(3), Yellow(4)<->Azure(8), Gray(5)<->Magenta(6). Other colors map to themselves.
4. Identify and store the coordinates and original colors of all non-background (0), non-axis (1) pixels ("object pixels").
5. Iterate through the identified original object pixels:
   a. Determine the swapped color based on the defined pairs.
   b. Update the output grid at the *original* pixel's coordinate with the swapped color.
   c. Calculate the reflection coordinate across the axis.
   d. If the reflection coordinate is within grid bounds, update the output grid at that coordinate with the *same* swapped color.
6. Return the modified output grid.
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
    Applies the reflection and color swap to both original and reflected pixels.
    
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
        # print("Warning: No single horizontal or vertical blue axis found.") # Optional warning
        return output_grid

    # 3. Define the color swap map 
    color_swap_map = {
        2: 3, 3: 2,  # Red <-> Green
        4: 8, 8: 4,  # Yellow <-> Azure
        5: 6, 6: 5   # Gray <-> Magenta
    }
    # Include identity mapping for colors not in pairs (0, 1, 7, 9)
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

    # 5. Iterate through object pixels, swap colors, update original and reflected positions
    for pixel_info in original_object_pixels:
        r, c, color = pixel_info['r'], pixel_info['c'], pixel_info['color']
        
        # 5a. Determine the swapped color
        swapped_color = color_swap_map.get(color, color) # Use .get for safety

        # 5b. Update the output grid at the original pixel's coordinate
        # Check coordinate validity just in case, although it should always be valid here
        if 0 <= r < rows and 0 <= c < cols:
            output_grid[r, c] = swapped_color
        
        # 5c. Calculate reflected coordinates
        nr, nc = -1, -1
        if orientation == 'horizontal':
            axis_row_idx = index
            nr = axis_row_idx + (axis_row_idx - r)
            nc = c
        elif orientation == 'vertical':
            axis_col_idx = index
            nr = r
            nc = axis_col_idx + (axis_col_idx - c)

        # 5d. Check if the reflection coordinate is within grid bounds
        # 5e. If valid, update the output grid at the reflected coordinate
        if 0 <= nr < rows and 0 <= nc < cols:
            output_grid[nr, nc] = swapped_color
        # Else: Reflection is outside the grid, do nothing further for this pixel's reflection.

    # 6. Return the modified grid
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
0 0 0 3 0 3 0 0 0
0 0 3 2 3 3 0 0 0
0 0 0 0 3 0 0 0 0
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
Pixels Off: 7
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 12.962962962962962

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
0 0 6 5 5 6 0 0 0 0 0
0 0 5 5 5 5 0 0 0 0 0
0 0 5 0 0 5 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 10
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 12.987012987013003
