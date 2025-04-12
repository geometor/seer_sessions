```python
import numpy as np
from collections import Counter, deque
import math

"""
Applies a conditional horizontal alignment based on an isolated marker.

1.  Determines the background color (most common color).
2.  Finds all 'isolated markers': single non-background pixels with no adjacent non-background neighbors (8-way).
3.  If no isolated markers exist, returns the input grid unchanged.
4.  Identifies the 'reference marker': the isolated marker with the smallest row index, then smallest column index. Records its column (`ref_col`) and color (`ref_color`).
5.  Creates an output grid filled with the background color.
6.  Places the reference marker pixel at its original coordinates in the output grid.
7.  For every other isolated marker, places its color in the output grid at its original row but in column `ref_col`.
8.  Finds all 'objects': connected components (8-way) of non-background pixels with size > 1, or single non-background pixels that were not isolated.
9.  For each object:
    a. Calculates its geometric center column (`center_col`) by rounding the mean of its pixel column indices.
    b. Checks if the object contains any pixel matching the `ref_color`.
    c. Determines the horizontal shift (`dx`):
        i.  If the object contains the `ref_color`:
            1.  Finds the top-most, left-most pixel within the object having the `ref_color`. Records its column as `local_ref_c`.
            2.  If `abs(center_col - local_ref_c) <= 1`, sets `dx = ref_col - local_ref_c`.
            3.  Else, sets `dx = ref_col - center_col`.
        ii. If the object does not contain the `ref_color`, sets `dx = ref_col - center_col`.
    d. Applies the shift: For each pixel `(r, c)` in the object, places its original color into the output grid at `(r, c + dx)`, checking bounds. Overwrites are possible.
10. Returns the completed output grid.

(Note: This procedure is based on Examples 1 and 3. Example 2 requires a different transformation logic.)
"""

# --- Helper Functions ---

def find_background(grid: np.ndarray) -> int:
    """Finds the most frequent color, assumed to be the background."""
    colors, counts = np.unique(grid, return_counts=True)
    if counts.size == 0: return -1 # Handle empty grid case
    return colors[np.argmax(counts)]

def find_components(grid: np.ndarray, background_color: int) -> list[dict]:
    """
    Finds all connected components of non-background pixels using BFS (8-way connectivity).
    Returns a list of dictionaries, each representing a component with its pixels and size.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []
    component_id_counter = 0

    for r in range(rows):
        for c in range(cols):
            # Find the start of a new component
            if grid[r, c] != background_color and not visited[r, c]:
                component_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                
                # Perform BFS to find all connected pixels
                while q:
                    row, col = q.popleft()
                    component_pixels.append((row, col))
                    
                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0: continue
                            nr, nc = row + dr, col + dc
                            
                            # Check bounds and if it's a non-background pixel not yet visited
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               grid[nr, nc] != background_color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                
                # Store the found component
                if component_pixels:
                    components.append({
                        'id': component_id_counter,
                        'pixels': sorted(component_pixels), # Sort for consistency
                        'size': len(component_pixels)
                    })
                    component_id_counter += 1
    return components

def is_isolated(pixel_coord: tuple[int, int], all_non_bg_coords: set[tuple[int, int]], rows: int, cols: int) -> bool:
    """Checks if a single pixel has no non-background neighbors (8-way)."""
    r, c = pixel_coord
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0: continue
            nr, nc = r + dr, c + dc
            # Check if neighbor is within bounds AND is a non-background pixel
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) in all_non_bg_coords:
                return False # Found a non-background neighbor
    return True # No non-background neighbors found

def get_component_center_col(component_pixels: list[tuple[int, int]]) -> int:
    """Calculates the center column by rounding the mean of column indices."""
    if not component_pixels: return -1
    cols = [c for r, c in component_pixels]
    return int(round(np.mean(cols)))

# --- Main Transformation Function ---

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    # Convert input to numpy array for efficient operations
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # Handle edge case: empty grid
    if rows == 0 or cols == 0:
        return input_grid

    # 1. Determine the background color
    background_color = find_background(input_np)
    if background_color == -1: # Grid was likely empty or had issues
         return input_grid

    # 2. Find all non-background coordinates (used for isolation checks)
    all_non_bg_coords = set()
    for r in range(rows):
        for c in range(cols):
            if input_np[r, c] != background_color:
                all_non_bg_coords.add((r, c))

    # Handle edge case: grid contains only background color
    if not all_non_bg_coords:
        return input_grid 

    # 3. Find all connected components
    all_components = find_components(input_np, background_color)
    if not all_components:
         # This case should ideally not be reached if all_non_bg_coords is populated
         return input_grid 

    # 4. Identify isolated markers and objects
    isolated_markers = [] # Stores {'id': comp_id, 'pixel': (r,c), 'color': color}
    objects = [] # Stores component dictionaries {'id': comp_id, 'pixels': [...], 'size': size}
    
    for comp in all_components:
        if comp['size'] == 1:
            pixel_coord = comp['pixels'][0]
            # Check for strict isolation (needs all_non_bg_coords *excluding itself*)
            if is_isolated(pixel_coord, all_non_bg_coords - {pixel_coord}, rows, cols):
                 isolated_markers.append({
                     'id': comp['id'], 
                     'pixel': pixel_coord, 
                     'color': input_np[pixel_coord]
                 })
            else:
                 # Non-isolated single pixel, treat as object
                 objects.append(comp) 
        else:
            # Multi-pixel component, treat as object
            objects.append(comp)

    # 5. Determine reference marker and column
    if not isolated_markers:
        # No isolated markers found, return input unchanged as per rule
        return input_grid 

    # Sort markers by row, then column to find the top-most, left-most
    isolated_markers.sort(key=lambda m: m['pixel']) 
    ref_marker = isolated_markers[0]
    ref_col = ref_marker['pixel'][1]
    ref_color = ref_marker['color']
    
    # 6. Initialize output grid
    output_np = np.full_like(input_np, background_color)

    # 7. Place the reference marker at its original position
    ref_r, ref_c = ref_marker['pixel']
    # Ensure marker is within bounds (should always be true)
    if 0 <= ref_r < rows and 0 <= ref_c < cols:
        output_np[ref_r, ref_c] = ref_marker['color']

    # 8. Place other isolated markers at the reference column
    for marker in isolated_markers[1:]:
        r, _ = marker['pixel'] # Original row
        color = marker['color']
        new_c = ref_col
        # Check bounds before writing
        if 0 <= r < rows and 0 <= new_c < cols:
            output_np[r, new_c] = color

    # 9. Process and move objects
    for obj_comp in objects:
        obj_pixels = obj_comp['pixels']
        
        # Calculate geometric center column
        center_col = get_component_center_col(obj_pixels)
        if center_col == -1: continue # Skip if object is empty (shouldn't happen)

        # Check if object contains the reference color and find local ref column if it does
        contains_ref_color = False
        local_ref_c = -1
        ref_color_pixels = []
        for r, c in obj_pixels:
            if input_np[r, c] == ref_color:
                contains_ref_color = True
                ref_color_pixels.append((r, c))
        
        # Determine the horizontal shift (dx) based on the V4 hypothesis
        dx = 0 # Default shift if no rule applied (shouldn't happen with valid objects)
        if contains_ref_color:
            # Sort pixels with ref_color to find top-left one
            ref_color_pixels.sort()
            local_ref_c = ref_color_pixels[0][1]
            
            # Check distance between geometric center and local ref point
            if abs(center_col - local_ref_c) <= 1:
                # Rule: Use local reference point alignment
                dx = ref_col - local_ref_c
            else:
                # Rule: Local reference point too far, use geometric center alignment
                dx = ref_col - center_col
        else:
            # Rule: Object doesn't contain ref color, use geometric center alignment
            dx = ref_col - center_col

        # Apply the calculated shift dx to each pixel of the object
        for (r, c) in obj_pixels:
            new_c = c + dx
            # Check bounds before writing to output grid
            if 0 <= r < rows and 0 <= new_c < cols:
                # Use original color from input grid
                output_np[r, new_c] = input_np[r, c] 

    # 10. Convert the result back to list of lists and return
    return output_np.tolist()
```