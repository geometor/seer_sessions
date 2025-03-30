
Previous Code:
```python
import numpy as np
from typing import List, Tuple

"""
Identify the primary non-black color (C) in the input grid.
Iterate through each pixel of the input grid.
If a pixel has color C:
  Count its orthogonal neighbors (up, down, left, right) that also have color C.
  If the count is exactly 2, change the pixel's color to yellow (4) in the output grid.
  If the count is exactly 3, change the pixel's color to red (2) in the output grid.
Otherwise, keep the original color.
The black background pixels remain unchanged.
"""

def find_primary_color(grid: np.ndarray) -> int:
    """Finds the most frequent non-black color in the grid."""
    colors, counts = np.unique(grid, return_counts=True)
    non_black_indices = np.where(colors != 0)[0]
    if not non_black_indices.size:
        return 0 # Should not happen based on examples, but handle gracefully
    
    # Find the index of the most frequent non-black color
    most_frequent_non_black_index = non_black_indices[np.argmax(counts[non_black_indices])]
    return colors[most_frequent_non_black_index]

def get_orthogonal_neighbors(grid: np.ndarray, r: int, c: int) -> List[Tuple[int, int]]:
    """Gets the coordinates of orthogonal neighbors within grid bounds."""
    neighbors = []
    rows, cols = grid.shape
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    for dr, dc in moves:
        nr, nc = r + dr, c + dc
        if 0 <= nr < rows and 0 <= nc < cols:
            neighbors.append((nr, nc))
    return neighbors

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Transforms the input grid by changing colors of pixels based on their
    orthogonal neighbors count.
    Pixels with 2 same-colored neighbors become yellow (4).
    Pixels with 3 same-colored neighbors become red (2).
    """
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    rows, cols = input_np.shape

    # Find the main color of the shapes
    primary_color = find_primary_color(input_np)
    if primary_color == 0: # No non-black color found
        return output_np.tolist() 

    # Iterate through each pixel of the input grid
    for r in range(rows):
        for c in range(cols):
            # Check if the pixel is of the primary color
            if input_np[r, c] == primary_color:
                neighbor_count = 0
                # Get orthogonal neighbors
                neighbors = get_orthogonal_neighbors(input_np, r, c)
                # Count neighbors with the primary color
                for nr, nc in neighbors:
                    if input_np[nr, nc] == primary_color:
                        neighbor_count += 1

                # Apply transformation rules based on neighbor count
                if neighbor_count == 2:
                    output_np[r, c] = 4 # Yellow
                elif neighbor_count == 3:
                    output_np[r, c] = 2 # Red

    return output_np.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 3 0 0 0 0 0
0 0 3 3 3 0 0 3 0 0 0 0 0
0 0 3 0 0 0 0 3 0 0 0 0 0
0 0 3 0 0 3 3 3 0 0 0 0 0
0 0 3 3 3 3 0 0 0 3 3 3 0
0 0 0 0 0 0 0 0 3 3 0 3 0
0 0 0 0 0 0 0 0 3 0 0 3 0
0 0 0 0 3 3 3 3 3 0 0 3 0
0 0 0 0 3 0 0 0 0 0 0 3 0
0 0 0 0 3 0 0 0 3 3 3 3 0
0 0 0 0 3 3 3 3 3 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 3 3 4 0 0 0 0 0
0 0 4 3 2 0 0 3 0 0 0 0 0
0 0 3 0 0 0 0 3 0 0 0 0 0
0 0 3 0 0 2 3 4 0 0 0 0 0
0 0 4 3 3 4 0 0 0 4 3 4 0
0 0 0 0 0 0 0 0 4 2 0 3 0
0 0 0 0 0 0 0 0 3 0 0 3 0
0 0 0 0 4 3 3 3 2 0 0 3 0
0 0 0 0 3 0 0 0 0 0 0 3 0
0 0 0 0 3 0 0 0 2 3 3 4 0
0 0 0 0 4 3 3 3 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 4 4 0 0 0 0 0
0 0 4 4 4 0 0 4 0 0 0 0 0
0 0 4 0 0 0 0 4 0 0 0 0 0
0 0 4 0 0 4 4 4 0 0 0 0 0
0 0 4 4 4 4 0 0 0 4 4 4 0
0 0 0 0 0 0 0 0 4 4 0 4 0
0 0 0 0 0 0 0 0 4 0 0 4 0
0 0 0 0 4 4 4 4 4 0 0 4 0
0 0 0 0 4 0 0 0 0 0 0 4 0
0 0 0 0 4 0 0 0 4 4 4 4 0
0 0 0 0 4 4 4 4 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 31
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 36.68639053254438

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 0 0 0 0 0 0 0
0 8 0 0 0 0 0 8 0 0 0 0 0 0 0
0 8 8 0 0 0 0 8 0 0 0 0 0 0 0
0 0 8 0 0 0 0 8 0 0 8 8 8 8 8
0 0 8 0 8 8 8 8 0 0 8 0 0 0 8
0 0 8 8 8 0 0 0 0 0 8 8 0 0 8
0 0 0 0 0 0 0 0 0 0 0 8 0 0 8
0 0 0 0 0 0 0 0 0 8 8 8 0 8 8
0 0 8 8 8 0 0 0 0 8 0 0 0 8 0
0 0 8 0 8 0 0 0 0 8 8 8 8 8 0
0 0 8 8 8 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 8 8 8 8 8 4 0 0 0 0 0 0 0
0 8 0 0 0 0 0 8 0 0 0 0 0 0 0
0 4 2 0 0 0 0 8 0 0 0 0 0 0 0
0 0 8 0 0 0 0 8 0 0 4 8 8 8 4
0 0 8 0 2 8 8 4 0 0 8 0 0 0 8
0 0 4 8 4 0 0 0 0 0 4 2 0 0 8
0 0 0 0 0 0 0 0 0 0 0 8 0 0 8
0 0 0 0 0 0 0 0 0 4 8 2 0 2 4
0 0 4 8 4 0 0 0 0 8 0 0 0 8 0
0 0 8 0 8 0 0 0 0 4 8 8 8 4 0
0 0 4 8 4 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 4 4 0 0 0 0 0 0 0
0 4 0 0 0 0 0 4 0 0 0 0 0 0 0
0 4 4 0 0 0 0 4 0 0 0 0 0 0 0
0 0 4 0 0 0 0 4 0 0 4 4 4 4 4
0 0 4 0 4 4 4 4 0 0 4 0 0 0 4
0 0 4 4 4 0 0 0 0 0 4 4 0 0 4
0 0 0 0 0 0 0 0 0 0 0 4 0 0 4
0 0 0 0 0 0 0 0 0 4 4 4 0 4 4
0 0 4 4 4 0 0 0 0 4 0 0 0 4 0
0 0 4 0 4 0 0 0 0 4 4 4 4 4 0
0 0 4 4 4 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 37
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 41.111111111111114

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 1 1 1 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 1 0 0 0 0 0 0 0
0 1 1 1 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 1 0 0 1 1 1 0 0 0 0 0 0 0
0 0 0 1 1 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 1 1 1 0 0
0 0 0 0 0 0 0 0 1 1 1 0 0 1 1 0
0 0 0 1 1 1 1 1 1 0 0 0 0 0 1 0
0 0 0 1 0 0 0 0 0 0 1 1 1 0 1 0
0 0 0 1 1 1 1 1 1 1 1 0 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 1 1 1 1 4 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 2 1 4 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0 1 0 0 0 0 0 0 0
0 4 1 2 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 1 0 0 2 1 4 0 0 0 0 0 0 0
0 0 0 4 1 1 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 4 1 1 4 0 0
0 0 0 0 0 0 0 0 4 1 2 0 0 2 4 0
0 0 0 4 1 1 1 1 2 0 0 0 0 0 1 0
0 0 0 1 0 0 0 0 0 0 2 1 2 0 1 0
0 0 0 4 1 1 1 1 1 1 4 0 4 1 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 4 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 4 4 4 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 4 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 4 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 4 0 0 0 0 0 0 0
0 0 0 4 0 0 4 4 4 0 0 0 0 0 0 0
0 0 0 4 4 4 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 4 4 4 4 0 0
0 0 0 0 0 0 0 0 4 4 4 0 0 4 4 0
0 0 0 4 4 4 4 4 4 0 0 0 0 0 4 0
0 0 0 4 0 0 0 0 0 0 4 4 4 0 4 0
0 0 0 4 4 4 4 4 4 4 4 0 4 4 4 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 42
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 37.5
