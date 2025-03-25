
Previous Code:
```python
"""
1.  **Object Identification:** Identify all contiguous, non-zero colored regions (objects) in the input grid. Record their color, top-left corner position, and the pixels that define them.

2.  **Row 5 Check:** Examine Row 5 (index 4) of the *input* grid.

3.  **Conditional Action (Above Row 5):**
    *   **If Row 5 has *any* non-zero pixels:** Remove all objects whose top-left corner is *strictly above* Row 5 (row index < 4) from the output.
    * **If Row 5 has *only* zero pixels:** Duplicate the objects with their top-left pixels above row 5. Copy them from their original positions to row five and below until row 5 is filled.

4.  **Reposition Objects (At or Below Row 5):** Iterate through the objects whose top-left corners were originally at or below Row 5 in the input grid. Maintain their original order (top-to-bottom, left-to-right).

5.  **Placement:**
    * Find empty spaces in the output grid, defined as runs of contiguous zeros.
    * Place each of the remaining objects in the first available empty space in the output that fully accommodates the object, going from top left to right.
    * Objects must fit without changing shape.

6. **Output:** Return filled output grid.
"""

import numpy as np

def find_objects(grid):
    """Finds contiguous objects in a grid."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = []

    def dfs(row, col, color, obj_pixels):
        if (row < 0 or row >= rows or col < 0 or col >= cols or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj_pixels.append((row, col))
        dfs(row + 1, col, color, obj_pixels)
        dfs(row - 1, col, color, obj_pixels)
        dfs(row, col + 1, color, obj_pixels)
        dfs(row, col - 1, color, obj_pixels)

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] != 0:
                obj_pixels = []
                dfs(r, c, grid[r, c], obj_pixels)
                # find top-left
                min_row = min(p[0] for p in obj_pixels)
                min_col = min(p[1] for p in obj_pixels)

                objects.append({
                    'color': grid[r, c],
                    'initial_position': (min_row, min_col),
                    'pixels': obj_pixels,
                    'shape': 'contiguous'
                })
    return objects

def find_empty_spaces(grid):
    """Finds contiguous blocks of zeros (empty spaces)."""
    rows, cols = grid.shape
    empty_spaces = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, current_space):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
                visited[r, c] or grid[r, c] != 0):
            return
        visited[r, c] = True
        current_space.append((r, c))
        dfs(r + 1, c, current_space)
        dfs(r - 1, c, current_space)
        dfs(r, c + 1, current_space)
        dfs(r, c - 1, current_space)

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] == 0:
                current_space = []
                dfs(r, c, current_space)
                if current_space:
                    min_row = min(p[0] for p in current_space)
                    min_col = min(p[1] for p in current_space)
                    max_row = max(p[0] for p in current_space)
                    max_col = max(p[1] for p in current_space)
                    empty_spaces.append(((min_row, min_col), (max_row - min_row + 1, max_col - min_col + 1)))
    return empty_spaces

def can_place(grid, obj_pixels, start_row, start_col):
    """Checks if an object can be placed."""
    rows, cols = grid.shape
    for r, c in obj_pixels:
        new_r, new_c = start_row + (r - obj_pixels[0][0]), start_col + (c - obj_pixels[0][1])
        if (new_r < 0 or new_r >= rows or new_c < 0 or new_c >= cols or
                grid[new_r, new_c] != 0):
            return False
    return True

def place_object(grid, obj_pixels, color, start_row, start_col):
    """Places an object onto the grid."""
    for r, c in obj_pixels:
        new_r, new_c = start_row + (r - obj_pixels[0][0]), start_col + (c - obj_pixels[0][1])
        grid[new_r, new_c] = color


def transform(input_grid):
    # initialize output_grid
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # 1. Object Identification
    objects = find_objects(input_grid)

    # 2. Row 5 Check
    row_5_has_non_zero = np.any(input_grid[min(4, rows - 1), :] != 0)

    # 3. Conditional Action (Above Row 5)
    objects_above_row_5 = [obj for obj in objects if obj['initial_position'][0] < min(4, rows)]
    objects_at_or_below_row_5 = [obj for obj in objects if obj['initial_position'][0] >= min(4, rows)]

    if row_5_has_non_zero:
        # Remove objects above Row 5
        pass  # Don't add them to the output
    else:
        # Duplicate and shift objects above row 5
        row_index = min(4, rows - 1)
        for obj in objects_above_row_5:
            obj_height = max(r for r, _ in obj['pixels']) - min(r for r, _ in obj['pixels']) + 1
            if row_index + obj_height <= rows: # check if it fits
              place_object(output_grid, obj['pixels'], obj['color'], row_index, obj['initial_position'][1])
              row_index += obj_height

    # 4. Reposition Objects (At or Below Row 5) & 5. Placement

    empty_spaces = find_empty_spaces(output_grid)
    empty_space_index = 0

    for obj in objects_at_or_below_row_5:
        placed = False
        while empty_space_index < len(empty_spaces) and not placed:
            (start_row, start_col), (space_rows, space_cols) = empty_spaces[empty_space_index]
            if can_place(output_grid, obj['pixels'], start_row, start_col):
                place_object(output_grid, obj['pixels'], obj['color'], start_row, start_col)
                placed = True
                # Recalculate empty spaces
                empty_spaces = find_empty_spaces(output_grid)
                empty_space_index = 0  # Reset to start from top-left
            else:
                empty_space_index += 1

    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
9 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 1 1 1 1 0 0 0
0 0 0 0 5 0 0 0 1 0 0 0
0 0 0 0 5 0 0 0 1 0 0 0
0 0 6 3 3 3 0 5 5 7 0 0
0 0 6 0 0 3 0 5 0 7 0 0
0 0 6 0 0 3 0 5 0 7 0 0
0 4 2 2 2 2 2 2 2 2 7 0
0 4 0 0 0 0 0 0 0 0 7 0
0 4 0 0 0 0 0 0 0 0 7 0
0 4 0 0 0 0 0 0 0 0 7 0
```
Expected Output:
```
9 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 1 1 1 1 0 0 0
0 0 0 0 5 0 0 0 1 0 0 0
0 0 0 0 5 0 0 0 1 0 0 0
0 0 6 3 3 3 0 5 5 7 0 0
0 0 6 0 0 3 0 5 0 7 0 0
0 0 6 0 0 3 0 5 0 7 0 0
0 4 2 2 2 2 2 2 2 2 7 0
0 4 0 0 0 0 0 0 0 0 7 0
0 4 0 0 0 0 0 0 0 0 7 0
0 4 0 0 0 0 0 0 0 0 7 0
```
Transformed Output:
```
6 0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 43
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 59.72222222222223

## Example 2:
Input:
```
4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 5 5 5 8 0 0
0 0 0 0 0 2 0 0 0 8 0 0
0 0 0 0 0 2 0 0 0 8 0 0
0 0 0 0 0 2 0 0 0 8 0 0
0 0 9 4 4 4 7 0 2 3 3 0
0 0 9 0 0 0 7 0 2 0 3 0
0 0 9 0 0 0 7 0 2 0 3 0
0 6 5 5 0 1 7 7 7 7 4 0
0 6 0 5 0 1 0 0 0 0 4 0
0 6 0 5 0 1 0 0 0 0 4 0
```
Expected Output:
```
4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 0 0 2 5 5 5 8 0 0
0 0 9 0 0 2 0 0 0 8 0 0
0 0 9 0 0 2 0 0 0 8 0 0
0 0 9 0 0 2 7 0 2 8 0 0
0 6 5 5 0 1 7 0 2 3 3 0
0 6 0 5 0 1 7 0 2 0 3 0
0 6 0 5 0 1 7 7 7 7 3 0
```
Transformed Output:
```
9 0 0 0 0 0 0 0 0 0 0 0
9 0 0 0 0 0 0 0 0 0 0 0
9 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 42
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 58.333333333333314

