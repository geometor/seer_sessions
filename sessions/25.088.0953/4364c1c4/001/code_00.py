import numpy as np
from scipy.ndimage import label, find_objects
from collections import defaultdict

"""
Transforms the input grid by applying horizontal shifts to distinct objects based on their relative vertical positions when they share the same leftmost column.

1.  Identifies the background color (most frequent color).
2.  Finds all distinct objects (contiguous non-background pixels).
3.  Determines the leftmost column and topmost row for each object.
4.  Groups objects sharing the same leftmost column.
5.  For groups of exactly two objects:
    a.  Identifies the upper and lower object based on their topmost row.
    b.  If the objects are Magenta (6) and Green (3), assigns shifts of -1 (left) to the upper and +1 (right) to the lower.
    c.  Otherwise, assigns shifts of -1 (left) to the upper and +2 (right) to the lower.
6.  Applies the calculated horizontal shift to each pixel of every object, drawing the shifted object onto an initially background-filled output grid. Pixels shifted outside the grid boundaries are discarded.
"""

def get_background_color(grid):
    """Finds the most frequent color in the grid, assumed to be the background."""
    unique, counts = np.unique(grid, return_counts=True)
    return unique[np.argmax(counts)]

def find_all_objects(grid, background_color):
    """Finds all distinct objects in the grid."""
    objects = []
    unique_colors = np.unique(grid)
    object_id_counter = 0

    for color in unique_colors:
        if color == background_color:
            continue

        # Create a mask for the current color
        mask = (grid == color)
        # Label connected components (objects) of this color
        labeled_mask, num_labels = label(mask)

        # Find the location (slices) of each labeled object
        object_slices = find_objects(labeled_mask)

        for i in range(num_labels):
            obj_label = i + 1
            slices = object_slices[i]
            # Extract the pixels belonging to this specific object
            obj_grid_part = grid[slices]
            mask_part = (labeled_mask[slices] == obj_label)
            
            pixels = set()
            min_row, min_col = float('inf'), float('inf')
            
            rows, cols = np.where(mask_part)
            for r, c in zip(rows, cols):
                abs_r, abs_c = r + slices[0].start, c + slices[1].start
                pixels.add((abs_r, abs_c))
                min_row = min(min_row, abs_r)
                min_col = min(min_col, abs_c)

            if pixels: # Ensure the object is not empty
                 objects.append({
                    'id': object_id_counter,
                    'color': color,
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

    # 1. Identify the background color
    background_color = get_background_color(input_grid_np)

    # 2. Initialize output grid with background color
    output_grid = np.full((height, width), background_color, dtype=int)

    # 3. Find all distinct objects
    objects = find_all_objects(input_grid_np, background_color)
    if not objects:
        return output_grid.tolist() # Return background if no objects

    # 4. Group objects by leftmost column
    grouped_by_leftmost_col = defaultdict(list)
    for obj in objects:
        grouped_by_leftmost_col[obj['leftmost_col']].append(obj)

    # 5. Create mapping for object shifts, initialized to 0
    object_shifts = {obj['id']: 0 for obj in objects}

    # 6. Iterate through groups and calculate shifts for pairs
    for col, group in grouped_by_leftmost_col.items():
        if len(group) == 2:
            obj_a, obj_b = group[0], group[1]

            # a. Determine upper and lower objects
            if obj_a['top_row'] < obj_b['top_row']:
                obj_upper, obj_lower = obj_a, obj_b
            else:
                obj_upper, obj_lower = obj_b, obj_a

            # b. Check for special Magenta/Green case
            colors = {obj_upper['color'], obj_lower['color']}
            is_special_case = (colors == {6, 3}) # 6: Magenta, 3: Green

            # c/d. Assign shifts based on case
            shift_upper = -1
            shift_lower = +1 if is_special_case else +2

            # e. Store shifts
            object_shifts[obj_upper['id']] = shift_upper
            object_shifts[obj_lower['id']] = shift_lower

    # 7. Apply shifts and draw objects onto the output grid
    for obj in objects:
        shift = object_shifts[obj['id']]
        color = obj['color']
        
        for r, c in obj['pixels']:
            new_c = c + shift
            # Check grid boundaries
            if 0 <= new_c < width:
                output_grid[r, new_c] = color

    # 8. Return the final grid
    return output_grid.tolist()