import numpy as np
from collections import Counter, deque

"""
Transformation Rule:

1.  Identify the `Input Frame Color` from the second row (index 1) of the input grid.
2.  Define the `Inner Area` as rows 2 through 8 (indices 2 to 8) and columns 1 through 8 (indices 1 to 8).
3.  Count the frequency of each color within the input grid's `Inner Area`, excluding white (color 0) and the `Input Frame Color`.
4.  Determine the `Output Fill Color` as the color with the highest frequency count from step 3.
5.  Create an output grid of the same dimensions as the input grid.
6.  Copy the first row (index 0) from the input grid to the output grid.
7.  Fill the entire second row (index 1) of the output grid with the `Output Fill Color`.
8.  Fill the outer frame columns (index 0 and index 9) from row 2 downwards (indices 2 to 9) with the `Output Fill Color`.
9.  Fill the bottom frame row (index 9), between columns 1 and 8 (indices 1 to 8), with the `Output Fill Color`.
10. Fill the top inner frame row (index 2), between columns 1 and 8 (indices 1 to 8), with the `Output Fill Color`.
11. Initialize the rest of the `Inner Area` in the output grid (rows 3-8, columns 1-8) to white (color 0).
12. Identify all `Seed Points`: the coordinates (row, column) within the input grid's `Inner Area` where the color matches the `Output Fill Color`.
13. For each `Seed Point` (r, c), set the corresponding cell `output_grid[r, c]` to the `Output Fill Color`.
14. Perform a flood fill operation starting from all `Seed Points` simultaneously on the output grid:
    *   Use a queue and a set of visited coordinates, initialized with the `Seed Points`.
    *   While the queue is not empty, dequeue a coordinate (r, c).
    *   For each 4-way adjacent neighbor (nr, nc) of (r, c):
        *   Check if (nr, nc) is within the bounds of the `Inner Area` (rows 2-8, columns 1-8).
        *   Check if the neighbor has not been visited yet.
        *   Check if `output_grid[nr, nc]` is currently white (0).
        *   Check if the corresponding cell in the *input* grid, `input_grid[nr, nc]`, is also white (0).
        *   If all these conditions are true:
            *   Set `output_grid[nr, nc]` to the `Output Fill Color`.
            *   Mark (nr, nc) as visited.
            *   Enqueue (nr, nc).
15. Return the completed output grid.
"""

def _find_most_frequent_inner_color(input_grid, frame_color):
    """
    Counts colors in the inner area (rows 2-8, cols 1-8), excluding white 
    and the frame_color, and returns the most frequent one.
    """
    rows, cols = input_grid.shape
    # Inner area: rows 2 to rows-2, cols 1 to cols-2 (inclusive indices)
    # For 10x10 grid: rows 2-8, cols 1-8
    inner_area = input_grid[2:rows-1, 1:cols-1] 
    
    color_counts = Counter()
    for r in range(inner_area.shape[0]):
        for c in range(inner_area.shape[1]):
            color = inner_area[r, c]
            if color != 0 and color != frame_color:
                color_counts[color] += 1
                
    if not color_counts:
        # Fallback if no valid colors found - this shouldn't happen based on examples
        # Returning 0 might be safer than None if required by caller.
        # Let's assume a color will always be found as per analysis.
        # If this assumption breaks, we need error handling or a defined fallback.
        return 0 

    # Find the color with the maximum count.
    most_frequent_color = max(color_counts, key=color_counts.get)
    return most_frequent_color

def _flood_fill(output_grid, input_grid, start_coords, fill_color):
    """
    Performs a 4-way flood fill on the output_grid's inner area (rows 2-8, cols 1-8).
    Starts from start_coords, fills only cells that are white (0) in output_grid 
    AND were also white (0) in input_grid.
    Modifies the output_grid in place.
    """
    rows, cols = output_grid.shape
    q = deque(start_coords)
    visited = set(start_coords) # Keep track of initial seeds and filled cells

    # Initial seed points are already colored in the main function.
    # The queue starts with these seed points.

    while q:
        r, c = q.popleft()

        # Explore neighbours (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check boundaries (inner area: rows 2-8, cols 1-8)
            # Indices: rows 2 to rows-2, cols 1 to cols-2
            if 2 <= nr <= rows - 2 and 1 <= nc <= cols - 2:
                # Check if the neighbor hasn't been visited
                if (nr, nc) not in visited:
                    # Check if the neighbor is white (0) in the output grid
                    # AND the corresponding cell was white (0) in the input grid
                    if output_grid[nr, nc] == 0 and input_grid[nr, nc] == 0:
                        output_grid[nr, nc] = fill_color
                        visited.add((nr, nc))
                        q.append((nr, nc))


def transform(input_grid_list):
    """
    Applies the transformation rule derived from the examples.
    """
    input_np = np.array(input_grid_list, dtype=int)
    rows, cols = input_np.shape
    
    # Initialize output grid with zeros
    output_grid = np.zeros_like(input_np)

    # 1. Identify Input Frame Color (from row index 1)
    input_frame_color = input_np[1, 0] 

    # 2. Define Inner Area (implicit in helper function and flood fill)

    # 3. & 4. Analyze inner area and determine Output Fill Color
    output_fill_color = _find_most_frequent_inner_color(input_np, input_frame_color)

    # 5. Create output grid (already done with zeros)

    # 6. Copy the first row
    output_grid[0, :] = input_np[0, :]

    # 7. Fill the second row (index 1) with Output Fill Color
    output_grid[1, :] = output_fill_color
    
    # 8. Fill the outer frame columns (0 and cols-1) from row 2 down
    output_grid[2:rows, 0] = output_fill_color  
    output_grid[2:rows, cols-1] = output_fill_color 

    # 9. Fill the bottom frame row (rows-1) inner part
    output_grid[rows-1, 1:cols-1] = output_fill_color 

    # 10. Fill the top inner frame row (row 2) inner part
    output_grid[2, 1:cols-1] = output_fill_color 

    # 11. Initialize the rest of the Inner Area (rows 3-8, cols 1-8) to white (0)
    # Indices: rows 3 to rows-2, cols 1 to cols-2
    if rows > 3 and cols > 2: # Check if this area exists
         output_grid[3:rows-1, 1:cols-1] = 0
    # Note: Pixels initialized to 0 by np.zeros_like, but this explicitly sets the core inner area

    # 12. Identify Seed Points in the input's inner area
    seed_coords = []
    for r in range(2, rows - 1): # Rows 2 to rows-2 (e.g., 2-8 for 10x10)
        for c in range(1, cols - 1): # Cols 1 to cols-2 (e.g., 1-8 for 10x10)
            if input_np[r, c] == output_fill_color:
                # Ensure seed point is within the flood fill boundary (redundant check, but safe)
                 if 2 <= r <= rows - 2 and 1 <= c <= cols - 2:
                    seed_coords.append((r, c))

    # 13. Set Seed Points in the output grid
    for r, c in seed_coords:
        # Check bounds just in case, though seed_coords generation should guarantee this
        if 2 <= r <= rows - 2 and 1 <= c <= cols - 2:
            output_grid[r, c] = output_fill_color

    # 14. Perform flood fill on the output grid's inner area
    # Pass both output_grid (to modify) and input_np (to check original white cells)
    _flood_fill(output_grid, input_np, seed_coords, output_fill_color)

    # 15. Return the completed output grid as a list of lists
    return output_grid.tolist()