## Example 3:
Input:
```
6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 5 5 5 8 0 0
0 0 0 0 0 2 0 0 0 8 0 0
0 0 0 0 0 2 0 0 0 8 0 0
0 0 0 0 0 2 0 0 0 8 0 0
0 0 9 4 4 4 7 0 2 3 3 0
0 0 9 0 0 0 7 0 2 0 3 0
0 0 9 0 0 0 7 0 2 0 3 0
0 6 5 5 0 1 7 7 7 7 4 0
0 6 0 5 0 1 0 0 0 0 4 0
0 6 0 5 0 1 0 0 0 0 4 0
```
Expected Output:
```
6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 2 5 5 5 8 0 0
0 0 0 0 0 2 0 0 0 8 0 0
0 0 0 0 0 2 7 0 2 3 3 0
0 0 0 0 0 2 7 0 2 0 3 0
0 0 9 4 4 4 7 0 2 0 3 0
0 0 9 5 0 1 7 7 7 7 4 0
0 0 9 5 0 1 0 0 0 0 4 0
0 0 5 5 0 1 0 0 0 0 4 0
```
Transformed Output:
```
9 0 0 0 0 0 0 0 0 0 0 0
9 0 0 0 0 0 0 0 0 0 0 0
9 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 44
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 61.111111111111114

## Example 4:
Input:
```
4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 1 1 1 1 0 0 0
0 0 0 0 5 0 0 0 1 0 0 0
0 0 0 0 5 0 0 0 1 0 0 0
0 0 6 3 3 3 0 5 5 7 0 0
0 0 6 0 0 3 0 5 0 7 0 0
0 0 6 0 0 3 0 5 0 7 0 0
0 4 2 2 2 2 2 2 2 2 7 0
0 4 0 0 0 0 0 0 0 0 7 0
0 4 0 0 0 0 0 0 0 0 7 0
0 4 0 0 0 0 0 0 0 0 7 0
```
Expected Output:
```
4 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 1 1 1 1 0 0 0
0 0 0 0 5 0 0 0 1 0 0 0
0 0 0 0 5 0 0 0 1 0 0 0
0 0 6 3 3 3 0 5 5 7 7 0
0 0 6 0 0 3 0 5 0 7 7 0
0 0 6 0 0 3 0 5 0 7 7 0
0 0 2 2 2 2 2 2 2 2 7 0
```
Transformed Output:
```
6 0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 39
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 54.166666666666686

