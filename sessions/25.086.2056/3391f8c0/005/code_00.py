import numpy as np
from scipy.ndimage import label, find_objects

"""
Transformation Rule:
1. Initialize an output grid with the same dimensions as the input grid, filled with the background color (white, 0).
2. Identify the two unique non-background colors present in the input grid. Call them `color_A` and `color_B`.
3. Define a connectivity structure that includes diagonal neighbors (8-connectivity).
4. Find all distinct, contiguous objects composed of `color_A` using the defined connectivity.
5. Find all distinct, contiguous objects composed of `color_B` using the defined connectivity.
6. From the first `color_A` object found, extract its shape pattern (the set of relative coordinates of its pixels from its top-left corner). Call this `shape_A`. If no `color_A` objects exist, `shape_A` is empty.
7. From the first `color_B` object found, extract its shape pattern. Call this `shape_B`. If no `color_B` objects exist, `shape_B` is empty.
8. Determine the list of top-left corner coordinates for all objects originally composed of `color_A`. Call this list `locations_A`.
9. Determine the list of top-left corner coordinates for all objects originally composed of `color_B`. Call this list `locations_B`.
10. For each coordinate (`r`, `c`) in `locations_A`:
    * Draw `shape_B` onto the output grid, using `color_B`, anchoring its pattern at (`r`, `c`). Ensure drawing stays within grid bounds.
11. For each coordinate (`r`, `c`) in `locations_B`:
    * Draw `shape_A` onto the output grid, using `color_A`, anchoring its pattern at (`r`, `c`). Ensure drawing stays within grid bounds.
12. Return the final output grid.
"""

def get_objects_and_shape(grid_np, color, connectivity_structure):
    """
    Finds objects of a specific color, their locations, and the shape of the first object.

    Args:
        grid_np: The input numpy grid.
        color: The color of the objects to find.
        connectivity_structure: The structure defining pixel connectivity for label().

    Returns:
        A tuple: (list_of_locations, shape_pattern)
        list_of_locations: List of (row, col) tuples for the top-left corner of each object.
        shape_pattern: List of (dr, dc) relative coordinates defining the shape,
                       or None if no objects of this color are found.
    """
    # Create a binary mask where the target color is present
    mask = (grid_np == color)
    
    # Label connected components (objects) in the mask
    labeled_grid, num_labels = label(mask, structure=connectivity_structure)
    
    if num_labels == 0:
        return [], None  # No objects found

    # Find the bounding boxes (slices) for each labeled object
    object_slices = find_objects(labeled_grid)

    locations = []
    shape_pattern = None

    for i, slc in enumerate(object_slices):
        # Location is the top-left corner of the slice
        top_left = (slc[0].start, slc[1].start)
        locations.append(top_left)

        # Extract the shape pattern from the first object found (label 1)
        if i == 0: # find_objects returns slices ordered by label number starting from 1
             # Get the portion of the original grid corresponding to the object's bounding box
            object_bounding_box = grid_np[slc]
             # Create a mask for the specific object within its bounding box
            object_mask_in_bbox = (object_bounding_box == color) & (labeled_grid[slc] == (i + 1))
             # Find the relative coordinates of the object's pixels within its bounding box
            relative_coords = np.argwhere(object_mask_in_bbox)
            if relative_coords.size > 0:
                # Store shape as list of [dr, dc] tuples/lists
                shape_pattern = relative_coords.tolist()
            else:
                 # This case should ideally not happen if find_objects found something,
                 # but handle it defensively.
                 shape_pattern = [[0, 0]] # Default to a single pixel if extraction fails

    # Ensure shape_pattern is not None if objects were found but pattern extraction failed
    if locations and shape_pattern is None:
         shape_pattern = [[0, 0]] # Fallback shape

    return locations, shape_pattern

def draw_shape(output_grid, anchor_r, anchor_c, shape_pattern, color):
    """
    Draws a shape onto the output grid at a given anchor point.

    Args:
        output_grid: The numpy array representing the output grid.
        anchor_r: The row coordinate of the anchor point (top-left).
        anchor_c: The column coordinate of the anchor point (top-left).
        shape_pattern: List of [dr, dc] relative coordinates defining the shape.
        color: The color to draw the shape with.
    """
    if shape_pattern is None:
        return # Nothing to draw if shape is None

    grid_height, grid_width = output_grid.shape
    for dr, dc in shape_pattern:
        r, c = anchor_r + dr, anchor_c + dc
        # Check bounds before drawing
        if 0 <= r < grid_height and 0 <= c < grid_width:
            output_grid[r, c] = color

def transform(input_grid):
    """
    Swaps the locations of shapes defined by the two non-background colors.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed grid.
    """
    # Convert input to numpy array
    input_np = np.array(input_grid, dtype=int)
    
    # Initialize output grid with background color (0)
    output_np = np.zeros_like(input_np)
    
    # Define 8-connectivity (includes diagonals)
    connectivity_structure = np.ones((3, 3), dtype=bool)

    # Find the unique non-background colors
    unique_colors = np.unique(input_np)
    non_bg_colors = unique_colors[unique_colors != 0]

    # Ensure exactly two non-background colors exist
    if len(non_bg_colors) != 2:
        # If not exactly two, return the original grid (or handle as error)
        # Based on analysis, valid examples always have two.
        return input_grid

    color_A, color_B = non_bg_colors[0], non_bg_colors[1]

    # Get locations and shape for color A
    locations_A, shape_A = get_objects_and_shape(input_np, color_A, connectivity_structure)

    # Get locations and shape for color B
    locations_B, shape_B = get_objects_and_shape(input_np, color_B, connectivity_structure)

    # Draw Shape B at Color A's original locations
    for r, c in locations_A:
        draw_shape(output_np, r, c, shape_B, color_B)

    # Draw Shape A at Color B's original locations
    for r, c in locations_B:
        draw_shape(output_np, r, c, shape_A, color_A)

    # Convert the result back to list of lists
    return output_np.tolist()