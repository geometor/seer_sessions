import numpy as np
from collections import Counter
from scipy.ndimage import label, find_objects

"""
Identifies the background color (most frequent) and the largest contiguous object (LCO) of a non-background color. 
Then, for each 'agent' pixel (neither background nor LCO color), it checks if the agent pixel is aligned horizontally or vertically with the LCO's bounding box. 
If aligned, it checks the path of background pixels between the agent and the LCO along that axis. 
If the path consists only of background pixels, it 'paints' this path with the agent pixel's color, stopping just before reaching the LCO.
"""

def find_most_frequent_color(grid):
    """Finds the most frequent color in the grid."""
    counts = Counter(grid.flatten())
    if not counts:
        return 0 # Default to white/0 if grid is empty, though ARC constraints prevent this
    # Common case: return most frequent
    # Handle ties arbitrarily if necessary, but usually background is clear
    return counts.most_common(1)[0][0]

def find_largest_contiguous_object(grid, background_color):
    """Finds the largest connected component of non-background pixels."""
    mask = grid != background_color
    labeled_array, num_features = label(mask)
    
    if num_features == 0:
        return None, -1, None # No non-background objects found

    components = {}
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            lbl = labeled_array[r, c]
            if lbl > 0: # Belongs to a component
                if lbl not in components:
                    components[lbl] = {'coords': [], 'color': grid[r, c]}
                components[lbl]['coords'].append((r, c))
                # Verify all pixels in a component have the same color (as per definition)
                # In practice, label() works on the mask, so color consistency needs checking
                # If the LCO can be multi-colored according to problem, this needs adjustment
                # For this task, LCOs seem monochromatic based on examples. Let's assume this.
                if components[lbl]['color'] != grid[r, c]:
                     # This case indicates an issue or multi-colored object assumption is wrong.
                     # For now, let's stick to the first color found for the component.
                     pass 


    largest_size = 0
    largest_component_label = -1
    
    # Iterate through components found by label()
    object_slices = find_objects(labeled_array) # Get slices for each labeled object
    component_sizes = {}
    
    # Calculate sizes using the labeled array directly
    unique_labels, counts = np.unique(labeled_array[labeled_array > 0], return_counts=True)
    component_sizes = dict(zip(unique_labels, counts))

    if not component_sizes:
         return None, -1, None # No components found

    largest_component_label = max(component_sizes, key=component_sizes.get)
    largest_size = component_sizes[largest_component_label]
    
    # Find the color and bounding box of the largest component
    lco_coords = np.argwhere(labeled_array == largest_component_label)
    if lco_coords.size == 0:
         return None, -1, None # Should not happen if component_sizes is not empty

    lco_color = grid[lco_coords[0, 0], lco_coords[0, 1]] # Get color from the first pixel
    min_r, min_c = lco_coords.min(axis=0)
    max_r, max_c = lco_coords.max(axis=0)
    lco_bbox = (min_r, max_r, min_c, max_c)
    
    return lco_bbox, lco_color, lco_coords # Returning coords too might be useful but bbox is needed per logic

def transform(input_grid):
    """
    Applies the dripping/painting transformation.
    """
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np)
    height, width = input_np.shape

    # 1. Identify background color
    background_color = find_most_frequent_color(input_np)

    # 2. Find the Largest Contiguous Object (LCO) and its properties
    lco_bbox, lco_color, _ = find_largest_contiguous_object(input_np, background_color)

    # Handle case where no LCO is found
    if lco_bbox is None:
        return output_grid.tolist() # Return copy of input

    min_row_lco, max_row_lco, min_col_lco, max_col_lco = lco_bbox

    # 3. Identify agent pixels
    agent_pixels = []
    for r in range(height):
        for c in range(width):
            color = input_np[r, c]
            if color != background_color and color != lco_color:
                agent_pixels.append({'r': r, 'c': c, 'color': color})

    # 4. Process each agent pixel
    for agent in agent_pixels:
        ar, ac, agent_color = agent['r'], agent['c'], agent['color']

        # 5a. Check Vertical Alignment and Path
        if min_col_lco <= ac <= max_col_lco:
            # Agent is above LCO
            if ar < min_row_lco:
                path_clear = True
                for r_path in range(ar + 1, min_row_lco):
                    if output_grid[r_path, ac] != background_color:
                        path_clear = False
                        break
                if path_clear:
                    for r_paint in range(ar + 1, min_row_lco):
                        output_grid[r_paint, ac] = agent_color
            # Agent is below LCO
            elif ar > max_row_lco:
                path_clear = True
                for r_path in range(max_row_lco + 1, ar):
                    if output_grid[r_path, ac] != background_color:
                        path_clear = False
                        break
                if path_clear:
                    for r_paint in range(max_row_lco + 1, ar):
                        output_grid[r_paint, ac] = agent_color

        # 5b. Check Horizontal Alignment and Path
        if min_row_lco <= ar <= max_row_lco:
            # Agent is to the left of LCO
            if ac < min_col_lco:
                path_clear = True
                for c_path in range(ac + 1, min_col_lco):
                    if output_grid[ar, c_path] != background_color:
                        path_clear = False
                        break
                if path_clear:
                    for c_paint in range(ac + 1, min_col_lco):
                        output_grid[ar, c_paint] = agent_color
            # Agent is to the right of LCO
            elif ac > max_col_lco:
                path_clear = True
                for c_path in range(max_col_lco + 1, ac):
                    if output_grid[ar, c_path] != background_color:
                        path_clear = False
                        break
                if path_clear:
                    for c_paint in range(max_col_lco + 1, ac):
                        output_grid[ar, c_paint] = agent_color

    # 6. Return the modified grid
    return output_grid.tolist()