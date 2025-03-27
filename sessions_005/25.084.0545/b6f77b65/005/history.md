
Previous Code:
```python
"""
1.  **Identify Objects:** Identify all contiguous, non-zero colored regions in the input grid as distinct objects. Record their color, initial position (top-left corner), and shape.

2.  **Examine Row 5:** Determine if Row 5 of the input grid contains any non-zero pixels.

3.  **Conditional Object Removal/Duplication:**
    *   **If Row 5 has non-zero pixels:** Remove all objects that are entirely *above* row 5 in the input grid.
    *  **If and only if Row 5 is all zeros:** Duplicate all of the objects from above row 5 to row 5 downwards, until row 5 is filled with non-zero entries.

4.  **Move and Merge (Objects at or below Row 5):**
     * Iterate through the objects that were originally located at or below Row 5 in the input grid, preserving their original order (row-major order: top-to-bottom, then left-to-right).

5. **Fill available space:**
    * Find empty spaces, defined as runs of zeros.
    * For each object identified in step 4:
      *   Place it in the first available empty space in the output grid that can accommodate its shape, starting from the top-left corner (0,0) and proceeding in row-major order.
      * Do not split objects.

6. **Output:** The filled output array.
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
                    'shape': 'contiguous' # for this task all objects are contiguous
                })
    return objects

def find_empty_spaces(grid):
    """
    Finds contiguous blocks of zeros (empty spaces) in the grid.
    Returns a list of tuples, where each tuple contains the (row, col) of
    the top-left corner of the empty space, and its size (rows, cols).
    """
    rows, cols = grid.shape
    empty_spaces = []
    visited = np.zeros_like(grid, dtype=bool)

    def dfs(r, c, current_space):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
                visited[r, c] or grid[r, c] != 0):
            return
        visited[r, c] = True
        current_space.append((r,c))
        dfs(r + 1, c, current_space)
        dfs(r - 1, c, current_space)
        dfs(r, c + 1, current_space)
        dfs(r, c - 1, current_space)

    for r in range(rows):
        for c in range(cols):
            if not visited[r,c] and grid[r,c] == 0:
                current_space = []
                dfs(r, c, current_space)
                if current_space:
                    # calculate size of empty space
                    min_row = min(p[0] for p in current_space)
                    min_col = min(p[1] for p in current_space)
                    max_row = max(p[0] for p in current_space)
                    max_col = max(p[1] for p in current_space)

                    empty_spaces.append(((min_row, min_col), (max_row - min_row + 1, max_col - min_col + 1)))
    return empty_spaces

def can_place(grid, object_pixels, start_row, start_col):
    """Checks if an object can be placed at the given location without overlapping."""
    rows, cols = grid.shape
    for r, c in object_pixels:
        new_r, new_c = start_row + (r-object_pixels[0][0]), start_col + (c - object_pixels[0][1]) # offset based on topleft
        if (new_r < 0 or new_r >= rows or new_c < 0 or new_c >= cols or
                grid[new_r, new_c] != 0):
            return False
    return True

def place_object(grid, object_pixels, color, start_row, start_col):
    """Places the object onto the grid at the specified location."""
    for r, c in object_pixels:
        new_r, new_c = start_row + (r - object_pixels[0][0]), start_col + (c - object_pixels[0][1])  # offset based on topleft
        grid[new_r, new_c] = color

def transform(input_grid):
    """Transforms the input grid according to the observed rules."""
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # 1. Identify Objects
    objects = find_objects(input_grid)

    # 2. Examine Row 5
    row_5_has_non_zero = np.any(input_grid[min(4, rows-1), :] != 0)  # min handles edge case

    # 3. Conditional Object Removal / Duplication
    objects_above_row_5 = [obj for obj in objects if obj['initial_position'][0] < min(5,rows)]
    objects_at_or_below_row_5 = [obj for obj in objects if obj['initial_position'][0] >= min(5,rows)]
    
    if row_5_has_non_zero:
      pass # objects above row 5 removed by not adding to output
    else:
        # Duplicate objects above row 5
        row_index = min(4, rows-1)
        
        while row_index < rows and not np.any(output_grid[row_index,:] != 0):
          for obj in objects_above_row_5:
            fill_row = row_index
            fill_col = 0
            for r, c in obj['pixels']:
              if fill_row < rows:
                output_grid[fill_row,fill_col] = obj['color']
                fill_col += 1
                if fill_col == cols:
                    fill_col = 0
                    fill_row += 1


            row_index += (max(r for r, c in obj['pixels']) - min(r for r, c in obj['pixels'])) + 1
          
            

    # 4 & 5. Move and Merge (Objects at or below Row 5) and place remaining from above
    
    
    empty_spaces = find_empty_spaces(output_grid)
    empty_space_index = 0

    
    for obj in objects_at_or_below_row_5:
      placed = False
      while empty_space_index < len(empty_spaces) and not placed:
            (start_row, start_col), (space_rows, space_cols) = empty_spaces[empty_space_index]
            if can_place(output_grid, obj['pixels'], start_row, start_col):
                place_object(output_grid, obj['pixels'], obj['color'], start_row, start_col)
                placed = True

                # update empty spaces
                new_empty_spaces = find_empty_spaces(output_grid)
                empty_spaces = new_empty_spaces
                empty_space_index = 0 # start from the beginning to fill any gaps made by the placement

            else:
                empty_space_index += 1

      if not placed:
        # no more space, drop the object, in theory this should not occur based
        # on the problem definition.
        pass


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
Okay, let's analyze the results and refine the natural language program.

**General Assessment:**

The code fails to correctly transform the input grids in all test cases. The primary issues seem to be:

1.  **Incorrect Object Placement:** The logic for placing objects in available empty spaces, especially after conditional removal or duplication, is flawed. It doesn't correctly handle the positioning and arrangement of objects based on the examples. It appears to be filling the grid with zeros.
2.  **Misinterpretation of Row 5 Condition:** The code's interpretation of the "Row 5" condition isn't entirely accurate. It seems to be removing *all* objects above row 5, not just when there are non-zero entries.
3. Duplication does not appear to be working.
4. The object placement is overwriting itself.

**Strategy for Resolving Errors:**

1.  **Refine Object Placement:** We need a more precise algorithm for placing objects. The current approach of simply iterating through empty spaces and attempting to place the first object that fits is insufficient. We may need to explicitly consider spatial relationships and constraints, such as not splitting up objects, and making sure objects stay within the bounds of the source object.
2.  **Clarify Row 5 Logic:** Double-check the condition for removing/duplicating objects above Row 5. Ensure the logic matches the provided descriptions.
3. **Improve Duplication:** The code to copy objects down to row 5 needs to be made more robust so that the copying works.
4. **Improve object order placement:** Right now objects are overwritten.

**Gather Metrics:**

I will use code execution to confirm some suspicions, collect and print specific metric data.


*code_execution:*
```python
import numpy as np