## Example 5:
Input:
```
7 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 1 1 1 1 0 0 0
0 0 0 0 5 0 0 0 1 0 0 0
0 0 0 0 5 0 0 0 1 0 0 0
0 0 6 3 3 3 0 5 5 7 0 0
0 0 6 0 0 3 0 5 0 7 0 0
0 0 6 0 0 3 0 5 0 7 0 0
0 4 2 2 2 2 2 2 2 2 7 0
0 4 0 0 0 0 0 0 0 0 7 0
0 4 0 0 0 0 0 0 0 0 7 0
0 4 0 0 0 0 0 0 0 0 7 0
```
Expected Output:
```
7 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 5 0 0 0 0 0 0 0
0 0 0 0 5 1 1 1 1 0 0 0
0 4 6 3 3 3 0 5 1 0 0 0
0 4 6 0 0 3 0 5 1 0 0 0
0 4 6 0 0 3 0 5 5 0 0 0
0 4 2 2 2 2 2 2 2 2 0 0
```
Transformed Output:
```
6 0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0 0
6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 36
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 50.0
Here's an analysis of the provided examples and a revised natural language program:

**General Assessment:**

The current code has significant errors. It seems to struggle with correctly identifying and placing objects based on the Row 5 condition. The primary issue is that it often removes or misplaces objects, especially those above Row 5, even when Row 5 *does* contain non-zero pixels. It also fails to correctly handle cases where Row 5 has only zero pixels, where object duplication and shifting is required and is not performed correctly. Recalculating empty spaces in the inner loop causes problems with object placement order.

**Strategy:**

1.  **Simplify Object Placement:** Remove the recalculation of empty spaces inside the object placement loop. The empty spaces should be calculated *once* after handling objects above row 5, and then iterated through sequentially.

2.  **Correct Row 5 Logic:**  The conditional logic for handling objects above Row 5 needs careful review. The current implementation seems to misunderstand the instructions. Objects above Row 5 should be *removed* if Row 5 has non-zero pixels, and *duplicated and moved* to row 5 if the row has *all zeros*.

3.  **Object-Centric Approach:** Maintain a clear separation between object identification and placement. Ensure the 'can_place' function accurately reflects whether an object can fit in a given space *without overlapping other objects* or exceeding grid boundaries.

4. **Shape Detection**: The original shapes needs to be determined, to know how big the available output block must be to fit the object.

**Metrics and Observations (using code execution):**



*code_execution:*
```python
import numpy as np

