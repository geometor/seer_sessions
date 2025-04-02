
Previous Code:
```python
import numpy as np
from collections import deque

"""
Transformation Rule Description:

1. Identify the background color, which is orange (7).
2. Find all non-background pixels (any color other than 7) that are located on the grid's border (top/bottom row, left/right column).
3. Starting from these border non-background pixels, perform a search (e.g., Breadth-First Search or Depth-First Search) to identify all other non-background pixels that are connected to them through a path of adjacent (including diagonals) non-background pixels. Mark these reachable pixels as "border-connected".
4. Create the output grid by initially copying the input grid.
5. Iterate through every pixel in the input grid. If a pixel is non-background AND it was *not* marked as "border-connected" in step 3, change its color in the output grid to the background color (orange, 7).
6. Pixels that were originally the background color or were non-background but marked as "border-connected" retain their original color in the output grid.
7. Return the modified output grid.

Essentially, the transformation preserves non-background pixels (and shapes formed by them) that touch or are connected to the grid's border, while removing (filling with background color) any non-background pixels or shapes completely surrounded by the background color.
"""

def transform(input_grid):
    """
    Transforms the input grid by removing non-background pixels that are not connected 
    to the grid border via a path of other non-background pixels.

    Args:
        input_grid (list of list of int): The input grid.

    Returns:
        list of list of int: The transformed output grid.
    """
    # Convert input to numpy array for efficient operations
    input_np = np.array(input_grid, dtype=int)
    output_np = np.copy(input_np)
    H, W = input_np.shape
    bg_color = 7

    # Set to store coordinates of non-background pixels connected to the border
    connected_pixels = set()
    # Queue for BFS
    queue = deque()

    # Initialize the search with non-background pixels on the border
    for r in range(H):
        for c in range(W):
            if r == 0 or r == H - 1 or c == 0 or c == W - 1:
                if input_np[r, c] != bg_color and (r, c) not in connected_pixels:
                    connected_pixels.add((r, c))
                    queue.append((r, c))

    # Perform BFS to find all connected non-background pixels
    while queue:
        r, c = queue.popleft()

        # Check 8 neighbors (including diagonals)
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue # Skip self

                nr, nc = r + dr, c + dc

                # Check boundaries
                if 0 <= nr < H and 0 <= nc < W:
                    # Check if neighbor is non-background and not already visited/connected
                    if input_np[nr, nc] != bg_color and (nr, nc) not in connected_pixels:
                        connected_pixels.add((nr, nc))
                        queue.append((nr, nc))

    # Iterate through the grid and change non-connected non-background pixels to background
    for r in range(H):
        for c in range(W):
            # If a pixel is not background AND it's not in the connected set
            if input_np[r, c] != bg_color and (r, c) not in connected_pixels:
                # Change it to background color in the output grid
                output_np[r, c] = bg_color

    # Convert numpy array back to list of lists
    output_grid = output_np.tolist()
    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
4 7 1 3 7 7 7 9 6 4 7 7 7 7 7 7
7 7 7 3 7 7 7 4 5 9 7 7 0 0 0 7
2 7 7 3 7 7 7 0 0 0 7 7 0 4 0 7
3 3 3 3 7 7 7 0 0 0 7 7 0 0 1 7
7 7 7 7 7 7 7 6 5 0 7 7 0 2 0 7
7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 7
7 7 7 0 0 0 0 9 0 0 5 7 7 7 7 7
7 7 7 0 0 9 0 2 9 0 0 7 7 7 0 0
7 7 7 2 0 0 0 0 0 0 0 7 7 7 1 4
7 7 7 0 0 1 0 4 0 0 8 7 7 7 0 0
7 7 7 7 7 7 7 7 7 7 7 7 7 7 1 0
0 0 0 0 0 0 0 1 7 0 0 0 0 7 0 0
9 5 0 9 0 0 8 6 7 9 0 0 8 7 6 0
0 4 2 6 0 0 0 0 7 0 6 0 5 7 0 0
2 0 0 0 6 0 0 0 7 0 0 0 0 7 0 0
7 7 7 7 7 7 7 7 7 0 2 2 0 7 0 8
```
Expected Output:
```
4 7 1 3 7 7 7 9 6 4 7 7 7 7 7 7
7 7 7 3 7 7 7 4 5 9 7 7 7 7 7 7
2 7 7 3 7 7 7 0 0 0 7 7 7 7 7 7
3 3 3 3 7 7 7 0 0 0 7 7 7 7 7 7
7 7 7 7 7 7 7 6 5 0 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0
7 7 7 7 7 7 7 7 7 7 7 7 7 7 1 4
7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0
7 7 7 7 7 7 7 7 7 7 7 7 7 7 1 0
7 7 7 7 7 7 7 7 7 0 0 0 0 7 0 0
7 7 7 7 7 7 7 7 7 9 0 0 8 7 6 0
7 7 7 7 7 7 7 7 7 0 6 0 5 7 0 0
7 7 7 7 7 7 7 7 7 0 0 0 0 7 0 0
7 7 7 7 7 7 7 7 7 0 2 2 0 7 0 8
```
Transformed Output:
```
4 7 1 3 7 7 7 9 6 4 7 7 7 7 7 7
7 7 7 3 7 7 7 4 5 9 7 7 7 7 7 7
2 7 7 3 7 7 7 0 0 0 7 7 7 7 7 7
3 3 3 3 7 7 7 0 0 0 7 7 7 7 7 7
7 7 7 7 7 7 7 6 5 0 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0
7 7 7 7 7 7 7 7 7 7 7 7 7 7 1 4
7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0
7 7 7 7 7 7 7 7 7 7 7 7 7 7 1 0
0 0 0 0 0 0 0 1 7 0 0 0 0 7 0 0
9 5 0 9 0 0 8 6 7 9 0 0 8 7 6 0
0 4 2 6 0 0 0 0 7 0 6 0 5 7 0 0
2 0 0 0 6 0 0 0 7 0 0 0 0 7 0 0
7 7 7 7 7 7 7 7 7 0 2 2 0 7 0 8
```
Match: False
Pixels Off: 32
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 25.0

