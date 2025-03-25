
Previous Code:
```python
"""
Moves all green (3) pixels to the last available empty spots before the leftmost azure (8) pixel in their respective row,
provided they are not already adjacent to an azure, and that at least one azure exists in the row.
"""

import numpy as np

def get_indices(grid, value):
    """Helper function to find indices of a specific value in the grid."""
    return np.where(grid == value)

def is_adjacent(grid, row, col, target_value):
    """Helper function to check if a cell is adjacent to a cell with the target_value."""
    rows, cols = grid.shape
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            new_row, new_col = row + dr, col + dc
            if 0 <= new_row < rows and 0 <= new_col < cols and grid[new_row, new_col] == target_value:
                return True
    return False

def transform(input_grid):
    """Transforms the input grid according to the specified rule."""
    output_grid = np.copy(input_grid)
    rows, cols = output_grid.shape

    for row_index in range(rows):
        row = output_grid[row_index]
        threes = np.where(row == 3)[0]
        eights = np.where(row == 8)[0]
        
        # If there are no 3s or 8s in this row, continue
        if threes.size == 0 or eights.size == 0:
            continue

        #Find the leftmost 8
        leftmost_eight_index = eights[0]


        # Find the available 0s before the leftmost 8
        insert_indices = []
        for i in reversed(range(leftmost_eight_index)):
            if row[i] == 0:
              insert_indices.append(i)
            else:
              break #stop at the last string of zeros
        
        insert_indices.reverse() #make indices ascending

        #Move all 3s that are not adjacent to 8
        moved_count = 0
        for three_index in threes:
          adjacent_to_eight = False
          for eight_index in eights:
                if abs(three_index - eight_index) <= 1:
                     adjacent_to_eight = True
          if not adjacent_to_eight:
            if moved_count < len(insert_indices):
                # Remove the 3 from its current position
                output_grid[row_index, three_index] = 0
                output_grid[row_index, insert_indices[moved_count]] = 3
                moved_count +=1

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 8 0 0 8 3
0 8 0 0 8 0 0 3
8 8 0 8 0 0 8 3
8 8 0 0 0 0 0 3
0 0 0 8 8 0 0 8
8 0 0 0 0 0 0 0
0 0 0 8 8 8 0 0
```
Expected Output:
```
0 0 0 8 0 0 8 3
0 8 0 0 8 3 0 0
8 8 0 8 0 0 8 3
8 8 3 0 0 0 0 0
0 0 0 8 8 0 0 8
8 0 0 0 0 0 0 0
0 0 0 8 8 8 0 0
```
Transformed Output:
```
0 0 0 8 0 0 8 3
3 8 0 0 8 0 0 0
8 8 0 8 0 0 8 3
8 8 0 0 0 0 0 3
0 0 0 8 8 0 0 8
8 0 0 0 0 0 0 0
0 0 0 8 8 8 0 0
```
Match: False
Pixels Off: 4
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 7.142857142857139

## Example 2:
Input:
```
0 0 0 8 0 0
0 0 8 0 0 8
8 0 0 0 0 8
0 0 8 0 8 0
0 0 0 0 3 3
8 0 8 0 3 3
0 8 0 8 8 0
```
Expected Output:
```
0 0 0 8 0 0
0 0 8 0 0 8
8 0 0 0 0 8
0 0 8 0 8 0
3 3 0 0 0 0
8 0 8 3 3 0
0 8 0 8 8 0
```
Transformed Output:
```
0 0 0 8 0 0
0 0 8 0 0 8
8 0 0 0 0 8
0 0 8 0 8 0
0 0 0 0 3 3
8 0 8 0 3 3
0 8 0 8 8 0
```
Match: False
Pixels Off: 6
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 14.285714285714292

## Example 3:
Input:
```
0 0 0 0 8 8 8 8
0 0 0 8 0 8 3 3
8 0 0 8 0 0 3 3
8 8 0 0 0 0 3 3
8 8 0 0 8 8 0 8
0 0 0 8 0 8 0 3
0 8 0 0 0 0 0 3
0 0 0 8 8 0 8 3
8 0 0 8 8 8 0 8
```
Expected Output:
```
0 0 0 0 8 8 8 8
0 0 0 8 0 8 3 3
8 0 0 8 3 3 0 0
8 8 3 3 0 0 0 0
8 8 0 0 8 8 0 8
0 0 0 8 0 8 3 0
0 8 3 0 0 0 0 0
0 0 0 8 8 0 8 3
8 0 0 8 8 8 0 8
```
Transformed Output:
```
0 0 0 0 8 8 8 8
3 0 0 8 0 8 3 0
8 0 0 8 0 0 3 3
8 8 0 0 0 0 3 3
8 8 0 0 8 8 0 8
3 0 0 8 0 8 0 0
3 8 0 0 0 0 0 0
0 0 0 8 8 0 8 3
8 0 0 8 8 8 0 8
```
Match: False
Pixels Off: 14
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 19.444444444444443
