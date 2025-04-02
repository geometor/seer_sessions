import numpy as np
from scipy.ndimage import label, find_objects as nd_find_objects

"""
Transformation Rule:
1. Identify the single contiguous non-background (non-white/0) object in the input grid.
2. Determine the dimensions (height and width) of its minimal bounding box.
3. Compare the height and width of the bounding box.
4. If the height is strictly greater than the width, the object is translated 3 cells down.
5. Otherwise (if height is less than or equal to width), the object is translated 3 cells right.
6. The output grid contains the translated object on the original background color.
"""

def find_single_object_pixels_and_color(grid):
    """Finds the coordinates and color of the single non-background object."""
    non_background_pixels = np.where(grid != 0)
    if len(non_background_pixels[0]) == 0:
        return None, -1 # No object found

    # Assume the first non-background pixel belongs to the object
    start_row, start_col = non_background_pixels[0][0], non_background_pixels[1][0]
    object_color = grid[start_row, start_col]

    # Use labeling to find all connected components of this color
    labeled_grid, num_labels = label(grid == object_color)

    # Find the label corresponding to our start pixel
    object_label = labeled_grid[start_row, start_col]

    # Get all coordinates for this specific label
    object_pixels = set(zip(*np.where(labeled_grid == object_label)))

    # Verify it's the only non-background object
    all_non_background_coords = set(zip(*non_background_pixels))
    if all_non_background_coords != object_pixels:
        # This indicates multiple objects or colors, which contradicts the examples' pattern
        # For now, proceed assuming the largest object if ambiguity arises,
        # but the examples suggest only one object.
        # Let's refine based on the assumption of a single object.
         pass # Stick with the first found connected component matching the first non-zero pixel

    return object_pixels, object_color


def get_bounding_box_dims(obj_pixels):
    """Calculates the height and width of the bounding box for a set of pixels."""
    if not obj_pixels:
        return 0, 0
    rows = [r for r, c in obj_pixels]
    cols = [c for r, c in obj_pixels]
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    return height, width

def translate_object(obj_pixels, vector):
    """Applies a translation vector to object pixels."""
    dr, dc = vector
    translated_pixels = set()
    for r, c in obj_pixels:
        translated_pixels.add((r + dr, c + dc))
    return translated_pixels

def transform(input_grid):
    """
    Applies the transformation rule: Translates the single non-background object
    down by 3 if its bounding box height > width, otherwise right by 3.
    """
    # Convert input to numpy array
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # Initialize output grid with background color (0)
    output_np = np.zeros_like(input_np)

    # 1. Identify the single non-background object and its color
    object_pixels, object_color = find_single_object_pixels_and_color(input_np)

    # If no object is found, return the empty grid
    if object_pixels is None:
        return output_np.tolist()

    # 2. Calculate bounding box dimensions
    height, width = get_bounding_box_dims(object_pixels)

    # 3. & 4. & 5. Determine translation vector based on dimensions
    if height > width:
        translation_vector = (3, 0) # Move down
    else:
        translation_vector = (0, 3) # Move right

    # 6. & 7. Calculate new object positions
    translated_object_pixels = translate_object(object_pixels, translation_vector)

    # 8. Place the translated object in the output grid
    for r, c in translated_object_pixels:
        # Ensure the new position is within the grid boundaries
        if 0 <= r < rows and 0 <= c < cols:
            output_np[r, c] = object_color

    # Convert output back to list of lists
    return output_np.tolist()