"""
1.  **Identify Shapes:** Locate all connected components (shapes) of green (value 3) pixels in the input grid. Each distinct connected component will be treated as a separate object.

2.  **Determine Output Color based on shape id**:
    *   If the shape looks similar to a reversed "L", change the color to red (2).
    *   If the shape is a horizontal or vertical line, change to blue (1).
    *   If the shape looks like "U", change the color to magenta (6).

3.  **Recolor Shapes:** For each identified shape:
    *   Replace all pixels of color green (3) with respective new colors.

4.  **Preserve Background:** Leave all pixels with a value of 0 (white) unchanged.

5.  **Output:** Create an output grid identical in dimensions to the input grid, with recolored shapes and the unchanged background.
"""

import numpy as np
from scipy.ndimage import label, measurements

def find_shapes(grid, color):
    """Find connected components of a specific color."""
    colored_pixels = (grid == color).astype(int)
    labeled_array, num_features = label(colored_pixels)
    return labeled_array, num_features

def get_shape_coords(labeled_array, shape_label):
    """Get coordinates of pixels belonging to a specific shape."""
    return np.where(labeled_array == shape_label)

def is_line(coords):
    """Determine if a shape is approximately a line (horizontal or vertical)."""
    rows = coords[0]
    cols = coords[1]
    if len(set(rows)) == 1 or len(set(cols)) == 1:
        return True

    # Check for near-linearity allowing some tolerance
    if len(rows) > 2:  # Check only if more than 2 points to avoid division by zero/small numbers
      row_range = np.max(rows) - np.min(rows)
      col_range = np.max(cols) - np.min(cols)

      # If primarily horizontal or vertical (with a small tolerance)
      if (row_range > 0 and col_range/max(1,row_range) < 0.2) or \
         (col_range > 0 and row_range/max(1,col_range) < 0.2):
          return True

    return False

def is_reversed_L(coords):
    """
    Determine if a shape resembles a reversed "L". This is a simplified check
    and might need refinement for more complex cases or rotations.

    A simple heuristic: check if it has two "arms" that meet at a near-90 degree angle.
    This is approximated by looking for distinct row and column clusters.
    """
    rows = coords[0]
    cols = coords[1]
    if len(rows) < 3 : return False

    # divide into 3 segments and calculate the center of mass for each one.
    indices = np.argsort(rows)
    rows_sorted = rows[indices]
    cols_sorted = cols[indices]
    
    segment_size = len(rows) // 3

    if (segment_size == 0): return False
    
    segments = []
    for i in range(3):
        start_index = i * segment_size
        end_index = (i + 1) * segment_size if i < 2 else len(rows)
        segments.append((rows_sorted[start_index:end_index], cols_sorted[start_index:end_index]))
    
    centroids = []
    for segment in segments:
      centroids.append((np.mean(segment[0]), np.mean(segment[1])))

    # Check if the center point connects the other two and that those lines are orthogonal
    if len(centroids) == 3:
        # Check if the middle point is near the first point in either row/col
        dist1_row = abs(centroids[0][0]- centroids[1][0]) < 2
        dist1_col = abs(centroids[0][1] - centroids[1][1]) < 2
        dist2_row = abs(centroids[1][0]- centroids[2][0]) < 2
        dist2_col = abs(centroids[1][1] - centroids[2][1]) < 2

        if dist1_row and dist2_col or dist1_col and dist2_row :
            return True

    return False

def is_U(coords):
    """
    Determine if shape resembles "U". Very basic heuristic.  Could use refinement
    """
    rows = coords[0]
    cols = coords[1]

    if len(rows) < 3: return False # Need at least 3 pixels

    min_row, max_row = np.min(rows), np.max(rows)
    min_col, max_col = np.min(cols), np.max(cols)

    # Check if more pixels are towards the top (smaller row indices), suggesting a "U" shape.
    top_count = np.sum(rows == min_row)
    bottom_count = np.sum(rows == max_row)

    if top_count > 1 and bottom_count > 1:
        return True


    return False

def transform(input_grid):
    """
    Transforms the input grid according to the observed rules:
    - Green shapes are identified and recolored based on their shape.
    - Background (white, 0) remains unchanged.
    """
    # initialize output_grid
    output_grid = np.copy(input_grid)
    labeled_array, num_features = find_shapes(input_grid, 3)

    # change output pixels
    for i in range(1, num_features + 1):
        coords = get_shape_coords(labeled_array, i)
        if is_line(coords):
            output_grid[coords] = 1  # Blue
        elif is_reversed_L(coords):
            output_grid[coords] = 2  # Red
        elif is_U(coords):
            output_grid[coords] = 6 # Magenta
        else:
            #default to blue
            output_grid[coords] = 1


    return output_grid