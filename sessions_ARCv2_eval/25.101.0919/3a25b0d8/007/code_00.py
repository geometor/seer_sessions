import numpy as np
from collections import Counter, deque

"""
Transformation Rule:
1. Identify the background color (most frequent pixel value) and the container color (the non-background color adjacent to the most diverse set of other non-background colors).
2. Find all distinct, connected objects composed solely of the container color ('container_objects'). Find all distinct, connected objects composed of any single color that is neither the background color nor the container color ('content_objects'). Use 4-connectivity for object definition.
3. Map content objects to patterns: For each content_object, find its adjacent (8-way) container_color pixels ('frame_coords'). If frame_coords exist and the content_object hasn't been processed, store its coordinates ('content_coords'), the frame_coords, and the minimum row index from content_coords ('sort_key'). Mark the content_object's coordinates as processed.
4. Extract and Sort Patterns: For each stored definition, combine content_coords and frame_coords, calculate the minimal bounding box, extract the corresponding subgrid ('pattern_grid') from the input, and store the pair (sort_key, pattern_grid). Sort these pairs by sort_key.
5. Assemble and Duplicate Rows: Concatenate all rows from the sorted pattern_grids into an initial list ('assembled_rows'). Create a final list ('final_rows'). Iterate through assembled_rows: add the row to final_rows. Then, extract the 'true_content_pixels' (those != background and != container color). If this sequence is non-empty and palindromic, add the row to final_rows again.
6. Pad and Finalize: Calculate the maximum width of rows in final_rows. Pad each row symmetrically with the background_color to match this width. Stack the padded rows to form the output grid.
"""

# --- Helper Functions ---

