
Previous Code:
```python
import numpy as np
from collections import deque, Counter

"""
Natural Language Program Description:

1.  Identify the background color (the most common color in the input grid, excluding the boundary color red (2)).
2.  Identify the boundary color (red, color 2).
3.  Identify all other pixels as "seeds", noting their color and location.
4.  Create a copy of the input grid to serve as the output grid.
5.  Create a helper grid (`filled_mask`) of the same dimensions, initially all `False`, to track which pixels are considered "filled" (boundaries, seeds, or already colored by the process). Mark the locations of all boundary pixels (red, 2) and all initial seed pixels as `True` in the `filled_mask`.
6.  Create a list of all identified seeds.
7.  Sort the list of seeds based on a priority rule: first by the lowest color index, then by the lowest row index, and finally by the lowest column index as tie-breakers.
8.  Iterate through the sorted seeds one by one, from highest priority (lowest index values) to lowest.
9.  For the current seed (with color `seed_color` at location `seed_loc`):
    a.  Start a Breadth-First Search (BFS) or Flood Fill originating from `seed_loc`. Use a queue. The queue will store locations to explore *from*.
    b.  While the BFS queue is not empty:
        i.  Get the current location (`current_loc`) from the front of the queue.
        ii. Examine the 4 direct neighbors (`neighbor_loc`) of `current_loc`.
        iii. For each `neighbor_loc` that is within the grid boundaries:
            *   Check if the pixel at `neighbor_loc` in the input grid has the background color AND if `filled_mask[neighbor_loc]` is `False`.
            *   If both conditions are true, it means this is an unfilled background pixel adjacent to the current fill area:
                *   Set the color of the pixel at `neighbor_loc` in the output grid to `seed_color`.
                *   Mark `filled_mask[neighbor_loc]` as `True`.
                *   Add `neighbor_loc` to the BFS queue to continue the fill from there.
10. After iterating through all seeds, the output grid contains the final transformed state. Return the output grid.
"""


def find_background_color(grid: np.ndarray, boundary_color: int) -> int:
    """Finds the most frequent color in the grid, ignoring the boundary color."""
    counts = Counter(grid.flatten())
    if boundary_color in counts:
        del counts[boundary_color] # Don't consider boundary color as background
    if not counts: # Handle edge case of grid with only boundary color
        # Fallback: if no other colors, maybe default to 0 or the most frequent *overall*?
        # Let's pick the most frequent overall if available, else 0.
        overall_counts = Counter(grid.flatten())
        if overall_counts:
            return overall_counts.most_common(1)[0][0]
        else:
            return 0 # Default if grid is empty or truly unusual
    return counts.most_common(1)[0][0]

def bfs_fill(grid: np.ndarray, 
             output_grid: np.ndarray, 
             filled_mask: np.ndarray, 
             start_loc: tuple[int, int], 
             seed_color: int, 
             background_color: int, 
             boundary_color: int):
    """Performs BFS fill starting from neighbors of start_loc."""
    q = deque()
    height, width = grid.shape

    # Initial seeding: Add valid background neighbors of the seed point to the queue
    r_start, c_start = start_loc
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r_start + dr, c_start + dc
        if 0 <= nr < height and 0 <= nc < width:
            neighbor_loc = (nr, nc)
            # Check if neighbor is background and not already filled
            if grid[neighbor_loc] == background_color and not filled_mask[neighbor_loc]:
                 # Fill it immediately
                output_grid[neighbor_loc] = seed_color
                filled_mask[neighbor_loc] = True
                q.append(neighbor_loc) # Add to queue for further exploration

    # Start BFS from the initial neighbors
    while q:
        r, c = q.popleft()

        # Explore neighbors of the current cell
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check bounds
            if 0 <= nr < height and 0 <= nc < width:
                neighbor_loc = (nr, nc)
                # Check if neighbor is background and not already filled
                if grid[neighbor_loc] == background_color and not filled_mask[neighbor_loc]:
                    # Fill the neighbor
                    output_grid[neighbor_loc] = seed_color
                    filled_mask[neighbor_loc] = True
                    q.append(neighbor_loc) # Add to queue

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by performing a competitive flood fill.
    Regions defined by a boundary color (red, 2) are filled based on 
    'seed' pixels within them. Filling prioritizes seeds by color index, 
    then row, then column. The fill expands into the background color pixels.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    output_grid = np.copy(input_np)

    # --- Define constants ---
    boundary_color = 2 

    # --- Identify background color ---
    background_color = find_background_color(input_np, boundary_color)

    # --- Identify seeds and initialize filled_mask ---
    seeds = []
    filled_mask = np.zeros_like(input_np, dtype=bool)
    for r in range(height):
        for c in range(width):
            color = input_np[r, c]
            if color == boundary_color:
                filled_mask[r, c] = True
            elif color != background_color:
                seeds.append((color, r, c)) # Store color, row, col
                filled_mask[r, c] = True # Seed locations are considered filled

    # --- Sort seeds by priority: color, then row, then column ---
    seeds.sort()

    # --- Perform competitive BFS fill for each seed ---
    for seed_color, r_seed, c_seed in seeds:
        seed_loc = (r_seed, c_seed)
        # The BFS function handles filling the adjacent background areas
        bfs_fill(input_np, output_grid, filled_mask, seed_loc, seed_color, background_color, boundary_color)

    # --- Return the result ---
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
7 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 8
1 8 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 4 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 3 2 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 4 1 2 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 2 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 2 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 2 1 1 1
1 1 1 1 1 1 1 1 2 2 2 2 2 2 2 2 2 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 2 1 1 1 1 1 1 1 1 1 1 1
```
Expected Output:
```
7 7 7 7 7 7 7 7 2 8 8 8 8 8 8 8 8 8 8 8
7 8 8 8 8 8 8 7 2 8 4 4 4 4 4 4 4 4 4 8
7 8 7 7 7 7 8 7 2 8 4 8 8 8 8 8 8 8 4 8
7 8 7 8 8 7 8 7 2 8 4 8 4 4 4 4 4 8 4 8
7 8 7 8 8 7 8 7 2 8 4 8 4 8 8 8 4 8 4 8
7 8 7 8 8 7 8 7 2 8 4 8 4 4 4 4 4 8 4 8
7 8 7 8 8 7 8 7 2 8 4 8 8 8 8 8 8 8 4 8
7 8 7 8 8 7 8 7 2 8 4 4 4 4 4 4 4 4 4 8
7 8 7 8 8 7 8 7 2 8 8 8 8 8 8 8 8 8 4 8
7 8 7 8 8 7 8 7 2 2 2 2 2 2 2 2 2 8 4 8
7 8 7 8 8 7 8 7 2 3 3 3 3 3 3 3 2 8 4 8
7 8 7 8 8 7 8 7 2 3 4 4 4 4 4 3 2 8 4 8
7 8 7 8 8 7 8 7 2 3 4 3 3 3 4 3 2 8 4 8
7 8 7 8 8 7 8 7 2 3 4 4 4 4 4 3 2 8 4 8
7 8 7 8 8 7 8 7 2 3 3 3 3 3 3 3 2 8 4 8
7 8 7 8 8 7 8 7 2 2 2 2 2 2 2 2 2 8 4 8
7 8 7 8 8 7 8 7 2 8 8 8 8 8 8 8 8 8 4 8
7 8 7 7 7 7 8 7 2 8 4 4 4 4 4 4 4 4 4 8
7 8 8 8 8 8 8 7 2 8 4 4 4 4 4 4 4 4 4 8
7 7 7 7 7 7 7 7 2 8 8 8 8 8 8 8 8 8 8 8
```
Transformed Output:
```
7 7 7 7 7 7 7 7 2 4 4 4 4 4 4 4 4 4 4 8
7 8 7 7 7 7 7 7 2 4 4 4 4 4 4 4 4 4 4 4
7 7 7 7 7 7 7 7 2 4 4 4 4 4 4 4 4 4 4 4
7 7 7 7 7 7 7 7 2 4 4 4 4 4 4 4 4 4 4 4
7 7 7 7 7 7 7 7 2 4 4 4 4 4 4 4 4 4 4 4
7 7 7 7 7 7 7 7 2 4 4 4 4 4 4 4 4 4 4 4
7 7 7 7 7 7 7 7 2 4 4 4 4 4 4 4 4 4 4 4
7 7 7 7 7 7 7 7 2 4 4 4 4 4 4 4 4 4 4 4
7 7 7 7 7 7 7 7 2 4 4 4 4 4 4 4 4 4 4 4
7 7 7 7 7 7 7 7 2 2 2 2 2 2 2 2 2 4 4 4
7 7 7 7 7 7 7 7 2 3 3 3 3 3 3 3 2 4 4 4
7 7 7 7 7 7 7 7 2 3 3 3 3 3 4 3 2 4 4 4
7 7 7 7 7 7 7 7 2 3 3 3 3 3 3 3 2 4 4 4
7 7 7 7 7 7 7 7 2 3 3 3 3 3 3 3 2 4 4 4
7 7 7 7 7 7 7 7 2 3 3 3 3 3 3 3 2 4 4 4
7 7 7 7 7 7 7 7 2 2 2 2 2 2 2 2 2 4 4 4
7 7 7 7 7 7 7 7 2 4 4 4 4 4 4 4 4 4 4 4
7 7 7 7 7 7 7 7 2 4 4 4 4 4 4 4 4 4 4 4
7 7 7 7 7 7 7 7 2 4 4 4 4 4 4 4 4 4 4 4
7 7 7 7 7 7 7 7 2 4 4 4 4 4 4 4 4 4 4 4
```
Match: False
Pixels Off: 178
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 88.99999999999999

