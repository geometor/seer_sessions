```python
import numpy as np
from collections import Counter, deque

"""
Transformation Rule:
1. Identify the background color (most frequent pixel value).
2. Identify the 'container' color: This is the non-background color whose objects are most consistently found adjacent to objects of other diverse non-background colors ('true content').
3. Find all distinct connected objects ('content_blobs') composed of pixels that are neither the background color nor the container color.
4. For each content_blob:
    a. Find all container color pixels ('frame_pixels') adjacent (8-way) to the content_blob.
    b. If frame_pixels exist, combine the coordinates of the content_blob and frame_pixels.
    c. Calculate the minimal bounding box enclosing these combined coordinates.
    d. Extract the rectangular subgrid ('pattern') defined by the bounding box.
    e. Record the pattern and the minimum row index of the content_blob's coordinates.
    f. Mark the content_blob as processed to avoid duplicates.
5. Sort the extracted patterns based on the minimum row index of their original content (top to bottom).
6. Assemble the output rows:
    a. Create a list by sequentially taking all rows from the sorted patterns.
    b. Create a final list. Iterate through the assembled rows:
        i. Add the current row to the final list.
        ii. Extract the 'true_content' pixels from the row (pixels != background and != container_color).
        iii. If the true_content pixel sequence is non-empty and horizontally symmetrical (a palindrome), add the row to the final list again.
7. Pad the final list of rows: Calculate the maximum width and pad each row symmetrically with the background color to match this width.
8. Construct the final output grid by stacking the padded rows.
"""

# --- Helper Functions ---

def find_objects(grid, color, connectivity=4):
    """
    Finds all connected components of a given color using BFS.
    Connectivity: 4 (von Neumann) or 8 (Moore).
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
    """Gets valid neighbor coordinates."""
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
    return seq == seq[::-1]

# --- Main Transformation Function ---

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule described in the module docstring.
    """
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape

    # Handle empty or trivial grids
    if grid.size == 0: return []
    unique_colors, counts = np.unique(grid, return_counts=True)
    if len(unique_colors) <= 1: return input_grid # No transformation needed

    # --- Step 1: Identify Background Color ---
    background_color = unique_colors[np.argmax(counts)]
    non_background_colors = [c for c in unique_colors if c != background_color]

    # Handle case where only background exists after filtering
    if not non_background_colors: return input_grid

    # --- Step 2: Identify Container Color ---
    adjacency_map = {color: set() for color in non_background_colors}
    all_objects_cache = {} # Cache objects to avoid recalculating: {color: [obj1_coords, obj2_coords,...]}

    for current_color in non_background_colors:
        # Find objects of the current color if not cached
        if current_color not in all_objects_cache:
            # Use 4-connectivity for identifying distinct objects
            all_objects_cache[current_color] = find_objects(grid, current_color, connectivity=4)

        # Check adjacency for each object of the current color
        for obj_coords in all_objects_cache[current_color]:
            for r, c in obj_coords:
                # Check 8-way neighbors for adjacent colors
                for nr, nc in get_neighbors(r, c, height, width, connectivity=8):
                    neighbor_color = grid[nr, nc]
                    # If neighbor is non-background and NOT the current color itself
                    if neighbor_color != background_color and neighbor_color != current_color:
                        # Record that 'neighbor_color' is adjacent to 'current_color'
                        adjacency_map[neighbor_color].add(current_color)

    # Determine the container color: the one adjacent to the most *diverse* other non-background colors
    container_color = -1
    max_diversity = -1
    sorted_non_bg = sorted(non_background_colors) # Sort for deterministic tie-breaking if needed

    for potential_container in sorted_non_bg:
        diversity = len(adjacency_map.get(potential_container, set()))
        if diversity > max_diversity:
            max_diversity = diversity
            container_color = potential_container

    # Fallback if no container color found (e.g., no adjacencies)
    if container_color == -1:
         if len(non_background_colors) == 1:
              container_color = non_background_colors[0] # Only one possibility
         else:
              # Fallback: Maybe the largest non-background object's color?
               max_size = -1
               for c in sorted_non_bg:
                    if c not in all_objects_cache: all_objects_cache[c] = find_objects(grid, c, connectivity=4)
                    if all_objects_cache[c]:
                         current_max = max(len(obj) for obj in all_objects_cache[c])
                         if current_max > max_size:
                              max_size = current_max
                              container_color = c
               if container_color == -1: return [] # Still couldn't determine

    # --- Step 3: Locate Content Blobs ---
    content_colors = [c for c in non_background_colors if c != container_color]
    all_content_blobs = []
    for c_color in content_colors:
        if c_color not in all_objects_cache:
            all_objects_cache[c_color] = find_objects(grid, c_color, connectivity=4)
        all_content_blobs.extend(all_objects_cache[c_color])

    # --- Step 4: Extract Patterns ---
    patterns_data = []
    processed_content_coords = set() # Track content pixels already part of an extracted pattern

    for content_blob_coords in all_content_blobs:
        # Check if any part of this blob has already been processed
        if not content_blob_coords.isdisjoint(processed_content_coords):
            continue

        frame_pixels = set()
        min_content_row = height # Initialize high to find the minimum later
        
        # Find adjacent container pixels and min row of content blob
        for r_content, c_content in content_blob_coords:
            min_content_row = min(min_content_row, r_content)
            # Check 8-way neighbors for container color
            for nr, nc in get_neighbors(r_content, c_content, height, width, connectivity=8):
                if grid[nr, nc] == container_color:
                    frame_pixels.add((nr, nc))

        # If this content blob is adjacent to the container color
        if frame_pixels:
            # Combine content and frame coordinates
            pattern_coords = content_blob_coords.union(frame_pixels)

            # Calculate bounding box and extract pattern
            bb = get_bounding_box(pattern_coords)
            if bb:
                min_r, min_c, max_r, max_c = bb
                 # Ensure valid slice indices after potential clamping by get_bounding_box logic if added
                min_r = max(0, min_r); min_c = max(0, min_c)
                max_r = min(height - 1, max_r); max_c = min(width - 1, max_c)
                
                if max_r >= min_r and max_c >= min_c: # Check if bbox is valid
                    # Extract using calculated bounds
                    pattern = grid[min_r : max_r + 1, min_c : max_c + 1]
                    patterns_data.append({
                        'min_content_row': min_content_row, # Sort key
                        'pattern': pattern.tolist()         # The extracted data
                    })
                    # Mark these content coordinates as processed
                    processed_content_coords.update(content_blob_coords)

    # --- Step 5: Sort Patterns ---
    patterns_data.sort(key=lambda x: x['min_content_row'])

    # --- Step 6: Assemble and Duplicate Rows ---
    assembled_rows = []
    for data in patterns_data:
        assembled_rows.extend(data['pattern']) # Add all rows from the pattern sequentially

    final_output_rows = []
    for row in assembled_rows:
        final_output_rows.append(list(row)) # Add the row initially

        # Extract true content for palindrome check
        true_content_pixels = [p for p in row if p != background_color and p != container_color]

        # Check duplication rule: non-empty and palindrome
        if true_content_pixels and is_palindrome(true_content_pixels):
            final_output_rows.append(list(row)) # Duplicate the row

    # Handle case where no patterns resulted in output rows
    if not final_output_rows:
        return []

    # --- Step 7: Pad Rows ---
    max_width = 0
    for row in final_output_rows:
        max_width = max(max_width, len(row))

    padded_grid = []
    for row in final_output_rows:
        current_width = len(row)
        pad_total = max_width - current_width
        pad_left = pad_total // 2
        pad_right = pad_total - pad_left
        # Construct the padded row using background color
        padded_row = ([background_color] * pad_left) + row + ([background_color] * pad_right)
        padded_grid.append(padded_row)

    # --- Step 8: Construct Final Output ---
    return padded_grid
```