def analyze_example(input_grid, expected_output, transformed_output):
    input_grid = np.array(input_grid)
    expected_output = np.array(expected_output)
    transformed_output = np.array(transformed_output)

    row5_nonzero = np.any(input_grid[min(4, input_grid.shape[0] - 1), :] != 0)

    input_objects = find_objects(input_grid)
    expected_objects = find_objects(expected_output)
    transformed_objects = find_objects(transformed_output)


    return {
        'row5_nonzero': bool(row5_nonzero),
        'input_objects_count': len(input_objects),
        'expected_objects_count': len(expected_objects),
        'transformed_objects_count': len(transformed_objects)
    }

def find_objects(grid):
    """Finds contiguous objects in a grid."""
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    objects = []

    def dfs(row, col, color, obj_pixels):
        if (row < 0 or row >= rows or col < 0 or col >= cols or
                visited[row, col] or grid[row, col] != color):
            return
        visited[row, col] = True
        obj_pixels.append((row, col))
        dfs(row + 1, col, color, obj_pixels)
        dfs(row - 1, col, color, obj_pixels)
        dfs(row, col + 1, color, obj_pixels)
        dfs(row, col - 1, color, obj_pixels)

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] != 0:
                obj_pixels = []
                dfs(r, c, grid[r, c], obj_pixels)
                # find top-left
                min_row = min(p[0] for p in obj_pixels)
                min_col = min(p[1] for p in obj_pixels)
                # find shape
                max_row = max(p[0] for p in obj_pixels)
                max_col = max(p[1] for p in obj_pixels)

                objects.append({
                    'color': grid[r, c],
                    'initial_position': (min_row, min_col),
                    'pixels': obj_pixels,
                    'shape': (max_row - min_row + 1, max_col - min_col + 1)
                })
    return objects


