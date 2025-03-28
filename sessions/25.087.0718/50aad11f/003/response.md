```python
import numpy as np
from scipy.ndimage import label, find_objects
import math

"""
Identifies 'markers' (pixels not white 0 or magenta 6) and 'magenta shapes' (connected magenta 6 pixels) in the input grid.
Associates each marker with the geometrically closest magenta shape based on minimum Euclidean distance.
For each association, extracts a 4x4 pattern:
  Finds the top-left corner of the magenta shape's bounding box.
  Creates a 4x4 grid (initially white 0).
  For each pixel belonging *only* to the associated magenta shape, calculates its position relative to the bounding box top-left corner.
  If the relative position is within the 4x4 bounds, sets the corresponding pixel in the 4x4 grid to the marker's color.
Determines the arrangement direction by comparing the range of marker row indices to the range of marker column indices.
  If row_range > col_range, arrangement is 'vertical', sort key is marker row index.
  Otherwise (col_range >= row_range or single marker), arrangement is 'horizontal', sort key is marker column index.
Sorts the generated 4x4 patterns based on the determined sort key.
Concatenates the sorted patterns: vertically if arrangement is 'vertical', horizontally otherwise.
"""

def find_markers(grid):
    """Finds pixels that are not background (0) or magenta (6)."""
    markers = []
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # Identify markers: color is not 0 (white) and not 6 (magenta)
            if color != 0 and color != 6:
                markers.append({'color': color, 'pos': (r, c)})
    return markers

def find_magenta_objects(grid):
    """Finds connected components of magenta (6) pixels."""
    # Create a mask where only magenta pixels are True
    magenta_mask = grid == 6
    # Label connected components in the mask
    labeled_array, num_features = label(magenta_mask)
    
    objects_coords = []
    if num_features > 0:
        # Iterate through each found feature (connected component)
        for i in range(1, num_features + 1):
            # Find the coordinates of all pixels belonging to the current component
            coords = np.argwhere(labeled_array == i)
            if coords.size > 0:
                # Store coordinates as a list of [row, col] pairs
                objects_coords.append(coords.tolist())
                
    return objects_coords # List of lists, each inner list contains [row, col] pairs for an object

def get_bounding_box(obj_coords):
    """Calculates the minimal bounding box (min_row, min_col, max_row, max_col) for a list of coordinates."""
    if not obj_coords:
        return None, None, None, None
    # Extract all row and column coordinates
    rows = [coord[0] for coord in obj_coords]
    cols = [coord[1] for coord in obj_coords]
    # Return the min/max row and column
    return min(rows), min(cols), max(rows), max(cols)

def calculate_min_distance(marker_pos, obj_coords):
    """Calculates the minimum Euclidean distance between a marker point and any point in a list of object coordinates."""
    min_dist_sq = float('inf')
    marker_r, marker_c = marker_pos
    # Calculate squared Euclidean distance to avoid sqrt until the end
    for r, c in obj_coords:
        dist_sq = (marker_r - r)**2 + (marker_c - c)**2
        if dist_sq < min_dist_sq:
            min_dist_sq = dist_sq
    # Return the actual distance
    return math.sqrt(min_dist_sq)

def extract_and_recolor_4x4_pattern(obj_coords, marker_color):
    """
    Creates a 4x4 pattern based on the object's pixels relative
    to its bounding box top-left corner and recolors using the marker color.
    """
    # Handle empty object coordinates list
    if not obj_coords:
        return np.zeros((4, 4), dtype=int)

    # Calculate the top-left corner of the minimal bounding box
    min_r, min_c, _, _ = get_bounding_box(obj_coords)
    if min_r is None: # Check if bounding box calculation failed
         return np.zeros((4, 4), dtype=int)

    # Initialize the 4x4 pattern with background color (0)
    pattern = np.zeros((4, 4), dtype=int)

    # Iterate through *only* the pixels belonging to this specific object
    for r, c in obj_coords:
        # Calculate the relative position within the 4x4 frame anchored at the bounding box top-left
        relative_r = r - min_r
        relative_c = c - min_c

        # Check if the relative position is within the 4x4 bounds (0 to 3)
        if 0 <= relative_r < 4 and 0 <= relative_c < 4:
            # Place the marker's color at this relative position in the pattern
            pattern[relative_r, relative_c] = marker_color

    return pattern


def transform(input_grid):
    """
    Transforms the input grid by associating markers with magenta shapes,
    extracting/recoloring 4x4 patterns, determining arrangement based on marker spread,
    sorting the patterns, and concatenating them.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    
    # 1. Identify Components
    markers = find_markers(input_grid_np)
    magenta_objects = find_magenta_objects(input_grid_np)
    
    # Handle cases with no markers or no magenta objects
    if not markers or not magenta_objects:
         # Return an empty grid (0x0) if essential components are missing
         return np.array([[]], dtype=int).tolist() 

    # 2. Associate Markers to Shapes
    associations = []
    marker_positions = [] # Keep track of marker positions for arrangement logic
    used_objects = set() # Keep track of objects already associated to handle 1-to-1 mapping if needed (though current logic uses closest)

    for marker in markers:
        min_dist = float('inf')
        closest_obj_coords = None
        closest_obj_index = -1

        for idx, obj_coords in enumerate(magenta_objects):
            if not obj_coords: continue # Skip if an object somehow has no coords
            dist = calculate_min_distance(marker['pos'], obj_coords)
            
            # Find the closest object
            if dist < min_dist:
                min_dist = dist
                closest_obj_coords = obj_coords
                closest_obj_index = idx
            # Potential tie-breaking needed? Examples suggest unique closest.
                
        if closest_obj_coords:
            associations.append({
                'marker_color': marker['color'],
                'marker_pos': marker['pos'],
                'object_coords': closest_obj_coords
            })
            marker_positions.append(marker['pos'])
            # Note: Multiple markers might associate with the same object if it's closest to them.

    # Check if any associations were made
    if not associations:
        return np.array([[]], dtype=int).tolist()

    # 3. Extract and Recolor Patterns
    processed_patterns = []
    for assoc in associations:
        pattern = extract_and_recolor_4x4_pattern(
            assoc['object_coords'], 
            assoc['marker_color']
        )
        # Store pattern along with marker's position for sorting
        processed_patterns.append({
            'pattern': pattern,
            'marker_row': assoc['marker_pos'][0], 
            'marker_col': assoc['marker_pos'][1] 
        })

    # 4. Determine Arrangement and Sort Order
    arrangement_mode = 'horizontal' # Default
    sort_key_func = lambda x: x['marker_col'] # Default sort by column

    # Only need to check range if more than one marker exists
    if len(marker_positions) > 1:
        rows = [pos[0] for pos in marker_positions]
        cols = [pos[1] for pos in marker_positions]
        row_range = max(rows) - min(rows)
        col_range = max(cols) - min(cols)

        # If the spread in rows is greater than the spread in columns, arrange vertically
        if row_range > col_range:
            arrangement_mode = 'vertical'
            sort_key_func = lambda x: x['marker_row'] # Sort by row index
        # Otherwise, stick to horizontal arrangement, sorting by column (default)

    # 5. Sort Patterns
    processed_patterns.sort(key=sort_key_func)

    # 6. Combine Patterns
    final_patterns = [p['pattern'] for p in processed_patterns]
    
    # Concatenate based on the determined arrangement mode
    if arrangement_mode == 'vertical':
        output_grid = np.vstack(final_patterns)
    else: # 'horizontal'
        output_grid = np.hstack(final_patterns)

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()
```