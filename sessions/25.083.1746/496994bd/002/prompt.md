
Previous Code:
```python
"""
The transformation rule is as follows:

1. Identify the number of rows from the bottom of the input grid that contain non-black (non-zero) colors.
2. Separate the input grid into two groups: the top rows (which may include black rows) and the identified bottom rows.
3. Move the identified bottom rows to the bottom of the output.
4. Reverse the order of these moved rows.
5. Combine the unmoved top rows and the reversed bottom rows to form the output grid.
"""

import numpy as np

def get_bottom_segment(input_grid):
    """
    Helper Function:
    Identify segment by first looking all the way up-down 
    and keep appending rows when color of the row is not black
    """
    bottom_segment = []
    for row in reversed(input_grid):
        if np.any(row != 0):
            bottom_segment.append(row)
        else:
          break    
    return bottom_segment

def transform(input_grid):
    # Convert to numpy array for easier manipulation
    input_grid = np.array(input_grid)

    # 1 & 2: Separate the input grid
    bottom_segment = get_bottom_segment(input_grid)    
    n_bottom = len(bottom_segment)
    top_segment = input_grid[:-n_bottom] if n_bottom > 0 else input_grid

    # 3. Move the identified bottom rows, 4.Reverse bottom segment
    reversed_bottom_segment = bottom_segment[::-1]

    # 5: Combine
    if len(reversed_bottom_segment) > 0 :
      output_grid = np.vstack((top_segment, reversed_bottom_segment))
    else:
      output_grid = top_segment

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
Match: False
Pixels Off: 9
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 60.0
