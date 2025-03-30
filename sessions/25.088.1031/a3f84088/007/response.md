```python
import numpy as np
from collections import deque

"""
Transforms the pixels within a gray rectangular frame based on adjacency rules and the presence of internal gray pixels.

1.  Identify the gray (5) rectangular frame by finding the bounding box of all gray pixels.
2.  Check if any gray (5) pixels exist within the area strictly enclosed by the frame's bounding box.
3.  If no internal gray pixels exist (Case 1):
    a.  Perform a layered fill starting from the frame boundary inwards.
    b.  The first layer adjacent to the frame is colored red (2).
    c.  The next layer adjacent to the red layer is colored gray (5).
    d.  Subsequent layers alternate between red (2) and gray (5).
    e.  This continues until no more white (0) pixels inside the frame can be colored by adjacent layers.
4.  If internal gray pixels exist (Case 2):
    a.  Find all white (0) pixels strictly inside the frame's bounding box that are adjacent (8-connectivity) to *any* gray pixel (either on the frame or internal).
    b.  Change these adjacent white pixels to red (2).
    c.  Leave all other pixels unchanged (including internal grays and non-adjacent whites).
5.  If no gray pixels are found in the input, return the input grid unchanged.
"""

def _find_frame_and_internal_gray(input_array):
    """
    Finds the bounding box of gray pixels and checks for internal grays.

    Args:
        input_array (np.array): The input grid.

    Returns:
        tuple: (frame_coords, has_internal_gray)
               frame_coords is (min_r, max_r, min_c, max_c) or None if no gray pixels.
               has_internal_gray is bool.
    """
    gray_pixels = np.argwhere(input_array == 5)

    if gray_pixels.size == 0:
        return None, False # No gray pixels at all

    min_r = np.min(gray_pixels[:, 0])
    max_r = np.max(gray_pixels[:, 0])
    min_c = np.min(gray_pixels[:, 1])
    max_c = np.max(gray_pixels[:, 1])

    frame_coords = (min_r, max_r, min_c, max_c)

    # --- Check for Internal Grays ---
    has_internal_gray = False
    # Check only if there's a potential internal area
    if max_r > min_r + 1 and max_c > min_c + 1:
        for r in range(min_r + 1, max_r):
            for c in range(min_c + 1, max_c):
                if input_array[r, c] == 5:
                    has_internal_gray = True
                    break
            if has_internal_gray:
                break

    return frame_coords, has_internal_gray


def transform(input_grid):
    """
    Applies the iterative fill or single-layer red fill based on internal grays.

    Args:
        input_grid (list[list[int]]): The input grid.

    Returns:
        list[list[int]]: The transformed grid.
    """
    input_array = np.array(input_grid, dtype=int)
    output_array = np.copy(input_array)
    height, width = input_array.shape

    # --- 1. Identify Frame and Internal Grays ---
    frame_coords, has_internal_gray = _find_frame_and_internal_gray(input_array)

    if frame_coords is None:
        # No gray pixels found, return original grid
        return input_grid

    min_r, max_r, min_c, max_c = frame_coords

    # --- 2. Apply Transformation based on Case ---

    if has_internal_gray:
        # --- Case 2: Internal Grays Exist ---
        # Find coordinates of all gray pixels (frame and internal)
        all_gray_coords_set = set(tuple(coord) for coord in np.argwhere(input_array == 5))

        # Iterate through pixels strictly inside the frame bounds
        for r in range(min_r + 1, max_r):
            for c in range(min_c + 1, max_c):
                if output_array[r, c] == 0: # Check only white pixels
                    is_adj_to_gray = False
                    # Check 8 neighbors
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0: continue
                            nr, nc = r + dr, c + dc
                            # Check bounds implicitly via set lookup efficiency
                            if (nr, nc) in all_gray_coords_set:
                                is_adj_to_gray = True
                                break
                        if is_adj_to_gray:
                            break # Break outer loop too once adjacency found
                    # Color red if adjacent to any gray
                    if is_adj_to_gray:
                        output_array[r, c] = 2 # Red

    else:
        # --- Case 1: No Internal Grays ---
        # Use BFS for layered coloring
        q = deque()
        visited = set() # Keep track of visited internal cells to avoid cycles and re-coloring
        initial_color = 2 # Start with Red

        # Find initial layer: white cells inside adjacent to the frame
        frame_pixels_set = set()
        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                 if input_array[r,c] == 5:
                      # Check if it's actually part of the boundary frame lines
                      if r == min_r or r == max_r or c == min_c or c == max_c:
                           frame_pixels_set.add((r,c))

        current_layer_coords = set()
        for r_frame, c_frame in frame_pixels_set:
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0: continue
                    nr, nc = r_frame + dr, c_frame + dc

                    # Check if neighbor is strictly inside the frame and is white
                    if min_r < nr < max_r and min_c < nc < max_c and output_array[nr, nc] == 0:
                        coord = (nr, nc)
                        if coord not in visited:
                           current_layer_coords.add(coord)

        # Add initial layer to queue and color them
        for r, c in current_layer_coords:
             output_array[r, c] = initial_color
             visited.add((r, c))
             q.append(((r, c), initial_color)) # Store coordinate and its color

        # Perform BFS
        while q:
            (r, c), current_color = q.popleft()
            next_color = 5 if current_color == 2 else 2 # Toggle color for the next layer

            # Explore neighbors
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0: continue
                    nr, nc = r + dr, c + dc

                    # Check if neighbor is strictly inside, is white, and not visited
                    if (min_r < nr < max_r and
                        min_c < nc < max_c and
                        output_array[nr, nc] == 0 and
                        (nr, nc) not in visited):

                        visited.add((nr, nc))
                        output_array[nr, nc] = next_color
                        q.append(((nr, nc), next_color))


    # Convert back to list of lists for the expected output format
    return output_array.tolist()
```