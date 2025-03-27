
Previous Code:
```python
import numpy as np

"""
Transformation Rule:

1. Identify the set of unique colors present in the input grid, excluding yellow (4) and orange (7). Call this the set of 'dynamic colors'.
2. Determine the specific color swapping/mapping rule based on the exact composition of the set of dynamic colors:
    - If the dynamic colors are {blue(1), red(2), green(3), magenta(6)}, then the mapping is: blue(1) -> green(3), green(3) -> blue(1), red(2) -> magenta(6), magenta(6) -> red(2).
    - If the dynamic colors are {blue(1), magenta(6), maroon(9)}, then the mapping is: blue(1) -> maroon(9), maroon(9) -> blue(1), magenta(6) -> magenta(6).
    - If the dynamic colors are {gray(5), magenta(6)}, then the mapping is: gray(5) -> magenta(6), magenta(6) -> gray(5).
3. Yellow(4) and orange(7) always map to themselves (they are static).
4. Apply this mapping to every pixel in the input grid to produce the output grid.
"""

def transform(input_grid):
    """
    Applies a conditional color swap transformation based on the set of non-static colors present.

    Args:
        input_grid (list of lists): A 2D list of integers representing the input grid.

    Returns:
        list of lists: A 2D list of integers representing the transformed output grid.
    """
    # Convert input to a numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape

    # --- Determine the transformation rule ---

    # Find all unique colors present in the grid
    unique_colors = set(np.unique(grid))

    # Identify the dynamic colors (excluding static yellow(4) and orange(7))
    static_colors = {4, 7}
    dynamic_colors = unique_colors - static_colors
    
    # Define the color mapping based on the set of dynamic colors
    color_map = {}

    # Always map static colors to themselves
    color_map[4] = 4
    color_map[7] = 7

    # Determine swaps based on the dynamic color set
    dynamic_colors_tuple = tuple(sorted(list(dynamic_colors))) # Use sorted tuple for reliable matching

    if dynamic_colors_tuple == (1, 2, 3, 6):
        # Case 1: {blue(1), red(2), green(3), magenta(6)}
        color_map.update({1: 3, 3: 1, 2: 6, 6: 2})
    elif dynamic_colors_tuple == (1, 6, 9):
         # Case 2: {blue(1), magenta(6), maroon(9)}
        color_map.update({1: 9, 9: 1, 6: 6}) # Magenta(6) maps to itself
    elif dynamic_colors_tuple == (5, 6):
         # Case 3: {gray(5), magenta(6)}
        color_map.update({5: 6, 6: 5})
    else:
        # If other dynamic colors are present but not in the defined cases,
        # assume they map to themselves (though this shouldn't happen based on examples).
        for color in dynamic_colors:
            if color not in color_map:
                 color_map[color] = color

    # --- Apply the transformation ---

    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(grid)

    # Iterate through each pixel and apply the color mapping
    for r in range(height):
        for c in range(width):
            input_color = grid[r, c]
            # Use .get with default as input_color itself in case a color wasn't explicitly added to map
            # (like static colors or unhandled dynamic colors)
            output_grid[r, c] = color_map.get(input_color, input_color)

    # Convert the result back to a list of lists
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
6 6 7 4 4 7 2 2
6 7 4 4 4 4 7 2
7 4 4 4 4 4 4 7
4 4 4 4 4 4 4 7
7 4 4 4 7 7 7 3
1 7 4 4 7 3 3 3
1 1 7 4 7 3 3 3
1 1 1 7 7 3 3 3
```
Expected Output:
```
1 1 7 4 4 7 6 6
1 7 4 4 4 4 7 6
7 4 4 4 4 4 4 7
4 4 4 4 4 4 4 7
7 4 4 4 7 7 7 2
3 7 4 4 7 2 2 2
3 3 7 4 7 2 2 2
3 3 3 7 7 2 2 2
```
Transformed Output:
```
2 2 7 4 4 7 6 6
2 7 4 4 4 4 7 6
7 4 4 4 4 4 4 7
4 4 4 4 4 4 4 7
7 4 4 4 7 7 7 1
3 7 4 4 7 1 1 1
3 3 7 4 7 1 1 1
3 3 3 7 7 1 1 1
```
Match: False
Pixels Off: 13
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 40.625

## Example 2:
Input:
```
1 1 7 4 4 7 6 6
1 7 4 4 4 7 6 6
7 4 4 4 4 7 6 6
9 7 4 4 4 7 6 6
9 9 7 4 4 7 6 6
9 9 9 7 4 7 6 6
9 9 9 9 7 7 6 6
9 9 9 9 9 7 6 6
```
Expected Output:
```
9 9 7 4 4 7 1 1
9 7 4 4 4 7 1 1
7 4 4 4 4 7 1 1
6 7 4 4 4 7 1 1
6 6 7 4 4 7 1 1
6 6 6 7 4 7 1 1
6 6 6 6 7 7 1 1
6 6 6 6 6 7 1 1
```
Transformed Output:
```
9 9 7 4 4 7 6 6
9 7 4 4 4 7 6 6
7 4 4 4 4 7 6 6
1 7 4 4 4 7 6 6
1 1 7 4 4 7 6 6
1 1 1 7 4 7 6 6
1 1 1 1 7 7 6 6
1 1 1 1 1 7 6 6
```
Match: False
Pixels Off: 31
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 96.875

## Example 3:
Input:
```
6 6 6 6 6 6 6 6
6 6 6 6 6 6 6 6
7 7 7 7 7 7 7 6
7 4 4 4 4 4 4 7
7 4 4 4 4 7 7 7
7 4 7 7 7 5 5 5
7 7 5 5 5 5 5 5
7 5 5 5 5 5 5 5
```
Expected Output:
```
5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5
7 7 7 7 7 7 7 5
7 4 4 4 4 4 4 7
7 4 4 4 4 7 7 7
7 4 7 7 7 6 6 6
7 7 6 6 6 6 6 6
7 6 6 6 6 6 6 6
```
Transformed Output:
```
5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5
7 7 7 7 7 7 7 5
7 4 4 4 4 4 4 7
7 4 4 4 4 7 7 7
7 4 7 7 7 6 6 6
7 7 6 6 6 6 6 6
7 6 6 6 6 6 6 6
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0