## Example 2:
Input:
```
4 4 4 4 4 4 4 4 4 4 2 8 4 4 4 4 4 4 4 4
4 3 4 4 4 4 4 4 4 4 2 4 1 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 2 2 2 2 2 2 2 2 2
4 4 4 4 4 4 4 4 4 4 2 5 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 0 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 1 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 2 4 4 4 4 4 4 4 4 4
```
Expected Output:
```
4 4 4 4 4 4 4 4 4 4 2 8 8 8 8 8 8 8 8 8
4 3 3 3 3 3 3 3 3 4 2 8 1 1 1 1 1 1 1 8
4 3 4 4 4 4 4 4 3 4 2 8 1 8 8 8 8 8 1 8
4 3 4 3 3 3 3 4 3 4 2 8 1 8 1 1 1 8 1 8
4 3 4 3 4 4 3 4 3 4 2 8 1 8 1 8 1 8 1 8
4 3 4 3 4 4 3 4 3 4 2 8 1 8 1 8 1 8 1 8
4 3 4 3 4 4 3 4 3 4 2 8 1 8 1 8 1 8 1 8
4 3 4 3 4 4 3 4 3 4 2 8 1 8 1 8 1 8 1 8
4 3 4 3 4 4 3 4 3 4 2 8 1 8 1 1 1 8 1 8
4 3 4 3 4 4 3 4 3 4 2 8 1 8 8 8 8 8 1 8
4 3 4 3 4 4 3 4 3 4 2 8 1 1 1 1 1 1 1 8
4 3 4 3 4 4 3 4 3 4 2 8 8 8 8 8 8 8 8 8
4 3 4 3 4 4 3 4 3 4 2 2 2 2 2 2 2 2 2 2
4 3 4 3 4 4 3 4 3 4 2 5 5 5 5 5 5 5 5 5
4 3 4 3 4 4 3 4 3 4 2 5 0 0 0 0 0 0 0 5
4 3 4 3 4 4 3 4 3 4 2 5 0 1 1 1 1 1 0 5
4 3 4 3 3 3 3 4 3 4 2 5 0 1 5 5 5 1 0 5
4 3 4 4 4 4 4 4 3 4 2 5 0 1 1 1 1 1 0 5
4 3 3 3 3 3 3 3 3 4 2 5 0 0 0 0 0 0 0 5
4 4 4 4 4 4 4 4 4 4 2 5 5 5 5 5 5 5 5 5
```
Transformed Output:
```
3 3 3 3 3 3 3 3 3 3 2 8 1 1 1 1 1 1 1 1
3 3 3 3 3 3 3 3 3 3 2 1 1 1 1 1 1 1 1 1
3 3 3 3 3 3 3 3 3 3 2 1 1 1 1 1 1 1 1 1
3 3 3 3 3 3 3 3 3 3 2 1 1 1 1 1 1 1 1 1
3 3 3 3 3 3 3 3 3 3 2 1 1 1 1 1 1 1 1 1
3 3 3 3 3 3 3 3 3 3 2 1 1 1 1 1 1 1 1 1
3 3 3 3 3 3 3 3 3 3 2 1 1 1 1 1 1 1 1 1
3 3 3 3 3 3 3 3 3 3 2 1 1 1 1 1 1 1 1 1
3 3 3 3 3 3 3 3 3 3 2 1 1 1 1 1 1 1 1 1
3 3 3 3 3 3 3 3 3 3 2 1 1 1 1 1 1 1 1 1
3 3 3 3 3 3 3 3 3 3 2 1 1 1 1 1 1 1 1 1
3 3 3 3 3 3 3 3 3 3 2 1 1 1 1 1 1 1 1 1
3 3 3 3 3 3 3 3 3 3 2 2 2 2 2 2 2 2 2 2
3 3 3 3 3 3 3 3 3 3 2 5 0 0 0 0 0 0 0 0
3 3 3 3 3 3 3 3 3 3 2 0 0 0 0 0 0 0 0 0
3 3 3 3 3 3 3 3 3 3 2 0 0 1 0 0 0 0 0 0
3 3 3 3 3 3 3 3 3 3 2 0 0 0 0 0 0 0 0 0
3 3 3 3 3 3 3 3 3 3 2 0 0 0 0 0 0 0 0 0
3 3 3 3 3 3 3 3 3 3 2 0 0 0 0 0 0 0 0 0
3 3 3 3 3 3 3 3 3 3 2 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 224
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 112.0
