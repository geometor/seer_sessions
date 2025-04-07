```python
import numpy as np
from collections import deque, Counter

"""
Transformation Rule:

1. Identify Enclosed Pixels: For each non-white color C present in the grid, find all pixels of color C that are "enclosed". A pixel is considered enclosed if it cannot reach the boundary of the grid by moving only through white (0) pixels or pixels of the same color C. This is determined using a Breadth-First Search (BFS) starting from all boundary cells, propagating only through white cells. Any non-white cell *not* reached by this BFS is potentially enclosed. We then filter these potentially enclosed cells to find those specifically of color C.

2. Remove Enclosed Pixels: Change the color of all identified enclosed pixels (for all colors) to white (0) in a copy of the input grid.

3. Add Indicator Pixels: For each color C for which enclosed pixels were found and removed:
    a. Collect the locations (row, column) of the removed pixels of color C.
    b. Count the frequency of each column index among these locations.
    c. Find the maximum frequency (the highest number of removed pixels in a single column).
    d. Identify all column indices that have this maximum frequency.
    e. Select the minimum (leftmost) column index among those identified in step 3d. Let this be `target_col`.
    f. Count the number of unique row indices among the removed pixel locations for color C. Let this be `N`.
    g. In the `target_col`, change the color of the top `N` pixels (rows 0 to N-1) to color C.

4. Final Grid: The grid after performing steps 2 and 3 for all relevant colors is the final output. If no pixels are enclosed according to the definition in step 1, the output grid is identical to the input grid. This rule specifically addresses the pattern observed in Examples 2 and 3. Example 1 appears to follow a different logic not covered here.
"""

def find_unreachable_non_white(grid):
    """
    Finds all non-white pixels that cannot reach the grid boundary via white cells.
    Uses BFS starting from the boundary, propagating only through white cells (0).
    """
    rows, cols = grid.shape
    reachable = np.zeros_like(grid, dtype=bool)
    q = deque()

    # Add boundary white cells to the queue
    for r in range(rows):
        for c in [0, cols - 1]:
            if not reachable[r, c] and grid[r, c] == 0:
                q.append((r, c))
                reachable[r, c] = True
    for c in range(cols):
        for r in [0, rows - 1]:
             if not reachable[r, c] and grid[r, c] == 0:
                q.append((r, c))
                reachable[r, c] = True

    # Perform BFS through white cells
    while q:
        r, c = q.popleft()

        # Explore neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check bounds and if neighbor is white and not visited
            if 0 <= nr < rows and 0 <= nc < cols and \
               not reachable[nr, nc] and grid[nr, nc] == 0:
                reachable[nr, nc] = True
                q.append((nr, nc))

    # Identify non-white pixels that were not reached
    unreachable_locations = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not reachable[r, c]:
                unreachable_locations.append(((r, c), grid[r,c])) # Store location and color

    return unreachable_locations

def transform(input_grid):
    """
    Applies the enclosure transformation rule to the input grid.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Find all potentially enclosed non-white pixels and their colors
    potentially_enclosed_pixels = find_unreachable_non_white(input_grid)

    # Group potentially enclosed pixels by their color
    enclosed_by_color = {}
    for (r, c), color in potentially_enclosed_pixels:
        if color not in enclosed_by_color:
            enclosed_by_color[color] = []
        enclosed_by_color[color].append((r, c))

    # Check if these potentially enclosed pixels are *actually* enclosed
    # (i.e., cannot escape via cells of their own color either)
    # This check is implicitly handled by the BFS logic in find_unreachable_non_white
    # because the BFS *only* travels through white. If a non-white cell isn't
    # reachable via white cells, it's considered enclosed for this problem's definition.

    # Store locations to remove and process later
    all_removed_pixels_by_color = {}

    for color, locations in enclosed_by_color.items():
         if locations: # If any pixels of this color were found to be enclosed
             all_removed_pixels_by_color[color] = locations
             # 2. Remove these enclosed pixels from the output grid
             for r, c in locations:
                 output_grid[r, c] = 0 # Set to white


    # 3. Add new pixels at the top of the target column for each color
    for color, removed_locations in all_removed_pixels_by_color.items():
        if not removed_locations:
            continue

        # a. Get column indices
        columns = [c for r, c in removed_locations]
        if not columns: continue

        # b. Calculate column frequencies
        col_counts = Counter(columns)

        # c. Find maximum frequency
        # Handle case where col_counts might be empty if columns was empty (shouldn't happen with check above)
        if not col_counts: continue
        max_freq = max(col_counts.values())

        # d. Find columns with max frequency
        candidate_cols = [col for col, count in col_counts.items() if count == max_freq]

        # e. Select the minimum (leftmost) column index
        target_col = min(candidate_cols)

        # f. Count unique rows
        unique_rows = set(r for r, c in removed_locations)
        N = len(unique_rows)

        # g. Add pixels to the top of the target column
        for i in range(min(N, rows)): # Ensure we don't write past grid boundary
            output_grid[i, target_col] = color

    return output_grid
```