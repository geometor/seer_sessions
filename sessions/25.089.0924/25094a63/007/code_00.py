import numpy as np

"""
The transformation identifies all maximal monochromatic rectangles within the input grid.
A rectangle is monochromatic if all its pixels share the same color.
A rectangle is maximal if it cannot be expanded in any of the four cardinal directions (up, down, left, right)
without either going out of bounds or including a pixel of a different color.

For each maximal monochromatic rectangle found, its area (height * width) is calculated.
If the area is 36 or greater, all pixels within the bounds of that rectangle in the output grid
are replaced with the color yellow (4).
If the area is less than 36, the pixels within that rectangle remain unchanged from the input grid.
All pixels outside of any maximal monochromatic rectangle also remain unchanged.
"""

def find_maximal_monochromatic_rectangles(grid):
    """
    Finds all maximal monochromatic rectangles in the grid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, each representing a maximal monochromatic rectangle
              with keys 'r' (row), 'c' (column), 'h' (height), 'w' (width), 'color'.
    """
    rows, cols = grid.shape
    # visited tracks cells that are part of *confirmed* maximal rectangles
    visited = np.zeros_like(grid, dtype=bool)
    rectangles = []

    # Iterate through each cell as a potential top-left corner of a rectangle
    for r in range(rows):
        for c in range(cols):
            # Skip if this cell has already been included in a confirmed maximal rectangle
            if visited[r, c]:
                continue

            color = grid[r, c]

            # --- Find the largest possible rectangle starting at (r, c) ---
            # 1. Find initial max width in the starting row 'r'
            current_w = 0
            for k in range(c, cols):
                if grid[r, k] == color:
                    current_w += 1
                else:
                    break # Stop at first color change or boundary

            if current_w == 0: # Should not happen normally, but safeguard
                 continue # No rectangle starts here

            # 2. Expand height downwards, adjusting width (min_w) if rows don't support initial width
            final_h = 0
            min_w = current_w # Start with width from the first row
            for i in range(r, rows):
                row_w_check = 0
                possible = True
                # Check if the current row 'i' supports the current min_w
                for j in range(c, c + min_w):
                     # Check boundary and color match
                    if j >= cols or grid[i, j] != color:
                        min_w = j - c # Reduce width to the matched part
                        possible = False
                        break # Stop checking this row
                    row_w_check += 1

                if not possible or min_w == 0: # If row didn't match full min_w or width became 0
                    break # Stop extending height

                # If the row fully matched the current min_w, increment height
                final_h += 1

            # Potential rectangle found: anchored at (r, c) with dimensions (final_h, min_w)
            if final_h > 0 and min_w > 0:
                # --- Check if this specific rectangle is Maximal ---
                is_maximal = True

                # Check Up: Can it extend upwards? (Check row r-1 within the rect's width)
                if r > 0:
                    for k in range(c, c + min_w):
                        if grid[r - 1, k] == color:
                            is_maximal = False
                            break

                # Check Down: Can it extend downwards? (Check row r+final_h within the rect's width)
                if is_maximal and r + final_h < rows:
                    for k in range(c, c + min_w):
                        if grid[r + final_h, k] == color:
                            is_maximal = False
                            break

                # Check Left: Can it extend leftwards? (Check col c-1 within the rect's height)
                if is_maximal and c > 0:
                    for i in range(r, r + final_h):
                        if grid[i, c - 1] == color:
                            is_maximal = False
                            break

                # Check Right: Can it extend rightwards? (Check col c+min_w within the rect's height)
                if is_maximal and c + min_w < cols:
                     for i in range(r, r + final_h):
                        if grid[i, c + min_w] == color:
                            is_maximal = False
                            break

                # --- Store if Maximal and Mark Visited ---
                if is_maximal:
                    # Check if any part of this maximal rectangle has *already* been visited.
                    # This prevents adding duplicates if the algorithm somehow restarts
                    # within an already found maximal region due to complex overlaps.
                    if not visited[r : r + final_h, c : c + min_w].any():
                        rectangles.append({'r': r, 'c': c, 'h': final_h, 'w': min_w, 'color': color})
                        # Mark the *entire area* of the confirmed maximal rectangle as visited
                        visited[r : r + final_h, c : c + min_w] = True
                # If not maximal, we do nothing. We don't add it, and we don't mark (r,c) visited,
                # allowing (r,c) to be included when the *actual* maximal rectangle containing it is found.

    return rectangles


def transform(input_grid):
    """
    Transforms the input grid by filling large monochromatic rectangles with yellow.

    Args:
        input_grid (list[list[int]]): The input grid represented as a list of lists.

    Returns:
        list[list[int]]: The transformed grid.
    """
    # Convert input to a NumPy array for easier manipulation and slicing
    np_grid = np.array(input_grid, dtype=int)
    # Initialize the output grid as a copy of the input
    output_grid = np_grid.copy()

    # Define the minimum area threshold for filling
    min_area = 36

    # Find all maximal monochromatic rectangles in the input grid
    # Uses the refined helper function designed to correctly identify maximality.
    rectangles = find_maximal_monochromatic_rectangles(np_grid)

    # Iterate through the found maximal rectangles
    for rect in rectangles:
        # Calculate the area of the rectangle
        area = rect['h'] * rect['w']

        # Check if the area meets the threshold
        if area >= min_area:
            # Get the rectangle's position (top-left) and dimensions
            r, c = rect['r'], rect['c']
            h, w = rect['h'], rect['w']

            # Fill the corresponding area in the output grid with yellow (color 4)
            # NumPy slicing makes this efficient.
            output_grid[r : r + h, c : c + w] = 4

    # Convert the final NumPy array back to a list of lists format for the ARC standard output
    return output_grid.tolist()