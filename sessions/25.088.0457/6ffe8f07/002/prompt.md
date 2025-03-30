
Previous Code:
```python
import numpy as np
from collections import deque

"""
Identify all white (0) pixels directly adjacent (horizontally or vertically) 
to any azure (8) pixel in the input grid. Starting from these adjacent white 
pixels, perform a flood fill using yellow (4). The fill should only spread 
into other white (0) pixels and stop at the grid boundaries or any non-white 
pixel (including the original azure pixels and any other colored objects). 
All original non-white pixels retain their color.
"""

def transform(input_grid):
    """
    Performs a flood fill operation starting from white neighbors of azure pixels.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    
    # Convert input list of lists to numpy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input_grid
    output_grid = np.copy(input_grid_np)
    rows, cols = output_grid.shape

    # Define colors
    WHITE = 0
    AZURE = 8
    YELLOW = 4

    # Queue for Breadth-First Search (BFS) flood fill
    queue = deque()
    # Set to keep track of visited pixels to avoid redundant processing
    visited = set()

    # Find initial white neighbors of azure pixels
    for r in range(rows):
        for c in range(cols):
            if input_grid_np[r, c] == AZURE:
                # Check direct neighbors (up, down, left, right)
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    # Check if neighbor is within bounds
                    if 0 <= nr < rows and 0 <= nc < cols:
                        # Check if neighbor is white in the original grid
                        if input_grid_np[nr, nc] == WHITE:
                            # Check if this starting point hasn't been added yet
                            if (nr, nc) not in visited:
                                # Add to queue and visited set
                                queue.append((nr, nc))
                                visited.add((nr, nc))
                                # Immediately color the starting pixel yellow in the output
                                output_grid[nr, nc] = YELLOW 
                                
    # Perform flood fill starting from the initial neighbors
    while queue:
        r, c = queue.popleft()

        # Explore neighbors of the current pixel
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if neighbor is within bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if the neighbor is white in the *original* grid 
                # (or equivalently, if it hasn't been colored yellow yet in the output grid)
                # and hasn't been visited yet
                if output_grid[nr, nc] == WHITE and (nr, nc) not in visited:
                    # Color the neighbor yellow
                    output_grid[nr, nc] = YELLOW
                    # Add to visited set
                    visited.add((nr, nc))
                    # Add to queue for further exploration
                    queue.append((nr, nc))

    # Return the modified grid
    return output_grid.tolist() # Convert back to list of lists if required by the environment
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0
0 0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 8 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 8 8 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 8 8 0 0 0 2 2 2 2 2 2
0 0 0 0 0 0 8 8 8 8 0 0 0 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 2 2 2 4 4 4 4 2 2 2 2 2 2 0 0 0
0 0 0 2 2 2 4 4 4 4 2 2 2 2 2 2 0 0 0
0 0 0 2 2 2 4 4 4 4 2 2 2 2 2 2 0 0 0
0 0 0 0 0 0 4 4 4 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 4 4 4 4 0 0 0 0 0 0 0 0 0
4 4 4 4 4 4 8 8 8 8 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 8 8 8 8 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 8 8 8 8 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 8 8 8 8 4 4 4 4 4 4 4 4 4
0 0 0 0 0 0 4 4 4 4 0 0 0 2 2 2 2 2 2
0 0 0 0 0 0 4 4 4 4 0 0 0 2 2 2 2 2 2
0 0 0 0 0 0 4 4 4 4 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 4 4 4 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 4 4 4 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 4 4 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 4 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 4 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 4 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 4 4 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
4 4 4 2 2 2 2 2 2 2 2 2 2 2 2 2 4 4 4
4 4 4 2 2 2 2 2 2 2 2 2 2 2 2 2 4 4 4
4 4 4 2 2 2 2 2 2 2 2 2 2 2 2 2 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 8 8 8 8 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 8 8 8 8 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 8 8 8 8 4 4 4 2 2 2 2 2 2
4 4 4 4 4 4 8 8 8 8 4 4 4 2 2 2 2 2 2
4 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 2
4 4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 2
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 1 1 1 1 1 4 4 4 4 4 4 4 4 4 4 4 4
4 4 1 1 1 1 1 4 4 4 4 4 4 4 4 4 4 4 4
4 4 1 1 1 1 1 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
```
Match: False
Pixels Off: 202
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 111.91135734072022

