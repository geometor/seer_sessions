import numpy as np
from collections import deque, Counter

"""
Identifies pixels of a specific color (C_enclosed) that are enclosed by pixels of any other non-white color. 
Enclosed means that any path from the pixel to the grid boundary must pass through a non-white pixel that is not C_enclosed.

Steps:
1. Iterate through each non-white color `C_enclosed` present in the input grid.
2. For each `C_enclosed`, determine which pixels of this color are enclosed.
   - Perform a Breadth-First Search (BFS) starting from all boundary cells of the grid.
   - The BFS can only travel through white pixels (0) or pixels of color `C_enclosed`.
   - Any pixel of color `C_enclosed` that is *not* reached by this BFS is considered enclosed.
3. Collect all enclosed pixels for all colors. Store them grouped by their original color.
4. Create an output grid, initially a copy of the input.
5. Remove all identified enclosed pixels from the output grid by setting their color to white (0).
6. For each color `C_enclosed` that had enclosed pixels removed:
   a. Calculate the frequency of column indices among the removed pixel locations for this color.
   b. Find the maximum frequency (most pixels removed in a single column).
   c. Identify the column index (or indices) with this maximum frequency. Select the minimum (leftmost) column index among them (`target_col`).
   d. Count the number of unique row indices among the removed pixel locations for this color (`N`).
   e. In the `output_grid`, set the color of the pixels in the `target_col` from row 0 to row `N-1` to `C_enclosed`.
7. Return the final modified output grid.
"""

def find_enclosed_pixels(grid, color_to_check):
    """
    Finds pixels of `color_to_check` that are enclosed.
    Uses BFS starting from the boundary, propagating through white cells and cells of `color_to_check`.
    """
    rows, cols = grid.shape
    reachable = np.zeros_like(grid, dtype=bool)
    q = deque()

    # Add boundary cells to the queue if they are white or the color_to_check
    for r in range(rows):
        for c in [0, cols - 1]:
            if not reachable[r, c] and (grid[r, c] == 0 or grid[r, c] == color_to_check):
                q.append((r, c))
                reachable[r, c] = True
    for c in range(cols):
        for r in [0, rows - 1]:
             if not reachable[r, c] and (grid[r, c] == 0 or grid[r, c] == color_to_check):
                q.append((r, c))
                reachable[r, c] = True

    # Perform BFS
    while q:
        r, c = q.popleft()

        # Explore neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if neighbor is reachable (white or target color) and not visited
                if not reachable[nr, nc] and (grid[nr, nc] == 0 or grid[nr, nc] == color_to_check):
                    reachable[nr, nc] = True
                    q.append((nr, nc))

    # Identify enclosed pixels (target color pixels that were not reached)
    enclosed_locations = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color_to_check and not reachable[r, c]:
                enclosed_locations.append((r, c))

    return enclosed_locations


def transform(input_grid):
    """
    Applies the enclosure transformation rule to the input grid.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    unique_colors = np.unique(input_grid[input_grid != 0]) # Get all non-white colors

    all_removed_pixels_by_color = {}

    # 1. Find all enclosed pixels for each color
    for color in unique_colors:
        enclosed_locations = find_enclosed_pixels(input_grid, color)
        if enclosed_locations:
            all_removed_pixels_by_color[color] = enclosed_locations

    # 2. Remove enclosed pixels from the output grid
    for color, locations in all_removed_pixels_by_color.items():
        for r, c in locations:
            output_grid[r, c] = 0 # Set to white

    # 3. Add new pixels at the top of the target column for each color
    for color, removed_locations in all_removed_pixels_by_color.items():
        if not removed_locations:
            continue

        # a. Calculate column frequencies
        columns = [c for r, c in removed_locations]
        if not columns: continue # Should not happen if removed_locations is not empty, but safety check
        
        col_counts = Counter(columns)
        max_freq = 0
        for col, count in col_counts.items():
             if count > max_freq:
                 max_freq = count
        
        # b. Find leftmost column(s) with max frequency
        candidate_cols = []
        for col, count in col_counts.items():
            if count == max_freq:
                candidate_cols.append(col)
        
        target_col = min(candidate_cols)


        # c. Count unique rows
        unique_rows = set(r for r, c in removed_locations)
        N = len(unique_rows)

        # d. Add pixels to the top of the target column
        for i in range(min(N, rows)): # Ensure we don't write past grid boundary
            output_grid[i, target_col] = color

    return output_grid