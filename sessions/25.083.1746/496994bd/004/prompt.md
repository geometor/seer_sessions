
Previous Code:
```python
"""
1.  **Identify Non-Black Rows:** Scan the entire input grid and identify all rows that contain at least one pixel that is *not* black (value not equal to 0).
2.  **Keep Track of Black Rows and Their Original Order:** Make not of the rows that contain only black (value equal to 0), and keep their top-down ordering.
3.  **Reverse Non-Black Rows:** Reverse the order of the identified non-black rows.
4.  **Construct Output:** Create the output grid by first placing the all-black rows in their original order, and stacking the reversed non-black rows at the bottom.
"""

import numpy as np

def transform(input_grid):
    # Convert to numpy array for easier manipulation
    input_grid = np.array(input_grid)

    # 1. Identify Non-Black Rows
    non_black_rows = []
    black_rows = []
    for i, row in enumerate(input_grid):
        if np.any(row != 0):
            non_black_rows.append(row)
        else:
          black_rows.append(row)

    # 2. Reverse Non-Black Rows
    non_black_rows.reverse()

    # 3. Construct Output
    output_grid = np.vstack(black_rows + non_black_rows) if len(black_rows) + len(non_black_rows) > 0 else input_grid

    return output_grid.tolist()
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
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
8 8 8 8 8
2 2 2 2 2
```
Match: False
Pixels Off: 10
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 40.0

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
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
0 0 0
3 3 3
2 2 2
2 2 2
```
Match: False
Pixels Off: 9
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 60.0
