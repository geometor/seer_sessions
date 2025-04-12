```python
"""
Identifies strictly isolated single non-background pixels as 'markers'.
Uses the top-most, left-most marker to define a reference column ('ref_col').
The reference marker stays in place.
Other isolated markers are moved horizontally to the 'ref_col', keeping their original row.
All other non-background components ('objects' - multi-pixel or non-isolated single pixel) are shifted horizontally.
The shift amount for an object is calculated so that its center column (rounded mean of pixel columns) aligns with the 'ref_col'.
The internal structure of objects is preserved.
This rule is derived from Examples 1 and 3 and may not apply to all cases (like Example 2).
"""

import numpy as np
from collections import Counter, deque

def find_background(grid: np.ndarray) -> int:
    """Finds the most frequent color, assumed to be the background."""
    colors, counts = np.unique(grid, return_counts=True)
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
            if grid[r, c] != background_color and not visited[r, c]:
                component_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    component_pixels.append((row, col))
                    
                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0: continue
                            nr, nc = row + dr, col + dc
                            
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               grid[nr, nc] != background_color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                
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

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule: align objects and non-reference markers 
    to the reference marker's column.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # 1. Find background color
    background_color = find_background(input_np)

    # 2. Find all non-background coordinates for isolation checks
    all_non_bg_coords = set()
    for r in range(rows):
        for c in range(cols):
            if input_np[r, c] != background_color:
                all_non_bg_coords.add((r, c))

    if not all_non_bg_coords:
        return input_grid # Empty grid or all background

    # 3. Find all connected components
    all_components = find_components(input_np, background_color)
    if not all_components:
         return input_grid # Should not happen if all_non_bg_coords is not empty

    # 4. Identify isolated markers and objects
    isolated_markers = [] # Stores {'id': comp_id, 'pixel': (r,c), 'color': color}
    objects = [] # Stores component dictionaries {'id': comp_id, 'pixels': [...], 'size': size}
    
    for comp in all_components:
        if comp['size'] == 1:
            pixel_coord = comp['pixels'][0]
            # Check for strict isolation (no non-bg neighbors at all)
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
        # No isolated markers found, apply no transformation based on derived rule
        # (Could potentially define a fallback rule here if needed)
        return input_grid 

    # Sort markers by row, then column to find the top-most, left-most
    isolated_markers.sort(key=lambda m: m['pixel']) 
    ref_marker = isolated_markers[0]
    ref_col = ref_marker['pixel'][1]
    
    # 6. Initialize output grid
    output_np = np.full_like(input_np, background_color)

    # 7. Place reference marker
    ref_r, ref_c = ref_marker['pixel']
    output_np[ref_r, ref_c] = ref_marker['color']

    # 8. Place other isolated markers
    for marker in isolated_markers[1:]:
        r, _ = marker['pixel'] # Original row
        color = marker['color']
        new_c = ref_col
        if 0 <= r < rows and 0 <= new_c < cols:
            output_np[r, new_c] = color

    # 9. Move objects
    for obj_comp in objects:
        obj_pixels = obj_comp['pixels']
        center_col = get_component_center_col(obj_pixels)
        
        if center_col == -1: continue # Should not happen for valid objects

        dx = ref_col - center_col

        # Apply shift to each pixel of the object
        for (r, c) in obj_pixels:
            new_c = c + dx
            # Check bounds before writing to output
            if 0 <= r < rows and 0 <= new_c < cols:
                output_np[r, new_c] = input_np[r, c] # Use original color

    # 10. Return result
    return output_np.tolist()
```