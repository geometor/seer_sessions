Warning: Response generation stopped. Finish Reason: MAX_TOKENS (2)
Partial text available:
---
```python
import numpy as np
import collections

"""
Identifies a primary diagonal or anti-diagonal line segment composed of a single, 
repeated non-zero integer in the input grid. This segment is then projected 
horizontally by a fixed offset (observed as 7 columns to the right in examples). 
The cells at the projected coordinates in the output grid are overwritten with 
the number composing the source line segment.
"""

def _find_source_line(grid):
    """
    Finds the primary diagonal or anti-diagonal line segment.

    Identifies connected components of identical non-zero numbers using Breadth-First Search (BFS).
    Checks if a component forms a true diagonal (row - col = constant) or 
    anti-diagonal (row + col = constant) line segment.
    Filters out components that are purely horizontal or vertical lines.
    Ensures the identified segment is contiguous along its diagonal/anti-diagonal path.
    If multiple valid diagonal/anti-diagonal line segments are found, it selects the one
    whose coordinates include the minimum row index (topmost). If rows are tied, it chooses 
    the one starting at the minimum column index (leftmost).

    Args:
        grid (np.array): The input grid as a NumPy array.

    Returns:
        tuple: (source_number, source_coords) or (None, []) if no suitable line is found.
            source_number (int or None): The integer value composing the line, or None.
            source_coords (list): A list of (row, col) tuples for the segment, or empty list.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    potential_segments = []

    for r in range(rows):
        for c in range(cols):
            # Start BFS from an unvisited non-zero cell
            if grid[r, c] > 0 and not visited[r, c]:
                num = grid[r, c]
                component_coords = set()
                q = collections.deque([(r, c)])
                visited[r, c] = True
                component_coords.add((r, c))

                # Find all connected cells (8-connectivity) with the same number
                while q:
                    row, col = q.popleft()
                    # Check 8 neighbors
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0: continue # Skip self
                            nr, nc = row + dr, col + dc
                            # Check bounds and if neighbor matches number and is unvisited
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               grid[nr, nc] == num and not visited[nr, nc]:
                                visited[nr, nc] = True
                                component_coords.add((nr, nc))
                                q.append((nr, nc))

                # Analyze the found component
                if len(component_coords) >= 2:
                    # Sort coordinates primarily by row, then column for consistent checks
                    coords_list = sorted(list(component_coords), key=lambda x: (x[0], x[1]))

                    # Check if it's a pure row (all rows same) or column (all cols same)
                    is_row = all(cr == coords_list[0][0] for cr, cc in coords_list)
                    is_col = all(cc == coords_list[0][1] for cr, cc in coords_list)

                    # Filter out pure rows and columns
                    if not is_row and not is_col:
                        # Check if it forms a diagonal (r-c = const) or anti-diagonal (r+c = const)
                        is_diag = len(set(cr - cc for cr, cc in coords_list)) == 1
                        is_anti = len(set(cr + cc for cr, cc in coords_list)) == 1

                        # Check for contiguity along the diagonal/anti-diagonal path
                        is_contiguous = True
                        if len(coords_list) > 1:
                           diffs = set()
                           # Check the step between consecutive sorted points
                           for i in range(len(coords_list) - 1):
                               dr = coords_list[i+1][0] - coords_list[i][0]
                               dc = coords_list[i+1][1] - coords_list[i][1]
                               diffs.add((dr, dc))
                           # A contiguous diagonal/anti-diagonal should only have one type of step:
                           # (1, 1) for anti-diagonal down-right
                           # (1, -1) for diagonal down-left
                           # (-1,-1) for anti-diagonal up-left (covered by sorting/starting point)
                           # (-1, 1) for diagonal up-right (covered by sorting/starting point)
                           # We expect only one step type like (1,1) or (1,-1) etc.
                           # And the magnitude of row/col step must be 1 for diagonal adjacency
                           if len(diffs) != 1 or abs(list(diffs)[0][0]) != 1 or abs(list(diffs)[0][1]) != 1:
                               is_contiguous = False

                        # If it's a valid, contiguous diagonal or anti-diagonal segment
                        if (is_diag or is_anti) and is_contiguous:
                            potential_segments.append((num, coords_list))


    # --- Selection of the primary segment ---
    if not potential_segments:
        # No segments found matching the criteria
        # print("Debug: No suitable source line segment found.") # Optional debug message
        return None, []
    elif len(potential_segments) == 1:
        # Exactly one segment found
        return potential_segments[0]
    else:
        # Multiple segments found, apply tie-breaking rules
        # Sort by the minimum row index in the segment's coordinates
        # If rows are tied, sort by the minimum column index among points with the minimum row index
        potential_segments.sort(key=lambda s: (
            min(r for r, c in s[1]), 
            min(c for r, c in s[1] if r == min(r_ for r_, c_ in s[1]))
        ))
        # print(f"Debug: Found {len(potential_segments)} potential source lines. Choosing the topmost/leftmost one.") # Optional debug message
        return potential_segments[0]


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists of integers.

    Returns:
        list of lists: The transformed grid.
    """
    # --- Initialization ---
    # Convert input list of lists to a NumPy array for efficient processing
    input_array = np.array(input_grid, dtype=int)
    if input_array.size == 0: # Handle empty input
        return []
    rows, cols = input_array.shape
    # Create a copy of the input array to modify, this will become the output
    output_grid = np.copy(input_array)

    # --- Parameters ---
    # Define the fixed horizontal offset used for projection
    offset = 7

    # --- Core Logic ---
    # 1. Find the specific source diagonal/anti-diagonal line segment
    source_number, source_coords = _find_source_line(input_array)

    # If no valid source line was found, return the unmodified grid copy
    if source_number is None:
        # print("Warning: No source line identified, returning copy of input.") # Optional warning
        return output_grid.tolist() # Convert back to list of lists format

    # 2. Apply the projection and overwrite values
    # Iterate through each coordinate (row, col) of the identified source line
    for r, c_source in source_coords:
        # Calculate the target column by adding the offset
        c_target = c_source + offset

        # Check if the calculated target column is within the grid's column bounds
        if 0 <= c_target < cols:
            # If within bounds, overwrite the value in the output grid
            # at the target coordinate (same row, shifted column)
            # with the number from the source line segment.
            output_grid[r, c_target] = source_number

    # --- Output ---
    # Convert the final NumPy array back to a list of lists format for the return value
    return output_grid.tolist
---
