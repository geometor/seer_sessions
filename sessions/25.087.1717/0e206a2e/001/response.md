```python
import numpy as np
from scipy.ndimage import label, find_objects
from collections import defaultdict
import math

"""
This program transforms an input grid based on identifying a 'pattern object', pairs of red and blue pixels, and associated yellow pixels.

1.  **Find Pattern Object:** Identifies the largest contiguous object (group of connected pixels of the same color) that is not composed solely of red (2), blue (1), or yellow (4). The color of this object is recorded ('Line Color').
2.  **Identify Targets and Association:** Locates all red, blue, and yellow pixels. Determines which of these are 'associated' with the pattern object (either part of it or directly adjacent, cardinally or diagonally).
3.  **Find Valid Pairs:** Finds pairs of (Red pixel, Blue pixel) where neither pixel in the pair is associated with the pattern object.
4.  **Initialize Output & Remove Pattern:** Creates an output grid by copying the input, then removes the pattern object by setting its pixels to white (0).
5.  **Draw Lines:** For each valid (Red, Blue) pair:
    a.  Calculates the coordinates for a line segment connecting them using the 'Line Color'.
    b.  The line segment runs along the main cardinal axis (horizontal or vertical) between the pair.
    c.  It starts one pixel away from the Blue pixel (towards Red) and ends one pixel away from the Red pixel (towards Blue).
    d.  Draws this line on the output grid. The original Red and Blue pixels of the pair are removed (set to white 0).
6.  **Reposition Yellows:** Identifies Yellow pixels not associated with the pattern object.
    a.  For each such Yellow pixel, finds the closest Red or Blue pixel that belongs to a valid pair found in step 3.
    b.  If the distance is within a threshold (<= 5 units):
        i.  Determines which end (Red or Blue) of the pair the Yellow is closest to.
        ii. Finds the corresponding end-pixel of the line segment drawn for that pair in step 5.
        iii.Calculates the Yellow's original column offset relative to its closest Red/Blue partner.
        iv. Removes the original Yellow pixel from the output grid.
        v.  Places the Yellow pixel in the output grid at a new location: same row as the line segment's end-pixel, and column calculated by adding the original column offset to the line segment end-pixel's column.
7.  **Final Output:** Returns the modified grid containing the drawn lines and repositioned yellows, with the pattern object and original paired red/blue/yellow pixels removed.
"""

def get_neighbors(coord, grid_shape, include_diagonal=True):
    """Gets valid neighbor coordinates for a given coordinate."""
    r, c = coord
    neighbors = []
    rows, cols = grid_shape
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            if not include_diagonal and abs(dr) + abs(dc) != 1:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
    return neighbors

def find_connected_components(grid):
    """Finds all connected components (objects) in the grid."""
    objects = defaultdict(list)
    labeled_grid, num_features = label(grid > 0) # Label non-background pixels

    if num_features == 0:
        return objects

    # Use find_objects to get bounding boxes, then refine
    slices = find_objects(labeled_grid)
    for i, sl in enumerate(slices):
        if sl is None: continue
        label_id = i + 1
        component_mask = (labeled_grid[sl] == label_id)
        coords = np.argwhere(component_mask)
        
        # Adjust coordinates relative to the original grid
        offset_r, offset_c = sl[0].start, sl[1].start
        abs_coords = [(r + offset_r, c + offset_c) for r, c in coords]

        # Get the color (assuming uniform color within component)
        if abs_coords:
            color = grid[abs_coords[0]]
            objects[label_id] = {'color': color, 'coords': abs_coords, 'size': len(abs_coords)}

    return objects
    
def calculate_distance(p1, p2):
    """Calculates Euclidean distance between two points."""
    return math.sqrt((p1[0] - p2[0])**2 + (p1[1] - p2[1])**2)


def transform(input_grid_np):
    """
    Applies the transformation rule to the input grid.
    """
    input_grid = input_grid_np.tolist() # Work with lists of lists for easier modification initially
    rows = len(input_grid)
    cols = len(input_grid[0])
    output_grid = [row[:] for row in input_grid] # Make a deep copy

    # --- 1. Find Pattern Object ---
    objects = find_connected_components(np.array(input_grid))
    pattern_object = None
    max_size = -1
    pattern_object_pixels = set()
    line_color = 0 # Default to white if no pattern object found

    candidate_objects = []
    for obj_id, obj_data in objects.items():
        color = obj_data['color']
        # Exclude objects made entirely of red, blue, or yellow
        if color not in [1, 2, 4]:
             candidate_objects.append(obj_data)

    if candidate_objects:
        # Find the largest among the candidates
        pattern_object = max(candidate_objects, key=lambda o: o['size'])
        line_color = pattern_object['color']
        pattern_object_pixels = set(pattern_object['coords'])
        # print(f"Found Pattern Object: Color={line_color}, Size={pattern_object['size']}")
    else:
        # Handle case where no suitable pattern object is found (maybe return input?)
        # print("No suitable pattern object found.")
        pass # Continue processing without a pattern object removal/line color?

    # --- 2. Identify Targets and Association ---
    red_pixels = []
    blue_pixels = []
    yellow_pixels = []
    for r in range(rows):
        for c in range(cols):
            color = input_grid[r][c]
            if color == 2:
                red_pixels.append((r, c))
            elif color == 1:
                blue_pixels.append((r, c))
            elif color == 4:
                yellow_pixels.append((r, c))

    associated_pixels = set(pattern_object_pixels)
    if pattern_object:
        for r_obj, c_obj in pattern_object_pixels:
            neighbors = get_neighbors((r_obj, c_obj), (rows, cols), include_diagonal=True)
            associated_pixels.update(neighbors)

    non_associated_red = [p for p in red_pixels if p not in associated_pixels]
    non_associated_blue = [p for p in blue_pixels if p not in associated_pixels]
    non_associated_yellow = [p for p in yellow_pixels if p not in associated_pixels]

    # --- 3. Find Valid Pairs ---
    # For simplicity, assume pairs are axis-aligned and unique for now
    # A more robust approach might check distances or relative positions
    valid_pairs = []
    paired_red = set()
    paired_blue = set()
    all_pair_partners = [] # Store coords of all red/blue pixels in valid pairs

    # Try pairing based on being on the same row or column
    # Horizontal pairs
    row_blues = defaultdict(list)
    row_reds = defaultdict(list)
    for r, c in non_associated_blue: row_blues[r].append((r,c))
    for r, c in non_associated_red: row_reds[r].append((r,c))

    for r in row_blues:
        if r in row_reds:
            # Simple 1-to-1 pairing for now
            for b_coord in row_blues[r]:
                 if b_coord in paired_blue: continue
                 # Find closest red in the same row
                 closest_r_coord = min(row_reds[r], key=lambda r_coord: abs(r_coord[1] - b_coord[1]) if r_coord not in paired_red else float('inf'))
                 if closest_r_coord not in paired_red:
                     valid_pairs.append({'red': closest_r_coord, 'blue': b_coord, 'axis': 'h'})
                     paired_red.add(closest_r_coord)
                     paired_blue.add(b_coord)
                     all_pair_partners.extend([closest_r_coord, b_coord])


    # Vertical pairs (only consider remaining unpaired pixels)
    col_blues = defaultdict(list)
    col_reds = defaultdict(list)
    for r, c in non_associated_blue:
        if (r,c) not in paired_blue: col_blues[c].append((r,c))
    for r, c in non_associated_red:
        if (r,c) not in paired_red: col_reds[c].append((r,c))

    for c in col_blues:
        if c in col_reds:
             # Simple 1-to-1 pairing for now
            for b_coord in col_blues[c]:
                 if b_coord in paired_blue: continue
                 # Find closest red in the same column
                 closest_r_coord = min(col_reds[c], key=lambda r_coord: abs(r_coord[0] - b_coord[0]) if r_coord not in paired_red else float('inf'))
                 if closest_r_coord not in paired_red:
                     valid_pairs.append({'red': closest_r_coord, 'blue': b_coord, 'axis': 'v'})
                     paired_red.add(closest_r_coord)
                     paired_blue.add(b_coord)
                     all_pair_partners.extend([closest_r_coord, b_coord])

    # --- 4. Initialize Output Grid and Remove Pattern Object ---
    if pattern_object:
        for r_obj, c_obj in pattern_object_pixels:
            output_grid[r_obj][c_obj] = 0 # Set pattern object pixels to white

    # --- 5. Draw Lines ---
    line_endpoints = {} # Store {pair_index: {'red_end': (r,c), 'blue_end': (r,c)}}
    pixels_to_clear = set() # Track original pair pixels to remove

    for i, pair in enumerate(valid_pairs):
        r_r, c_r = pair['red']
        r_b, c_b = pair['blue']
        pixels_to_clear.add((r_r, c_r))
        pixels_to_clear.add((r_b, c_b))

        start_r, start_c = -1, -1 # Pixel next to blue, towards red
        end_r, end_c = -1, -1 # Pixel next to red, towards blue

        if pair['axis'] == 'h': # Horizontal
            start_r, end_r = r_r, r_r # Same row
            if c_r > c_b: # Red is right of Blue
                start_c = c_b + 1
                end_c = c_r - 1
                for c in range(start_c, end_c + 1):
                   if 0 <= c < cols: output_grid[start_r][c] = line_color
            else: # Blue is right of Red
                start_c = c_b - 1
                end_c = c_r + 1
                for c in range(end_c, start_c + 1):
                    if 0 <= c < cols: output_grid[start_r][c] = line_color
            line_endpoints[i] = {'blue_end': (start_r, start_c), 'red_end': (end_r, end_c)}

        elif pair['axis'] == 'v': # Vertical
            start_c, end_c = c_r, c_r # Same col
            if r_r > r_b: # Red is below Blue
                start_r = r_b + 1
                end_r = r_r - 1
                for r in range(start_r, end_r + 1):
                   if 0 <= r < rows: output_grid[r][start_c] = line_color
            else: # Blue is below Red
                start_r = r_b - 1
                end_r = r_r + 1
                for r in range(end_r, start_r + 1):
                    if 0 <= r < rows: output_grid[r][start_c] = line_color
            line_endpoints[i] = {'blue_end': (start_r, start_c), 'red_end': (end_r, end_c)}

    # --- 6 & 7. Identify and Reposition Yellow Pixels ---
    yellows_to_move = [] # Store (original_coord, new_coord)

    for y_coord in non_associated_yellow:
        if not all_pair_partners: break # No pairs to associate with

        # Find closest red/blue partner
        closest_dist = float('inf')
        closest_partner = None
        partner_type = None # 'red' or 'blue'
        closest_pair_index = -1

        for idx, pair in enumerate(valid_pairs):
             dist_r = calculate_distance(y_coord, pair['red'])
             dist_b = calculate_distance(y_coord, pair['blue'])

             if dist_r < closest_dist:
                 closest_dist = dist_r
                 closest_partner = pair['red']
                 partner_type = 'red'
                 closest_pair_index = idx
             if dist_b < closest_dist:
                 closest_dist = dist_b
                 closest_partner = pair['blue']
                 partner_type = 'blue'
                 closest_pair_index = idx

        # Check distance threshold
        if closest_dist <= 5.0 and closest_pair_index != -1:
            # Get corresponding line endpoint
            if partner_type == 'red':
                line_end_coord = line_endpoints[closest_pair_index]['red_end']
            else: # partner_type == 'blue'
                line_end_coord = line_endpoints[closest_pair_index]['blue_end']

            # Calculate original column offset
            col_offset = y_coord[1] - closest_partner[1]

            # Calculate new position
            new_r = line_end_coord[0]
            new_c = line_end_coord[1] + col_offset

            # Check bounds before adding to move list
            if 0 <= new_r < rows and 0 <= new_c < cols:
                 yellows_to_move.append({'from': y_coord, 'to': (new_r, new_c)})


    # Perform yellow moves after calculating all
    moved_yellow_origins = set()
    for move in yellows_to_move:
        from_r, from_c = move['from']
        to_r, to_c = move['to']
        
        # Important: Only clear original if not overwritten by a line or another yellow's target
        # Check if target is already occupied by something important (line, another yellow)
        # Simple approach: just move, potentially overwriting. Refined logic might be needed.
        
        # Clear original position (add to set to clear later, avoid issues if multiple yellows map to same origin)
        moved_yellow_origins.add((from_r, from_c))
        
        # Place yellow at new position
        output_grid[to_r][to_c] = 4 # Yellow color


    # --- 8. Final Cleanup ---
    # Clear original red/blue pair pixels and moved yellow origins
    pixels_to_clear.update(moved_yellow_origins)
    for r_clear, c_clear in pixels_to_clear:
         # Only clear if not occupied by a *newly placed* yellow target or a line segment endpoint
         is_new_yellow_target = any(move['to'] == (r_clear, c_clear) for move in yellows_to_move)
         is_line_endpoint = any(ep == (r_clear, c_clear) for pair_ends in line_endpoints.values() for ep in pair_ends.values())
         
         # Check if it's part of a drawn line segment (more thorough)
         is_on_line = False
         # ... (complex to check efficiently here, current drawing overwrites anyway)

         # Simple clear for now
         if not is_new_yellow_target: # Prioritize keeping the moved yellow
              output_grid[r_clear][c_clear] = 0


    return np.array(output_grid) # Convert back to numpy array

```