def analyze_results(results):
    """Analyzes the results of the transform function."""
    analysis = {}
    for i, example in enumerate(results):
        input_grid = np.array(example['input'])
        expected_output = np.array(example['expected_output'])
        transformed_output = np.array(example['transformed_output'])
        
        
        # check if row 5 has non-zero elements
        row5_nonzero = np.any(input_grid[min(4, input_grid.shape[0]-1), :] != 0)

        # find objects in input
        objects = find_objects(input_grid)
        objects_above_5 = [obj for obj in objects if obj['initial_position'][0] < min(5, input_grid.shape[0])]
        objects_below_5 = [obj for obj in objects if obj['initial_position'][0] >= min(5, input_grid.shape[0])]

        analysis[f'example_{i+1}'] = {
            'row5_nonzero': row5_nonzero,
            'num_objects_above_5': len(objects_above_5),
            'num_objects_below_5': len(objects_below_5),
        }
    return analysis


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
                    'shape': 'contiguous' # for this task all objects are contiguous
                })
    return objects

results = [
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
        "expected_output": [
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
        "transformed_output": [
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
        ],
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
        "expected_output": [
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
        "transformed_output": [
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
        ],
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
        "expected_output": [
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
        "transformed_output": [
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
        ],
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
        "expected_output": [
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
        "transformed_output": [
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
        ],
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
        "expected_output": [
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
        "transformed_output": [
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
        ],
    },
]

analysis = analyze_results(results)
print(analysis)

```

*code_execution_result:*
outcome: 1
```
{'example_1': {'row5_nonzero': np.True_, 'num_objects_above_5': 3, 'num_objects_below_5': 7}, 'example_2': {'row5_nonzero': np.True_, 'num_objects_above_5': 4, 'num_objects_below_5': 9}, 'example_3': {'row5_nonzero': np.True_, 'num_objects_above_5': 4, 'num_objects_below_5': 9}, 'example_4': {'row5_nonzero': np.True_, 'num_objects_above_5': 3, 'num_objects_below_5': 7}, 'example_5': {'row5_nonzero': np.True_, 'num_objects_above_5': 3, 'num_objects_below_5': 7}}

```
**YAML Facts:**


```yaml
task: 'conditional_object_manipulation'
description: 'Manipulate objects based on the content of Row 5.'
examples:
  - example_1:
      row5_nonzero: True
      objects_above_5_count: 3 # Objects with top-left corner above row 5
      objects_below_5_count: 7 # Objects with top-left corner at or below row 5.
      action: 'remove_above' # Remove objects entirely above Row 5
  - example_2:
      row5_nonzero: True
      objects_above_5_count: 4
      objects_below_5_count: 9
      action: 'remove_above'
  - example_3:
    row5_nonzero: True
    objects_above_5_count: 4
    objects_below_5_count: 9
    action: 'remove_above'
  - example_4:
    row5_nonzero: True
    objects_above_5_count: 3
    objects_below_5_count: 7
    action: 'remove_above'
  - example_5:
    row5_nonzero: True
    objects_above_5_count: 3
    objects_below_5_count: 7
    action: 'remove_above'
objects:
  - definition: 'contiguous region of non-zero pixels'
  - properties:
      color: 'integer value (0-9)'
      position: 'top-left corner coordinates (row, col)'
      shape: 'contiguous block'
actions:
  - remove_above:
    condition: 'Row 5 contains any non-zero pixels.'
    operation: 'Remove all objects located entirely *above* Row 5.'
  - duplicate_and_shift:
    condition: 'row 5 is all zeros'
    operation: copy all objects from above row 5 down to row 5 and below until row 5 has
      non-zero entries
  - reposition_below:
      condition: always
      operation: 'place objects that were originally at or below row 5 in the first available
       empty space in the output grid. Do not break objects.'
```


**Natural Language Program:**

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

