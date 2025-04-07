import numpy as np
from collections import deque

"""
Identifies two distinct non-zero objects based on their unique colors in the input grid.
Retains the object with the numerically higher color value and discards the other.
Places the retained object's pixels onto an initially empty output grid.
Adds a single pixel to the output grid whose color matches the retained object's color.
The position of this new pixel depends on the relative vertical positions of the centers of the retained and discarded objects:
- If the retained object's topmost row is strictly less than the discarded object's topmost row (retained is 'above'):
    The new pixel is placed at (discarded_object.topmost_row, retained_object.anchor_col).
- Otherwise (retained object is 'below' or at the same level):
    The new pixel is placed at (discarded_object.lowest_row, discarded_object.anchor_col).
The anchor column (anchor_col) is the column index of the object's top-most, left-most pixel.
"""

def find_objects_by_color(grid):
    """
    Finds connected components based on unique non-zero colors.

    Args:
        grid: A 2D numpy array representing the input grid.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        and contains:
        - 'pixels': A set of (row, col) tuples for the object's pixels.
        - 'color': The integer color of the object.
        - 'topmost_row': The minimum row index of the object.
        - 'lowest_row': The maximum row index of the object.
        - 'anchor_col': The column index of the top-most, left-most pixel.
                        Returns None if no pixels are found (should not happen for non-empty objects).
    """
    rows, cols = grid.shape
    visited = set()
    objects = []
    unique_colors = np.unique(grid[grid != 0])

    for color in unique_colors:
        object_pixels = set()
        min_row = rows # Initialize min_row to max possible value
        max_row = -1   # Initialize max_row to min possible value
        anchor_candidates = [] # Store potential anchor points (top-most pixels)

        for r in range(rows):
            for c in range(cols):
                if grid[r, c] == color:
                    object_pixels.add((r, c))
                    if r < min_row:
                        min_row = r
                        anchor_candidates = [(r, c)] # New topmost row, reset candidates
                    elif r == min_row:
                        anchor_candidates.append((r, c)) # Add candidate on same topmost row
                    max_row = max(max_row, r)

        if not object_pixels:
            continue # Skip if no pixels found for this color

        # Determine the anchor point (top-most, then left-most)
        anchor_candidates.sort(key=lambda item: item[1]) # Sort by column
        anchor_point = anchor_candidates[0]
        anchor_col = anchor_point[1]

        objects.append({
            'pixels': object_pixels,
            'color': color,
            'topmost_row': min_row,
            'lowest_row': max_row,
            'anchor_col': anchor_col
        })

    return objects

def transform(input_grid_list):
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid_list: A list of lists representing the input grid.

    Returns:
        A list of lists representing the output grid.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    rows, cols = input_grid.shape

    # Initialize output grid with background color 0
    output_grid = np.zeros_like(input_grid)

    # 1. Identify the distinct non-zero objects by color
    objects = find_objects_by_color(input_grid)

    # Expecting exactly two objects based on the problem description
    if len(objects) != 2:
        print(f"Warning: Expected 2 objects based on color, found {len(objects)}. Returning empty grid.")
        return output_grid.tolist()

    # 2. Determine which object is retained (higher color) and which is discarded
    obj_A = objects[0]
    obj_B = objects[1]

    if obj_A['color'] > obj_B['color']:
        retained_object = obj_A
        discarded_object = obj_B
    else: # obj_B['color'] > obj_A['color'] (assuming colors are distinct)
        retained_object = obj_B
        discarded_object = obj_A

    # 3. Extract properties needed for the transformation
    retained_color = retained_object['color']
    retained_pixels = retained_object['pixels']
    retained_anchor_col = retained_object['anchor_col']
    retained_topmost_row = retained_object['topmost_row']

    discarded_topmost_row = discarded_object['topmost_row']
    discarded_lowest_row = discarded_object['lowest_row']
    discarded_anchor_col = discarded_object['anchor_col']


    # 4. Copy the retained object to the output grid
    for r, c in retained_pixels:
        # Bounds check (good practice, though pixels should be within bounds)
        if 0 <= r < rows and 0 <= c < cols:
            output_grid[r, c] = retained_color

    # 5. Determine the position for the new pixel based on relative vertical position
    if retained_topmost_row < discarded_topmost_row:
        # Retained object is above the discarded object
        new_pixel_row = discarded_topmost_row
        new_pixel_col = retained_anchor_col
    else:
        # Retained object is below or at the same level as the discarded object
        new_pixel_row = discarded_lowest_row
        new_pixel_col = discarded_anchor_col

    # 6. Place the single derived pixel
    # Bounds check for the new pixel placement
    if 0 <= new_pixel_row < rows and 0 <= new_pixel_col < cols:
        output_grid[new_pixel_row, new_pixel_col] = retained_color
    else:
        # Handle cases where the calculated position is outside the grid if necessary
        print(f"Warning: Calculated new pixel position ({new_pixel_row}, {new_pixel_col}) is out of bounds.")

    # Return the grid as a list of lists
    return output_grid.tolist()