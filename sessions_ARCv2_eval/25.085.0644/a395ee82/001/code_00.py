import numpy as np
from scipy.ndimage import label, find_objects
from collections import Counter

"""
1. Determine the background color by finding the most frequent color in the input grid.
2. Identify all connected objects (groups of same-colored, adjacent pixels) that are not the background color.
3. Identify the 'pattern object' as the largest connected object found in step 2. Record its shape (pixel coordinates relative to its bounding box top-left), color, and bounding box.
4. Identify the 'marker color' as the color of the smallest connected non-background object(s) found in step 2.
5. Find the coordinates of all pixels in the input grid that have the 'marker color'. These are the 'marker locations'.
6. Create a new output grid with the same dimensions as the input grid, filled entirely with the background color.
7. Place the original 'pattern object' onto the output grid using its original bounding box coordinates.
8. For each 'marker location' identified in step 5:
    a. Calculate the center coordinates of the 'pattern object's' bounding box relative to its top-left corner (e.g., `center_row = height // 2`, `center_col = width // 2`).
    b. Determine the target top-left coordinate on the output grid for placing the pattern, such that the pattern's calculated relative center aligns with the current 'marker location'. The target top-left is `(marker_row - center_row, marker_col - center_col)`.
    c. Copy the pixels forming the 'pattern object' (using the relative coordinates from step 3) onto the output grid, starting at the calculated target top-left coordinate. Overwrite any existing pixels in the output grid during this copy operation, ensuring coordinates stay within grid bounds.
9. The resulting grid is the final output.
"""

def find_connected_objects(grid):
    """
    Finds all connected objects in the grid.
    Returns a dictionary where keys are object IDs (1-based) and
    values are dictionaries containing 'color', 'coords', 'size', 'bbox'.
    """
    unique_colors = np.unique(grid)
    objects = {}
    current_label = 0

    for color in unique_colors:
        # Create a binary mask for the current color
        mask = (grid == color)
        # Label connected components for this color
        labeled_array, num_features = label(mask)

        if num_features > 0:
            # Find the locations (slices) of each labeled object
            locations = find_objects(labeled_array)
            for i in range(num_features):
                obj_label = i + 1
                obj_slice = locations[i]
                # Extract coordinates within the bounding box slice
                coords_in_slice = np.argwhere(labeled_array[obj_slice] == obj_label)
                # Convert to absolute grid coordinates
                abs_coords = coords_in_slice + np.array([obj_slice[0].start, obj_slice[1].start])

                current_label += 1
                objects[current_label] = {
                    'color': color,
                    'coords': abs_coords,
                    'size': len(abs_coords),
                    'bbox': obj_slice  # Store the slice directly
                }
    return objects


def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_grid = np.array(input_grid)
    height, width = input_grid.shape

    # 1. Determine the background color
    background_color = Counter(input_grid.flatten()).most_common(1)[0][0]

    # 2. Identify all connected non-background objects
    all_objects = find_connected_objects(input_grid)
    non_background_objects = {
        obj_id: obj_data
        for obj_id, obj_data in all_objects.items()
        if obj_data['color'] != background_color
    }

    if not non_background_objects:
        # Handle case with no non-background objects (e.g., return input or background)
        return input_grid.copy()

    # 3. Identify the 'pattern object' (largest)
    pattern_obj_id = max(non_background_objects, key=lambda k: non_background_objects[k]['size'])
    pattern_obj = non_background_objects[pattern_obj_id]
    pattern_color = pattern_obj['color']
    pattern_bbox = pattern_obj['bbox']
    pattern_coords_absolute = pattern_obj['coords']

    # Calculate pattern shape relative to its bounding box top-left
    pattern_bbox_top_left = np.array([pattern_bbox[0].start, pattern_bbox[1].start])
    pattern_coords_relative = pattern_coords_absolute - pattern_bbox_top_left

    # 4. Identify the 'marker color' (color of smallest object(s))
    min_size = min(obj['size'] for obj in non_background_objects.values())
    # Taking the first color found with min_size. Assumes consistency if multiple exist.
    marker_color = next(obj['color'] for obj in non_background_objects.values() if obj['size'] == min_size)

    # 5. Find the coordinates of all 'marker locations'
    marker_locations = np.argwhere(input_grid == marker_color)

    # 6. Create a new output grid filled with the background color
    output_grid = np.full_like(input_grid, background_color)

    # 7. Place the original 'pattern object' onto the output grid
    for r, c in pattern_coords_absolute:
        if 0 <= r < height and 0 <= c < width:
             output_grid[r, c] = pattern_color

    # 8. For each 'marker location', copy the pattern centered on it
    # a. Calculate the relative center of the pattern's bounding box
    bbox_height = pattern_bbox[0].stop - pattern_bbox[0].start
    bbox_width = pattern_bbox[1].stop - pattern_bbox[1].start
    center_dr = bbox_height // 2
    center_dc = bbox_width // 2

    for marker_r, marker_c in marker_locations:
        # b. Determine the target top-left for placing the pattern
        target_top_left_r = marker_r - center_dr
        target_top_left_c = marker_c - center_dc

        # c. Copy the pattern pixels relative to the target top-left
        for rel_r, rel_c in pattern_coords_relative:
            output_r = target_top_left_r + rel_r
            output_c = target_top_left_c + rel_c

            # Ensure the pixel is within the grid bounds before painting
            if 0 <= output_r < height and 0 <= output_c < width:
                output_grid[output_r, output_c] = pattern_color

    # 9. Return the resulting grid
    return output_grid.tolist() # Convert back to list of lists if needed by ARC environment