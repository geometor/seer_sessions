import numpy as np
from collections import Counter
from skimage.measure import label
from skimage.draw import polygon
from scipy.spatial import ConvexHull
from scipy.ndimage import binary_dilation, generate_binary_structure

"""
Transformation Rule:

1.  Determine the background color (the most frequent color in the grid).
2.  Identify the two non-background colors present.
3.  Determine the 'frame' color by finding which of the two non-background colors has more pixels directly adjacent (up, down, left, right) to background pixels. The other non-background color is the 'fill' color.
4.  Find all connected groups (objects) of pixels that have the 'frame' color, using orthogonal adjacency.
5.  Create the output grid, starting as a copy of the input grid.
6.  For each 'frame' object found:
    a. If the object has 1 or 2 pixels, find all background pixels orthogonally adjacent to it and change them to the 'fill' color in the output grid.
    b. If the object has 3 or more pixels:
        i. Get the coordinates of the pixels in the object.
        ii. Calculate the convex hull covering these coordinates.
        iii. Determine all integer grid coordinates that fall within this filled convex hull.
        iv. Find all background pixels in the input grid that are orthogonally adjacent to any pixel of this 'frame' object.
        v. From this set of adjacent background pixels, keep only those whose coordinates do *not* fall inside the calculated filled convex hull of the 'frame' object.
        vi. Change the color of these remaining 'exterior' adjacent background pixels to the 'fill' color in the output grid.
7.  Return the final output grid.
"""

def _identify_colors(input_array):
    """Identifies background, frame, and fill colors."""
    colors, counts = np.unique(input_array, return_counts=True)
    
    if len(colors) <= 1:
        # Not enough colors to perform the transformation
        return None, None, None 

    background_color = colors[np.argmax(counts)]
    non_background_colors = sorted([c for c in colors if c != background_color])

    if len(non_background_colors) != 2:
        # Requires exactly two non-background colors
        return None, None, None

    color1, color2 = non_background_colors[0], non_background_colors[1]
    rows, cols = input_array.shape
    adj_counts = {color1: 0, color2: 0}
    
    # Create shifted arrays to find neighbors efficiently
    neighbors = {}
    neighbors['up'] = np.pad(input_array[1:, :], ((0, 1), (0, 0)), mode='constant', constant_values=-1)
    neighbors['down'] = np.pad(input_array[:-1, :], ((1, 0), (0, 0)), mode='constant', constant_values=-1)
    neighbors['left'] = np.pad(input_array[:, 1:], ((0, 0), (0, 1)), mode='constant', constant_values=-1)
    neighbors['right'] = np.pad(input_array[:, :-1], ((0, 0), (1, 0)), mode='constant', constant_values=-1)

    # Count adjacencies to background for each non-background color
    for color in [color1, color2]:
        mask_color = (input_array == color)
        count = 0
        for direction in ['up', 'down', 'left', 'right']:
            is_bg_neighbor = (neighbors[direction] == background_color)
            count += np.sum(mask_color & is_bg_neighbor)
        adj_counts[color] = count # Note: This counts adjacencies, not pixels with adjacent bg

    # Determine frame and fill based on counts
    if adj_counts[color1] == 0 and adj_counts[color2] == 0:
        return None, None, None # Neither touches background
    elif adj_counts[color1] > adj_counts[color2]:
        frame_color = color1
        fill_color = color2
    elif adj_counts[color2] > adj_counts[color1]:
        frame_color = color2
        fill_color = color1
    else: # Equal counts or one is zero - default to simple adjacency check / min value
        # Check if only one touches at all
        c1_touches = np.any((input_array == color1) & np.isin(neighbors['up'], background_color) | \
                            (input_array == color1) & np.isin(neighbors['down'], background_color) | \
                            (input_array == color1) & np.isin(neighbors['left'], background_color) | \
                            (input_array == color1) & np.isin(neighbors['right'], background_color))
        c2_touches = np.any((input_array == color2) & np.isin(neighbors['up'], background_color) | \
                            (input_array == color2) & np.isin(neighbors['down'], background_color) | \
                            (input_array == color2) & np.isin(neighbors['left'], background_color) | \
                            (input_array == color2) & np.isin(neighbors['right'], background_color))

        if c1_touches and not c2_touches:
            frame_color = color1
            fill_color = color2
        elif c2_touches and not c1_touches:
             frame_color = color2
             fill_color = color1
        else: # Still ambiguous or both touch equally, use min value as tie-breaker
             frame_color = min(color1, color2)
             fill_color = max(color1, color2)
             
    return background_color, frame_color, fill_color