## Example 2:
Input:
```
7 9 7 3 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 3 7 7 0 0 0 7 7 7 0 0 0 7
5 7 6 3 7 7 1 0 0 7 7 7 6 0 4 7
3 3 3 3 7 7 0 5 0 7 7 7 0 0 0 7
7 7 7 7 7 7 0 0 0 7 7 7 0 9 0 7
7 7 7 7 7 7 2 0 6 7 7 7 0 0 0 7
7 7 7 7 7 7 0 0 0 7 7 7 0 8 0 7
7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 0 0 0 1 0 0 0 7 7 7 7 7 7 7 7
7 0 0 0 0 0 5 0 7 7 7 7 7 7 7 7
7 0 9 0 8 0 0 0 7 7 7 0 0 0 0 9
7 0 0 0 0 0 4 0 7 7 7 0 6 0 0 0
7 0 2 0 4 0 0 0 7 7 7 0 0 0 0 0
7 7 7 7 7 7 7 7 7 7 7 0 0 5 1 0
7 7 7 7 7 7 7 7 7 7 7 8 0 0 0 0
```
Expected Output:
```
7 9 7 3 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 3 7 7 0 0 0 7 7 7 0 0 0 7
5 7 6 3 7 7 1 0 0 7 7 7 6 0 4 7
3 3 3 3 7 7 0 5 0 7 7 7 0 0 0 7
7 7 7 7 7 7 0 0 0 7 7 7 0 9 0 7
7 7 7 7 7 7 2 0 6 7 7 7 0 0 0 7
7 7 7 7 7 7 0 0 0 7 7 7 0 8 0 7
7 7 7 7 7 7 7 7 7 7 7 7 0 0 0 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 0 0 0 1 0 0 0 7 7 7 7 7 7 7 7
7 0 0 0 0 0 5 0 7 7 7 7 7 7 7 7
7 0 9 0 8 0 0 0 7 7 7 7 7 7 7 7
7 0 0 0 0 0 4 0 7 7 7 7 7 7 7 7
7 0 2 0 4 0 0 0 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
```
Transformed Output:
```
7 9 7 3 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 3 7 7 7 7 7 7 7 7 7 7 7 7
5 7 6 3 7 7 7 7 7 7 7 7 7 7 7 7
3 3 3 3 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 9
7 7 7 7 7 7 7 7 7 7 7 0 6 0 0 0
7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0
7 7 7 7 7 7 7 7 7 7 7 0 0 5 1 0
7 7 7 7 7 7 7 7 7 7 7 8 0 0 0 0
```
Match: False
Pixels Off: 99
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 77.34375

