import numpy as np
from collections import defaultdict

"""
Identify unique non-background colors (non-zero) in the input grid.
Calculate the average position (centroid) for each unique color.
Determine the dominant spatial arrangement (vertical or horizontal) by comparing the range of average row coordinates versus the range of average column coordinates across all colors.
If the vertical range (max_avg_row - min_avg_row) is greater than or equal to the horizontal range (max_avg_col - min_avg_col), the primary axis is vertical. Otherwise, it's horizontal.
Sort the unique non-background colors based on their average coordinate along the primary axis (average row for vertical, average column for horizontal).
Construct a 1D output grid (a column if the primary axis is vertical, a row if horizontal) containing the sorted colors.
"""

def transform(input_grid):
    """
    Transforms the input grid based on the spatial arrangement of its non-background colors.

    Args:
        input_grid (list of lists or np.ndarray): The input grid of color values (0-9).

    Returns:
        np.ndarray: A 1D numpy array (row or column) containing the sorted 
                    non-background colors. Returns an empty array if no 
                    non-background colors are found.
    """
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape

    # --- 1 & 2: Find unique colors and calculate sums for centroids ---
    color_data = defaultdict(lambda: {'sum_row': 0, 'sum_col': 0, 'count': 0})
    unique_colors_ordered = [] # To maintain discovery order if needed, though sorting will override

    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color != 0:  # Ignore background color (white)
                if color not in color_data:
                     unique_colors_ordered.append(color) # Keep track of unique colors
                color_data[color]['sum_row'] += r
                color_data[color]['sum_col'] += c
                color_data[color]['count'] += 1

    # --- 5: Handle edge case: no non-background colors ---
    if not color_data:
        # Returning an empty array. Adjust if a different empty representation is needed.
        return np.array([], dtype=int).reshape(0,0) # Or maybe np.array([[]])? Let's start with 0x0

    # --- 6: Calculate centroids ---
    centroids = []
    for color in unique_colors_ordered: # Use the ordered list to process colors found
        data = color_data[color]
        count = data['count']
        avg_row = data['sum_row'] / count
        avg_col = data['sum_col'] / count
        centroids.append({'color': color, 'avg_row': avg_row, 'avg_col': avg_col})

    # --- Handle edge case: only one non-background color ---
    if len(centroids) == 1:
        # Output should be 1x1 grid containing the single color
        # The axis determination below defaults to vertical, resulting in Nx1.
        # So, we return a 1x1 array explicitly here.
        # Actually, let's let the logic run. If only one color, ranges are 0.
        # row_range >= col_range (0 >= 0) is true -> vertical axis -> 1x1 output.
        # This seems correct based on general logic, though not explicitly shown in examples.
        pass # Let the standard logic handle this case.

    # --- 7: Determine range of centroids ---
    if len(centroids) > 0:
        min_avg_row = min(c['avg_row'] for c in centroids)
        max_avg_row = max(c['avg_row'] for c in centroids)
        min_avg_col = min(c['avg_col'] for c in centroids)
        max_avg_col = max(c['avg_col'] for c in centroids)
        row_range = max_avg_row - min_avg_row
        col_range = max_avg_col - min_avg_col
    else: # Should not happen due to the earlier check, but for safety
        row_range = 0
        col_range = 0
        
    # --- 8: Determine primary axis and sort ---
    is_vertical_axis = row_range >= col_range

    if is_vertical_axis:
        # Sort by average row index (top to bottom)
        centroids.sort(key=lambda c: c['avg_row'])
    else:
        # Sort by average column index (left to right)
        centroids.sort(key=lambda c: c['avg_col'])

    # Extract sorted colors
    sorted_colors = [c['color'] for c in centroids]

    # --- 9 & 10: Construct output grid ---
    num_colors = len(sorted_colors)
    if is_vertical_axis:
        # Create N x 1 column vector
        output_grid = np.array(sorted_colors, dtype=int).reshape(num_colors, 1)
    else:
        # Create 1 x N row vector
        output_grid = np.array(sorted_colors, dtype=int).reshape(1, num_colors)

    return output_grid