
Previous Code:
```python
"""
Extracts non-zero pixels from the input grid, sorts them based on their original
positions (first by row, then by column), and arranges them into a new,
smaller output grid in row-major order.
"""

import numpy as np

def get_non_zero_pixels(grid):
    """Extracts non-zero pixels with their coordinates."""
    non_zero_pixels = []
    for row_index, row in enumerate(grid):
        for col_index, value in enumerate(row):
            if value != 0:
                non_zero_pixels.append(((row_index, col_index), value))
    return non_zero_pixels

def sort_pixels(pixels):
    """Sorts pixels first by row (ascending), then by column (ascending)."""
    return sorted(pixels, key=lambda item: (item[0][0], item[0][1]))

def transform(input_grid):
    # Extract non-zero pixels and their original locations.
    non_zero_pixels = get_non_zero_pixels(input_grid)

    # Sort the extracted pixels based on their original row and column.
    sorted_pixels = sort_pixels(non_zero_pixels)

    # if no pixels, return empty array
    if not sorted_pixels:
      return np.array([[0]])

    # Determine output grid dimensions and create an empty output grid.
    values = [p[1] for p in sorted_pixels]

    # calculate the size and shape of the output
    n = len(values)
    cols = int(np.ceil(np.sqrt(n)))
    rows = int(np.ceil(n / cols))

    output_grid = np.zeros((rows, cols), dtype=int)

    # Arrange the sorted pixel values into the output grid in row-major order.
    for i in range(rows):
        for j in range(cols):
            idx = i * cols + j
            if idx < n:
                output_grid[i,j] = values[idx]

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 2
0 0 0 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0
9 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 5 0
0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
9 3 4
5 8 6
2 0 0
```
Transformed Output:
```
4 2 8
6 9 5
3 0 0
```
Match: False
Pixels Off: 7
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 77.77777777777777

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 1 0 0 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
3 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 7 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 9
0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
3 1 8
9 7 6
0 0 0
```
Transformed Output:
```
1 6 3
7 9 8
```
Match: False
Pixels Off: None
Size Correct: False
Color Palette Correct: True
Color Count Correct: False
Score: None

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 3
0 0 5 0 0 9 0 0 0 0
0 0 0 0 0 0 0 0 1 0
0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
2 4 5
1 9 3
5 1 3
```
Transformed Output:
```
3 5 9
1 4 5
3 2 1
```
Match: False
Pixels Off: 8
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 88.88888888888889
