
Previous Code:
```python
"""
1.  **Object Identification:** Identify distinct objects (contiguous same-color pixels, excluding white).
2.  **Object Categorization:** Categorize objects based on their initial position (top_left, top_right, middle_left, other).
3.  **Object Transformation (Movement):** Move objects based on their category:
    *   `top_left` objects move down to the middle_left area.
    *   `top_right` objects move down to the middle_right area.
    *   `middle_left` objects move to the bottom_middle area.
    *   `other` objects remain in their original positions.
4.  **Grid Reconstruction:** Create a new grid and place transformed objects, filling the rest with white (0).
"""

import numpy as np

def find_objects(grid):
    """Finds distinct objects in the grid."""
    objects = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, color, object_pixels):
        if (r < 0 or r >= grid.shape[0] or c < 0 or c >= grid.shape[1] or
                visited[r, c] or grid[r, c] != color):
            return
        visited[r, c] = True
        object_pixels.append((r, c))
        dfs(r + 1, c, color, object_pixels)
        dfs(r - 1, c, color, object_pixels)
        dfs(r, c + 1, color, object_pixels)
        dfs(r, c - 1, color, object_pixels)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if not visited[r, c] and grid[r, c] != 0:
                object_pixels = []
                dfs(r, c, grid[r, c], object_pixels)
                if object_pixels:
                    objects.append({
                        'color': grid[r, c],
                        'pixels': object_pixels
                    })
    return objects

def categorize_objects(objects, grid_shape):
    """Categorizes objects based on their initial position."""
    top_left = []
    top_right = []
    middle_left = []
    other = []

    for obj in objects:
        min_r, min_c = float('inf'), float('inf')
        for r, c in obj['pixels']:
            min_r = min(min_r, r)
            min_c = min(min_c, c)

        if min_r < grid_shape[0] // 3 and min_c < grid_shape[1] // 2:
            top_left.append(obj)
        elif min_r < grid_shape[0] // 3 and min_c >= grid_shape[1] // 2:
            top_right.append(obj)
        elif min_r < grid_shape[0] * (2 / 3) and min_c < grid_shape[1] // 2 and min_r >= grid_shape[0] // 3:
            middle_left.append(obj)
        else:
            other.append(obj)
    return top_left, top_right, middle_left, other

def move_objects(objects, grid_shape, category):
    """Moves objects based on their category."""
    moved_objects = []

    for obj in objects:
        new_pixels = []
        if category == "top_left":
            min_row = min([r for r, c in obj['pixels']])
            row_offset = (grid_shape[0] // 3) - min_row
            for r, c in obj['pixels']:
                new_pixels.append((r + row_offset, c))  # Integer addition

        elif category == "top_right":
            min_row = min([r for r, c in obj['pixels']])
            row_offset = (grid_shape[0] // 3) - min_row
            for r, c in obj['pixels']:
                new_pixels.append((r + row_offset, c))  # Integer addition

        elif category == "middle_left":
            min_row = min([r for r, c in obj['pixels']])
            row_offset = (grid_shape[0] * 2 // 3) - min_row  # Integer division
            for r, c in obj['pixels']:
                new_pixels.append((r + row_offset, c))

        else:
            new_pixels = obj['pixels']  # No movement for 'other'

        moved_objects.append({
            'color': obj['color'],
            'pixels': new_pixels
        })
    return moved_objects

def reconstruct_grid(moved_objects, original_grid_shape):
    """Reconstructs the grid from the transformed objects."""
    new_grid = np.zeros(original_grid_shape, dtype=int)
    for obj in moved_objects:
        for r, c in obj['pixels']:
            if 0 <= r < original_grid_shape[0] and 0 <= c < original_grid_shape[1]:
                new_grid[r, c] = obj['color']
    return new_grid

def transform(input_grid):
    """Transforms the input grid according to the defined rules."""
    original_grid_shape = input_grid.shape
    objects = find_objects(input_grid)
    top_left, top_right, middle_left, other = categorize_objects(objects, original_grid_shape)
    moved_top_left = move_objects(top_left, original_grid_shape, "top_left")
    moved_top_right = move_objects(top_right, original_grid_shape, "top_right")
    moved_middle_left = move_objects(middle_left, original_grid_shape, "middle_left")
    moved_other = move_objects(other, original_grid_shape, "other")
    all_moved_objects = moved_top_left + moved_top_right + moved_middle_left + moved_other
    output_grid = reconstruct_grid(all_moved_objects, original_grid_shape)
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 5 5 5 8 0 0 0 2 2 2 2 2 0 0 0 0 0 0 0 0
0 8 5 5 5 8 0 0 0 2 1 1 1 2 0 8 8 8 8 8 0 0
0 8 5 5 5 8 0 0 0 2 1 1 1 2 0 8 3 3 3 8 0 0
0 8 8 8 8 8 0 0 0 2 1 1 1 2 0 8 3 3 3 8 0 0
0 0 0 0 0 0 0 0 0 2 2 2 2 2 0 8 3 3 3 8 0 0
0 0 0 0 2 2 2 2 2 0 0 0 0 0 0 8 8 8 8 8 0 0
0 0 0 0 2 3 3 3 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 3 3 3 2 0 0 0 0 2 2 2 2 2 0 0 0 0
0 0 0 0 2 3 3 3 2 0 0 0 0 2 9 9 9 2 0 0 0 0
0 0 0 0 2 2 2 2 2 0 0 0 0 2 9 9 9 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 2 9 9 9 2 0 0 0 0
2 2 2 2 2 0 0 0 0 0 0 0 0 2 2 2 2 2 0 0 0 0
2 6 6 6 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
2 6 6 6 2 0 0 0 0 0 0 0 8 8 8 8 8 0 0 0 0 0
2 6 6 6 2 2 2 2 2 2 0 0 8 4 4 4 8 0 0 0 0 0
2 2 2 2 2 2 4 4 4 2 0 0 8 4 4 4 8 0 0 0 0 0
0 0 0 0 0 2 4 4 4 2 0 0 8 4 4 4 8 0 0 0 0 0
0 0 0 0 0 2 4 4 4 2 0 0 8 8 8 8 8 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
8 5 5 5 8 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2
8 5 5 5 8 8 8 8 8 8 0 0 0 0 0 0 0 2 1 1 1 2
8 5 5 5 8 8 3 3 3 8 0 0 0 0 0 0 0 2 1 1 1 2
8 8 8 8 8 8 3 3 3 8 0 0 0 0 0 0 0 2 1 1 1 2
0 0 0 0 0 8 3 3 3 8 0 0 0 0 0 0 0 2 2 2 2 2
0 0 0 0 0 8 8 8 8 8 0 0 2 2 2 2 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 2 3 3 3 2 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 2 3 3 3 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 2 3 3 3 2 2 9 9 9 2
0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 9 9 9 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 9 9 9 2
0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 2 6 6 6 2 0 0 0 0 0
8 8 8 8 8 0 0 0 0 0 0 0 2 6 6 6 2 0 0 0 0 0
8 4 4 4 8 0 0 0 0 0 0 0 2 6 6 6 2 2 2 2 2 2
8 4 4 4 8 0 0 0 0 0 0 0 2 2 2 2 2 2 4 4 4 2
8 4 4 4 8 0 0 0 0 0 0 0 0 0 0 0 0 2 4 4 4 2
8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 2 4 4 4 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 5 5 5 8 0 0 0 2 1 1 1 2 0 8 3 3 3 8 0 0
0 8 5 5 5 8 0 0 0 2 1 1 1 2 0 8 3 3 3 8 0 0
0 8 5 5 5 8 0 0 0 2 1 1 1 2 2 2 2 2 3 8 0 0
0 8 0 0 0 8 0 0 0 2 0 0 0 2 9 9 9 2 0 8 0 0
0 8 8 8 8 8 0 0 0 2 2 2 2 2 9 9 9 2 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 2 9 9 9 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 0 0 0 0
2 6 6 6 2 3 3 3 2 0 0 0 0 0 0 0 0 0 0 0 0 0
2 6 6 6 2 3 3 3 2 0 0 0 8 8 8 8 8 0 0 0 0 0
2 6 6 6 2 3 3 3 2 0 0 0 8 4 4 4 8 0 0 0 0 0
2 0 0 0 2 2 4 4 4 2 0 0 8 4 4 4 8 0 0 0 0 0
2 2 2 2 2 2 4 4 4 2 0 0 8 4 4 4 8 0 0 0 0 0
0 0 0 0 0 2 4 4 4 2 0 0 8 8 8 8 8 0 0 0 0 0
0 0 0 0 0 2 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 278
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 114.87603305785123

## Example 2:
Input:
```
4 4 4 4 4 4 4 4 2 2 2 2 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 2 5 5 5 2 4 4 4 4 4 4 4 4 4
4 4 8 8 8 8 8 4 2 5 5 5 2 4 2 2 2 2 2 4 4 4
4 4 8 9 9 9 8 4 2 5 5 5 2 4 2 3 3 3 2 4 4 4
4 4 8 9 9 9 8 4 2 2 2 2 2 4 2 3 3 3 2 4 4 4
4 4 8 9 9 9 8 4 4 4 4 4 4 4 2 3 3 3 2 4 4 4
4 4 8 8 8 8 8 4 4 4 4 4 4 4 2 2 2 2 2 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 4
8 3 3 3 8 4 4 4 4 4 4 4 4 4 4 4 2 6 6 6 2 4
8 3 3 3 8 4 4 4 4 4 4 4 4 4 4 4 2 6 6 6 2 4
8 3 3 3 8 4 4 4 4 4 4 4 4 4 4 4 2 6 6 6 2 4
8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 8 8 8 8 8 4 4 4 4 4 4 4 2 2 2 2 2 4 4 4
4 4 8 1 1 1 8 4 4 4 4 4 4 4 2 1 1 1 2 4 4 4
4 4 8 1 1 1 8 4 8 8 8 8 8 4 2 1 1 1 2 4 4 4
4 4 8 1 1 1 8 4 8 6 6 6 8 4 2 1 1 1 2 4 4 4
4 4 8 8 8 8 8 4 8 6 6 6 8 4 2 2 2 2 2 4 4 4
4 4 4 4 4 4 4 4 8 6 6 6 8 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 8 8 8 8 8 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
```
Expected Output:
```
4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 2 5 5 5 2 4 4 4 4 4
8 8 8 8 8 4 4 4 4 4 4 4 2 5 5 5 2 2 2 2 2 2
8 9 9 9 8 4 4 4 4 4 4 4 2 5 5 5 2 2 3 3 3 2
8 9 9 9 8 4 4 4 4 4 4 4 2 2 2 2 2 2 3 3 3 2
8 9 9 9 8 4 4 4 4 4 4 4 4 4 4 4 4 2 3 3 3 2
8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2
8 3 3 3 8 4 4 4 4 4 4 4 4 4 4 4 4 2 6 6 6 2
8 3 3 3 8 4 4 4 4 4 4 4 4 4 4 4 4 2 6 6 6 2
8 3 3 3 8 4 4 4 4 4 4 4 4 4 4 4 4 2 6 6 6 2
8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2
8 1 1 1 8 4 4 4 4 4 4 4 4 4 4 4 4 2 1 1 1 2
8 1 1 1 8 8 8 8 8 8 4 4 4 4 4 4 4 2 1 1 1 2
8 1 1 1 8 8 6 6 6 8 4 4 4 4 4 4 4 2 1 1 1 2
8 8 8 8 8 8 6 6 6 8 4 4 4 4 4 4 4 2 2 2 2 2
4 4 4 4 4 8 6 6 6 8 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 8 8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
4 4 8 9 9 9 8 4 2 5 5 5 2 4 2 3 3 3 2 4 4 4
4 4 8 9 9 9 8 4 2 5 5 5 2 4 2 3 2 2 2 2 2 4
4 4 8 9 9 9 8 4 2 5 5 5 2 4 2 3 2 6 6 6 2 4
4 4 8 0 0 0 8 4 2 0 0 0 2 4 2 0 2 6 6 6 2 4
4 4 8 8 8 8 8 4 2 2 2 2 2 4 2 2 2 6 6 6 2 4
4 4 0 0 0 0 0 4 4 4 4 4 4 4 0 0 2 2 2 2 2 4
4 4 0 0 0 0 0 4 4 4 4 4 4 4 0 0 0 0 0 4 4 4
8 3 8 8 8 8 8 4 4 4 4 4 4 4 2 2 2 2 2 4 4 4
8 3 8 1 1 1 8 4 4 4 4 4 4 4 2 1 1 1 2 0 0 4
8 3 8 1 1 1 8 4 8 8 8 8 8 4 2 1 1 1 2 0 0 4
8 0 8 1 1 1 8 4 8 6 6 6 8 4 2 1 1 1 2 0 0 4
8 8 8 8 8 8 8 4 8 6 6 6 8 4 2 2 2 2 2 0 0 4
0 0 0 0 0 4 4 4 8 6 6 6 8 4 4 4 0 0 0 0 0 4
4 4 4 4 4 4 4 4 8 8 8 8 8 4 4 4 4 4 4 4 4 4
4 4 0 0 0 0 0 4 4 4 4 4 4 4 0 0 0 0 0 4 4 4
```
Match: False
Pixels Off: 362
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 299.1735537190083

## Example 3:
Input:
```
1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 1 1 1 1 1
1 1 1 8 8 8 8 8 1 1 1 1 2 3 3 3 2 1 1 1 1 1
1 1 1 8 2 2 2 8 1 1 1 1 2 3 3 3 2 1 1 1 1 1
1 1 1 8 2 2 2 8 1 1 1 1 2 3 3 3 2 1 1 1 1 1
1 1 1 8 2 2 2 8 1 1 1 1 2 2 2 2 2 1 1 1 1 1
1 1 1 8 8 8 8 8 1 1 1 1 8 8 8 8 8 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 8 6 6 6 8 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 8 6 6 6 8 1 1 1 1 1
1 1 2 2 2 2 2 1 1 1 1 1 8 6 6 6 8 1 1 1 1 1
1 1 2 5 5 5 2 1 1 1 1 1 8 8 8 8 8 1 1 1 1 1
1 1 2 5 5 5 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 2 5 5 5 2 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 2 2 2 2 2 1 1 1 1 1 1 1 2 2 2 2 2 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 4 4 4 2 1 1 1
1 1 1 1 1 1 1 8 8 8 8 8 1 1 2 4 4 4 2 1 1 1
1 1 1 1 1 1 1 8 3 3 3 8 1 1 2 4 4 4 2 1 1 1
1 1 1 1 1 1 1 8 3 3 3 8 1 1 2 2 2 2 2 1 1 1
1 1 1 1 1 1 1 8 3 3 3 8 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 8 8 8 8 8 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```
Expected Output:
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2
8 8 8 8 8 1 1 1 1 1 1 1 1 1 1 1 1 2 3 3 3 2
8 2 2 2 8 1 1 1 1 1 1 1 1 1 1 1 1 2 3 3 3 2
8 2 2 2 8 1 1 1 1 1 1 1 1 1 1 1 1 2 3 3 3 2
8 2 2 2 8 1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2
8 8 8 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 8 6 6 6 8 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 8 6 6 6 8 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 8 6 6 6 8 1 1 2 2 2 2 2 1 1 1 1 1
1 1 1 1 1 8 8 8 8 8 1 1 2 5 5 5 2 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 2 5 5 5 2 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 2 5 5 5 2 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 2
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 4 4 4 2
8 8 8 8 8 1 1 1 1 1 1 1 1 1 1 1 1 2 4 4 4 2
8 3 3 3 8 1 1 1 1 1 1 1 1 1 1 1 1 2 4 4 4 2
8 3 3 3 8 1 1 1 1 1 1 1 1 1 1 1 1 2 2 2 2 2
8 3 3 3 8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
8 8 8 8 8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 8 2 2 2 8 1 1 1 1 8 6 6 6 8 1 1 1 1 1
1 1 1 8 2 2 2 8 1 1 1 1 8 6 6 6 8 1 1 1 1 1
1 1 1 8 2 2 2 8 1 1 1 1 8 6 6 6 8 1 1 1 1 1
1 1 1 8 0 0 0 8 1 1 1 1 8 0 0 0 8 1 1 1 1 1
1 1 1 8 8 8 8 8 1 1 1 1 8 8 8 8 8 1 1 1 1 1
1 1 1 0 0 0 0 0 1 1 1 1 0 0 2 2 2 2 2 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 0 0 2 4 4 4 2 1 1 1
1 1 2 5 5 5 2 8 8 8 8 8 0 0 2 4 4 4 2 1 1 1
1 1 2 5 5 5 2 8 3 3 3 8 0 0 2 4 4 4 2 1 1 1
1 1 2 5 5 5 2 8 3 3 3 8 0 0 2 2 2 2 2 1 1 1
1 1 2 0 0 0 2 8 3 3 3 8 1 1 1 1 1 1 1 1 1 1
1 1 2 2 2 2 2 8 8 8 8 8 1 1 1 1 1 1 1 1 1 1
1 1 0 0 0 0 0 1 1 1 1 1 1 1 0 0 0 0 0 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 0 0 0 0 0 1 1 1
1 1 1 1 1 1 1 0 0 0 0 0 1 1 0 0 0 0 0 1 1 1
```
Match: False
Pixels Off: 342
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 282.64462809917353
