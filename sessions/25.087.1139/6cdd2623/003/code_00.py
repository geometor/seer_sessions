import numpy as np

"""
Transforms an input grid based on matching non-white pixel colors on opposite edges.

1. Identifies pairs of same-colored pixels on opposite horizontal edges (left/right) 
   for each row.
2. Identifies pairs of same-colored pixels on opposite vertical edges (top/bottom) 
   for each column.
3. Determines the set of colors that have matches both horizontally ('H_colors') 
   and vertically ('V_colors'). Calculate the intersection ('Intersection_colors').
4. If 'Intersection_colors' is not empty, draw lines ONLY for the colors present 
   in the intersection. For each intersecting color, draw all its corresponding 
   horizontal lines and vertical lines onto an initially white output grid.
5. If 'Intersection_colors' is empty, draw ALL identified horizontal lines and 
   ALL identified vertical lines onto the output grid.
6. Lines overwrite any existing pixels in their path. Vertical lines are drawn 
   after horizontal lines in the 'else' case, potentially overwriting intersections.
"""

def transform(input_grid):
    """
    Applies the edge-matching line drawing transformation.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    height, width = input_grid.shape
    # Initialize output_grid with the same dimensions as input, filled with white (0)
    output_grid = np.zeros_like(input_grid)

    # --- Find Matches ---
    h_matches = {} # {color: [list of rows]}
    for r in range(height):
        left_pixel_color = input_grid[r, 0]
        right_pixel_color = input_grid[r, width - 1]
        # Check if edge pixels match and are not white (0)
        if left_pixel_color != 0 and left_pixel_color == right_pixel_color:
            color = left_pixel_color
            if color not in h_matches:
                h_matches[color] = []
            h_matches[color].append(r)

    v_matches = {} # {color: [list of columns]}
    for c in range(width):
        top_pixel_color = input_grid[0, c]
        bottom_pixel_color = input_grid[height - 1, c]
        # Check if edge pixels match and are not white (0)
        if top_pixel_color != 0 and top_pixel_color == bottom_pixel_color:
            color = top_pixel_color
            if color not in v_matches:
                v_matches[color] = []
            v_matches[color].append(c)

    # --- Determine Color Sets ---
    h_colors = set(h_matches.keys())
    v_colors = set(v_matches.keys())
    intersection_colors = h_colors.intersection(v_colors)

    # --- Conditional Drawing Logic ---
    if intersection_colors: # If the intersection is NOT empty
        # Draw lines only for colors present in the intersection
        for color in intersection_colors:
            # Draw horizontal lines for this color
            if color in h_matches:
                for r in h_matches[color]:
                    output_grid[r, :] = color
            # Draw vertical lines for this color
            if color in v_matches:
                 for c in v_matches[color]:
                    output_grid[:, c] = color
    else: # If the intersection IS empty
        # Draw all horizontal lines found
        for color, rows in h_matches.items():
            for r in rows:
                output_grid[r, :] = color
        # Draw all vertical lines found (may overwrite horizontal intersections)
        for color, cols in v_matches.items():
            for c in cols:
                output_grid[:, c] = color

    return output_grid