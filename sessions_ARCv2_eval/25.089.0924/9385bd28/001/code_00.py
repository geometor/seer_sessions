import numpy as np
from scipy.ndimage import label, find_objects, sum as ndi_sum

"""
Identifies closed loops formed by a single non-white color. 
For each loop, it determines the largest non-white object (if any) located strictly inside the loop, excluding any pixels matching the loop's border color.
Based on the loop's border color and the color of the largest interior object (or lack thereof), a specific fill color is determined using a predefined mapping.
All white (0) pixels strictly inside the loop are then changed to this fill color in the output grid.
Pixels forming the loop border, pixels of interior objects, and pixels outside any loop remain unchanged.

The fill color mapping is:
- Border Red(2), Largest Interior Blue(1) -> Fill Green(3)
- Border Yellow(4), Largest Interior Blue(1) -> Fill Gray(5)
- Border Red(2), Largest Interior Yellow(4) -> Fill Maroon(9)
- Border Blue(1), No distinct Interior Object -> Fill Magenta(6)
- Border Green(3), No distinct Interior Object -> Fill Green(3)
- Border Magenta(6), No distinct Interior Object -> Fill Orange(7)
- Border Yellow(4), No distinct Interior Object -> Fill Yellow(4)
- Border Orange(7), No distinct Interior Object -> Fill Magenta(6)
"""

def find_connected_components(grid, include_colors=None, exclude_colors=None):
    """Finds connected components for specified colors."""
    mask = np.zeros_like(grid, dtype=bool)
    if include_colors:
        for color in include_colors:
            mask[grid == color] = True
    elif exclude_colors:
        mask = np.ones_like(grid, dtype=bool)
        for color in exclude_colors:
            mask[grid == color] = False
    else: # include all non-background
         mask[grid != 0] = True

    labeled_array, num_features = label(mask)
    objects = find_objects(labeled_array)
    components = []
    for i in range(num_features):
        loc = objects[i]
        component_mask = (labeled_array[loc] == (i + 1))
        coords = np.argwhere(component_mask)
        coords[:, 0] += loc[0].start
        coords[:, 1] += loc[1].start
        color = grid[coords[0, 0], coords[0, 1]] # Get color from first pixel
        components.append({'label': i + 1, 'coords': coords, 'color': color, 'size': len(coords)})
    return labeled_array, components

def get_neighbors(r, c, height, width):
    """Get valid neighbor coordinates."""
    neighbors = []
    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
            neighbors.append((nr, nc))
    return neighbors

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Fills enclosed white areas based on border color and largest interior object color.
    """
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

    # 1. Label all connected components in the grid (including background)
    # We use structure that connects only orthogonal neighbors
    structure = np.array([[0,1,0],[1,1,1],[0,1,0]], dtype=bool)
    labeled_grid, num_labels = label(input_grid, structure=structure)

    # 2. Identify white components (potential interiors)
    white_components = []
    for i in range(1, num_labels + 1):
        coords = np.argwhere(labeled_grid == i)
        if coords.size > 0 and input_grid[coords[0, 0], coords[0, 1]] == 0:
            white_components.append({'label': i, 'coords': coords})

    # 3. For each white component, check its neighbors
    for wc in white_components:
        neighbor_labels = set()
        border_color = -1 # Sentinel value
        is_enclosed = True
        
        # Find all unique neighboring labels
        for r, c in wc['coords']:
            for nr, nc in get_neighbors(r, c, height, width):
                neighbor_label = labeled_grid[nr, nc]
                # If neighbor is part of the same white component, skip
                if neighbor_label == wc['label']:
                    continue
                # If neighbor is background (0 label from scipy) or outside grid (handled by get_neighbors), 
                # it might mean it touches the edge implicitly if background reaches edge.
                # A more robust check: if any pixel of the white component is on the border, it's not enclosed.
                if r == 0 or r == height - 1 or c == 0 or c == width - 1:
                   is_enclosed = False
                   break 
                
                # Check if neighbor pixel itself is background but has label 0 (unlabeled region touching edge)
                if input_grid[nr, nc] == 0 and neighbor_label == 0:
                    is_enclosed = False
                    break

                # If neighbor is non-white, add its label
                if input_grid[nr, nc] != 0:
                   neighbor_labels.add(neighbor_label)
            if not is_enclosed:
                break
        
        if not is_enclosed:
            continue

        # 4. Check if enclosed by a single non-white component
        if len(neighbor_labels) == 1:
            border_label = list(neighbor_labels)[0]
            border_coords = np.argwhere(labeled_grid == border_label)
            if border_coords.size > 0:
                 border_color = input_grid[border_coords[0, 0], border_coords[0, 1]]
            else: # Should not happen if label exists
                continue

            # 5. Find the largest interior object (non-white, non-border color)
            interior_coords_list = wc['coords']
            interior_mask = np.zeros_like(input_grid, dtype=bool)
            for r, c in interior_coords_list:
                interior_mask[r, c] = True

            # Create a temporary grid containing only the interior pixels' original colors
            temp_interior_grid = np.full_like(input_grid, -1) # Use -1 to mark outside area
            temp_interior_grid[interior_mask] = input_grid[interior_mask]

            # Find components within this interior, excluding white and border color
            interior_obj_mask = (temp_interior_grid != -1) & (temp_interior_grid != 0) & (temp_interior_grid != border_color)
            
            labeled_interior_objs, num_interior_objs = label(interior_obj_mask, structure=structure)
            
            largest_interior_object_color = None
            max_size = 0

            if num_interior_objs > 0:
                interior_obj_indices = np.unique(labeled_interior_objs)
                # Ignore label 0 (background/non-object area)
                interior_obj_indices = interior_obj_indices[interior_obj_indices != 0] 
                
                object_sizes = ndi_sum(interior_obj_mask, labeled_interior_objs, index=interior_obj_indices)

                if object_sizes.size > 0:
                    largest_obj_index_in_list = np.argmax(object_sizes)
                    largest_obj_label = interior_obj_indices[largest_obj_index_in_list]
                    
                    # Find coordinates and color of the largest object
                    largest_obj_coords = np.argwhere(labeled_interior_objs == largest_obj_label)
                    if largest_obj_coords.size > 0:
                       largest_interior_object_color = input_grid[largest_obj_coords[0, 0], largest_obj_coords[0, 1]]
                       max_size = len(largest_obj_coords) # Or use object_sizes[largest_obj_index_in_list]

            # 6. Determine fill color
            fill_key = (border_color, largest_interior_object_color)
            if fill_key in fill_map:
                fill_color = fill_map[fill_key]

                # 7. Fill the white pixels in the output grid
                for r, c in interior_coords_list:
                    # Crucially, only fill if the pixel was originally white
                    if input_grid[r, c] == 0:
                        output_grid[r, c] = fill_color

    return output_grid