examples = [
    {
        "input": [
            [9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 5, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 5, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 5, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 6, 3, 3, 3, 0, 5, 5, 7, 0, 0],
            [0, 0, 6, 0, 0, 3, 0, 5, 0, 7, 0, 0],
            [0, 0, 6, 0, 0, 3, 0, 5, 0, 7, 0, 0],
            [0, 4, 2, 2, 2, 2, 2, 2, 2, 2, 7, 0],
            [0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0],
            [0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0],
            [0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0],
        ],
        "expected": [
            [9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 5, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 5, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 5, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 6, 3, 3, 3, 0, 5, 5, 7, 0, 0],
            [0, 0, 6, 0, 0, 3, 0, 5, 0, 7, 0, 0],
            [0, 0, 6, 0, 0, 3, 0, 5, 0, 7, 0, 0],
            [0, 4, 2, 2, 2, 2, 2, 2, 2, 2, 7, 0],
            [0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0],
            [0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0],
            [0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0],
        ],
        "transformed": [
            [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
    },
     {
        "input": [
            [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 5, 5, 5, 8, 0, 0],
            [0, 0, 0, 0, 0, 2, 0, 0, 0, 8, 0, 0],
            [0, 0, 0, 0, 0, 2, 0, 0, 0, 8, 0, 0],
            [0, 0, 0, 0, 0, 2, 0, 0, 0, 8, 0, 0],
            [0, 0, 9, 4, 4, 4, 7, 0, 2, 3, 3, 0],
            [0, 0, 9, 0, 0, 0, 7, 0, 2, 0, 3, 0],
            [0, 0, 9, 0, 0, 0, 7, 0, 2, 0, 3, 0],
            [0, 6, 5, 5, 0, 1, 7, 7, 7, 7, 4, 0],
            [0, 6, 0, 5, 0, 1, 0, 0, 0, 0, 4, 0],
            [0, 6, 0, 5, 0, 1, 0, 0, 0, 0, 4, 0],
        ],
        "expected": [
            [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 5, 5, 5, 8, 0, 0],
            [0, 0, 9, 0, 0, 2, 0, 0, 0, 8, 0, 0],
            [0, 0, 9, 0, 0, 2, 0, 0, 0, 8, 0, 0],
            [0, 0, 9, 0, 0, 2, 7, 0, 2, 8, 0, 0],
            [0, 6, 5, 5, 0, 1, 7, 0, 2, 3, 3, 0],
            [0, 6, 0, 5, 0, 1, 7, 0, 2, 0, 3, 0],
            [0, 6, 0, 5, 0, 1, 7, 7, 7, 7, 3, 0],
        ],
        "transformed": [
            [9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
    },
      {
        "input": [
            [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 5, 5, 5, 8, 0, 0],
            [0, 0, 0, 0, 0, 2, 0, 0, 0, 8, 0, 0],
            [0, 0, 0, 0, 0, 2, 0, 0, 0, 8, 0, 0],
            [0, 0, 0, 0, 0, 2, 0, 0, 0, 8, 0, 0],
            [0, 0, 9, 4, 4, 4, 7, 0, 2, 3, 3, 0],
            [0, 0, 9, 0, 0, 0, 7, 0, 2, 0, 3, 0],
            [0, 0, 9, 0, 0, 0, 7, 0, 2, 0, 3, 0],
            [0, 6, 5, 5, 0, 1, 7, 7, 7, 7, 4, 0],
            [0, 6, 0, 5, 0, 1, 0, 0, 0, 0, 4, 0],
            [0, 6, 0, 5, 0, 1, 0, 0, 0, 0, 4, 0],
        ],
        "expected": [
            [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 8, 0, 0],
            [0, 0, 0, 0, 0, 2, 5, 5, 5, 8, 0, 0],
            [0, 0, 0, 0, 0, 2, 0, 0, 0, 8, 0, 0],
            [0, 0, 0, 0, 0, 2, 7, 0, 2, 3, 3, 0],
            [0, 0, 0, 0, 0, 2, 7, 0, 2, 0, 3, 0],
            [0, 0, 9, 4, 4, 4, 7, 0, 2, 0, 3, 0],
            [0, 0, 9, 5, 0, 1, 7, 7, 7, 7, 4, 0],
            [0, 0, 9, 5, 0, 1, 0, 0, 0, 0, 4, 0],
            [0, 0, 5, 5, 0, 1, 0, 0, 0, 0, 4, 0],
        ],
        "transformed": [
            [9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [9, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
    },
    {
        "input": [
            [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 5, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 5, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 5, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 6, 3, 3, 3, 0, 5, 5, 7, 0, 0],
            [0, 0, 6, 0, 0, 3, 0, 5, 0, 7, 0, 0],
            [0, 0, 6, 0, 0, 3, 0, 5, 0, 7, 0, 0],
            [0, 4, 2, 2, 2, 2, 2, 2, 2, 2, 7, 0],
            [0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0],
            [0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0],
            [0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0],
        ],
        "expected": [
            [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 5, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 5, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 5, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 6, 3, 3, 3, 0, 5, 5, 7, 7, 0],
            [0, 0, 6, 0, 0, 3, 0, 5, 0, 7, 7, 0],
            [0, 0, 6, 0, 0, 3, 0, 5, 0, 7, 7, 0],
            [0, 0, 2, 2, 2, 2, 2, 2, 2, 2, 7, 0],
        ],
        "transformed": [
            [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
    },
    {
        "input": [
            [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 5, 1, 1, 1, 1, 0, 0, 0],
            [0, 0, 0, 0, 5, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 0, 0, 5, 0, 0, 0, 1, 0, 0, 0],
            [0, 0, 6, 3, 3, 3, 0, 5, 5, 7, 0, 0],
            [0, 0, 6, 0, 0, 3, 0, 5, 0, 7, 0, 0],
            [0, 0, 6, 0, 0, 3, 0, 5, 0, 7, 0, 0],
            [0, 4, 2, 2, 2, 2, 2, 2, 2, 2, 7, 0],
            [0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0],
            [0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0],
            [0, 4, 0, 0, 0, 0, 0, 0, 0, 0, 7, 0],
        ],
        "expected": [
            [7, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 5, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 5, 1, 1, 1, 1, 0, 0, 0],
            [0, 4, 6, 3, 3, 3, 0, 5, 1, 0, 0, 0],
            [0, 4, 6, 0, 0, 3, 0, 5, 1, 0, 0, 0],
            [0, 4, 6, 0, 0, 3, 0, 5, 5, 0, 0, 0],
            [0, 4, 2, 2, 2, 2, 2, 2, 2, 2, 0, 0],
        ],
        "transformed": [
            [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [6, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        ]
    }
]

results = []
for example in examples:
  results.append(analyze_example(example['input'], example['expected'], example['transformed']))

print(results)

```

*code_execution_result:*
outcome: 1
```
[{'row5_nonzero': True, 'input_objects_count': 10, 'expected_objects_count': 10, 'transformed_objects_count': 1}, {'row5_nonzero': True, 'input_objects_count': 13, 'expected_objects_count': 11, 'transformed_objects_count': 1}, {'row5_nonzero': True, 'input_objects_count': 13, 'expected_objects_count': 12, 'transformed_objects_count': 1}, {'row5_nonzero': True, 'input_objects_count': 10, 'expected_objects_count': 8, 'transformed_objects_count': 1}, {'row5_nonzero': True, 'input_objects_count': 10, 'expected_objects_count': 8, 'transformed_objects_count': 1}]

```
**YAML Fact Representation:**


```yaml
facts:
  - task: "Conditional Object Shifting"
  - grid_size: "12x12"
  - row_5_condition:
      description: "Objects above row 5 are removed if row 5 has non-zero pixels, otherwise, duplicated and shifted."
  - object_identification:
      method: "Contiguous non-zero regions"
      properties:
        - color
        - top_left_position
        - shape
        - pixels
  - object_placement:
    method: "Place objects in the first available empty space from top-left."
    constraints:
      - "Maintain original shape"
      - "No overlapping"

```


**Natural Language Program:**

1.  **Identify Objects:** Find all contiguous regions of non-zero pixels in the input grid. Each region is an object. Record the object's color, the top-left pixel's coordinates, the object's shape (width and height), and a list of all pixel coordinates within the object.

2.  **Check Row 5:** Determine if Row 5 (index 4) of the *input* grid contains any non-zero pixels. Note: If the grid height is less than 5, treat row 5 as the last row of the grid.

3.  **Conditional Object Removal/Duplication:**
    *   **If Row 5 has any non-zero pixels:** Remove all objects whose top-left corner's row coordinate is *strictly above* Row 5 (row index < 4).
    *   **If Row 5 has only zero pixels:**
        * Iterate through the objects with top-left corners above row 5.
        * Calculate each object's height and calculate the starting row to duplicate the object to.
        * Place each of these objects in their new position from top-to-bottom, left-to-right.

4.  **Place Remaining Objects:**
     * Create an empty output grid of same dimensions as the input.
     * Find all available empty spaces - contiguous blocks of zeros in the output grid, starting from the top-left.
     * Iterate over the remaining objects (those not removed in step 3) in their original order (top-to-bottom, left-to-right based on their initial positions in the *input* grid).
     * For each object:
          * Find the first empty space in the output grid (from top-left) large enough to fit the entire object without overlapping or going out of bounds.
          * If a suitable space is found, place the object in that space by copying its pixels to the corresponding positions in the output grid.
          * If not found, continue.

5.  **Output:** Return the filled output grid.

