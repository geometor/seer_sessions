import numpy as np
from scipy.ndimage import label, find_objects
import math

"""
Identify single-pixel 'markers' (not white 0 or magenta 6) and magenta (6) objects in the input grid. 
Associate each marker with the geometrically closest magenta object. 
For each associated pair, extract the pattern within the magenta object's minimal 4x4 bounding box (using the top-left corner of the minimal bounding box as the anchor, padding with 0 if necessary).
Recolor the extracted 4x4 pattern by changing magenta (6) pixels to the marker's color.
Sort these recolored 4x4 patterns based on the horizontal position (column index) of their original markers.
Concatenate the sorted patterns horizontally to form the output grid.
"""

def find_markers(grid):
    """Finds single pixels that are not background (0) or magenta (6)."""
    markers = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != 0 and color != 6:
                # Check if it's isolated (surrounded by 0 or 6, or grid boundary)
                # Although the examples show single pixels, let's just find non-0/6 colors for now.
                # The logic seems robust even if markers aren't strictly single pixels.
                markers.append({'color': color, 'pos': (r, c)})
    return markers

def find_magenta_objects(grid):
    """Finds connected components of magenta (6) pixels."""
    magenta_mask = grid == 6
    labeled_array, num_features = label(magenta_mask)
    
    # find_objects returns slices, convert them to coordinates
    objects_slices = find_objects(labeled_array)
    objects_coords = []
    
    if num_features > 0:
        for i in range(1, num_features + 1):
            coords = np.argwhere(labeled_array == i)
            if coords.size > 0:
                 # Store as list of (row, col) tuples
                objects_coords.append(coords.tolist())
                
    return objects_coords # List of lists, each inner list contains [row, col] pairs for an object

def get_bounding_box(obj_coords):
    """Calculates the minimal bounding box for a list of coordinates."""
    if not obj_coords:
        return None
    rows = [coord[0] for coord in obj_coords]
    cols = [coord[1] for coord in obj_coords]
    return min(rows), min(cols), max(rows), max(cols)

def calculate_min_distance(marker_pos, obj_coords):
    """Calculates the minimum Euclidean distance between a marker and any pixel of an object."""
    min_dist_sq = float('inf')
    marker_r, marker_c = marker_pos
    for r, c in obj_coords:
        dist_sq = (marker_r - r)**2 + (marker_c - c)**2
        if dist_sq < min_dist_sq:
            min_dist_sq = dist_sq
    return math.sqrt(min_dist_sq)

def extract_and_recolor_4x4_pattern(grid, obj_coords, marker_color):
    """Extracts a 4x4 pattern based on the object's bounding box and recolors it."""
    if not obj_coords:
        return np.zeros((4, 4), dtype=int)

    min_r, min_c, _, _ = get_bounding_box(obj_coords)
    
    # Define the 4x4 extraction area starting from the top-left of the bounding box
    pattern = np.zeros((4, 4), dtype=int)
    
    # Copy the relevant part of the input grid into the 4x4 pattern
    max_extract_r = min(grid.shape[0], min_r + 4)
    max_extract_c = min(grid.shape[1], min_c + 4)
    
    for r_in in range(min_r, max_extract_r):
        for c_in in range(min_c, max_extract_c):
            r_out = r_in - min_r
            c_out = c_in - min_c
            
            color = grid[r_in, c_in]
            # Only copy magenta pixels or background within the *actual* object coords
            # Check if (r_in, c_in) is part of the object
            is_object_pixel = False
            for obj_r, obj_c in obj_coords:
                if obj_r == r_in and obj_c == c_in:
                    is_object_pixel = True
                    break

            if is_object_pixel and color == 6:
                pattern[r_out, c_out] = marker_color # Recolor magenta
            elif is_object_pixel: # If part of object but not magenta (shouldn't happen?)
                 pattern[r_out, c_out] = 0 # Treat as background maybe? Or keep original? Let's use 0.
            # else: keep pattern[r_out, c_out] = 0 (background)
            # Refined logic: Copy everything within the 4x4 box, then recolor ONLY the magenta pixels
            
    # Alternative simpler logic: extract the 4x4 box directly, then recolor
    pattern_direct = np.zeros((4, 4), dtype=int)
    input_rows, input_cols = grid.shape
    for r_pat in range(4):
        for c_pat in range(4):
             r_in = min_r + r_pat
             c_in = min_c + c_pat
             if 0 <= r_in < input_rows and 0 <= c_in < input_cols:
                 color = grid[r_in, c_in]
                 if color == 6:
                     # Check if this specific magenta pixel belongs to *this* object
                     # This check prevents grabbing parts of other nearby magenta objects
                     is_correct_object_pixel = False
                     for obj_r, obj_c in obj_coords:
                         if obj_r == r_in and obj_c == c_in:
                             is_correct_object_pixel = True
                             break
                     if is_correct_object_pixel:
                           pattern_direct[r_pat, c_pat] = marker_color
                 # else: leave as 0 (background)

    return pattern_direct


def transform(input_grid):
    """
    Transforms the input grid according to the rules:
    1. Find markers and magenta objects.
    2. Associate markers with the closest magenta object.
    3. Extract 4x4 patterns based on object bounding boxes.
    4. Recolor patterns using marker colors.
    5. Sort patterns by marker column index.
    6. Concatenate patterns horizontally.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    
    # 1. Find markers and magenta objects
    markers = find_markers(input_grid_np)
    magenta_objects = find_magenta_objects(input_grid_np)
    
    if not markers or not magenta_objects:
        # Handle cases with no markers or no magenta objects if necessary
        # Based on examples, assume there's always at least one pair
        # Return empty or based on specific requirements if needed
        # For now, let's assume valid inputs based on examples.
        # Determining output size might be tricky here. Let's default to 4x0?
         return np.zeros((4, 0), dtype=int) # Match height 4 assumption

    # 2. Associate markers with closest magenta objects
    associations = []
    for marker in markers:
        min_dist = float('inf')
        closest_obj = None
        for obj_coords in magenta_objects:
            if not obj_coords: continue # Skip empty objects if any
            dist = calculate_min_distance(marker['pos'], obj_coords)
            if dist < min_dist:
                min_dist = dist
                closest_obj = obj_coords
                
        if closest_obj:
            associations.append({
                'marker_color': marker['color'],
                'marker_pos': marker['pos'],
                'object_coords': closest_obj
            })

    # 3. & 4. Extract and recolor patterns for each association
    processed_patterns = []
    for assoc in associations:
        pattern = extract_and_recolor_4x4_pattern(
            input_grid_np, 
            assoc['object_coords'], 
            assoc['marker_color']
        )
        # Store pattern along with marker's column for sorting
        processed_patterns.append({
            'pattern': pattern,
            'marker_col': assoc['marker_pos'][1] 
        })

    # 5. Sort patterns by marker column index
    processed_patterns.sort(key=lambda x: x['marker_col'])

    # 6. Concatenate patterns horizontally
    # Assume all patterns are 4x4 as per the extraction logic
    if not processed_patterns:
         return np.zeros((4, 0), dtype=int) # Consistent empty output

    final_patterns = [p['pattern'] for p in processed_patterns]
    
    # Check if final_patterns list is empty before attempting hstack
    if not final_patterns:
        # This case might occur if association failed, though unlikely with current logic
        return np.zeros((4, 0), dtype=int)
        
    output_grid = np.hstack(final_patterns)

    return output_grid.tolist() # Convert back to list of lists if required by ARC standard