import numpy as np

"""
Identify all unique non-white colors in the input grid.
For each unique color, find its minimal bounding box and calculate the area.
Sort the colors in descending order based on their bounding box areas.
Determine the size of the square output grid:
  - If the smallest bounding box area is 1, size = (2 * num_colors) - 1.
  - Otherwise, size = 2 * num_colors.
Construct the output grid by drawing concentric square layers.
Start with the color corresponding to the largest bounding box area for the outermost layer.
Subsequent inner layers use colors corresponding to progressively smaller bounding box areas.
The innermost layer uses the color with the smallest bounding box area.
"""

def _find_colored_pixels(grid, color):
    """Finds all coordinates (row, col) of a given color in the grid."""
    coords = []
    for r, row in enumerate(grid):
        for c, pixel in enumerate(row):
            if pixel == color:
                coords.append((r, c))
    return coords

def _get_bounding_box(coords):
    """Calculates the bounding box (min_row, min_col, max_row, max_col) for a list of coordinates."""
    if not coords:
        return None
    min_r = min(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_r = max(r for r, c in coords)
    max_c = max(c for r, c in coords)
    return min_r, min_c, max_r, max_c

def _get_bounding_box_area(bbox):
    """Calculates the area of a bounding box."""
    if bbox is None:
        return 0
    min_r, min_c, max_r, max_c = bbox
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    return height * width

def transform(input_grid):
    """
    Transforms the input grid based on the bounding box areas of colored objects.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    unique_colors = np.unique(input_np[input_np != 0]) # Find unique non-white colors

    if len(unique_colors) == 0:
        # Handle cases with no colored objects if necessary, maybe return empty or specific size grid?
        # Based on examples, this case likely doesn't occur or should return a small default grid.
        # Let's assume at least one color exists based on examples. If not, might need clarification.
        # Returning a 1x1 white grid seems safe if no colors are found.
         return [[0]]


    color_data = []
    # Calculate bounding box and area for each unique color
    for color in unique_colors:
        coords = _find_colored_pixels(input_np, color)
        bbox = _get_bounding_box(coords)
        area = _get_bounding_box_area(bbox)
        color_data.append({'color': color, 'area': area})

    # Sort colors by area in descending order
    sorted_colors_data = sorted(color_data, key=lambda x: x['area'], reverse=True)
    sorted_colors = [item['color'] for item in sorted_colors_data]
    min_area = sorted_colors_data[-1]['area']
    n = len(sorted_colors)

    # Determine output grid size
    if min_area == 1:
        s = (2 * n) - 1
    else:
        s = 2 * n

    # Initialize output grid (filled with the outermost color initially)
    output_grid = np.full((s, s), sorted_colors[0], dtype=int)

    # Fill concentric layers from outside in (or inside out, doesn't matter due to overwriting)
    # We iterate from the outermost layer (k=0) inwards.
    # The fill for layer k covers the rectangle from (k, k) to (s-1-k, s-1-k).
    # This approach fills outwards, ensuring inner layers overwrite outer ones correctly.
    for k in range(n):
        color_to_fill = sorted_colors[k]
        # Define the bounds for the current layer's fill area
        start_row, start_col = k, k
        end_row, end_col = s - 1 - k, s - 1 - k

        # Ensure bounds are valid (handles the center pixel/square)
        if start_row <= end_row and start_col <= end_col:
             output_grid[start_row:end_row+1, start_col:end_col+1] = color_to_fill


    # Convert back to list of lists for the required output format
    return output_grid.tolist()