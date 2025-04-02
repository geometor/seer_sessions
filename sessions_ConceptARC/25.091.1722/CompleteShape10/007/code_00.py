import numpy as np
from scipy.ndimage import label, binary_closing

"""
Transformation Rule:
1. Identify the largest connected component of non-background color (color != 0) in the input grid.
2. Perform a binary morphological closing operation on this largest component using a 3x3 orthogonal structuring element.
3. Create the output grid by placing the color of the original largest component onto a background grid at all locations covered by the closed component.
"""

def get_component_details(labeled_array, label_idx):
    """Gets coordinates and size of a specific component label."""
    coords = np.argwhere(labeled_array == label_idx)
    size = len(coords)
    return coords, size

def transform(input_grid):
    """
    Applies a morphological closing operation to the largest non-background object.
    """
    H, W = input_grid.shape
    background_color = 0

    # Step 1: Find all connected components of non-background colors.
    # Use default connectivity (orthogonal) which matches the default for binary_closing
    labeled_objects, num_objects = label(input_grid != background_color)

    # Handle case with no non-background objects
    if num_objects == 0:
        return np.copy(input_grid) # Return a copy of the input

    # Step 2: Determine the largest connected component (main object).
    object_sizes = []
    main_object_info = None
    max_size = 0

    for i in range(1, num_objects + 1):
        coords, size = get_component_details(labeled_objects, i)
        if size > 0:
            if size > max_size:
                max_size = size
                # Store coords and the original color
                color = input_grid[coords[0,0], coords[0,1]]
                main_object_info = {'label': i, 'size': size, 'coords': coords, 'color': color}
            elif size == max_size and main_object_info is None:
                 # Handle tie for largest if no object found yet (e.g. only one object exists)
                 color = input_grid[coords[0,0], coords[0,1]]
                 main_object_info = {'label': i, 'size': size, 'coords': coords, 'color': color}


    # Check if a main object was identified
    if main_object_info is None:
        return np.copy(input_grid) # Should not happen if num_objects > 0

    main_object_label = main_object_info['label']
    main_object_color = main_object_info['color']

    # Step 3: Create a binary mask of the largest object.
    binary_mask = (labeled_objects == main_object_label)

    # Step 4: Apply morphological closing.
    # The default structure for binary_closing is orthogonal connectivity:
    # [[0, 1, 0],
    #  [1, 1, 1],
    #  [0, 1, 0]]
    closed_mask = binary_closing(binary_mask)

    # Step 5: Reconstruct the output grid.
    # Start with a background grid.
    output_grid = np.full_like(input_grid, background_color)
    
    # Place the original non-background pixels back, except those belonging to the largest object
    for i in range(1, num_objects + 1):
        if i != main_object_label:
            coords, size = get_component_details(labeled_objects, i)
            if size > 0:
                color = input_grid[coords[0,0], coords[0,1]]
                for r, c in coords:
                    output_grid[r,c] = color # Restore smaller objects untouched

    # Apply the color of the largest object according to the closed mask.
    output_grid[closed_mask] = main_object_color
    
    # Alternative Step 5: Modify Input Copy
    # output_grid = np.copy(input_grid)
    # fill_coords = np.argwhere(closed_mask & (input_grid == background_color))
    # for r, c in fill_coords:
    #     output_grid[r, c] = main_object_color
    
    return output_grid