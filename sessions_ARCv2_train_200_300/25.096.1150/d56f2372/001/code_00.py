"""
Identify all distinct connected objects (groups of cells with the same non-zero color, connected 8-directionally) in the input grid.
For each object, determine its color, size (number of cells), and bounding box (minimum row, maximum row, minimum column, maximum column).

Apply the following selection criteria:
1. Find the object whose bounding box starts at the highest row (minimum row index). If there's a tie, choose the one starting at the leftmost column (minimum column index). Call this the 'highest-leftmost' object.
2. Find the minimum color value (`min_c`) present among all objects and the maximum size (`max_s`) among all objects.
3. Check if there is exactly one object that has *both* the color `min_c` AND the size `max_s`. Call this the 'special' object.
4. If such a unique 'special' object exists AND it is *different* from the 'highest-leftmost' object, then select the 'special' object.
5. Otherwise (either no unique 'special' object exists, or it's the same as the 'highest-leftmost' object), select the 'highest-leftmost' object.

Create the output grid by cropping the input grid to the bounding box of the selected object, containing only the cells of that selected object (maintaining their original color), with all other cells as 0.
"""

import numpy as np
from scipy.ndimage import label, find_objects

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Selects and extracts a specific object from the input grid based on position, color, and size criteria.

    Args:
        input_grid: A 2D list of integers representing the input grid.

    Returns:
        A 2D list of integers representing the extracted object within its minimal bounding box.
    """
    input_array = np.array(input_grid, dtype=int)
    if input_array.size == 0 or np.all(input_array == 0):
        return [] # Handle empty or all-zero input

    objects = []
    unique_colors = np.unique(input_array[input_array > 0])

    # 1. Find all objects and their properties
    for color in unique_colors:
        # Create a binary mask for the current color
        mask = (input_array == color)
        # Label connected components (8-connectivity)
        labeled_array, num_features = label(mask, structure=np.ones((3,3), dtype=bool))

        # Get slices representing bounding boxes
        object_slices = find_objects(labeled_array)

        for i in range(num_features):
            obj_label = i + 1
            # Extract coordinates and bounding box slice
            slices = object_slices[i]
            coords = np.argwhere(labeled_array[slices] == obj_label)
            # Adjust coordinates relative to the full grid
            coords[:, 0] += slices[0].start
            coords[:, 1] += slices[1].start

            min_row = slices[0].start
            max_row = slices[0].stop - 1
            min_col = slices[1].start
            max_col = slices[1].stop - 1
            size = coords.shape[0]

            objects.append({
                'color': color,
                'coords': coords,
                'bbox': (min_row, max_row, min_col, max_col),
                'size': size,
                'id': (color, min_row, min_col) # Simple ID for comparison
            })

    if not objects:
        return [] # No non-zero objects found

    # 2. Find the 'highest-leftmost' object
    highest_leftmost_object = min(objects, key=lambda obj: (obj['bbox'][0], obj['bbox'][2]))

    # 3. Find min_color and max_size
    min_c = min(obj['color'] for obj in objects)
    max_s = max(obj['size'] for obj in objects)

    # 4. Find 'special' objects (min color AND max size)
    special_candidates = [obj for obj in objects if obj['color'] == min_c and obj['size'] == max_s]

    # 5. Apply selection logic
    selected_object = highest_leftmost_object # Default selection
    if len(special_candidates) == 1:
        special_object = special_candidates[0]
        # Check if the unique special object is different from the highest-leftmost
        if special_object['id'] != highest_leftmost_object['id']:
             selected_object = special_object # Select the special object due to exception rule

    # 6. Create output grid
    min_row, max_row, min_col, max_col = selected_object['bbox']
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    output_array = np.zeros((height, width), dtype=int)

    # Populate the output grid with the selected object's pixels
    for r, c in selected_object['coords']:
        output_array[r - min_row, c - min_col] = selected_object['color']

    return output_array.tolist()
