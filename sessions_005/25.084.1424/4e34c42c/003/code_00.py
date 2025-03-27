import numpy as np
from collections import deque

"""
This program transforms an input grid based on identifying specific non-background objects and arranging them according to certain criteria.

1.  Identify the background color (most frequent color).
2.  Find all distinct objects (contiguous non-background pixels using 8-way connectivity).
3.  Determine a selection criterion:
    - 'maroon_adj': Objects adjacent (8-way) to maroon (9) pixels.
    - 'azure_contain': Objects containing azure (8) pixels.
    Only one criterion will apply per grid.
4.  Select objects matching the criterion.
5.  Calculate the bounding box for each selected object:
    - If 'maroon_adj', include the object pixels AND adjacent maroon pixels.
    - If 'azure_contain', include ONLY the object pixels.
6.  Determine assembly order based on the minimum column index of the object's original pixels:
    - If 'maroon_adj', sort right-to-left (descending min_col).
    - If 'azure_contain', sort left-to-right (ascending min_col).
7.  Extract the subgrids corresponding to the calculated bounding boxes.
8.  Concatenate the extracted subgrids horizontally in the determined order to form the output grid.
"""

# --- Helper Functions ---

def find_most_frequent_color(grid):
    """Finds the most frequent color (integer value) in the grid."""
    unique, counts = np.unique(grid, return_counts=True)
    if not unique.size:
        return 0 # Default background if grid is empty
    return unique[np.argmax(counts)]

