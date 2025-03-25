
Previous Code:
```python
"""
The transformation rule involves rearranging colored blocks within the input grid. Each column is processed independently.
Within each column, contiguous blocks of the same non-zero color are moved downwards, stacking them at the bottom of the grid.
The relative horizontal order of blocks across columns, as well as their sizes, are preserved. The color 0 acts as empty space.
"""

import numpy as np

def get_objects_per_column(grid):
    """
    Identifies contiguous blocks of non-zero colors within each column.
    Returns a list of lists, where each sublist represents a column and contains the objects found in that column.
    Objects in the list are represented as tuples: ((row_start, col), value, length)
    """
    columns = []
    num_cols = len(grid[0])
    num_rows = len(grid)

    for col in range(num_cols):
        current_column_objects = []
        start_row = None
        current_color = 0
        for row in range(num_rows):
            if grid[row][col] != 0:  # Non-zero color
                if start_row is None:  # Start of a new object
                    start_row = row
                    current_color = grid[row][col]
                elif grid[row][col] != current_color:
                    # append previous
                    current_column_objects.append(
                        ((start_row, col), current_color, row - start_row)
                    )
                    # Start of a new object
                    start_row = row
                    current_color = grid[row][col]
            elif start_row is not None:  # End of an object
                current_column_objects.append(
                    ((start_row, col), current_color, row - start_row)
                )
                start_row = None
                current_color = 0
        # Check for object at the end of the column
        if start_row is not None:
            current_column_objects.append(
                ((start_row, col), current_color, num_rows - start_row)
            )
        columns.append(current_column_objects)
    return columns
def get_objects_per_row(grid):
    rows = []
    num_cols = len(grid[0])
    num_rows = len(grid)

    for row in range(num_rows):
        current_row_objects = []
        start_col = None
        current_color = 0
        for col in range(num_cols):
            if grid[row][col] != 0:
                if start_col is None:
                    start_col = col
                    current_color = grid[row][col]
                elif grid[row][col] != current_color:
                    current_row_objects.append(
                        ((row, start_col), current_color, col - start_col)
                    )
                    start_col = col
                    current_color = grid[row][col]
            elif start_col is not None:
                current_row_objects.append(
                    ((row, start_col), current_color, col - start_col)
                )
                start_col = None
                current_color = 0

        if start_col is not None:
            current_row_objects.append(
                ((row, start_col), current_color, num_cols-start_col)
            )
        rows.append(current_row_objects)
    return rows

def get_adjacent_objects(input_grid, col_objects, row_objects):
    adjacent_objects_list = []
    num_rows = len(input_grid)
    num_cols = len(input_grid[0])
    processed = set()

    for col_obj_list in col_objects:
        for col_obj in col_obj_list:
            obj_id = (col_obj[0][0], col_obj[0][1], col_obj[1])  # (row, col, color)
            if obj_id in processed:
                continue
            
            adjacent_objects = []
            q = [col_obj]
            
            while q:
                curr = q.pop(0)
                obj_id = (curr[0][0], curr[0][1], curr[1])
                if obj_id in processed:
                    continue
                processed.add(obj_id)
                adjacent_objects.append(curr)                
                
                (r, c), val, l = curr
                
                # Find neighbors in column
                for neighbor_col_obj_list in col_objects:
                    for neighbor_col_obj in neighbor_col_obj_list:
                        (nr, nc), nval, nl = neighbor_col_obj
                        if nval == val and nc == c and (nr < r and nr + nl == r or nr == r + l):
                            q.append(neighbor_col_obj)

                # Find neighbors in row
                for neighbor_row_obj_list in row_objects:
                    for neighbor_row_obj in neighbor_row_obj_list:
                        (nr, nc), nval, nl = neighbor_row_obj
                        if nval == val and nr == r:  # Same row
                           if (nc < c and nc+nl==c) or (nc == c + 1):
                                for neighbor_col_obj_list in col_objects:
                                    for neighbor_col_obj in neighbor_col_obj_list:
                                        (nr2, nc2), nval2, nl2 = neighbor_col_obj
                                        if nr2 == nr and nc2 == nc and nval2==val:
                                            q.append(neighbor_col_obj)


            adjacent_objects_list.append(adjacent_objects)

    return adjacent_objects_list

def transform(input_grid):
    """
    Transforms the input grid by moving contiguous blocks of non-zero colors downwards within each column.
    """
    input_grid = np.array(input_grid)
    num_rows = len(input_grid)
    num_cols = len(input_grid[0])
    output_grid = np.zeros_like(input_grid)

    col_objects = get_objects_per_column(input_grid)
    row_objects = get_objects_per_row(input_grid)

    adjacent_objects_list = get_adjacent_objects(input_grid, col_objects, row_objects)

    for objects in adjacent_objects_list:
        current_row = num_rows
        for obj in reversed(objects):
            (r,c), val, l = obj
            current_row -= l
            for i in range(l):
                output_grid[current_row + i][c] = val

    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
2 0 0 3 3 0 0 4 4 0 0
2 0 0 0 0 5 0 0 0 0 0
2 0 0 0 0 5 0 0 6 6 0
2 0 0 0 0 0 0 8 0 0 0
2 0 7 7 0 0 0 8 0 0 0
```
Expected Output:
```
2 3 3 4 4 0 0 0 0 0 0
2 5 0 0 0 0 0 0 0 0 0
2 5 6 6 0 0 0 0 0 0 0
2 0 0 8 0 0 0 0 0 0 0
2 7 7 8 0 0 0 0 0 0 0
```
Transformed Output:
```
2 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 5 0 8 0 0 0
2 0 7 7 3 5 0 8 6 6 0
```
Match: False
Pixels Off: 18
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 65.45454545454547

## Example 2:
Input:
```
0 0 0 0 8 8
3 0 0 4 0 0
3 0 0 4 0 0
0 0 0 0 0 6
1 1 0 0 0 6
0 0 0 0 0 0
0 0 5 5 0 0
0 0 0 0 0 0
0 0 0 0 0 0
2 2 2 2 2 2
```
Expected Output:
```
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
3 0 0 4 8 8
3 0 0 4 0 6
1 1 5 5 0 6
2 2 2 2 2 2
```
Transformed Output:
```
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
0 0 0 0 0 0
3 0 0 4 0 6
2 2 2 2 2 2
```
Match: False
Pixels Off: 11
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 36.66666666666666

## Example 3:
Input:
```
0 4 4 0 0 0 0 0 0 2
0 0 0 5 5 0 0 6 0 2
0 0 0 0 0 0 0 6 0 2
0 9 0 0 8 8 0 0 0 2
0 9 0 0 0 0 0 0 0 2
```
Expected Output:
```
0 0 0 0 0 0 0 4 4 2
0 0 0 0 0 0 5 5 6 2
0 0 0 0 0 0 0 0 6 2
0 0 0 0 0 0 9 8 8 2
0 0 0 0 0 0 9 0 0 2
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 2
0 0 0 0 0 0 0 0 0 2
0 9 0 0 0 0 0 6 0 2
0 9 4 5 8 8 0 6 0 2
```
Match: False
Pixels Off: 17
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 68.0