## Example 3:
Input:
```
7 6 7 3 7 7 7 7 7 7 7 7 7 7 7 7
1 7 7 3 7 7 7 0 8 0 0 0 5 0 0 0
7 7 8 3 7 7 7 0 5 0 0 6 0 0 0 0
3 3 3 3 7 7 7 4 0 0 0 0 0 8 0 0
7 7 7 7 7 7 7 9 0 0 6 0 0 0 4 0
7 0 0 0 0 0 7 0 0 0 0 5 9 0 5 0
7 5 2 2 0 0 7 9 0 0 0 0 8 0 0 0
7 0 0 1 0 0 7 1 0 0 2 0 0 0 0 6
7 0 0 5 5 0 7 7 7 7 7 7 7 7 7 7
7 0 0 0 9 0 7 7 7 0 9 0 0 7 7 7
7 0 0 0 6 0 7 7 7 0 0 0 0 7 7 7
7 7 7 7 7 7 7 7 7 8 0 0 0 7 7 7
7 7 6 1 0 0 0 0 7 0 0 0 0 7 0 0
7 7 0 2 0 0 0 0 7 0 0 0 0 7 0 0
7 7 0 8 0 0 0 0 7 7 7 7 7 7 0 0
7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0
```
Expected Output:
```
7 6 7 3 7 7 7 7 7 7 7 7 7 7 7 7
1 7 7 3 7 7 7 7 7 7 7 7 7 7 7 7
7 7 8 3 7 7 7 7 7 7 7 7 7 7 7 7
3 3 3 3 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7
7 5 2 2 0 0 7 7 7 7 7 7 7 7 7 7
7 0 0 1 0 0 7 7 7 7 7 7 7 7 7 7
7 0 0 5 5 0 7 7 7 7 7 7 7 7 7 7
7 0 0 0 9 0 7 7 7 0 9 0 0 7 7 7
7 0 0 0 6 0 7 7 7 0 0 0 0 7 7 7
7 7 7 7 7 7 7 7 7 8 0 0 0 7 7 7
7 7 7 7 7 7 7 7 7 0 0 0 0 7 0 0
7 7 7 7 7 7 7 7 7 0 0 0 0 7 0 0
7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0
7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0
```
Transformed Output:
```
7 6 7 3 7 7 7 7 7 7 7 7 7 7 7 7
1 7 7 3 7 7 7 0 8 0 0 0 5 0 0 0
7 7 8 3 7 7 7 0 5 0 0 6 0 0 0 0
3 3 3 3 7 7 7 4 0 0 0 0 0 8 0 0
7 7 7 7 7 7 7 9 0 0 6 0 0 0 4 0
7 7 7 7 7 7 7 0 0 0 0 5 9 0 5 0
7 7 7 7 7 7 7 9 0 0 0 0 8 0 0 0
7 7 7 7 7 7 7 1 0 0 2 0 0 0 0 6
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0
7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0
7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0
7 7 7 7 7 7 7 7 7 7 7 7 7 7 0 0
```
Match: False
Pixels Off: 113
Size Correct: True
Color Palette Correct: False
Color Count Correct: False
Score: 176.5625
