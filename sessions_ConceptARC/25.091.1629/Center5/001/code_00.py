import numpy as np
from scipy.ndimage import label, find_objects as scipy_find_objects, center_of_mass

"""
Identify all distinct non-background colored objects (connected components) in the 
input grid. Determine the largest object; this is the "line". All other objects 
are "dots". Find the orientation (horizontal or vertical) and the midpoint 
coordinate of the line along its main axis (column for horizontal, row for vertical).
Calculate the centroid coordinate (average row and column) of all pixels belonging 
to the "dot" objects combined. Compare the centroid coordinate to the line's 
midpoint coordinate along the line's main axis to determine the movement direction 
(left/right for horizontal lines, up/down for vertical lines) and magnitude (the 
absolute difference between the centroid and midpoint coordinates along that axis). 
Create the output grid by copying the input grid. Erase the original "dot" objects 
from the output grid. Draw the "dot" objects in their new positions by shifting 
each original dot pixel according to the calculated direction and magnitude.
"""

def find_all_objects(grid):
    """
    Finds all connected components of non-background colors.
    Returns a list of objects, where each object is a tuple: 
    (color, list_of_coordinates).
    """
    objects = []
    # Iterate through colors 1 to 9
    for color in range(1, 10):
        # Create a binary mask for the current color
        binary_mask = (grid == color).astype(int)
        # Label connected components of this color
        labeled_array, num_features = label(binary_mask)
        if num_features > 0:
            # Find the locations (slices) of each component
            locations = scipy_find_objects(labeled_array)
            for i in range(num_features):
                loc = locations[i]
                # Get coordinates where the labeled array matches the current component index
                coords = np.argwhere(labeled_array[loc] == (i + 1))
                # Adjust coordinates relative to the original grid
                coords[:, 0] += loc[0].start
                coords[:, 1] += loc[1].start
                # Store as list of (row, col) tuples
                coord_list = [tuple(c) for c in coords]
                objects.append({'color': color, 'coords': coord_list, 'size': len(coord_list)})
    return objects

def get_line_properties(obj_coords):
    """
    Determines orientation, midpoint, min/max row/col for a line object.
    Returns a dictionary with properties or None if not a line.
    """
    if not obj_coords:
        return None

    rows = [r for r, c in obj_coords]
    cols = [c for r, c in obj_coords]

    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)

    is_horizontal = all(r == min_row for r in rows) and (max_col - min_col + 1 == len(obj_coords))
    is_vertical = all(c == min_col for c in cols) and (max_row - min_row + 1 == len(obj_coords))

    if is_horizontal:
        midpoint_row = min_row
        midpoint_col = (min_col + max_col) / 2.0
        return {
            'orientation': 'horizontal',
            'midpoint': (midpoint_row, midpoint_col),
            'min_row': min_row, 'max_row': max_row,
            'min_col': min_col, 'max_col': max_col
        }
    elif is_vertical:
        midpoint_row = (min_row + max_row) / 2.0
        midpoint_col = min_col
        return {
            'orientation': 'vertical',
            'midpoint': (midpoint_row, midpoint_col),
            'min_row': min_row, 'max_row': max_row,
            'min_col': min_col, 'max_col': max_col
        }
    else:
        # This function assumes the largest object is always a line per the analysis.
        # If it could be something else, more robust checks are needed.
        # Let's add a basic fallback for slightly imperfect lines found by connectivity.
        if max_row == min_row: # Horizontal tendency
            midpoint_row = min_row
            midpoint_col = (min_col + max_col) / 2.0
            return {
                'orientation': 'horizontal',
                'midpoint': (midpoint_row, midpoint_col),
                'min_row': min_row, 'max_row': max_row,
                'min_col': min_col, 'max_col': max_col
            }
        elif max_col == min_col: # Vertical tendency
             midpoint_row = (min_row + max_row) / 2.0
             midpoint_col = min_col
             return {
                'orientation': 'vertical',
                'midpoint': (midpoint_row, midpoint_col),
                'min_row': min_row, 'max_row': max_row,
                'min_col': min_col, 'max_col': max_col
            }
        return None # Not identifiable as a simple line


def get_combined_centroid(objects_list):
    """Calculates the centroid of all coordinates from a list of objects."""
    all_coords = []
    for obj in objects_list:
        all_coords.extend(obj['coords'])
    
    if not all_coords:
        return None

    rows = [r for r, c in all_coords]
    cols = [c for r, c in all_coords]
    
    centroid_row = sum(rows) / len(all_coords)
    centroid_col = sum(cols) / len(all_coords)
    
    return (centroid_row, centroid_col)

def transform(input_grid):
    """
    Transforms the input grid by moving dot objects relative to a central line object.
    """
    input_array = np.array(input_grid, dtype=int)
    output_array = np.copy(input_array)
    height, width = input_array.shape

    # 1. Identify all distinct non-background colored objects
    all_objects = find_all_objects(input_array)

    if not all_objects:
        return input_grid # No objects, return original grid

    # 2. Determine the largest object (line) and others (dots)
    all_objects.sort(key=lambda x: x['size'], reverse=True)
    line_object = all_objects[0]
    dot_objects = all_objects[1:]

    # 3. & 4. Find line properties (orientation, midpoint)
    line_properties = get_line_properties(line_object['coords'])
    if line_properties is None:
        # Fallback or error handling if largest object isn't a line
        print("Warning: Largest object doesn't appear to be a simple line.")
        # As a fallback, perhaps don't move anything? Or make a best guess?
        # For now, return original grid if line isn't clear.
        return input_grid 
        
    line_midpoint = line_properties['midpoint']
    line_orientation = line_properties['orientation']

    if not dot_objects:
        return input_grid # No dots to move

    # 5. Calculate the combined centroid of all dot objects
    dots_centroid = get_combined_centroid(dot_objects)
    if dots_centroid is None:
         return input_grid # Should not happen if dot_objects is not empty

    dots_centroid_row, dots_centroid_col = dots_centroid

    # 6. Determine movement vector (direction and magnitude)
    move_dr = 0
    move_dc = 0
    
    if line_orientation == 'horizontal':
        line_midpoint_col = line_midpoint[1]
        magnitude = abs(dots_centroid_col - line_midpoint_col)
        # Round magnitude to nearest integer for grid movement
        move_magnitude = int(round(magnitude)) 
        if dots_centroid_col < line_midpoint_col:
            move_dc = move_magnitude  # Move right
        elif dots_centroid_col > line_midpoint_col:
            move_dc = -move_magnitude # Move left
            
    elif line_orientation == 'vertical':
        line_midpoint_row = line_midpoint[0]
        magnitude = abs(dots_centroid_row - line_midpoint_row)
         # Round magnitude to nearest integer for grid movement
        move_magnitude = int(round(magnitude))
        if dots_centroid_row < line_midpoint_row:
            move_dr = move_magnitude  # Move down
        elif dots_centroid_row > line_midpoint_row:
            move_dr = -move_magnitude # Move up

    # 7. Create the output grid (already done by copying)

    # 8. Erase original dot objects
    for dot_obj in dot_objects:
        for r, c in dot_obj['coords']:
            if 0 <= r < height and 0 <= c < width:
                output_array[r, c] = 0 # Set to background color (white)

    # 9. Draw dot objects in new positions
    for dot_obj in dot_objects:
        color = dot_obj['color']
        for r, c in dot_obj['coords']:
            new_r, new_c = r + move_dr, c + move_dc
            # Draw only if the new position is within grid bounds
            if 0 <= new_r < height and 0 <= new_c < width:
                output_array[new_r, new_c] = color

    return output_array.tolist()