def _get_filled_convex_hull_coords(coords, grid_shape):
    """Computes the filled convex hull coordinates for a set of points."""
    if len(coords) < 3:
        return set(coords) # Hull is just the points themselves for 1 or 2 points

    points = np.array(coords)[:, ::-1] # Convert (row, col) to (x, y) for ConvexHull
    try:
        hull = ConvexHull(points)
        hull_vertices = points[hull.vertices]
    except: # QhullError might happen for collinear points
        # Fallback for collinear points: treat as a line segment or single point
         min_r, min_c = np.min(coords, axis=0)
         max_r, max_c = np.max(coords, axis=0)
         if min_r == max_r: # Horizontal line
             rr, cc = np.array([min_r] * (max_c - min_c + 1)), np.arange(min_c, max_c + 1)
         elif min_c == max_c: # Vertical line
             rr, cc = np.arange(min_r, max_r + 1), np.array([min_c] * (max_r - min_r + 1))
         else: # Diagonal or single point - skimage.draw.line? For now, just return points
              return set(coords) # Fallback for complex collinear cases
              
         hull_coords = set(zip(rr, cc))
         return hull_coords


    # Use skimage.draw.polygon to fill the hull
    # hull_vertices[:, 1] are row coordinates, hull_vertices[:, 0] are column coordinates
    rr, cc = polygon(hull_vertices[:, 1], hull_vertices[:, 0], shape=grid_shape)
    hull_coords = set(zip(rr, cc))
    return hull_coords


def transform(input_grid):
    """
    Applies the convex hull-based frame outlining transformation.
    """
    input_array = np.array(input_grid, dtype=int)
    output_array = np.copy(input_array)
    rows, cols = input_array.shape

    # 1, 2, 3: Identify background, frame, and fill colors
    background_color, frame_color, fill_color = _identify_colors(input_array)

    if background_color is None or frame_color is None or fill_color is None:
        # If colors can't be identified according to rules, return original grid
        return input_grid

    # 4: Find connected components (objects) of the frame color
    frame_mask = (input_array == frame_color)
    # Use connectivity=1 for 4-connectivity (orthogonal)
    labeled_frame_objects, num_labels = label(frame_mask, connectivity=1, background=0, return_num=True)

    # Define structure for orthogonal adjacency check (dilation)
    struct = generate_binary_structure(2, 1) 

    # 6: Process each frame object
    for i in range(1, num_labels + 1):
        # a/bi: Get coordinates of the current frame object
        frame_object_coords_tuple = tuple(map(tuple, np.argwhere(labeled_frame_objects == i)))
        frame_object_coords_set = set(frame_object_coords_tuple)
        
        # Create a mask for the current object
        current_object_mask = (labeled_frame_objects == i)

        # 4c / 6b iv: Find all adjacent pixels (including non-BG for now) using dilation
        dilated_object = binary_dilation(current_object_mask, structure=struct)
        adjacent_mask = dilated_object & ~current_object_mask 
        
        # Filter for adjacent pixels that are background color in the input
        adjacent_bg_mask = adjacent_mask & (input_array == background_color)
        adjacent_bg_coords_tuple = tuple(map(tuple, np.argwhere(adjacent_bg_mask)))
        
        if not adjacent_bg_coords_tuple:
             continue # No background neighbors for this object

        # Handle small objects (1 or 2 pixels) separately - fill all adjacent BG
        if len(frame_object_coords_set) < 3:
             for r, c in adjacent_bg_coords_tuple:
                 output_array[r,c] = fill_color
             continue # Move to next object

        # b ii/iii: Calculate filled convex hull coordinates
        hull_coords_set = _get_filled_convex_hull_coords(frame_object_coords_tuple, (rows, cols))

        # b v: Filter adjacent background pixels: keep only those outside the hull
        for r, c in adjacent_bg_coords_tuple:
            if (r, c) not in hull_coords_set:
                # b vi: Change color in output grid
                output_array[r, c] = fill_color

    # 7: Return the modified grid
    return output_array.tolist()