def find_objects(grid, color, connectivity=4):
    """
    Finds all connected components of a given color using BFS.
    Returns a list of sets, where each set contains (row, col) tuples for an object.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    if connectivity == 4:
        deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    elif connectivity == 8:
        deltas = [(dr, dc) for dr in [-1, 0, 1] for dc in [-1, 0, 1] if not (dr == 0 and dc == 0)]
    else:
        raise ValueError("Connectivity must be 4 or 8")

    for r in range(height):
        for c in range(width):
            if grid[r, c] == color and not visited[r, c]:
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))
                    for dr, dc in deltas:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                if obj_coords:
                    objects.append(obj_coords)
    return objects

def get_neighbors(r, c, height, width, connectivity=8):
    """Gets valid neighbor coordinates based on connectivity."""
    neighbors = set()
    if connectivity == 4:
        deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    elif connectivity == 8:
        deltas = [(dr, dc) for dr in [-1, 0, 1] for dc in [-1, 0, 1] if not (dr == 0 and dc == 0)]
    else:
        raise ValueError("Connectivity must be 4 or 8")
        
    for dr, dc in deltas:
        nr, nc = r + dr, c + dc
        if 0 <= nr < height and 0 <= nc < width:
            neighbors.add((nr, nc))
    return neighbors

def get_bounding_box(coords):
    """Calculates the min/max row/col for a set of coordinates."""
    if not coords:
        return None
    rows = [r for r, c in coords]
    cols = [c for r, c in coords]
    if not rows or not cols: return None # Handle empty lists case
    return min(rows), min(cols), max(rows), max(cols)

def is_palindrome(seq):
    """Checks if a list or tuple is a palindrome."""
    # Convert numpy array row to list if necessary
    if isinstance(seq, np.ndarray):
        seq = seq.tolist()
    return seq == seq[::-1]

# --- Main Transformation Function ---

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape

    # Handle edge cases
    if grid.size == 0: return []
    unique_colors, counts = np.unique(grid, return_counts=True)
    if len(unique_colors) <= 1: return input_grid 

    # --- Step 1: Identify Colors ---
    background_color = unique_colors[np.argmax(counts)]
    non_background_colors = [c for c in unique_colors if c != background_color]
    if not non_background_colors: return input_grid

    # --- Step 2: Identify Container Color ---
    adjacency_map = {color: set() for color in non_background_colors}
    all_objects_cache = {} # Cache objects: {color: [obj1_coords, obj2_coords,...]}

    # Build adjacency map based on 8-way connectivity between different non-background colors
    for current_color in non_background_colors:
        if current_color not in all_objects_cache:
            all_objects_cache[current_color] = find_objects(grid, current_color, connectivity=4)

        for obj_coords in all_objects_cache[current_color]:
            for r, c in obj_coords:
                # Check 8-way neighbors
                for nr, nc in get_neighbors(r, c, height, width, connectivity=8):
                    neighbor_color = grid[nr, nc]
                    if neighbor_color != background_color and neighbor_color != current_color:
                        adjacency_map[neighbor_color].add(current_color)

    # Determine container color by max diversity of adjacent colors
    container_color = -1
    max_diversity = -1
    sorted_non_bg = sorted(non_background_colors) # Deterministic tie-breaking

    for potential_container in sorted_non_bg:
        diversity = len(adjacency_map.get(potential_container, set()))
        if diversity > max_diversity:
            max_diversity = diversity
            container_color = potential_container
        # If diversity is equal, the sort order provides tie-breaking

    # Fallback if heuristic fails
    if container_color == -1:
         if len(non_background_colors) == 1:
              container_color = non_background_colors[0] 
         else: # Fallback: largest non-background object color
              max_size = -1
              for c in sorted_non_bg:
                   if c not in all_objects_cache: all_objects_cache[c] = find_objects(grid, c, connectivity=4)
                   if all_objects_cache.get(c):
                        current_max = max(len(obj) for obj in all_objects_cache[c])
                        if current_max > max_size:
                             max_size = current_max
                             container_color = c
              if container_color == -1: return [] # Total failure to identify container

    # --- Step 3: Locate Objects ---
    content_colors = [c for c in non_background_colors if c != container_color]
    all_content_objects = []
    for c_color in content_colors:
        if c_color not in all_objects_cache:
            all_objects_cache[c_color] = find_objects(grid, c_color, connectivity=4)
        all_content_objects.extend(all_objects_cache.get(c_color, []))

    # container_objects are needed implicitly by checking grid[nr,nc] == container_color later
    # No need to explicitly find them unless optimizing the frame finding step

    # --- Step 4: Map Content to Patterns ---
    pattern_definitions = []
    processed_content_coords = set() 

    for content_object_coords in all_content_objects:
        # Check if already processed
        if not content_object_coords.isdisjoint(processed_content_coords):
            continue

        frame_coords = set()
        min_content_row = height 
        
        # Find adjacent container pixels and min content row
        for r_content, c_content in content_object_coords:
            min_content_row = min(min_content_row, r_content)
            # Check 8-way neighbors for container color
            for nr, nc in get_neighbors(r_content, c_content, height, width, connectivity=8):
                if grid[nr, nc] == container_color:
                    frame_coords.add((nr, nc))

        # If content touches container color
        if frame_coords:
            pattern_definitions.append({
                'content_coords': content_object_coords,
                'frame_coords': frame_coords,
                'sort_key': min_content_row,
            })
            # Mark as processed
            processed_content_coords.update(content_object_coords)

    # --- Step 5: Extract and Sort Patterns ---
    extracted_patterns = []
    for definition in pattern_definitions:
        content_coords = definition['content_coords']
        frame_coords = definition['frame_coords']
        sort_key = definition['sort_key']
        
        pattern_coords = content_coords.union(frame_coords)
        
        bb = get_bounding_box(pattern_coords)
        if bb:
            min_r, min_c, max_r, max_c = bb
            # Clamp bounds to grid dimensions (redundant if get_neighbors is correct, but safe)
            min_r = max(0, min_r); min_c = max(0, min_c)
            max_r = min(height - 1, max_r); max_c = min(width - 1, max_c)
            
            if max_r >= min_r and max_c >= min_c: 
                pattern_grid = grid[min_r : max_r + 1, min_c : max_c + 1]
                extracted_patterns.append((sort_key, pattern_grid.tolist())) # Store pattern as list of lists

    # Sort patterns by the minimum row of their original content
    extracted_patterns.sort(key=lambda x: x[0])

    # --- Step 6: Assemble and Duplicate Rows ---
    assembled_rows = []
    for _, pattern_grid in extracted_patterns:
        assembled_rows.extend(pattern_grid) # Concatenate rows from sorted patterns

    final_rows = []
    for row in assembled_rows:
        final_rows.append(list(row)) # Add row (ensure it's a list)

        # Extract true content pixels for palindrome check
        true_content_pixels = [p for p in row if p != background_color and p != container_color]

        # Apply duplication rule
        if true_content_pixels and is_palindrome(true_content_pixels):
            final_rows.append(list(row)) # Add again if non-empty palindrome

    if not final_rows:
        return [] # Return empty if no patterns resulted in rows

    # --- Step 7: Pad and Finalize ---
    max_width = 0
    for row in final_rows:
        max_width = max(max_width, len(row))

    output_grid = []
    for row in final_rows:
        current_width = len(row)
        pad_total = max_width - current_width
        pad_left = pad_total // 2
        pad_right = pad_total - pad_left
        # Construct the padded row
        padded_row = ([background_color] * pad_left) + row + ([background_color] * pad_right)
        output_grid.append(padded_row)

    return output_grid