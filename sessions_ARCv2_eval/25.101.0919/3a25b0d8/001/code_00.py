import numpy as np
from collections import Counter, deque

# Helper function to find connected components (objects) using BFS
def find_objects(grid, color):
    """Finds all connected components of a given color in the grid."""
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    for r in range(height):
        for c in range(width):
            # If the cell has the target color and hasn't been visited yet
            if grid[r, c] == color and not visited[r, c]:
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check grid boundaries, target color, and visited status
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                # Add the found object (set of coordinates) to the list
                if obj_coords:
                    objects.append(obj_coords)
    return objects

# Helper function to get bounding box of a set of coordinates
def get_bounding_box(coords):
    """Calculates the min/max row/col for a set of coordinates."""
    if not coords:
        return None
    # Transpose coordinates if necessary (e.g., from find_objects)
    if isinstance(coords, set) or isinstance(coords, list) and coords and isinstance(coords[0], tuple):
       rows = [r for r, c in coords]
       cols = [c for r, c in coords]
    else: # Assume numpy array format N x 2
       rows = coords[:, 0]
       cols = coords[:, 1]

    if not rows or not cols:
        return None
        
    return min(rows), min(cols), max(rows), max(cols)


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Identifies patterns within 'containers' in the input grid and stacks them vertically,
    applying a duplication rule for specific rows, and padding the result.

    Transformation Steps:
    1. Identify the background color (most frequent pixel value).
    2. Find all contiguous objects for each color different from the background.
    3. For each object (potential container):
        a. Determine its bounding box.
        b. Identify all pixels within this bounding box that are NOT the background color ('non-background pixels').
        c. Identify all pixels within this bounding box that are NEITHER the background color NOR the container's color ('true content pixels').
        d. If any 'true content pixels' exist for this container object:
            i. Calculate the bounding box of the 'non-background pixels'.
            ii. Extract the rectangular subgrid from the input corresponding to this non-background bounding box. This is the 'pattern'.
            iii. Store the pattern, its top row index (min_r of non-background bbox), and the container color.
    4. Sort the extracted patterns based on their top row index.
    5. Assemble the final output grid row by row:
        a. For each pattern, iterate through its rows.
        b. Add the current row to the output list.
        c. Apply duplication rule: If the 'true content pixels' in the current row consist of exactly 3 pixels of the same color, add the row to the output list again.
    6. Pad all rows in the output list with the background color to match the width of the widest row.
    """
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape

    # Handle empty input grid
    if grid.size == 0: return []
    
    # 1. Identify background color
    counts = Counter(grid.flatten())
    # If grid is uniform color, handle appropriately (e.g., return empty or original)
    # For this task, assume diverse colors exist if examples show it.
    if not counts: return [] 
    background_color = counts.most_common(1)[0][0]

    # 2. Identify potential container colors
    unique_colors = np.unique(grid)
    potential_container_colors = [c for c in unique_colors if c != background_color]

    patterns_data = []

    # Keep track of objects already processed to avoid duplicates 
    processed_objects = set() 

    # 3. & 4. Find container objects and extract potential patterns
    for container_color in potential_container_colors:
        # Find all objects of the current potential container color
        container_objects = find_objects(grid, container_color)
        
        for obj_coords in container_objects:
            # Skip if object is empty
            if not obj_coords: continue
            
            # Use frozenset of coordinates to check if this object was already processed
            # This handles cases where an object might be found via different color searches if needed, though unlikely here.
            obj_frozen = frozenset(obj_coords)
            if obj_frozen in processed_objects:
                continue
            processed_objects.add(obj_frozen)

            # 3a. Get container object's bounding box
            c_bb = get_bounding_box(obj_coords)
            if c_bb is None: continue
            c_min_r, c_min_c, c_max_r, c_max_c = c_bb

            # 3b. Find non-background pixels within container BBox
            # Uses BBox as an approximation for "inside" the container for simplicity.
            non_bg_coords = set()
            for r in range(c_min_r, c_max_r + 1):
                 for c in range(c_min_c, c_max_c + 1):
                     # Check bounds and if pixel is not background
                     if 0 <= r < height and 0 <= c < width and grid[r, c] != background_color:
                         non_bg_coords.add((r,c))

            # 3c. Find true content pixels (non-bg, non-container) within the set of non-bg pixels found
            true_content_coords = set()
            if non_bg_coords:
                 for r, c in non_bg_coords:
                     if grid[r,c] != container_color:
                         true_content_coords.add((r,c))

            # 3d. Check if true content exists for this object
            if true_content_coords:
                 # 3d.i. Get bounding box of *non-background* pixels associated with this object
                 nb_bb = get_bounding_box(non_bg_coords)
                 if nb_bb:
                     nb_min_r, nb_min_c, nb_max_r, nb_max_c = nb_bb
                     
                     # Clamp bbox coordinates to grid dimensions to prevent slicing errors
                     nb_min_r = max(0, nb_min_r)
                     nb_max_r = min(height - 1, nb_max_r)
                     nb_min_c = max(0, nb_min_c)
                     nb_max_c = min(width - 1, nb_max_c)

                     # Ensure bbox is still valid after clamping
                     if nb_max_r >= nb_min_r and nb_max_c >= nb_min_c:
                         # 3d.ii. Extract the pattern subgrid based on the non-background bounding box
                         pattern = grid[nb_min_r:nb_max_r + 1, nb_min_c:nb_max_c + 1]
                         # 3d.iii Store pattern data for later processing
                         patterns_data.append({
                             'min_row': nb_min_r, # Use the top of the non-bg bounding box for sorting
                             'pattern': pattern.tolist(), # Convert numpy array to list of lists
                             'container_color': container_color
                         })

    # 5. Sort patterns based on original vertical position (top of non-bg bbox)
    patterns_data.sort(key=lambda x: x['min_row'])

    # 6. Assemble output rows and apply duplication rule
    output_rows_raw = []
    for data in patterns_data:
        pattern = data['pattern']
        container_color = data['container_color']
        # Iterate through each row of the extracted pattern
        for row in pattern:
            # 6a. Add current row to the list of rows to be potentially included in the output
            output_rows_raw.append(list(row))

            # 6b/c. Check for duplication rule
            # Find pixels in the current row that are neither background nor the container color
            true_content_pixels = [p for p in row if p != background_color and p != container_color]
            
            # Check if there are exactly 3 true content pixels
            if len(true_content_pixels) == 3:
                # Check if all three pixels are identical (only 1 unique color among them)
                if len(set(true_content_pixels)) == 1:
                     # If duplication rule met, add the row again
                     output_rows_raw.append(list(row)) 

    # Handle case where no patterns were found or processed
    if not output_rows_raw:
         return []

    # 7. Pad rows to max width
    max_width = 0
    # Find the maximum width among all collected rows
    for row in output_rows_raw:
        max_width = max(max_width, len(row))

    output_grid_final = []
    # Pad each row to the maximum width using the background color
    for row in output_rows_raw:
        current_width = len(row)
        pad_total = max_width - current_width
        # Calculate padding for left and right sides for centering
        pad_left = pad_total // 2
        pad_right = pad_total - pad_left
        # Construct the padded row
        padded_row = [background_color] * pad_left + row + [background_color] * pad_right
        output_grid_final.append(padded_row)

    return output_grid_final