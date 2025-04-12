"""
This program transforms an input grid based on identifying and processing specific objects within it.

The core logic observed, particularly from the second training example, involves:
1. Identifying all contiguous regions (objects) of non-background ('8') cells.
2. Filtering these objects to select those containing specific colors (e.g., both '3' and '9').
3. Calculating the geometric center of each selected object.
4. Determining a bounding box that encloses all these centers.
5. Creating an output grid filled with the background color ('8').
6. Populating the calculated bounding box in the output grid:
    a. Setting the border cells of the box to a specific color (e.g., '3').
    b. Filling the interior cells with a default color (e.g., '9').
    c. Overlaying specific colors (e.g., '3') from the selected input objects onto the interior of the output box. The position of these overlaid colors is determined by mapping the cell's position relative to its input object's center to a corresponding position relative to the center of the output bounding box.

Note: The logic for the first training example appears different (selection based on size/enclosure, different border/fill colors, potential color transformations within the object) and is not fully captured by this implementation. This code prioritizes the clearer pattern from the second example.
"""

import numpy as np
from skimage.measure import label, regionprops
from collections import namedtuple
import math

# Define structure for object properties
# Bbox is (min_row, min_col, max_row_inclusive, max_col_inclusive)
Object = namedtuple("Object", ["label", "coords", "colors", "bbox", "center", "size"])

def find_objects(grid: np.ndarray, background_color: int) -> list[Object]:
    """
    Identifies connected regions (objects) of non-background colors in the grid.

    Args:
        grid: The input numpy array.
        background_color: The integer value representing the background.

    Returns:
        A list of Object namedtuples, each containing properties of an object.
            - label: Unique integer ID for the object.
            - coords: Nx2 numpy array of (row, col) coordinates.
            - colors: Set of unique non-background colors in the object.
            - bbox: Tuple (min_row, min_col, max_row_incl, max_col_incl).
            - center: Tuple (center_row, center_col) - float coordinates.
            - size: Integer number of pixels in the object.
    """
    mask = grid != background_color
    # Use connectivity=1 for 4-way neighbors (up, down, left, right)
    labeled_grid, num_labels = label(mask, connectivity=1, background=0, return_num=True)

    objects = []
    # Use regionprops for efficient calculation of properties
    # Pass grid itself to intensity_image to access original values if needed
    props = regionprops(labeled_grid, intensity_image=grid)

    for region in props:
        # region.label is the label number
        coords = region.coords # Nx2 array of (row, col)
        if not coords.size > 0: continue # Skip empty regions if any

        # Extract colors present in the object using the coordinates
        colors_present = set(grid[coords[:, 0], coords[:, 1]])
        # Remove background color if present (though mask should prevent this)
        colors_present.discard(background_color)

        if not colors_present: continue # Skip if somehow only background was included

        # Bbox: (min_row, min_col, max_row, max_col) - Note: max is *exclusive* in skimage
        min_r, min_c, max_r_excl, max_c_excl = region.bbox
        # Convert to inclusive bbox for easier use later
        bbox_inclusive = (min_r, min_c, max_r_excl - 1, max_c_excl - 1)

        # Center: (centroid-0, centroid-1) -> (row, col)
        center_r, center_c = region.centroid

        # Size: number of pixels
        size = region.area

        objects.append(Object(
            label=region.label,
            coords=coords,
            colors=colors_present,
            bbox=bbox_inclusive,
            center=(center_r, center_c),
            size=size
        ))

    return objects

def transform(input_grid_list: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid according to the rules primarily derived from train_2.
    Finds objects containing both 3 and 9, calculates bbox of their centers,
    and populates this box with border 3, fill 9, overlaying 3s from inputs.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    height, width = input_grid.shape
    background_color = 8 # Deduced from examples
    output_grid = np.full_like(input_grid, background_color)

    # 1. Find all non-background objects
    objects = find_objects(input_grid, background_color)
    if not objects:
        return output_grid.tolist() # Return background if no objects found

    # 2. Filter objects: Select objects containing both 3 and 9 (train_2 logic)
    required_colors = {3, 9}
    border_color = 3
    fill_color = 9
    overlay_color = 3 # The color from input objects to overlay
    selected_objects = [obj for obj in objects if required_colors.issubset(obj.colors)]

    # If the primary filtering logic (train_2) doesn't yield results,
    # return the background grid, as the alternative (train_1) logic is unclear.
    if not selected_objects:
        # print("No objects found matching criteria {3, 9}. Returning background.")
        return output_grid.tolist()

    # 3. Determine the output bounding box based on centers of selected objects
    centers = [obj.center for obj in selected_objects]
    if not centers:
        # This case should not happen if selected_objects is not empty, but check anyway
        return output_grid.tolist()

    center_rows = [r for r, c in centers]
    center_cols = [c for r, c in centers]

    # Determine bounds by rounding the min/max of center coordinates
    # Using math.floor/math.ceil might be slightly more robust than round()
    # Let's use rounding as per initial thought process.
    min_r_bbox = int(round(min(center_rows)))
    max_r_bbox = int(round(max(center_rows)))
    min_c_bbox = int(round(min(center_cols)))
    max_c_bbox = int(round(max(center_cols)))

    # Ensure bbox coordinates are within grid dimensions
    min_r_bbox = max(0, min_r_bbox)
    min_c_bbox = max(0, min_c_bbox)
    max_r_bbox = min(height - 1, max_r_bbox)
    max_c_bbox = min(width - 1, max_c_bbox)

    # Handle degenerate cases where bbox might be invalid after rounding/clipping
    if min_r_bbox > max_r_bbox or min_c_bbox > max_c_bbox:
        # print("Degenerate bounding box calculated. Returning background.")
        return output_grid.tolist()

    # 4. Populate the output bounding box
    # Calculate the geometric center of the output bounding box
    out_center_r = (min_r_bbox + max_r_bbox) / 2.0
    out_center_c = (min_c_bbox + max_c_bbox) / 2.0

    # Fill border and interior first
    for r in range(min_r_bbox, max_r_bbox + 1):
        for c in range(min_c_bbox, max_c_bbox + 1):
            is_border = (r == min_r_bbox or r == max_r_bbox or
                         c == min_c_bbox or c == max_c_bbox)
            if is_border:
                output_grid[r, c] = border_color
            else:
                output_grid[r, c] = fill_color

    # Overlay the 'overlay_color' from selected input objects
    for obj in selected_objects:
        obj_center_r, obj_center_c = obj.center
        # Iterate through coordinates of the current object
        for r_in, c_in in obj.coords:
            # Check if this cell in the input object has the color to be overlaid
            if input_grid[r_in, c_in] == overlay_color:
                # Calculate position relative to the input object's center
                delta_r = r_in - obj_center_r
                delta_c = c_in - obj_center_c

                # Calculate target position in the output grid relative to the output box center
                r_out = int(round(out_center_r + delta_r))
                c_out = int(round(out_center_c + delta_c))

                # Check if the target position is strictly *inside* the output bbox (not on the border)
                # and also within the overall grid bounds (safety check)
                if (min_r_bbox < r_out < max_r_bbox and
                    min_c_bbox < c_out < max_c_bbox and
                    0 <= r_out < height and 0 <= c_out < width):
                     output_grid[r_out, c_out] = overlay_color

    return output_grid.tolist()