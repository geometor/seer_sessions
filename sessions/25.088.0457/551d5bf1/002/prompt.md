
Previous Code:
```python
import numpy as np
from collections import deque

"""
Transformation Rule:
1. Identify areas of white pixels (0) enclosed by blue pixels (1) or the grid boundaries.
2. Fill these enclosed areas with azure pixels (8).
3. Identify "leaks" where an azure pixel (from step 2) is adjacent to a white pixel (0) because a blue pixel is missing from the original enclosing frame.
4. Propagate the azure color outwards from these leak points based on the direction of the leak:
    - Downward leak: Fill the adjacent white pixel and the one directly below it (2 pixels total).
    - Rightward leak: Fill the adjacent white pixel (1 pixel total).
    - Upward leak: Fill the adjacent white pixel and continue filling upwards as long as the pixels are white (0) and within bounds, stopping at the grid edge, a blue pixel (1), or an existing azure pixel (8).
    - Leftward leak: Fill the adjacent white pixel and continue filling leftwards as long as the pixels are white (0) and within bounds, stopping at the grid edge, a blue pixel (1), or an existing azure pixel (8).
"""

def transform(input_grid):
    """
    Applies a fill and leak transformation to the input grid.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    input_array = np.array(input_grid, dtype=int)
    output_grid = input_array.copy()
    rows, cols = input_array.shape
    
    white = 0
    blue = 1
    azure = 8

    # Helper to check if coordinates are within grid bounds
    def is_valid(r, c):
        return 0 <= r < rows and 0 <= c < cols

    # 1. Find enclosed white areas using flood fill from borders
    visited = np.zeros_like(input_array, dtype=bool)
    q = deque()

    # Add all border white cells to the queue
    for r in range(rows):
        for c in [0, cols - 1]:
            if output_grid[r, c] == white and not visited[r, c]:
                visited[r, c] = True
                q.append((r, c))
    for c in range(cols):
        for r in [0, rows - 1]:
            if output_grid[r, c] == white and not visited[r, c]:
                visited[r, c] = True
                q.append((r, c))

    # Perform flood fill for exterior white cells
    while q:
        r, c = q.popleft()
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if is_valid(nr, nc) and output_grid[nr, nc] == white and not visited[nr, nc]:
                visited[nr, nc] = True
                q.append((nr, nc))

    # 2. Fill enclosed white areas (those not visited) with azure
    initial_fill_coords = []
    for r in range(rows):
        for c in range(cols):
            if output_grid[r, c] == white and not visited[r, c]:
                output_grid[r, c] = azure
                initial_fill_coords.append((r, c))

    # 3. & 4. Identify and propagate leaks
    
    # Queues for propagating leaks (up and left need queues)
    up_queue = deque()
    left_queue = deque()
    
    # Lists to store initial targets for fixed-distance leaks (down and right)
    down_targets = []
    right_targets = []

    # Identify initial leak points adjacent to the initially filled azure cells
    for r, c in initial_fill_coords:
        # Check neighbors of initially filled azure pixels
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            if is_valid(nr, nc) and output_grid[nr, nc] == white:
                # Found a white neighbor - potential leak target
                
                # Upward leak potential
                if dr == -1: 
                    up_queue.append((nr, nc))
                # Downward leak potential
                elif dr == 1:
                    down_targets.append((nr, nc))
                # Leftward leak potential
                elif dc == -1:
                    left_queue.append((nr, nc))
                # Rightward leak potential
                elif dc == 1:
                    right_targets.append((nr, nc))

    # Process fixed-distance leaks (Down: 2 cells, Right: 1 cell)
    # Make sure not to overwrite already processed cells by checking for white
    
    # Process Downward leaks (2 steps)
    processed_down = set()
    for r, c in down_targets:
        if (r,c) not in processed_down and output_grid[r,c] == white:
             output_grid[r, c] = azure
             processed_down.add((r,c))
             # Try second step down
             r2 = r + 1
             if is_valid(r2, c) and output_grid[r2, c] == white:
                 if (r2, c) not in processed_down:
                     output_grid[r2, c] = azure
                     processed_down.add((r2, c))

    # Process Rightward leaks (1 step)
    processed_right = set()
    for r, c in right_targets:
         if (r,c) not in processed_right and output_grid[r,c] == white:
            output_grid[r, c] = azure
            processed_right.add((r,c))


    # Process propagating leaks (Up and Left until boundary/obstacle)
    
    # Process Upward leaks
    processed_up = set() # Keep track to avoid redundant processing if queue has duplicates
    while up_queue:
        r, c = up_queue.popleft()
        
        if not is_valid(r, c) or (r, c) in processed_up or output_grid[r, c] != white:
            continue
            
        output_grid[r, c] = azure
        processed_up.add((r, c))
        
        # Add next cell up to the queue for propagation
        nr, nc = r - 1, c
        if is_valid(nr, nc) and output_grid[nr, nc] == white:
             if (nr, nc) not in processed_up:
                up_queue.append((nr, nc))


    # Process Leftward leaks
    processed_left = set() # Keep track
    while left_queue:
        r, c = left_queue.popleft()

        if not is_valid(r, c) or (r, c) in processed_left or output_grid[r, c] != white:
            continue

        output_grid[r, c] = azure
        processed_left.add((r, c))

        # Add next cell left to the queue for propagation
        nr, nc = r, c - 1
        if is_valid(nr, nc) and output_grid[nr, nc] == white:
            if (nr, nc) not in processed_left:
                left_queue.append((nr, nc))

    # Convert back to list of lists for the final output
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 0 0
0 1 0 0 0 0 1 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 1 0 0
0 1 0 0 0 0 1 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0
0 1 0 0 0 0 1 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 1 0 0
0 1 0 0 0 0 1 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 0 0
0 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 1 0 0 0 0 0 0 1 1 1 1 1 1 0 0 0
0 0 1 0 0 0 0 0 0 1 0 0 0 0 0 0 1 0 0 0 0 1 0 0 0
0 0 1 0 0 0 0 0 0 1 0 0 0 0 0 0 1 0 0 0 0 1 0 0 0
0 0 1 0 0 0 0 0 0 1 0 0 0 0 0 0 1 1 1 1 1 1 0 0 0
0 0 1 1 1 0 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 0 0
0 1 8 8 8 8 1 0 0 0 0 0 0 0 0 1 8 8 8 8 8 8 1 0 0
0 1 8 8 8 8 1 0 0 0 0 0 0 0 0 1 8 8 8 8 8 8 8 8 8
0 1 8 8 8 8 1 0 0 0 0 0 0 0 0 1 8 8 8 8 8 8 1 0 0
0 1 8 8 8 8 1 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 0 0
0 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 8 8 8 8 8 1 0 0 0 0 0 0 0 0
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 8 8 8 8 8 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 8 8 8 8 8 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 8 8 8 8 8 8 1 0 0 0 0 0 0 1 1 1 1 1 1 0 0 0
0 0 1 8 8 8 8 8 8 1 0 0 0 0 0 0 1 8 8 8 8 1 0 0 0
0 0 1 8 8 8 8 8 8 1 0 0 0 0 0 0 1 8 8 8 8 1 0 0 0
0 0 1 8 8 8 8 8 8 1 0 0 0 0 0 0 1 1 1 1 1 1 0 0 0
0 0 1 1 1 8 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 1 1 1 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 0 0
0 1 8 8 8 8 1 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 1 0 0
0 1 8 8 8 8 1 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0
0 1 8 8 8 8 1 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 1 0 0
0 1 8 8 8 8 1 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 0 0
0 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 1 0 0 0 0 0 0 1 1 1 1 1 1 0 0 0
0 0 1 0 0 0 0 0 0 1 0 0 0 0 0 0 1 8 8 8 8 1 0 0 0
0 0 1 0 0 0 0 0 0 1 0 0 0 0 0 0 1 8 8 8 8 1 0 0 0
0 0 1 0 0 0 0 0 0 1 0 0 0 0 0 0 1 1 1 1 1 1 0 0 0
0 0 1 1 1 0 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 79
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 26.333333333333343

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 0
0 0 1 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 1 0
0 0 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 0 1 1 1 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0
0 0 0 0 0 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 0 0 0 0 1 0 0 0 0 0 0 0 0 1 1 1 1 1 1 0 0 0
0 0 0 0 0 1 0 0 0 0 1 0 0 0 0 0 0 0 0 1 0 0 0 0 1 0 0 0
0 0 0 0 0 1 1 1 1 1 1 0 0 0 0 0 0 0 0 1 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 1 0 0 0 0 0 0 8 0 0 0 1 1 1 1 1 1 1 1 0
0 0 1 8 8 8 8 8 1 0 0 0 0 0 0 8 0 0 0 1 8 8 8 8 8 8 1 0
8 8 8 8 8 8 8 8 1 0 0 0 0 0 0 8 0 0 0 1 8 8 8 8 8 8 8 8
0 0 1 8 8 8 8 8 1 0 0 0 0 0 0 8 0 0 0 1 8 8 8 8 8 8 1 0
0 0 1 1 1 1 1 1 1 0 0 0 0 0 0 8 0 0 0 1 1 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 8 1 1 1 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 1 8 8 8 8 8 8 8 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 1 8 8 8 8 8 8 8 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 1 8 8 8 8 8 8 8 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 1 8 8 8 8 8 8 8 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 1 8 8 8 8 8 8 8 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0
0 0 0 0 0 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 8 8 8 8 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 8 8 8 8 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 8 8 8 8 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 8 8 8 8 1 0 0 0 0 0 0 0 0 1 1 1 1 1 1 0 0 0
0 0 0 0 0 1 8 8 8 8 1 0 0 0 0 0 0 0 0 1 8 8 8 8 1 0 0 0
0 0 0 0 0 1 1 1 1 1 1 0 0 0 0 0 0 0 0 1 8 8 8 8 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 8 8 8 8 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 0
0 0 1 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 1 0
0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 1 0
0 0 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 0 1 1 1 1 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0
0 0 0 0 0 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 8 8 8 8 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 8 8 8 8 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 8 8 8 8 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 1 8 8 8 8 1 0 0 0 0 0 0 0 0 1 1 1 1 1 1 0 0 0
0 0 0 0 0 1 8 8 8 8 1 0 0 0 0 0 0 0 0 1 8 8 8 8 1 0 0 0
0 0 0 0 0 1 1 1 1 1 1 0 0 0 0 0 0 0 0 1 8 8 8 8 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 8 8 8 8 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 81
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 24.10714285714286
