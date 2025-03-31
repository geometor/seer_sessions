
Previous Code:
```python
"""
Perform a constrained flood fill operation on the input grid.
1. Identify the unique 'fill color' which is not white (0) or azure (8).
2. Identify all pixels with this 'fill color' in the input grid; these are the 'seed points'.
3. Identify all white (0) pixels connected to the grid border without crossing any non-white pixels. Mark these as 'exterior white'.
4. Starting from the seed points, perform a 4-way flood fill on the grid.
5. The fill operation changes white (0) pixels to the 'fill color' *only if* the white pixel is *not* marked as 'exterior white'.
6. The fill stops at the grid boundaries, at pixels with the azure (8) color, and at 'exterior white' pixels.
7. The output grid is the input grid after the constrained flood fill operation.
"""

import numpy as np
from collections import deque

def transform(input_grid):
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    height, width = output_grid.shape

    # --- Find the unique fill color and seed points ---
    fill_color = -1
    seed_points = []
    unique_colors = np.unique(input_grid)

    for color in unique_colors:
        if color != 0 and color != 8: # 0 is white (background), 8 is azure (boundary)
            fill_color = color
            break # Assume only one such color based on problem description

    # If no specific fill color found (grid might be only 0s and 8s), return original
    if fill_color == -1:
        return output_grid

    # Find all initial locations of the fill color
    seed_points = list(zip(*np.where(input_grid == fill_color)))

    # If no seed points found, return original
    if not seed_points:
        return output_grid

    # --- Identify Exterior White Pixels ---
    is_exterior = np.zeros((height, width), dtype=bool)
    exterior_queue = deque()

    # Check border cells
    for r in range(height):
        for c in [0, width - 1]:
             if input_grid[r, c] == 0 and not is_exterior[r, c]:
                is_exterior[r, c] = True
                exterior_queue.append((r, c))
    for c in range(width):
        for r in [0, height - 1]:
             if input_grid[r, c] == 0 and not is_exterior[r, c]:
                is_exterior[r, c] = True
                exterior_queue.append((r, c))

    # BFS for exterior white pixels
    while exterior_queue:
        r, c = exterior_queue.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                if input_grid[nr, nc] == 0 and not is_exterior[nr, nc]:
                    is_exterior[nr, nc] = True
                    exterior_queue.append((nr, nc))

    # --- Perform Constrained Flood Fill (using BFS) ---
    fill_queue = deque(seed_points)
    # Initialize visited with seed points AND all exterior white points
    # We don't want the main fill to process exterior points at all.
    visited = set(seed_points)
    visited.update(zip(*np.where(is_exterior)))

    while fill_queue:
        r, c = fill_queue.popleft()

        # Explore 4-way neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if the neighbor is within bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor hasn't been visited yet
                if (nr, nc) not in visited:
                    # Check if the neighbor is a fillable area:
                    # Must be white (0) in the *output grid* (which starts as input)
                    # AND must NOT be an exterior white cell.
                    if output_grid[nr, nc] == 0 and not is_exterior[nr, nc]:
                        # Change color in the output grid
                        output_grid[nr, nc] = fill_color
                        # Mark as visited
                        visited.add((nr, nc))
                        # Add to queue for further exploration
                        fill_queue.append((nr, nc))
                    else:
                        # If it's not a fillable white cell (e.g., boundary 8, already filled, exterior white)
                        # mark it as visited so we don't check it again from another path.
                        visited.add((nr, nc))


    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0
0 0 8 0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 8 6 6 6 8 0 0 0
0 0 8 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 6 6 6 8 0 0 0
0 0 8 0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 8 6 6 6 8 0 0 0
0 0 8 8 8 8 8 8 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0
0 0 0 0 0 0 8 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 0 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 0 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 0 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 6 6 6 8 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 6 6 6 0 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 6 6 6 8 0 0 0 8 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0
0 0 8 0 0 0 8 6 6 6 8 6 6 6 8 6 6 6 8 6 6 6 8 0 0 0
0 0 8 0 0 0 8 6 6 6 6 6 6 6 6 6 6 6 6 6 6 6 8 0 0 0
0 0 8 0 0 0 8 6 6 6 8 6 6 6 8 6 6 6 8 6 6 6 8 0 0 0
0 0 8 8 8 8 8 8 6 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0
0 0 0 0 0 0 8 6 6 6 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 6 6 6 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 6 6 6 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 6 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 6 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 8 6 6 6 8 6 6 6 8 6 6 6 8 0 0 0 0 0 0 0
0 0 0 0 0 0 8 6 6 6 6 6 6 6 6 6 6 6 8 0 0 0 0 0 0 0
0 0 0 0 0 0 8 6 6 6 8 6 6 6 8 6 6 6 8 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 6 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 6 6 6 8 6 6 6 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 6 6 6 6 6 6 6 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 6 6 6 8 6 6 6 8 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0
0 0 8 0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 8 6 6 6 8 0 0 0
0 0 8 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 6 6 6 8 0 0 0
0 0 8 0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 8 6 6 6 8 0 0 0
0 0 8 8 8 8 8 8 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0
0 0 0 0 0 0 8 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 0 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 0 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 0 8 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 6 6 6 8 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 6 6 6 0 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 8 6 6 6 8 0 0 0 8 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 84
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 29.370629370629388

## Example 2:
Input:
```
0 0 0 8 4 4 4 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 4 4 4 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 4 4 4 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 8 0 8 8 8 8 8 8 0 0 0 0 0 0 8 8 8 8 8 8
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 0 0 0 0 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 8 8 8 8 8 0 8 8 0 0 0 0 0 0 8 8 8 8 8 8
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0 0 0 0 0 8 0
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 8 8 8 8 8 0 8 8 0 0 0 0 0 0 8 8 0 8 8 8
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 8 8 8 8 8 0 8 8 0 0 0 0 0 0 8 8 0 8 8 8
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 0 0 0 0 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 8 0 8 8 8 8 8 8 0 0 0 0 0 0 8 8 0 8 8 8
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 4
0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 4
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 4
0 0 0 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 8 8 8 8 8 8
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 8 8 8 8 8 8
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
```
Expected Output:
```
0 0 0 8 4 4 4 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 4 4 4 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 4 4 4 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 8 4 8 8 8 8 8 8 0 0 0 0 0 0 8 8 8 8 8 8
0 0 0 8 4 4 4 8 4 4 4 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 4 4 4 4 4 4 4 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 4 4 4 8 4 4 4 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 8 8 8 8 8 4 8 8 0 0 0 0 0 0 8 8 8 8 8 8
0 0 0 8 0 0 0 8 4 4 4 8 0 0 0 0 0 0 8 4 4 4 8 0
0 0 0 8 0 0 0 8 4 4 4 8 4 4 4 4 4 4 4 4 4 4 8 0
0 0 0 8 0 0 0 8 4 4 4 8 4 4 4 4 4 4 8 4 4 4 8 0
0 0 0 8 8 8 8 8 8 4 8 8 4 4 4 4 4 4 8 8 4 8 8 8
0 0 0 8 0 0 0 8 4 4 4 8 4 4 4 4 4 4 8 4 4 4 8 0
0 0 0 8 0 0 0 8 4 4 4 8 4 4 4 4 4 4 8 4 4 4 8 0
0 0 0 8 0 0 0 8 4 4 4 8 4 4 4 4 4 4 8 4 4 4 8 0
0 0 0 8 8 8 8 8 8 4 8 8 4 4 4 4 4 4 8 8 4 8 8 8
0 0 0 8 4 4 4 8 4 4 4 8 4 4 4 4 4 4 8 4 4 4 8 0
0 0 0 8 4 4 4 4 4 4 4 8 4 4 4 4 4 4 8 4 4 4 8 0
0 0 0 8 4 4 4 8 4 4 4 8 4 4 4 4 4 4 8 4 4 4 8 0
0 0 0 8 8 4 8 8 8 8 8 8 4 4 4 4 4 4 8 8 4 8 8 8
0 0 0 8 4 4 4 8 4 4 4 8 4 4 4 4 4 4 8 4 4 4 8 4
0 0 0 8 4 4 4 4 4 4 4 4 4 4 4 4 4 4 8 4 4 4 4 4
0 0 0 8 4 4 4 8 4 4 4 8 0 0 0 0 0 0 8 4 4 4 8 4
0 0 0 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 8 8 8 8 8 8
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 8 8 8 8 8 8
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
```
Transformed Output:
```
0 0 0 8 4 4 4 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 4 4 4 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 4 4 4 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 8 0 8 8 8 8 8 8 0 0 0 0 0 0 8 8 8 8 8 8
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 0 0 0 0 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 8 8 8 8 8 0 8 8 0 0 0 0 0 0 8 8 8 8 8 8
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0 0 0 0 0 8 0
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 8 8 8 8 8 0 8 8 0 0 0 0 0 0 8 8 0 8 8 8
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 8 8 8 8 8 0 8 8 0 0 0 0 0 0 8 8 0 8 8 8
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 0 0 0 0 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 8 0 8 8 8 8 8 8 0 0 0 0 0 0 8 8 0 8 8 8
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 4
0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 4
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 4
0 0 0 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 8 8 8 8 8 8
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
0 0 0 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 8 8 8 8 8 8
0 0 0 8 0 0 0 8 0 0 0 8 0 0 0 0 0 0 8 0 0 0 8 0
```
Match: False
Pixels Off: 200
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 57.471264367816076

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 3 3 3 3 3 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 3 3 3 3 3 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 3 3 3 3 3 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 3 3 3 3 3 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 3 3 3 3 3 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 8 8 0 8 8 8 0 0 0 0 8 8 8 8 8 0 0 0 0
0 0 8 0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 8 0 0 0 8 0 0 0 0
0 0 8 0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 8 0 0 0 0
0 0 8 0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 8 0 0 0 8 0 0 0 0
0 0 8 0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 8 8 0 8 8 0 0 0 0
0 0 8 0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 8 3 3 3 8 0 0 0 0
0 0 8 8 8 8 8 8 8 8 8 0 8 8 8 0 0 0 0 8 3 3 3 8 0 0 0 0
0 0 8 0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 8 3 3 3 8 0 0 0 0
0 0 8 0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 8 8 8 8 8 0 0 0 0
0 0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 8 0 0 0 8 0 0 0 0
0 0 8 0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 8 0 0 0 8 0 0 0 0
0 0 8 0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 8 0 0 0 8 0 0 0 0
0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 8 8 8 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 3 3 3 3 3 8 3 3 3 3 3 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 3 3 3 3 3 8 3 3 3 3 3 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 3 3 3 3 3 3 3 3 3 3 3 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 3 3 3 3 3 8 3 3 3 3 3 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 3 3 3 3 3 8 3 3 3 3 3 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 8 8 3 8 8 8 0 0 0 0 8 8 8 8 8 0 0 0 0
0 0 8 0 0 0 0 0 8 3 3 3 3 3 8 0 0 0 0 8 3 3 3 8 0 0 0 0
0 0 8 0 0 0 0 0 8 3 3 3 3 3 8 3 3 3 3 3 3 3 3 8 0 0 0 0
0 0 8 0 0 0 0 0 8 3 3 3 3 3 8 3 3 3 3 8 3 3 3 8 0 0 0 0
0 0 8 0 0 0 0 0 8 3 3 3 3 3 8 3 3 3 3 8 8 3 8 8 0 0 0 0
0 0 8 0 0 0 0 0 8 3 3 3 3 3 8 3 3 3 3 8 3 3 3 8 0 0 0 0
0 0 8 8 8 8 8 8 8 8 8 3 8 8 8 3 3 3 3 8 3 3 3 8 0 0 0 0
0 0 8 0 0 0 0 0 8 3 3 3 3 3 8 3 3 3 3 8 3 3 3 8 0 0 0 0
0 0 8 0 0 0 0 0 8 3 3 3 3 3 8 3 3 3 3 8 8 8 8 8 0 0 0 0
0 0 8 0 0 0 0 0 8 3 3 3 3 3 3 3 3 3 3 8 0 0 0 8 0 0 0 0
0 0 8 0 0 0 0 0 8 3 3 3 3 3 8 0 0 0 0 8 0 0 0 8 0 0 0 0
0 0 8 0 0 0 0 0 8 3 3 3 3 3 8 0 0 0 0 8 0 0 0 8 0 0 0 0
0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 8 8 8 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 3 3 3 3 3 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 3 3 3 3 3 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 3 3 3 3 3 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 3 3 3 3 3 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 3 3 3 3 3 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 8 8 8 0 8 8 8 0 0 0 0 8 8 8 8 8 0 0 0 0
0 0 8 0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 8 0 0 0 8 0 0 0 0
0 0 8 0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 8 0 0 0 0
0 0 8 0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 8 0 0 0 8 0 0 0 0
0 0 8 0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 8 8 0 8 8 0 0 0 0
0 0 8 0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 8 3 3 3 8 0 0 0 0
0 0 8 8 8 8 8 8 8 8 8 0 8 8 8 0 0 0 0 8 3 3 3 8 0 0 0 0
0 0 8 0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 8 3 3 3 8 0 0 0 0
0 0 8 0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 8 8 8 8 8 0 0 0 0
0 0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 8 0 0 0 8 0 0 0 0
0 0 8 0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 8 0 0 0 8 0 0 0 0
0 0 8 0 0 0 0 0 8 0 0 0 0 0 8 0 0 0 0 8 0 0 0 8 0 0 0 0
0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 8 8 8 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 122
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 36.309523809523824
