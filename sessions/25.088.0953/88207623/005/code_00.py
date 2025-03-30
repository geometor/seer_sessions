import numpy as np
from scipy.ndimage import label
from scipy.spatial.distance import cdist
import math

"""
Transformation Rule:

1.  **Identify Base Shapes:** Find all connected components (objects) in the input grid consisting solely of yellow (4) and red (2) pixels, ensuring each component includes at least one red pixel. Record the locations of all pixels in each shape, and the locations of the red pixels (sorted top-to-bottom, left-to-right).
2.  **Identify Marker Pixels:** Locate all single pixels in the grid that are *not* white (0), *not* yellow (4), *not* red (2), and do *not* belong to any identified valid base shape (a shape containing red). These are the marker pixels. Record their location and color.
3.  **Associate Markers with Shapes:** For each marker pixel, determine the base shape it is closest to (based on minimum Euclidean distance between the marker's location and any red pixel within the shape). Ensure each marker is associated with at most one shape (the closest), and each shape is associated with at most one marker (the closest one to it).
4.  **Determine Fill Properties:** For each base shape successfully associated with a marker:
    a.  The `fill_color` is the color of the associated marker pixel.
    b.  The `fill_direction` is determined by the marker's horizontal position relative to the shape's topmost, leftmost red pixel. If the marker's column index is greater than the red pixel's column index, the direction is 'right' (+1). Otherwise, it's 'left' (-1).
5.  **Perform Fill:** Create a copy of the input grid. For each associated (shape, marker) pair, iterate through every red pixel `(r, c)` within that shape. Starting from the column `c + fill_direction`, move horizontally in the `fill_direction`. At each step `fill_c`, check the pixel at `(r, fill_c)` in the *original input grid*. If the location is within bounds and the pixel is white (0), change the corresponding pixel in the *output grid* to the `fill_color`. Stop filling along row `r` (originating from that specific red pixel `(r, c)`) as soon as an originally non-white (1-9) pixel is encountered or the grid boundary is reached.
6.  **Output:** Return the modified grid after all fills are completed.
"""

# ================================= HELPER FUNCTIONS =================================

def find_objects_and_markers(grid):
    """
    Identifies base shapes (yellow/red containing red) and valid marker pixels.

    Args:
        grid: The input numpy array.

    Returns:
        A tuple: (shapes, markers)
        shapes: A dictionary where keys are shape IDs (starting from 1) and
                values are dictionaries {'all_pixels': set(), 'red_pixels': list()}.
                Red pixels are sorted. Only includes shapes with at least one red pixel.
        markers: A list of dictionaries {'loc': tuple(r, c), 'color': int}.
                 Markers are non-white, non-yellow, non-red, and not part of a valid base shape.
    """
    height, width = grid.shape
    # Mask for pixels that could potentially be part of a base shape
    base_mask = (grid == 4) | (grid == 2) # yellow or red
    # Label connected components in the mask
    labeled_shapes, num_potential_shapes = label(base_mask)

    # Store information about each potential shape component
    potential_shapes = {}
    for r in range(height):
        for c in range(width):
            shape_id = labeled_shapes[r, c]
            if shape_id > 0: # Pixel belongs to a potential shape
                loc = (r, c)
                if shape_id not in potential_shapes:
                    potential_shapes[shape_id] = {'all_pixels': set(), 'red_pixels': []}
                potential_shapes[shape_id]['all_pixels'].add(loc)
                # Record red pixels within the shape
                if grid[r, c] == 2:
                    potential_shapes[shape_id]['red_pixels'].append(loc)

    # Filter out shapes that do not contain any red pixels
    # These are the 'valid' base shapes for the transformation
    valid_shapes = {}
    for shape_id, data in potential_shapes.items():
        if data['red_pixels']:
            # Sort red pixels: top-to-bottom, then left-to-right
            data['red_pixels'].sort()
            valid_shapes[shape_id] = data

    # Collect the set of all pixels belonging to any valid base shape
    all_valid_base_pixels = set()
    for shape_id, data in valid_shapes.items():
        all_valid_base_pixels.update(data['all_pixels'])

    # Find marker pixels
    markers = []
    disallowed_marker_colors = {0, 2, 4} # white, red, yellow
    for r in range(height):
        for c in range(width):
            loc = (r, c)
            color = grid[r, c]
            # A marker must not be white/red/yellow AND must not be part of a valid base shape
            if color not in disallowed_marker_colors and loc not in all_valid_base_pixels:
                markers.append({'loc': loc, 'color': color})

    return valid_shapes, markers


