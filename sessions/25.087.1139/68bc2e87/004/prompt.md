
Previous Code:
```python
"""
Identify the sequence of nested frame colors in the input grid, starting from the outermost azure (8) background connected to the border and moving inwards. If the color red (2) is present anywhere in this sequence of frame colors, output a 1x1 grid containing red (2). Otherwise, output an empty grid.
"""

import numpy as np
import collections

def transform(input_grid):
    """
    Finds the sequence of nested frame colors inward from the azure border.
    Outputs [[2]] if red is found in the sequence, otherwise [].

    Args:
        input_grid (list of lists): The input grid.

    Returns:
        list of lists: [[2]] if red is in the frame sequence, otherwise [].
    """
    try:
        grid = np.array(input_grid, dtype=int)
        if grid.size == 0:
            return [] # Handle empty input
        rows, cols = grid.shape
    except Exception:
        return [] # Invalid grid format

    # Initialize data structures
    q = collections.deque()
    visited = np.zeros_like(grid, dtype=bool) # Tracks globally visited cells
    frame_colors_sequence = []
    background_color = 8
    found_colors = {background_color} # Keep track of colors identified as background or frames

    # --- Step 1: Find initial Azure background connected to border ---
    initial_boundary_cells = []
    # Initialize queue with border azure cells
    for r in range(rows):
        for c in [0, cols - 1]: # First and last columns
            if 0 <= r < rows and 0 <= c < cols:
                if grid[r, c] == background_color and not visited[r, c]:
                    q.append((r, c))
                    visited[r, c] = True
    for c in range(cols): # First and last rows (avoid double-adding corners)
         for r in [0, rows - 1]:
             if 0 <= r < rows and 0 <= c < cols:
                if grid[r, c] == background_color and not visited[r, c]:
                    q.append((r, c))
                    visited[r, c] = True

    if not q:
         # No azure background connected to border found
         return []

    # --- Step 2: Perform BFS to identify the full background region adjacent to the border ---
    # This ensures we start the frame search from the complete outer layer
    background_bfs_q = q.copy()
    current_boundary_pixels = list(q) # Initial set of pixels forming the boundary

    while background_bfs_q:
        r, c = background_bfs_q.popleft()
        # Store the coordinate as part of the current boundary
        # No, current_boundary_pixels should be the starting points for the *next* search
        # We need to find neighbors of the *entire* background region

        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and \
               grid[nr, nc] == background_color and not visited[nr, nc]:
                visited[nr, nc] = True
                background_bfs_q.append((nr, nc))
                # Add newly found background cells to the list from which we'll search for the first frame
                current_boundary_pixels.append((nr,nc))

    current_layer_color = background_color

    # --- Step 3: Iteratively find frame layers ---
    while True:
        next_layer_candidates = {} # Stores {color: set_of_coords} for adjacent, unvisited, new colors
        
        # Use a temporary queue for searching neighbors of the *entire* current boundary
        search_q = collections.deque(current_boundary_pixels)
        processed_in_search = set(current_boundary_pixels) # Prevent re-adding to search queue

        # Explore neighbors of all pixels in the current boundary layer
        while search_q:
            r, c = search_q.popleft()

            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc

                # Check bounds
                if 0 <= nr < rows and 0 <= nc < cols:
                    neighbor_color = grid[nr, nc]
                    neighbor_coords = (nr, nc)

                    # Check if neighbor is a new color and hasn't been visited yet
                    if neighbor_color != current_layer_color and \
                       neighbor_color not in found_colors and \
                       not visited[nr, nc]:
                        
                        if neighbor_color not in next_layer_candidates:
                            next_layer_candidates[neighbor_color] = set()
                        # Store the coordinate of this newly found adjacent pixel
                        next_layer_candidates[neighbor_color].add(neighbor_coords)
                    # Note: We don't need to expand within the current_layer_color here,
                    # as the initial background BFS and subsequent layer preparations handle finding all relevant pixels.

        # --- Step 4: Analyze candidates for the next layer ---
        if not next_layer_candidates:
            # No new adjacent colors found, all frames identified
            break

        # Check if exactly one new frame color was found adjacent to the current layer
        if len(next_layer_candidates) != 1:
            # Ambiguous structure based on training examples (expecting perfect nesting)
            # This indicates either an error in logic or an input structure not covered by examples.
            # Based on the problem derivation, this shouldn't happen for valid inputs yielding [[2]].
            # We'll stop and won't produce [[2]] in this case.
            # print(f"Ambiguity: Found {len(next_layer_candidates)} candidates {list(next_layer_candidates.keys())} adjacent to color {current_layer_color}.")
            return [] # Return empty list for ambiguous cases or non-perfect frames

        # Identify the single next frame color and its starting coordinates
        next_frame_color = list(next_layer_candidates.keys())[0]
        next_boundary_start_coords = list(next_layer_candidates[next_frame_color])

        # Add the found frame color to the sequence and mark it as found
        frame_colors_sequence.append(next_frame_color)
        found_colors.add(next_frame_color)

        # Mark the starting pixels of this new frame as visited globally
        for nr_next, nc_next in next_boundary_start_coords:
            visited[nr_next, nc_next] = True

        # --- Step 5: Prepare for the next iteration ---
        # The new boundary consists of the pixels we just found and marked visited
        current_boundary_pixels = next_boundary_start_coords
        current_layer_color = next_frame_color

        # If for some reason the list of starting coords is empty, break
        if not current_boundary_pixels:
             break

    # --- Step 6: Check if Red (2) is in the sequence ---
    target_color = 2
    if target_color in frame_colors_sequence:
        output_grid = [[target_color]]
    else:
        # Red was not found in the sequence, or no frames were found
        output_grid = []

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Error: list index out of range

## Example 2:
Error: list index out of range

## Example 3:
Error: list index out of range

## Example 4:
Error: list index out of range