def find_objects(grid, background_color):
    """
    Finds all distinct objects (contiguous non-background pixels) using 8-way connectivity.
    Returns a list of objects, where each object is represented by a list of its pixel coordinates [(r1, c1), (r2, c2), ...].
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    # Define 8 neighbors (relative coordinates)
    neighbors = [(-1, -1), (-1, 0), (-1, 1),
                 (0, -1),          (0, 1),
                 (1, -1), (1, 0), (1, 1)]

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != background_color and not visited[r, c]:
                # Start BFS to find a new object
                current_object_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    curr_r, curr_c = q.popleft()
                    current_object_pixels.append((curr_r, curr_c))
                    
                    # Explore neighbors
                    for dr, dc in neighbors:
                        nr, nc = curr_r + dr, curr_c + dc
                        
                        # Check bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # Check if neighbor is part of an object and not visited
                            if grid[nr, nc] != background_color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                                
                if current_object_pixels:
                    objects.append(np.array(current_object_pixels)) # Store as numpy array for easier slicing later
                    
    return objects

def get_adjacent_pixels_of_color(grid, obj_pixels_set, target_color):
    """
    Finds all pixels of target_color adjacent (8-way) to any pixel in obj_pixels_set.
    Args:
        grid (np.array): The input grid.
        obj_pixels_set (set): A set of (r, c) tuples representing the object's pixels.
        target_color (int): The color to search for in adjacent cells.
    Returns:
        set: A set of (r, c) tuples for adjacent pixels of target_color.
    """
    rows, cols = grid.shape
    adjacent_coords = set()
    neighbors = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    for r, c in obj_pixels_set:
        for dr, dc in neighbors:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if the neighbor has the target color AND is not part of the object itself
                if grid[nr, nc] == target_color and (nr, nc) not in obj_pixels_set:
                    adjacent_coords.add((nr, nc))
    return adjacent_coords

def check_adjacency(grid, obj_pixels_set, adj_color):
    """Checks if any pixel of the object is adjacent (8-way) to the adj_color."""
    rows, cols = grid.shape
    neighbors = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    for r, c in obj_pixels_set:
        for dr, dc in neighbors:
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == adj_color:
                 # Ensure the adjacent pixel isn't part of the object itself (relevant if obj can contain adj_color)
                 if (nr, nc) not in obj_pixels_set:
                     return True
    return False

def check_containment(grid, obj_pixels, contain_color):
    """Checks if any pixel within the object has the contain_color."""
    for r, c in obj_pixels:
        if grid[r, c] == contain_color:
            return True
    return False

def get_bounding_box(pixels):
    """Calculates the bounding box (min_r, min_c, max_r, max_c) for a set of pixel coordinates."""
    if not pixels: # Handle empty list/set
        return None
    
    pixels_np = np.array(list(pixels)) # Convert set or list of tuples to numpy array
    if pixels_np.size == 0:
        return None
        
    min_row = np.min(pixels_np[:, 0])
    min_col = np.min(pixels_np[:, 1])
    max_row = np.max(pixels_np[:, 0])
    max_col = np.max(pixels_np[:, 1])
    return min_row, min_col, max_row, max_col

# --- Main Transformation Function ---

def transform(input_grid):
    """
    Transforms the input grid by selecting objects based on adjacency to maroon (9)
    or containment of azure (8), calculating their bounding boxes (conditionally
    including adjacent maroon), sorting them (right-to-left for maroon, left-to-right
    for azure), and concatenating their extracted subgrids horizontally.
    """
    input_np = np.array(input_grid, dtype=int)
    if input_np.size == 0:
        return [] # Handle empty input

    # 1. Identify background color
    background_color = find_most_frequent_color(input_np)

    # 2. Identify all distinct non-background objects
    # Objects are returned as a list of numpy arrays, each array containing [(r,c), ...] coordinates
    all_objects = find_objects(input_np, background_color)

    if not all_objects:
        return [] # No objects found

    target_objects_info = []
    criterion = None # 'maroon_adj' or 'azure_contain'
    maroon_color = 9
    azure_color = 8

    # 3 & 4. Determine selection rule and filter objects
    objects_with_maroon_adj = []
    objects_with_azure_contain = []

    for idx, obj_pixels in enumerate(all_objects):
        if obj_pixels.size == 0:
            continue
        
        obj_pixels_set = set(map(tuple, obj_pixels)) # Use set for faster lookups

        # Check for maroon adjacency
        if check_adjacency(input_np, obj_pixels_set, maroon_color):
            objects_with_maroon_adj.append(idx)
            
        # Check for azure containment
        if check_containment(input_np, obj_pixels, azure_color):
             objects_with_azure_contain.append(idx)

    # Determine the criterion based on which list is non-empty
    target_indices = []
    if objects_with_maroon_adj:
        criterion = 'maroon_adj'
        target_indices = objects_with_maroon_adj
    elif objects_with_azure_contain:
        criterion = 'azure_contain'
        target_indices = objects_with_azure_contain
    else:
        # No matching objects found based on the known criteria
        return []

    # 5. Calculate bounding boxes for target objects
    for obj_idx in target_indices:
        obj_pixels = all_objects[obj_idx]
        obj_pixels_set = set(map(tuple, obj_pixels)) # Convert to set for efficiency

        if criterion == 'maroon_adj':
            # Include adjacent maroon pixels in the bounding box calculation
            adj_maroon_pixels_set = get_adjacent_pixels_of_color(input_np, obj_pixels_set, maroon_color)
            all_pixels_for_bbox = obj_pixels_set.union(adj_maroon_pixels_set)
            bbox = get_bounding_box(all_pixels_for_bbox)
        elif criterion == 'azure_contain':
            # Bounding box includes only the object pixels
            bbox = get_bounding_box(obj_pixels_set)
        else: # Should not happen if target_indices is populated
             continue

        if bbox:
            # Calculate min_col based on the *original object pixels* for sorting
            min_r_obj, min_c_obj, max_r_obj, max_c_obj = get_bounding_box(obj_pixels_set)
            
            target_objects_info.append({
                "index": obj_idx,
                "bbox": bbox, # Bbox used for extraction
                "min_col_obj": min_c_obj # Min col of original object used for sorting
            })

    # 6. Determine assembly order
    if criterion == 'maroon_adj':
        # Sort descending by min_col_obj (right-to-left)
        target_objects_info.sort(key=lambda x: x['min_col_obj'], reverse=True)
    elif criterion == 'azure_contain':
        # Sort ascending by min_col_obj (left-to-right)
        target_objects_info.sort(key=lambda x: x['min_col_obj'], reverse=False)

    # 7. Extract subgrids
    extracted_subgrids = []
    for obj_info in target_objects_info:
        min_r, min_c, max_r, max_c = obj_info['bbox']
        # Extract using the calculated bounding box
        subgrid = input_np[min_r : max_r + 1, min_c : max_c + 1]
        extracted_subgrids.append(subgrid)

    # 8. Concatenate horizontally
    if not extracted_subgrids:
        return [] 

    # Check if all subgrids have the same height before concatenating
    first_height = extracted_subgrids[0].shape[0]
    if not all(sg.shape[0] == first_height for sg in extracted_subgrids):
        # This case indicates a potential issue in logic or assumptions, 
        # as examples suggested consistent heights. Return empty for now.
        print(f"Warning: Subgrids have different heights: {[sg.shape for sg in extracted_subgrids]}")
        return []

    try:
        output_np = np.concatenate(extracted_subgrids, axis=1)
    except ValueError as e:
        # Fallback in case concatenation fails unexpectedly
        print(f"Error concatenating subgrids: {e}")
        return []

    # Convert final numpy array back to list of lists
    output_grid = output_np.tolist()

    return output_grid