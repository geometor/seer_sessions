import numpy as np
from collections import deque

"""
The transformation identifies a region enclosed by gray (5) pixels. 
Within this enclosed region, it finds the two most frequent non-gray, non-white colors present.
It then swaps all occurrences of the first color with the second color, and vice-versa, only within that enclosed region. 
Pixels outside the region, the gray boundary pixels themselves, and any white (0) pixels within the region remain unchanged.

The enclosed region is identified by performing a flood fill (BFS) starting from all non-gray pixels on the border of the grid. 
Any non-gray pixel not reached by this flood fill is considered part of the enclosed "inside" region.
"""

def transform(input_grid):
    """
    Transforms the input grid based on the swapping rule within a gray boundary.

    Args:
        input_grid (list of list of int): The input grid.

    Returns:
        list of list of int: The transformed grid.
    """
    # Convert input to numpy array for easier indexing and manipulation
    input_array = np.array(input_grid, dtype=int)
    # Initialize output array as a copy of the input
    output_array = input_array.copy()
    H, W = input_array.shape
    gray_color = 5
    white_color = 0

    # --- 1. Identify "outside" cells using flood fill from borders ---
    # visited array marks cells reachable from the border without crossing gray
    visited = np.zeros_like(input_array, dtype=bool)
    q = deque()

    # Add all non-gray border cells to the initial queue for BFS
    for c in range(W):
        # Top border
        if input_array[0, c] != gray_color and not visited[0, c]:
            q.append((0, c))
            visited[0, c] = True
        # Bottom border
        if input_array[H - 1, c] != gray_color and not visited[H - 1, c]:
            q.append((H - 1, c))
            visited[H - 1, c] = True
    for r in range(1, H - 1): # Avoid double-checking corners
        # Left border
        if input_array[r, 0] != gray_color and not visited[r, 0]:
            q.append((r, 0))
            visited[r, 0] = True
        # Right border
        if input_array[r, W - 1] != gray_color and not visited[r, W - 1]:
            q.append((r, W - 1))
            visited[r, W - 1] = True

    # Perform BFS flood fill to mark all "outside" cells
    while q:
        r, c = q.popleft()
        
        # Explore neighbors (4-directional connectivity)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            # Check if the neighbor is within bounds
            if 0 <= nr < H and 0 <= nc < W:
                # If neighbor is not gray and hasn't been visited, mark and add to queue
                if input_array[nr, nc] != gray_color and not visited[nr, nc]:
                    visited[nr, nc] = True
                    q.append((nr, nc))

    # --- 2. Identify "inside" pixels and collect their colors ---
    inside_pixels = []
    present_colors = set()
    for r in range(H):
        for c in range(W):
            # A pixel is "inside" if it's not gray and was not reached by the flood fill
            if input_array[r, c] != gray_color and not visited[r, c]:
                inside_pixels.append((r, c))
                present_colors.add(input_array[r, c])

    # --- 3. Determine the two colors to swap ---
    # Filter out white and gray colors from the set of colors present inside
    swap_candidates = {color for color in present_colors if color != white_color and color != gray_color}

    # --- 4. Perform the swap if exactly two candidate colors were found ---
    if len(swap_candidates) == 2:
        # Assign the two colors to be swapped
        color_a, color_b = list(swap_candidates)
        
        # Iterate through the identified "inside" pixels
        for r, c in inside_pixels:
            # Swap color_a with color_b
            if input_array[r, c] == color_a:
                output_array[r, c] = color_b
            # Swap color_b with color_a
            elif input_array[r, c] == color_b:
                output_array[r, c] = color_a
            # White pixels and any other unexpected colors inside remain unchanged

    # Convert the final numpy array back to a list of lists for the expected output format
    return output_array.tolist()