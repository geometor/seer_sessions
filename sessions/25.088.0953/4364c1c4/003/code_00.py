import numpy as np
from scipy.ndimage import label, find_objects
from collections import defaultdict

"""
Identifies pairs of distinct objects that are vertically aligned, sharing the same leftmost column coordinate. For each pair, shifts the higher object (smaller top row index) one column left, and shifts the lower object (larger top row index) one column right. Objects not part of such a pair remain stationary.
"""

def get_background_color(grid):
    """Finds the most frequent color in the grid, assumed to be the background."""
    unique, counts = np.unique(grid, return_counts=True)
    if not unique.size: # Handle empty grid case
        return 0 # Default to white if grid is empty
    return unique[np.argmax(counts)]

def find_all_objects(grid, background_color):
    """
    Finds all distinct objects (contiguous non-background pixels) in the grid.
    Returns a list of dictionaries, each representing an object with its
    id, color, pixels (set of (row, col) tuples), top_row, and leftmost_col.
    """
    objects = []
    object_id_counter = 0
    labeled_grid, num_labels = label(grid != background_color) # Label all non-background components

    # Find the location (slices) of each labeled object
    object_slices = find_objects(labeled_grid)

    for i in range(num_labels):
        obj_label = i + 1
        slices = object_slices[i]
        
        # Extract the mask for this specific object within its bounding box
        mask_part = (labeled_grid[slices] == obj_label)
        
        # Get the color (assuming an object has a single color)
        # Find the first pixel coordinates within the slice that belong to the object
        obj_coords_in_slice = np.argwhere(mask_part)
        if obj_coords_in_slice.size == 0:
            continue # Skip if somehow the object is empty within its slice
            
        first_pixel_r, first_pixel_c = obj_coords_in_slice[0]
        obj_color = grid[slices[0].start + first_pixel_r, slices[1].start + first_pixel_c]

        pixels = set()
        min_row, min_col = float('inf'), float('inf')

        # Find absolute coordinates and object properties
        rows, cols = np.where(mask_part)
        for r, c in zip(rows, cols):
            abs_r, abs_c = r + slices[0].start, c + slices[1].start
            pixels.add((abs_r, abs_c))
            min_row = min(min_row, abs_r)
            min_col = min(min_col, abs_c)

        if pixels: # Ensure the object is not empty
             objects.append({
                'id': object_id_counter,
                'color': obj_color,
                'pixels': pixels,
                'top_row': min_row,
                'leftmost_col': min_col,
             })
             object_id_counter += 1

    return objects

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    input_grid_np = np.array(input_grid)
    height, width = input_grid_np.shape
    if height == 0 or width == 0:
        return [] # Handle empty input grid

    # 1. Initialization: Determine background and create output grid
    background_color = get_background_color(input_grid_np)
    output_grid = np.full((height, width), background_color, dtype=int)

    # 2. Object Identification: Find all distinct objects
    objects = find_all_objects(input_grid_np, background_color)
    if not objects:
        return output_grid.tolist() # Return background if no objects

    # 3. Pair Identification: Group objects by leftmost column
    grouped_by_leftmost_col = defaultdict(list)
    for obj in objects:
        grouped_by_leftmost_col[obj['leftmost_col']].append(obj)

    # 4. Shift Calculation: Determine shifts for paired objects
    object_shifts = {obj['id']: 0 for obj in objects} # Initialize all shifts to 0

    for col, group in grouped_by_leftmost_col.items():
        if len(group) == 2: # Process groups with exactly two objects
            obj_a, obj_b = group[0], group[1]

            # Determine upper and lower objects based on top_row
            if obj_a['top_row'] < obj_b['top_row']:
                obj_upper, obj_lower = obj_a, obj_b
            else:
                obj_upper, obj_lower = obj_b, obj_a

            # Assign shifts: -1 for upper, +1 for lower
            object_shifts[obj_upper['id']] = -1
            object_shifts[obj_lower['id']] = +1

    # 5. Apply Transformation: Draw objects (shifted or stationary) onto output grid
    for obj in objects:
        shift = object_shifts[obj['id']]
        color = obj['color']

        for r, c in obj['pixels']:
            new_c = c + shift
            # Check grid boundaries before drawing
            if 0 <= new_c < width:
                # Ensure row is also within bounds (should always be true unless input grid dims were weird)
                if 0 <= r < height:
                     output_grid[r, new_c] = color

    # 6. Output: Return the final grid
    return output_grid.tolist()