import numpy as np
from itertools import combinations
from collections import deque

"""
Fill the white space between pairs of same-colored, aligned (horizontally or vertically) 
rectangles with azure (8), provided the space between them is currently empty (white, 0).
"""

def find_rectangles(grid):
    """
    Identifies all distinct, contiguous rectangular blocks of non-white pixels.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents a rectangle
              with keys 'color', 'top', 'bottom', 'left', 'right'.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    rectangles = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                q = deque([(r, c)])
                visited[r, c] = True
                pixels = set([(r, c)])
                min_r, max_r = r, r
                min_c, max_c = c, c

                # Use BFS to find all connected pixels of the same color
                while q:
                    row, col = q.popleft()
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)

                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            pixels.add((nr, nc))
                
                # Verify if the found shape is a solid rectangle
                is_rectangle = True
                if len(pixels) != (max_r - min_r + 1) * (max_c - min_c + 1):
                    is_rectangle = False # Not the right number of pixels for the bounding box
                else:
                    # Check if all pixels within the bounding box match the color
                     for rr in range(min_r, max_r + 1):
                         for cc in range(min_c, max_c + 1):
                            if grid[rr, cc] != color:
                                # This check isn't strictly necessary if we assume inputs are always rectangles
                                # but it helps confirm the object identification.
                                # We might only need to check if (rr, cc) is in the 'pixels' set found by BFS.
                                if (rr, cc) not in pixels:
                                    is_rectangle = False 
                                    break
                         if not is_rectangle:
                             break
                
                # Store if it's confirmed or assumed to be a rectangle based on BFS extent
                # For this problem, the shapes appear to always be solid rectangles.
                # We rely on the bounding box identified by BFS.
                rectangles.append({
                    'color': color,
                    'top': min_r,
                    'bottom': max_r,
                    'left': min_c,
                    'right': max_c
                })
                
    return rectangles

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid (np.ndarray): The input grid as a NumPy array.

    Returns:
        np.ndarray: The transformed output grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # Find all colored rectangles in the input grid
    rectangles = find_rectangles(input_grid)

    # Iterate through all unique pairs of rectangles
    for rect_a, rect_b in combinations(rectangles, 2):
        # Check if the rectangles have the same color
        if rect_a['color'] != rect_b['color']:
            continue

        # --- Check for Horizontal Alignment and Gap ---
        # Check if rows overlap
        overlap_rows = max(rect_a['top'], rect_b['top']) <= min(rect_a['bottom'], rect_b['bottom'])
        if overlap_rows:
            # Determine which rectangle is left and which is right
            left_rect, right_rect = (rect_a, rect_b) if rect_a['right'] < rect_b['left'] else (rect_b, rect_a)

            # Check if they are separated horizontally with a gap > 0
            if left_rect['right'] < right_rect['left'] -1:
                # Define the gap region boundaries
                gap_top = max(left_rect['top'], right_rect['top'])
                gap_bottom = min(left_rect['bottom'], right_rect['bottom'])
                gap_left = left_rect['right'] + 1
                gap_right = right_rect['left'] - 1

                # Check if the gap area in the input grid is entirely white
                if np.all(input_grid[gap_top : gap_bottom + 1, gap_left : gap_right + 1] == 0):
                    # Fill the gap area in the output grid with azure (8)
                    output_grid[gap_top : gap_bottom + 1, gap_left : gap_right + 1] = 8

        # --- Check for Vertical Alignment and Gap ---
        # Check if columns overlap
        overlap_cols = max(rect_a['left'], rect_b['left']) <= min(rect_a['right'], rect_b['right'])
        if overlap_cols:
            # Determine which rectangle is top and which is bottom
            top_rect, bottom_rect = (rect_a, rect_b) if rect_a['bottom'] < rect_b['top'] else (rect_b, rect_a)

            # Check if they are separated vertically with a gap > 0
            if top_rect['bottom'] < bottom_rect['top'] - 1:
                 # Define the gap region boundaries
                gap_top = top_rect['bottom'] + 1
                gap_bottom = bottom_rect['top'] - 1
                gap_left = max(top_rect['left'], bottom_rect['left'])
                gap_right = min(top_rect['right'], bottom_rect['right'])

                # Check if the gap area in the input grid is entirely white
                if np.all(input_grid[gap_top : gap_bottom + 1, gap_left : gap_right + 1] == 0):
                     # Fill the gap area in the output grid with azure (8)
                    output_grid[gap_top : gap_bottom + 1, gap_left : gap_right + 1] = 8

    return output_grid