
Previous Code:
```python
"""
1.  **Iterate** through the input grid's rows, top to bottom.
2.  **Identify** if each row contains only black pixels or contains at least one non-black pixel.
3.  **Store** the non-black rows in a list.
4.  **Reverse** the order of the stored list of non-black rows.
5.  Create a new empty result grid.
6.  **Iterate** through the original grid's row *indices*.
7.  For current index `i`:
    - If row `i` of original grid was black, add it to result grid.
    - If row `i` of original grid was non-black, add the next element of the reversed non-black-row list to result grid.
"""

import numpy as np

def transform(input_grid):
    input_grid = np.array(input_grid)
    non_black_rows = []
    original_row_types = []  # True for black row, False for non-black row

    # 1. Iterate and Identify row types
    for row in input_grid:
        if np.all(row == 0):
            original_row_types.append(True)
        else:
            original_row_types.append(False)
            non_black_rows.append(row)

    # 2. Reverse Non-Black Rows
    non_black_rows.reverse()

    # 3. Construct Output with original black row positions
    output_grid = []
    non_black_row_index = 0
    for is_black_row in original_row_types:
        if is_black_row:
            output_grid.append(input_grid[len(output_grid)]) #get the original black row
        else:
            output_grid.append(non_black_rows[non_black_row_index])
            non_black_row_index += 1

    return np.array(output_grid).tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
2 2 2 2 2
8 8 8 8 8
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```
Expected Output:
```
2 2 2 2 2
8 8 8 8 8
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
8 8 8 8 8
2 2 2 2 2
```
Transformed Output:
```
8 8 8 8 8
2 2 2 2 2
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
```
Match: False
Pixels Off: 20
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 80.0

## Example 2:
Input:
```
2 2 2
2 2 2
3 3 3
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
```
Expected Output:
```
2 2 2
2 2 2
3 3 3
0 0 0
0 0 0
0 0 0
0 0 0
3 3 3
2 2 2
2 2 2
```
Transformed Output:
```
3 3 3
2 2 2
2 2 2
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
```
Match: False
Pixels Off: 15
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 100.0