def associate_markers_to_shapes(shapes, markers):
    """
    Associates each marker to its closest shape based on red pixel distance.
    Ensures each shape is associated with at most one (the closest) marker,
    and each marker is associated with at most one (the closest) shape.

    Args:
        shapes: Dictionary of valid shapes from find_objects_and_markers.
        markers: List of valid markers from find_objects_and_markers.

    Returns:
        A dictionary mapping shape_id to the associated marker dictionary
        {'loc': tuple(r, c), 'color': int}.
    """
    if not shapes or not markers:
        return {}

    # --- Step 1: Find the closest shape for each marker ---
    marker_closest_shape = {} # marker_idx -> {'shape_id': int, 'dist': float, 'red_loc': tuple}

    # Prepare lists for distance calculation
    all_red_pixels = []
    red_pixel_shape_map = {} # Map red_pixel_loc back to its shape_id
    for shape_id, data in shapes.items():
        for red_loc in data['red_pixels']:
            all_red_pixels.append(red_loc)
            red_pixel_shape_map[red_loc] = shape_id

    if not all_red_pixels: # No red pixels found in any valid shape
        return {}

    marker_locs = [m['loc'] for m in markers]

    # Calculate distances: rows=markers, cols=red_pixels
    dist_matrix = cdist(marker_locs, all_red_pixels, metric='euclidean')

    # Determine closest red pixel (and thus shape) for each marker
    for i, marker in enumerate(markers):
        if dist_matrix.shape[1] == 0: continue # Should be caught by 'if not all_red_pixels'
        min_dist_marker = np.min(dist_matrix[i, :])
        # Find all red pixels at this minimum distance
        closest_red_pixel_indices = np.where(dist_matrix[i, :] == min_dist_marker)[0]
        # Tie-breaking for marker: Choose the red pixel that comes first in the sorted list
        # (which corresponds to the smallest index in closest_red_pixel_indices)
        closest_red_pixel_idx = closest_red_pixel_indices[0]
        closest_red_loc = all_red_pixels[closest_red_pixel_idx]
        closest_shape_id = red_pixel_shape_map[closest_red_loc]
        marker_closest_shape[i] = {
            'shape_id': closest_shape_id,
            'dist': min_dist_marker,
            'red_loc': closest_red_loc # Store which red pixel was closest
        }

    # --- Step 2: Assign markers to shapes, ensuring one marker per shape (the closest) ---
    shape_potential_markers = {} # shape_id -> list of {'marker_idx': int, 'dist': float}
    for marker_idx, assoc_info in marker_closest_shape.items():
        shape_id = assoc_info['shape_id']
        dist = assoc_info['dist']
        if shape_id not in shape_potential_markers:
            shape_potential_markers[shape_id] = []
        shape_potential_markers[shape_id].append({'marker_idx': marker_idx, 'dist': dist})

    # --- Step 3: Finalize associations by picking the closest marker for each shape ---
    final_associations = {} # shape_id -> {'marker': marker_dict, 'dist': min_dist}
    for shape_id, potential_marker_list in shape_potential_markers.items():
        # Sort potential markers for this shape by distance (ascending)
        potential_marker_list.sort(key=lambda x: x['dist'])
        # The closest marker is the first one in the sorted list
        closest_marker_info = potential_marker_list[0]
        marker_idx = closest_marker_info['marker_idx']
        min_dist = closest_marker_info['dist']
        # Store the association
        final_associations[shape_id] = {'marker': markers[marker_idx], 'dist': min_dist}

    # Return only the marker info keyed by shape_id
    return {shape_id: data['marker'] for shape_id, data in final_associations.items()}

# ================================= MAIN TRANSFORM FUNCTION =================================

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the fill transformation based on base shapes and marker pixels.

    Identifies base shapes (yellow/red blocks containing red pixels) and
    isolated marker pixels (non-white, non-yellow, non-red).
    Associates each marker with the nearest base shape (one-to-one mapping).
    For each associated shape, determines a fill color (from the marker) and
    direction (marker position relative to shape's top-leftmost red pixel).
    Performs a horizontal fill originating from each red pixel of the shape,
    replacing originally background (white) pixels in the output grid with the
    fill color until an originally non-background pixel or grid boundary is hit.
    """
    # Initialize output_grid as a copy of the input
    output_grid = input_grid.copy()
    height, width = output_grid.shape

    # 1. & 2. Identify Base Shapes (yellow/red with red) and Valid Marker Pixels
    shapes, markers = find_objects_and_markers(input_grid) # Use input_grid for analysis

    # Early exit if no shapes or markers are found
    if not shapes or not markers:
        return output_grid

    # 3. Associate Markers with Shapes (closest, one-to-one)
    shape_marker_associations = associate_markers_to_shapes(shapes, markers)

    # Early exit if no associations could be made
    if not shape_marker_associations:
        return output_grid

    # 4. & 5. Determine Fill Properties and Perform Fill for each associated shape
    for shape_id, associated_marker in shape_marker_associations.items():
        # Should always be a valid shape_id here, but check just in case
        if shape_id not in shapes:
            continue

        shape_data = shapes[shape_id]
        red_pixels = shape_data['red_pixels'] # Already sorted top-to-bottom, left-to-right

        # Should not happen due to filtering in find_objects_and_markers
        if not red_pixels: continue

        # Determine fill color from the associated marker
        fill_color = associated_marker['color']

        # Determine fill direction based on the first (topmost, leftmost) red pixel
        marker_col = associated_marker['loc'][1]
        # red_pixels is sorted, so red_pixels[0] is the topmost, leftmost red pixel
        ref_red_col = red_pixels[0][1]
        fill_direction = 1 if marker_col > ref_red_col else -1 # +1 for right, -1 for left

        # Perform fill originating from *each* red pixel in this shape
        for r, c in red_pixels:
            # Start filling from the column adjacent to the red pixel in the fill direction
            fill_c = c + fill_direction

            # Loop while the fill column is within the grid boundaries
            while 0 <= fill_c < width:
                # Check the pixel *in the ORIGINAL input grid* at the target fill location
                # Only fill if the original pixel was white (background color 0)
                if input_grid[r, fill_c] == 0:
                    # Fill the corresponding pixel in the output grid
                    output_grid[r, fill_c] = fill_color
                    # Move to the next column in the fill direction
                    fill_c += fill_direction
                else:
                    # If an originally non-white pixel is encountered in the input grid,
                    # stop filling along this row (r) originating from this specific red pixel (r, c).
                    break
            # End of while loop (either hit a non-white pixel in input_grid or grid boundary)

    # Return the modified grid
    return output_grid