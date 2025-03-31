import numpy as np
from collections import Counter

"""
Identify all distinct objects (connected components of non-background pixels) in the input grid.
For each object, determine its pattern (colors and relative positions within its minimal bounding box).
Count the occurrences of each unique pattern signature across all objects.
Filter the objects to find those whose pattern signature appears exactly once (unique patterns).
Among these unique-pattern objects, evaluate their symmetry (horizontal, vertical, or both).
Select the unique-pattern object with the highest degree of symmetry (both > horizontal or vertical > none).
If there's a tie in symmetry among unique-pattern objects, select the one whose pattern contains the non-background color with the lowest numerical value.
Extract the minimal bounding box containing the selected object and return it as the output grid.
"""

def find_objects(grid, target_colors):
    """Finds connected components of specified colors."""
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] in target_colors and not visited[r, c]:
                obj_coords = set()
                q = [(r, c)]
                visited[r, c] = True
                obj_color = grid[r,c] # Check if all pixels in an object must have same color? No, examples show multi-color objects.
                                      # The definition uses "contiguous block", implying connectivity, not necessarily same color.
                                      # Okay, so connectivity applies to any non-background color.

                while q:
                    row, col = q.pop(0)
                    obj_coords.add((row, col))
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] in target_colors and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                if obj_coords:
                    objects.append(list(obj_coords)) # Store as list for easier indexing later if needed
    return objects

def get_bounding_box(coords):
    """Calculates the minimal bounding box for a set of coordinates."""
    if not coords:
        return None, None
    rows = [r for r, c in coords]
    cols = [c for r, c in coords]
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)
    return (min_r, min_c), (max_r, max_c)

def extract_pattern(grid, coords):
    """Extracts the subgrid corresponding to the object's bounding box."""
    if not coords:
        return np.array([[]])
    (min_r, min_c), (max_r, max_c) = get_bounding_box(coords)
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    pattern = np.zeros((height, width), dtype=int)
    
    coord_set = set(coords) # Faster lookup
    
    # Create the pattern based on actual object pixels within the bounding box
    # Background (0) remains if a pixel in BB is not part of the object
    for r in range(height):
        for c in range(width):
            grid_r, grid_c = min_r + r, min_c + c
            if (grid_r, grid_c) in coord_set:
                 pattern[r, c] = grid[grid_r, grid_c]
            # else: pattern[r,c] remains 0 - this might be wrong based on how patterns are compared.
            # Let's rethink: The pattern should only contain the object pixels relative to its top-left corner,
            # possibly on a background of 0. Yes, the bounding box defines the shape, and pixels within it are filled.

    # Alternative: Use relative coordinates
    pattern = np.zeros((height, width), dtype=int)
    for r, c in coords:
        pattern[r - min_r, c - min_c] = grid[r, c]
        
    return pattern


def get_pattern_signature(pattern):
    """Returns a hashable representation of the pattern."""
    return tuple(map(tuple, pattern.tolist()))

def check_symmetry(pattern):
    """Checks for horizontal and vertical symmetry. Returns score: 2 (both), 1 (H or V), 0 (none)."""
    h_sym = np.array_equal(pattern, pattern[:, ::-1])
    v_sym = np.array_equal(pattern, pattern[::-1, :])
    if h_sym and v_sym:
        return 2
    elif h_sym or v_sym:
        return 1
    else:
        return 0

def get_min_color(pattern):
    """Finds the minimum non-zero color value in the pattern."""
    non_zero_colors = pattern[pattern > 0]
    if non_zero_colors.size == 0:
        return float('inf') # Should not happen for valid objects
    return np.min(non_zero_colors)

def transform(input_grid):
    """
    Transforms the input grid by identifying a unique, maximally symmetric object
    and returning its bounding box. Ties are broken by minimum color.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    rows, cols = input_grid_np.shape
    
    # Define background color and target colors for object detection
    background_color = 0
    target_colors = set(range(1, 10)) 

    # 1. Find all distinct objects
    objects_coords = find_objects(input_grid_np, target_colors)
    if not objects_coords:
        return np.array([[]]) # Or handle as error

    object_details = []
    pattern_signatures = []

    # 2. Analyze each object: pattern, signature, symmetry
    for coords in objects_coords:
        pattern = extract_pattern(input_grid_np, coords)
        signature = get_pattern_signature(pattern)
        symmetry_score = check_symmetry(pattern)
        min_color = get_min_color(pattern)
        
        object_details.append({
            'coords': coords,
            'pattern': pattern,
            'signature': signature,
            'symmetry': symmetry_score,
            'min_color': min_color
        })
        pattern_signatures.append(signature)

    # 3. Count pattern occurrences
    pattern_counts = Counter(pattern_signatures)

    # 4. Filter for unique patterns
    unique_objects = [
        obj for obj in object_details 
        if pattern_counts[obj['signature']] == 1
    ]

    if not unique_objects:
         # This case didn't appear in examples. If it happens, the logic is undefined.
         # Maybe return the object with the highest symmetry regardless of uniqueness?
         # Or the smallest/largest unique one? Let's stick to the derived logic.
         # If no *unique* patterns, maybe the task implies something else?
         # For now, return empty or maybe the input? Let's return empty.
        return np.array([[]]) 

    # 5. Find max symmetry among unique objects
    max_symmetry = -1
    for obj in unique_objects:
        if obj['symmetry'] > max_symmetry:
            max_symmetry = obj['symmetry']

    # 6. Filter for max symmetry
    max_symmetry_objects = [
        obj for obj in unique_objects 
        if obj['symmetry'] == max_symmetry
    ]

    # 7. Select the final object (handle ties)
    if len(max_symmetry_objects) == 1:
        selected_object = max_symmetry_objects[0]
    else:
        # Tie-breaker: minimum color
        min_min_color = float('inf')
        for obj in max_symmetry_objects:
            if obj['min_color'] < min_min_color:
                min_min_color = obj['min_color']
        
        tied_min_color_objects = [
            obj for obj in max_symmetry_objects
            if obj['min_color'] == min_min_color
        ]
        
        # If still tied (same max symmetry, same min color), pick the first one found.
        # (Could add other tie-breakers like size or position if needed later)
        selected_object = tied_min_color_objects[0] 

    # 8. Extract and return the pattern of the selected object
    output_grid = selected_object['pattern']
    
    return output_grid.tolist() # Convert back to list of lists for ARC standard
