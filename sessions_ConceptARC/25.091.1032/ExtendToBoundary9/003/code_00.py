import numpy as np
from scipy.ndimage import label, find_objects

"""
Transformation Rule:
1. Identify the two distinct non-white connected objects in the input grid.
2. Determine which object acts as the 'outer_frame' (it encloses the other object) and which is the 'inner_object'.
3. Record the color of the 'inner_object' ('inner_color').
4. Identify the 'interior white pixels': these are the pixels that have color white (0) in the input grid AND are not reachable by a flood fill starting from the white pixels on the grid's border.
5. Create a copy of the input grid.
6. Change the color of only the identified 'interior white pixels' in the copied grid to the 'inner_color'.
7. Return the modified grid.
"""

def find_connected_components(grid, background_color=0):
    """
    Finds connected components of non-background colors.

    Args:
        grid (np.array): The input grid.
        background_color (int): The color to treat as background.

    Returns:
        list: A list of dictionaries, each representing an object with keys:
              'label', 'color', 'coords', 'slice', 'size', 'bbox'.
              Returns an empty list if no non-background objects are found.
    """
    objects = []
    # Create a boolean mask where non-background pixels are True
    mask = grid != background_color
    # Label connected components (using default connectivity=1, 4-neighbors)
    # For 8-connectivity (including diagonals), use structure=np.ones((3,3))
    labeled_array, num_features = label(mask) 
    
    if num_features == 0:
        return objects

    # Find the locations (slices) of each labeled feature
    slices = find_objects(labeled_array)
    
    for i in range(num_features):
        component_label = i + 1
        loc = slices[i]
        # Get the coordinates of the pixels belonging to this component relative to the grid origin
        coords = np.argwhere(labeled_array == component_label)
        # Determine the color of the component (assuming it's uniform)
        # Take the color of the first pixel in the component
        if coords.size > 0:
            color = grid[coords[0, 0], coords[0, 1]] 
            # Calculate size (number of pixels)
            size = len(coords)
            # Bounding box: (min_row, min_col, max_row, max_col) inclusive
            min_row = loc[0].start
            min_col = loc[1].start
            max_row = loc[0].stop - 1 # slices are exclusive at stop
            max_col = loc[1].stop - 1
            bbox = (min_row, min_col, max_row, max_col)

            objects.append({
                'label': component_label,
                'color': color,
                'coords': coords,
                'slice': loc,
                'size': size,
                'bbox': bbox 
            })
        
    # Sort objects by size (descending) - might be useful but not strictly necessary for enclosure check
    # objects.sort(key=lambda o: o['size'], reverse=True) 
    
    return objects

def flood_fill_exterior(grid, background_color=0):
    """
    Performs a flood fill from the borders to identify exterior white pixels.
    
    Args:
        grid (np.array): The input grid.
        background_color (int): The color representing the background/empty space.

    Returns:
        np.array: A boolean mask of the same shape as grid. 
                  True indicates an exterior pixel (reachable background from border) 
                  or a non-background pixel. 
                  False indicates an interior background pixel.
    """
    rows, cols = grid.shape
    # Mask to keep track of visited/exterior pixels, initialized to False
    exterior_mask = np.zeros_like(grid, dtype=bool)
    
    # Queue for BFS (row, col)
    queue = []

    # Add all border background pixels to the queue and mark as exterior
    for r in range(rows):
        if grid[r, 0] == background_color and not exterior_mask[r, 0]:
            queue.append((r, 0))
            exterior_mask[r, 0] = True
        if grid[r, cols - 1] == background_color and not exterior_mask[r, cols - 1]:
            queue.append((r, cols - 1))
            exterior_mask[r, cols - 1] = True
            
    for c in range(cols):
        if grid[0, c] == background_color and not exterior_mask[0, c]:
            queue.append((0, c))
            exterior_mask[0, c] = True
        if grid[rows - 1, c] == background_color and not exterior_mask[rows - 1, c]:
            queue.append((rows - 1, c))
            exterior_mask[rows - 1, c] = True

    # Define 4-directional neighbors
    moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # BFS
    head = 0
    while head < len(queue):
        r, c = queue[head]
        head += 1

        for dr, dc in moves:
            nr, nc = r + dr, c + dc
            # Check bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # If neighbor is background and not yet visited
                if grid[nr, nc] == background_color and not exterior_mask[nr, nc]:
                    exterior_mask[nr, nc] = True
                    queue.append((nr, nc))
                    
    # Also mark all non-background pixels as non-interior (part of exterior_mask)
    # This prevents flood fill from crossing object boundaries implicitly
    # and ensures non-background pixels are never considered 'interior white'.
    exterior_mask[grid != background_color] = True

    return exterior_mask

def is_bbox_contained(inner_bbox, outer_bbox):
    """Checks if inner_bbox is strictly contained within outer_bbox."""
    inner_min_r, inner_min_c, inner_max_r, inner_max_c = inner_bbox
    outer_min_r, outer_min_c, outer_max_r, outer_max_c = outer_bbox
    return (outer_min_r < inner_min_r and
            outer_min_c < inner_min_c and
            outer_max_r > inner_max_r and
            outer_max_c > inner_max_c)

def transform(input_grid):
    """
    Fills the empty white space (0) inside an outer boundary shape 
    with the color of an inner shape, leaving the inner shape itself intact.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    background_color = 0
    
    # --- 1. Identify Objects ---
    objects = find_connected_components(input_grid, background_color=background_color)
    
    # Expect exactly two objects for this task based on examples
    if len(objects) != 2:
        # If not exactly two objects, the pattern doesn't match; return original grid.
        # This handles cases with no objects, one object, or more than two.
        # print(f"Warning: Expected 2 objects, found {len(objects)}. Returning original grid.")
        return output_grid 
        
    # --- 2. Determine Outer Frame and Inner Object ---
    obj1 = objects[0]
    obj2 = objects[1]
    
    # Check which object's bounding box contains the other's
    # Note: Using strict containment '<' and '>' to avoid ambiguity if boxes touch.
    if is_bbox_contained(obj2['bbox'], obj1['bbox']):
        outer_frame = obj1
        inner_object = obj2
    elif is_bbox_contained(obj1['bbox'], obj2['bbox']):
        outer_frame = obj2
        inner_object = obj1
    else:
        # Bounding boxes don't show clear containment, pattern might be different
        # or objects might be side-by-side. Return original grid.
        # print("Warning: Could not determine clear enclosure based on bounding boxes. Returning original grid.")
        return output_grid

    inner_color = inner_object['color']

    # --- 3. Identify Interior White Pixels using Flood Fill ---
    # exterior_mask is True for exterior background and all non-background pixels.
    # False indicates interior background pixels.
    exterior_mask = flood_fill_exterior(input_grid, background_color=background_color)

    # --- 4. Define the mask for pixels to be filled ---
    # Pixels to fill are those that are background (0) AND not exterior (i.e., interior)
    interior_white_mask = (input_grid == background_color) & (~exterior_mask)
                
    # --- 5. Fill Interior White Pixels ---
    # Use the boolean mask to update only the interior white pixels in the output grid
    output_grid[interior_white_mask] = inner_color
                
    return output_grid