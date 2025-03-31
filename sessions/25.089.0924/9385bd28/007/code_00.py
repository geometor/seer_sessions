import numpy as np
from scipy.ndimage import label, sum as ndi_sum

"""
Identifies connected regions of white (0) pixels that are fully enclosed by a single, 
contiguous non-white object (the border loop) and do not touch the grid edges. 
For each such enclosed region:
1. Determines the color of the border loop.
2. Finds the largest distinct object (contiguous block of pixels of the same color) 
   located strictly within the region, excluding any objects that are white (0) 
   or match the color of the border loop. Notes the color and coordinates of this 
   largest interior object. If no such valid object exists, it's noted as None.
3. Based on the border loop's color and the color of the largest valid interior object 
   (or None), a specific fill color is determined using a predefined mapping.
4. All pixels within the originally enclosed white region are changed to this fill color 
   in the output grid, *except* for the pixels belonging to the largest interior 
   object identified in step 2 (if one exists). 
Pixels forming the border loop, pixels of the largest interior object, and pixels 
in unenclosed regions or outside any loop remain unchanged from the input.

The fill color mapping is derived from the examples:
- Border Red(2), Largest Interior Blue(1) -> Fill Green(3)
- Border Yellow(4), Largest Interior Blue(1) -> Fill Gray(5)
- Border Red(2), Largest Interior Yellow(4) -> Fill Maroon(9)
- Border Blue(1), No valid Interior Object -> Fill Magenta(6)
- Border Green(3), No valid Interior Object -> Fill Green(3)
- Border Magenta(6), No valid Interior Object -> Fill Orange(7)
- Border Yellow(4), No valid Interior Object -> Fill Yellow(4)
- Border Orange(7), No valid Interior Object -> Fill Magenta(6) 
"""


def get_neighbors(r, c, height, width):
    """Get valid orthogonal neighbor coordinates."""
    neighbors = []
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
            neighbors.append((nr, nc))
    return neighbors

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Fills enclosed white areas based on border color and largest interior object color,
    preserving the largest interior object.
    """
    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # Define the fill color mapping based on (border_color, largest_interior_color)
    # Use None for largest_interior_color if no relevant interior object exists.
    fill_map = {
        (2, 1): 3,  # Border: Red, Inner: Blue -> Fill: Green
        (4, 1): 5,  # Border: Yellow, Inner: Blue -> Fill: Gray
        (2, 4): 9,  # Border: Red, Inner: Yellow -> Fill: Maroon
        (1, None): 6, # Border: Blue, Inner: None -> Fill: Magenta
        (3, None): 3, # Border: Green, Inner: None -> Fill: Green
        (6, None): 7, # Border: Magenta, Inner: None -> Fill: Orange
        (4, None): 4, # Border: Yellow, Inner: None -> Fill: Yellow
        (7, None): 6, # Border: Orange, Inner: None -> Fill: Magenta
    }

    # Define structure for orthogonal connectivity
    structure = np.array([[0, 1, 0], [1, 1, 1], [0, 1, 0]], dtype=bool)

    # Label all non-white connected components (potential borders)
    labeled_objects, _ = label(input_grid != 0, structure=structure)

    # Identify all distinct connected regions of white (0) pixels in the input grid.
    labeled_white, num_white_labels = label(input_grid == 0, structure=structure)

    # Iterate through each identified white region.
    for w_label in range(1, num_white_labels + 1):
        
        # Get coordinates of the current white region
        white_coords_list = np.argwhere(labeled_white == w_label)
        if white_coords_list.size == 0:
            continue # Should not happen, but safe check

        # Create a boolean mask for the current white region for easier indexing later
        # This mask identifies the pixels *originally* white in this component.
        original_white_mask = (labeled_white == w_label)

        # Check if any pixel of the white region lies on the outermost border of the grid.
        touches_boundary = np.any(white_coords_list[:, 0] == 0) or \
                           np.any(white_coords_list[:, 0] == height - 1) or \
                           np.any(white_coords_list[:, 1] == 0) or \
                           np.any(white_coords_list[:, 1] == width - 1)
        
        # If it touches the boundary, this region is not enclosed; skip to the next white region.
        if touches_boundary:
            continue 

        # Determine the set of unique, contiguous, non-white objects adjacent to the current white region.
        adjacent_object_labels = set()
        for r, c in white_coords_list:
            # Check orthogonal neighbors
            for nr, nc in get_neighbors(r, c, height, width):
                obj_label = labeled_objects[nr, nc]
                # If the neighbor is part of a non-white object (label > 0)
                if obj_label != 0: 
                    adjacent_object_labels.add(obj_label)

        # If the set contains *exactly one* non-white object label, the region is enclosed by a single border_loop.
        if len(adjacent_object_labels) == 1:
            border_label = list(adjacent_object_labels)[0]
            
            # Find the color of the border object (border_color)
            border_coords = np.argwhere(labeled_objects == border_label)
            if border_coords.size == 0 : 
                continue 
            border_color = input_grid[border_coords[0, 0], border_coords[0, 1]]

            # --- Find the largest interior object (non-white, non-border color) ---
            
            # Create a mask for pixels within the original white region bounds 
            # that are *not* white and *not* the border color in the input grid.
            potential_interior_obj_mask = original_white_mask & (input_grid != 0) & (input_grid != border_color)
            
            # Label connected components within this specific mask
            labeled_interior_objs, num_interior_objs = label(potential_interior_obj_mask, structure=structure)

            largest_interior_object_color = None
            largest_obj_mask = np.zeros_like(input_grid, dtype=bool) # Mask for the largest object's pixels

            # If one or more valid interior objects exist
            if num_interior_objs > 0:
                interior_obj_indices = np.arange(1, num_interior_objs + 1)
                # Sum the boolean mask 'potential_interior_obj_mask' over areas defined by 'labeled_interior_objs'
                object_sizes = ndi_sum(potential_interior_obj_mask, labeled_interior_objs, index=interior_obj_indices)

                if object_sizes.size > 0:
                    # Find the label corresponding to the largest size
                    largest_obj_local_label_idx = np.argmax(object_sizes)
                    largest_obj_label = interior_obj_indices[largest_obj_local_label_idx]
                    
                    # Create the mask for the largest object
                    largest_obj_mask = (labeled_interior_objs == largest_obj_label)
                    
                    # Find coordinates of this largest object to determine its color
                    largest_obj_coords = np.argwhere(largest_obj_mask)
                    if largest_obj_coords.size > 0:
                        largest_interior_object_color = input_grid[largest_obj_coords[0, 0], largest_obj_coords[0, 1]]

            # --- Determine the fill color using the map ---
            fill_key = (border_color, largest_interior_object_color)
            fill_color = fill_map.get(fill_key) 

            # --- Apply the fill color ---
            if fill_color is not None:
                # Define the mask for pixels to be filled:
                # They must be part of the original white region (original_white_mask)
                # AND they must *not* be part of the largest interior object (if one exists)
                fill_mask = original_white_mask & (~largest_obj_mask)
                
                # Apply the fill color to the output grid using the calculated mask
                output_grid[fill_mask] = fill_color

    # Return the final modified output grid.
    return output_grid