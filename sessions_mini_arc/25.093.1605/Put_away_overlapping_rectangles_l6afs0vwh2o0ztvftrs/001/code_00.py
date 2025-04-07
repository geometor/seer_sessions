import numpy as np
from collections import defaultdict

"""
Identifies the two distinct non-zero colored objects in the input 5x5 grid.
For each object, calculates its bounding box, dimensions (height, width), and centroid.
Determines the relative spatial position of the two objects based on their centroids (higher/lower, lefter/righter).
Assigns each object to a corner of the output grid based on its relative position:
- Higher and lefter object goes to TopLeft (TL).
- Higher and righter object goes to TopRight (TR).
- Lower and lefter object goes to BottomLeft (BL).
- Lower and righter object goes to BottomRight (BR).
The other object is assigned to the diagonally opposite corner.
Creates a new 5x5 output grid initialized with zeros.
Draws each object as a solid rectangle in its assigned corner of the output grid, using the object's color and the dimensions derived from its input bounding box.
"""

def find_objects(grid):
    """Finds all pixels associated with each non-zero color."""
    objects = defaultdict(list)
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != 0:
                objects[color].append((r, c))
    # Ensure we only return data for the first two distinct non-zero colors found
    found_colors = sorted([color for color in objects.keys() if color != 0])
    if len(found_colors) > 2:
       # According to the description, there are exactly two non-zero objects.
       # If more are found, we might need a different rule, but for now,
       # we'll stick to the first two distinct non-zero colors encountered.
       # A simple way is just taking the two smallest non-zero colors.
       # Or process based on order found - let's assume the dictionary keys
       # give a reasonable order or sort them.
       object_data = {color: objects[color] for color in found_colors[:2]}
    elif len(found_colors) < 2:
        # Handle cases with less than 2 objects if necessary, though problem implies 2.
        # For now, return what was found.
        object_data = objects
    else:
       object_data = {color: objects[color] for color in found_colors}


    return object_data

def calculate_properties(color, pixels):
    """Calculates bounding box, dimensions, and centroid for a set of pixels."""
    if not pixels:
        return None

    rows = [p[0] for p in pixels]
    cols = [p[1] for p in pixels]

    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)

    height = max_row - min_row + 1
    width = max_col - min_col + 1

    # Using float for centroid calculation
    centroid_row = sum(rows) / len(pixels)
    centroid_col = sum(cols) / len(pixels)

    return {
        'color': color,
        'pixels': pixels,
        'bounding_box': (min_row, min_col, max_row, max_col),
        'dimensions': (height, width),
        'centroid': (centroid_row, centroid_col)
    }

def draw_rectangle(output_grid, color, height, width, corner):
    """Draws a solid rectangle in the specified corner of the output grid."""
    rows, cols = output_grid.shape # Should be 5, 5

    if corner == 'TL': # TopLeft
        start_row, end_row = 0, height
        start_col, end_col = 0, width
    elif corner == 'TR': # TopRight
        start_row, end_row = 0, height
        start_col, end_col = cols - width, cols
    elif corner == 'BL': # BottomLeft
        start_row, end_row = rows - height, rows
        start_col, end_col = 0, width
    elif corner == 'BR': # BottomRight
        start_row, end_row = rows - height, rows
        start_col, end_col = cols - width, cols
    else:
        raise ValueError("Invalid corner specified")

    # Ensure indices are within bounds (though calculated dimensions should fit)
    start_row = max(0, start_row)
    end_row = min(rows, end_row)
    start_col = max(0, start_col)
    end_col = min(cols, end_col)

    output_grid[start_row:end_row, start_col:end_col] = color


def transform(input_grid):
    """
    Transforms the input grid by identifying two objects, calculating their
    properties, determining their relative positions, and drawing them as
    solid rectangles in opposite corners of the output grid.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # Initialize output_grid with zeros
    output_grid = np.zeros_like(input_np)

    # Find the pixels for each non-zero object
    object_pixels = find_objects(input_np)

    if len(object_pixels) != 2:
        # Handle error or unexpected input: problem statement guarantees 2 objects.
        # Returning the empty grid might be one option, or raise error.
        print(f"Warning: Expected 2 objects, found {len(object_pixels)}. Returning empty grid.")
        return output_grid.tolist() # Convert back to list of lists if needed

    # Calculate properties for the two objects
    colors = list(object_pixels.keys())
    obj1_props = calculate_properties(colors[0], object_pixels[colors[0]])
    obj2_props = calculate_properties(colors[1], object_pixels[colors[1]])

    # Determine relative positioning based on centroids
    centroid1_r, centroid1_c = obj1_props['centroid']
    centroid2_r, centroid2_c = obj2_props['centroid']

    # Assign corners based on relative position
    # Note: Smaller row index means 'higher', smaller col index means 'lefter'
    if centroid1_r < centroid2_r: # Object 1 is higher
        if centroid1_c < centroid2_c: # Object 1 is higher and lefter
            corner1 = 'TL'
            corner2 = 'BR'
        else: # Object 1 is higher and righter (or same column)
            corner1 = 'TR'
            corner2 = 'BL'
    else: # Object 1 is lower (or same row)
        if centroid1_c < centroid2_c: # Object 1 is lower and lefter
            corner1 = 'BL'
            corner2 = 'TR'
        else: # Object 1 is lower and righter (or same row/column)
            corner1 = 'BR'
            corner2 = 'TL'

    # Draw the rectangles in the output grid
    h1, w1 = obj1_props['dimensions']
    draw_rectangle(output_grid, obj1_props['color'], h1, w1, corner1)

    h2, w2 = obj2_props['dimensions']
    draw_rectangle(output_grid, obj2_props['color'], h2, w2, corner2)

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()