## Example 2:
Input:
```
0 0 0 0 0 0 1 1 1 0 2 2 2 2 2 0 0 0 0
0 2 2 2 2 0 1 1 1 0 2 2 2 2 2 0 0 0 0
0 2 2 2 2 0 1 1 1 0 2 2 2 2 2 0 0 0 0
0 2 2 2 2 0 0 0 0 0 2 2 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 0 0 0 0
0 1 1 0 0 0 0 0 0 0 2 2 2 2 2 0 0 0 0
0 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 8 8 8 8 0 0 0 0 0 0 0 0
0 0 0 0 0 8 8 8 8 8 8 0 0 0 0 2 2 2 2
2 2 2 2 0 8 8 8 8 8 8 0 0 0 0 2 2 2 2
2 2 2 2 0 8 8 8 8 8 8 0 0 0 0 2 2 2 2
2 2 2 2 0 8 8 8 8 8 8 0 0 0 0 0 0 0 0
2 2 2 2 0 8 8 8 8 8 8 0 2 2 0 0 0 0 0
0 0 0 0 0 8 8 8 8 8 8 0 2 2 0 0 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 2 2 0 0 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1
0 0 0 0 2 2 2 2 2 0 1 1 1 1 0 0 0 0 0
0 0 0 0 2 2 2 2 2 0 1 1 1 1 0 0 0 0 0
0 0 0 0 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 4 1 1 1 4 4 2 2 2 2 0 0 0 0
0 2 2 2 2 4 1 1 1 4 4 2 2 2 2 0 0 0 0
0 2 2 2 2 4 1 1 1 4 4 2 2 2 2 0 0 0 0
0 2 2 2 2 4 4 4 4 4 4 2 2 2 2 0 0 0 0
0 0 0 0 0 4 4 4 4 4 4 2 2 2 2 0 0 0 0
0 1 1 0 0 4 4 4 4 4 4 2 2 2 2 0 0 0 0
0 1 1 0 0 4 4 4 4 4 4 0 0 0 0 0 0 0 0
4 4 4 4 4 8 8 8 8 8 8 4 4 4 4 4 4 4 4
4 4 4 4 4 8 8 8 8 8 8 4 4 4 4 4 4 4 4
4 4 4 4 4 8 8 8 8 8 8 4 4 4 4 4 4 4 4
4 4 4 4 4 8 8 8 8 8 8 4 4 4 4 4 4 4 4
4 4 4 4 4 8 8 8 8 8 8 4 4 4 4 4 4 4 4
4 4 4 4 4 8 8 8 8 8 8 4 4 4 4 4 4 4 4
4 4 4 4 4 8 8 8 8 8 8 4 4 4 4 4 1 1 1
0 0 0 0 0 4 4 4 4 4 4 0 2 2 0 0 1 1 1
0 0 0 0 0 4 4 4 4 4 4 0 0 0 0 0 1 1 1
0 0 0 0 2 4 4 4 4 4 1 1 1 1 0 0 0 0 0
0 0 0 0 2 4 4 4 4 4 1 1 1 1 0 0 0 0 0
0 0 0 0 2 4 4 4 4 4 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
4 4 4 4 4 4 1 1 1 4 2 2 2 2 2 4 4 4 4
4 2 2 2 2 4 1 1 1 4 2 2 2 2 2 4 4 4 4
4 2 2 2 2 4 1 1 1 4 2 2 2 2 2 4 4 4 4
4 2 2 2 2 4 4 4 4 4 2 2 2 2 2 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 4 4 4 4
4 1 1 4 4 4 4 4 4 4 2 2 2 2 2 4 4 4 4
4 1 1 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 8 8 8 8 8 8 4 4 4 4 4 4 4 4
4 4 4 4 4 8 8 8 8 8 8 4 4 4 4 2 2 2 2
2 2 2 2 4 8 8 8 8 8 8 4 4 4 4 2 2 2 2
2 2 2 2 4 8 8 8 8 8 8 4 4 4 4 2 2 2 2
2 2 2 2 4 8 8 8 8 8 8 4 4 4 4 4 4 4 4
2 2 2 2 4 8 8 8 8 8 8 4 2 2 4 4 4 4 4
4 4 4 4 4 8 8 8 8 8 8 4 2 2 4 4 1 1 1
4 4 4 4 4 4 4 4 4 4 4 4 2 2 4 4 1 1 1
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 1 1 1
4 4 4 4 2 2 2 2 2 4 1 1 1 1 4 4 4 4 4
4 4 4 4 2 2 2 2 2 4 1 1 1 1 4 4 4 4 4
4 4 4 4 2 2 2 2 2 4 4 4 4 4 4 4 4 4 4
```
Match: False
Pixels Off: 150
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 83.10249307479225

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 0 0 1 1 1 1 1 1 1 1 1
0 1 1 1 0 2 2 2 0 0 1 1 1 1 1 1 1 1 1
0 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 8 8 8 8 8 8 8 0 0 0 0 0 0
0 1 1 1 0 0 8 8 8 8 8 8 8 0 0 0 0 0 0
0 0 0 0 0 0 8 8 8 8 8 8 8 0 0 0 0 0 0
0 0 0 0 0 0 8 8 8 8 8 8 8 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0
0 0 0 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 0
0 0 2 2 2 2 2 2 2 0 0 0 2 2 2 2 2 2 0
0 0 2 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 4 4 4 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 4 4 4 4 1 1 1 1 1 1 1 1 1
0 1 1 1 0 2 4 4 4 4 1 1 1 1 1 1 1 1 1
0 1 1 1 0 0 4 4 4 4 4 4 4 0 0 0 0 0 0
0 1 1 1 0 0 4 4 4 4 4 4 4 0 0 0 0 0 0
0 1 1 1 4 4 8 8 8 8 8 8 8 4 4 4 4 4 4
0 1 1 1 4 4 8 8 8 8 8 8 8 4 4 4 4 4 4
4 4 4 4 4 4 8 8 8 8 8 8 8 4 4 4 4 4 4
4 4 4 4 4 4 8 8 8 8 8 8 8 4 4 4 4 4 4
0 0 0 0 0 0 4 4 4 4 4 4 4 0 0 0 0 0 0
0 0 0 1 1 1 1 1 1 1 4 4 4 0 0 0 0 0 0
0 0 0 1 1 1 1 1 1 1 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 4 4 4 2 2 2 2 2 0
0 0 0 0 0 0 0 0 0 0 4 4 4 2 2 2 2 2 0
0 0 2 2 2 2 2 2 2 0 4 4 4 2 2 2 2 2 0
0 0 2 2 2 2 2 2 2 0 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 4 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 4 4 4 0 0 0 0 0 0
```
Transformed Output:
```
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 2 2 2 4 4 1 1 1 1 1 1 1 1 1
4 1 1 1 4 2 2 2 4 4 1 1 1 1 1 1 1 1 1
4 1 1 1 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 1 1 1 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 1 1 1 4 4 8 8 8 8 8 8 8 4 4 4 4 4 4
4 1 1 1 4 4 8 8 8 8 8 8 8 4 4 4 4 4 4
4 4 4 4 4 4 8 8 8 8 8 8 8 4 4 4 4 4 4
4 4 4 4 4 4 8 8 8 8 8 8 8 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 1 1 1 1 1 1 1 4 4 4 4 4 4 4 4 4
4 4 4 1 1 1 1 1 1 1 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 2 4
4 4 4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 2 4
4 4 2 2 2 2 2 2 2 4 4 4 2 2 2 2 2 2 4
4 4 2 2 2 2 2 2 2 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
```
Match: False
Pixels Off: 162
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 89.75069252077563

## Example 4:
Input:
```
0 0 0 1 1 1 0 2 2 2 2 2 0 0 0 0 0 0
0 0 0 1 1 1 0 2 2 2 2 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 2 2 0 0 0 0 0
1 1 0 0 0 0 0 0 0 0 2 2 2 0 0 0 0 0
1 1 0 0 0 0 0 0 0 0 2 2 2 0 0 0 0 0
1 1 0 0 8 8 8 8 0 0 0 0 0 0 0 0 0 0
1 1 0 0 8 8 8 8 0 0 0 0 0 0 0 0 0 0
1 1 0 0 8 8 8 8 0 0 0 0 0 1 1 1 0 0
0 0 0 0 8 8 8 8 0 0 0 0 0 1 1 1 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 0 0
0 0 0 0 0 0 2 2 2 0 0 0 0 1 1 1 0 0
0 0 0 0 0 0 2 2 2 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 2 2 2 2 2 0 0 0
0 2 2 2 0 0 0 0 0 0 2 2 2 2 2 0 0 0
0 2 2 2 0 0 1 1 0 0 2 2 2 2 2 0 0 0
0 2 2 2 0 0 1 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 1 1 1 4 4 2 2 2 2 0 0 0 0 0 0
0 0 0 1 1 1 4 4 2 2 2 2 0 0 0 0 0 0
0 0 0 0 4 4 4 4 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 4 4 0 0 2 2 2 0 0 0 0 0
1 1 0 0 4 4 4 4 0 0 2 2 2 0 0 0 0 0
1 1 0 0 4 4 4 4 0 0 2 2 2 0 0 0 0 0
1 1 4 4 8 8 8 8 4 4 4 4 4 4 4 4 4 4
1 1 4 4 8 8 8 8 4 4 4 4 4 4 4 4 4 4
1 1 4 4 8 8 8 8 4 4 4 4 4 1 1 1 0 0
4 4 4 4 8 8 8 8 4 4 4 4 4 1 1 1 0 0
0 0 0 0 4 4 4 4 0 0 0 0 0 1 1 1 0 0
0 0 0 0 4 4 4 4 2 0 0 0 0 1 1 1 0 0
0 0 0 0 4 4 4 4 2 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 4 4 0 0 2 2 2 2 2 0 0 0
0 2 2 2 4 4 4 4 0 0 2 2 2 2 2 0 0 0
0 2 2 2 4 4 1 1 0 0 2 2 2 2 2 0 0 0
0 2 2 2 4 4 1 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
4 4 4 1 1 1 4 2 2 2 2 2 4 4 4 4 4 4
4 4 4 1 1 1 4 2 2 2 2 2 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 2 2 4 4 4 4 4
1 1 4 4 4 4 4 4 4 4 2 2 2 4 4 4 4 4
1 1 4 4 4 4 4 4 4 4 2 2 2 4 4 4 4 4
1 1 4 4 8 8 8 8 4 4 4 4 4 4 4 4 4 4
1 1 4 4 8 8 8 8 4 4 4 4 4 4 4 4 4 4
1 1 4 4 8 8 8 8 4 4 4 4 4 1 1 1 4 4
4 4 4 4 8 8 8 8 4 4 4 4 4 1 1 1 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 1 1 1 4 4
4 4 4 4 4 4 2 2 2 4 4 4 4 1 1 1 4 4
4 4 4 4 4 4 2 2 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 4 4 4
4 2 2 2 4 4 4 4 4 4 2 2 2 2 2 4 4 4
4 2 2 2 4 4 1 1 4 4 2 2 2 2 2 4 4 4
4 2 2 2 4 4 1 1 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
```
Match: False
Pixels Off: 169
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 98.83040935672514
