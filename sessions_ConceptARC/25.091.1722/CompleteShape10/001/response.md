```python
import numpy as np
from scipy.ndimage import label

"""
Identifies the largest connected component of a non-background color in the input grid.
Finds all enclosed regions (holes) of the background color within this largest component.
Calculates the size of each hole.
If there is a unique largest hole among all internal holes, fills all *other* holes with the color of the largest component.
Otherwise (if there's a tie for the largest hole, or only one hole exists), fills *all* internal holes with the color of the largest component.
The background color is assumed to be white (0).
"""

def find_connected_components(grid, target_value=None, background_value=None):
    """
    Finds connected components in a grid.

    Args:
        grid (np.array): The input grid.
        target_value (int, optional): If provided, find components of this value.
        background_value (int, optional): If provided, find components *not* of this value.

    Returns:
        tuple: (labeled_array, num_features) from scipy.ndimage.label
               or (None, 0) if no components found or invalid args.
    """
    if target_value is not None:
        binary_grid = (grid == target_value)
    elif background_value is not None:
        binary_grid = (grid != background_value)
    else:
        # Requires either target_value or background_value
        return None, 0
        
    # Default connectivity (structure) considers orthogonal neighbors:
    # [[0,1,0],
    #  [1,1,1],
    #  [0,1,0]]
    labeled_array, num_features = label(binary_grid)
    return labeled_array, num_features

def get_component_coords(labeled_array, label_idx):
    """Gets the coordinates of pixels belonging to a specific component label."""
    return np.argwhere(labeled_array == label_idx)

def get_component_size(labeled_array, label_idx):
    """Gets the size (pixel count) of a specific component label."""
    return np.sum(labeled_array == label_idx)

def transform(input_grid):
    """
    Fills internal background holes within the largest colored object,
    except for the uniquely largest hole, if one exists.
    """
    output_grid = np.copy(input_grid)
    H, W = input_grid.shape
    background_color = 0

    # 1. Find all connected components of non-background colors.
    labeled_objects, num_objects = find_connected_components(input_grid, background_value=background_color)

    # Handle case with no non-background objects
    if num_objects == 0:
        return output_grid

    # 2. Determine the largest connected component (main object).
    object_sizes = [get_component_size(labeled_objects, i) for i in range(1, num_objects + 1)]
    largest_object_size = 0
    main_object_label = 0
    if object_sizes:
       largest_object_size = max(object_sizes)
       # Find the first label corresponding to the max size (handles ties by picking one)
       main_object_label = object_sizes.index(largest_object_size) + 1 
       
    # Handle edge case maybe? if main_object_label remains 0 something went wrong or no objects
    if main_object_label == 0:
         return output_grid # Should have been caught by num_objects == 0 check

    # 3. Get the color of the main object.
    main_object_coords = get_component_coords(labeled_objects, main_object_label)
    # Check if coords were found before accessing
    if len(main_object_coords) == 0:
        # This shouldn't happen if main_object_label > 0 and based on a valid size
        return output_grid 
    main_object_color = input_grid[main_object_coords[0, 0], main_object_coords[0, 1]]

    # 4. Find all connected components of the background color.
    labeled_background, num_background_components = find_connected_components(input_grid, target_value=background_color)

    # 5. Identify internal holes (background components not touching the border).
    internal_holes = [] # Store tuples of (label_index, size, coordinates)
    for i in range(1, num_background_components + 1):
        bg_coords = get_component_coords(labeled_background, i)
        if len(bg_coords) == 0:
            continue # Skip if component somehow has no coords

        # Check if any coordinate touches the border
        touches_border = np.any((bg_coords[:, 0] == 0) | (bg_coords[:, 0] == H - 1) | 
                                (bg_coords[:, 1] == 0) | (bg_coords[:, 1] == W - 1))

        if not touches_border:
            # It's an internal hole candidate. We assume based on task structure
            # that these are holes within the 'main object' context.
            hole_size = len(bg_coords)
            internal_holes.append({'label': i, 'size': hole_size, 'coords': bg_coords})

    # 6. If no internal holes are found, return the original grid.
    if not internal_holes:
        return output_grid

    # 7. Calculate sizes and find the maximum size among internal holes.
    hole_sizes = [hole['size'] for hole in internal_holes]
    if not hole_sizes: # Should be caught by 'if not internal_holes', but safety check
        return output_grid
        
    max_hole_size = max(hole_sizes)

    # 8. Count how many holes share this maximum size.
    max_size_count = hole_sizes.count(max_hole_size)

    # 9. Determine which holes to fill and modify the output grid.
    holes_to_fill = []
    if max_size_count == 1:
        # Fill all holes EXCEPT the unique largest one
        for hole in internal_holes:
            if hole['size'] != max_hole_size:
                holes_to_fill.append(hole)
    else:
        # Fill ALL internal holes (tie for largest, or only one hole exists which is max)
        holes_to_fill = internal_holes

    # 10. Fill the selected holes with the main object's color.
    for hole in holes_to_fill:
        for r, c in hole['coords']:
            # Ensure coordinates are within bounds (should be, but safe)
            if 0 <= r < H and 0 <= c < W:
                output_grid[r, c] = main_object_color

    # 11. Return the modified grid.
    return output_grid
```