```python
import numpy as np
from collections import deque

"""
Transformation Rule:
1. Identify all hollow rectangular frames made of red (2) pixels in the input grid.
2. For each red frame, identify the single non-red, non-white color present inside it (the 'pattern color') and the coordinates of all pixels forming this pattern.
3. Order the identified frames based on their top-left corner coordinates (row first, then column).
4. Determine the total number of frames, N.
5. Create a mapping for pattern colors based on N:
    - If N=3: The 1st frame's pattern area gets the 2nd frame's original pattern color. The 2nd gets the 3rd's color. The 3rd gets the 1st's color.
    - If N=4: The 1st frame's pattern area gets the 3rd frame's original pattern color. The 2nd gets the 1st's color. The 3rd gets the 4th's color. The 4th gets the 2nd's color.
    - Assume other values of N might have specific permutations if encountered.
6. Construct the output grid by copying the input grid, then overwriting the pattern pixels within each frame using the new color determined by the permutation mapping.
"""

def _find_connected_components(grid, color):
    """Finds all connected components of a given color."""
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                component_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    row, col = q.popleft()
                    component_pixels.append((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check 8 neighbors (including diagonals for connectivity)
                    # Although frames are orthogonal, connectivity check is safer with 8
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               grid[nr, nc] == color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                
                if component_pixels: # Should always be true here
                     components.append({
                         'pixels': component_pixels,
                         'min_r': min_r,
                         'min_c': min_c,
                         'max_r': max_r,
                         'max_c': max_c
                     })
    return components

def _find_pattern_in_container(grid, container_info):
    """Finds the pattern color and coordinates within a container's bounds."""
    min_r, min_c = container_info['min_r'], container_info['min_c']
    max_r, max_c = container_info['max_r'], container_info['max_c']
    
    pattern_color = None
    pattern_coords = []

    # Scan the interior of the bounding box
    for r in range(min_r + 1, max_r):
        for c in range(min_c + 1, max_c):
            pixel_color = grid[r, c]
            # Pattern color is not background (0) and not frame (2)
            if pixel_color != 0 and pixel_color != 2: 
                if pattern_color is None:
                    pattern_color = pixel_color
                # Assuming only one pattern color per container
                if pixel_color == pattern_color:
                    pattern_coords.append((r, c))
                else:
                    # Handle potential error: multiple non-frame/bg colors inside?
                    # For now, stick to the first one found.
                    pass 
                    
    if pattern_color is not None:
        return pattern_color, pattern_coords
    else:
        return None, []


def transform(input_grid):
    """
    Applies the color swapping transformation based on red rectangular containers.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    # 1. Find all red (2) components (potential containers)
    red_components = _find_connected_components(input_grid, 2)

    containers = []
    # 2. For each component, find its pattern
    for comp in red_components:
        # Basic check: A container must have an inside area
        if comp['max_r'] > comp['min_r'] + 1 and comp['max_c'] > comp['min_c'] + 1:
            pattern_color, pattern_coords = _find_pattern_in_container(input_grid, comp)
            # Only consider components that actually contain a pattern
            if pattern_color is not None and pattern_coords:
                 containers.append({
                     'min_r': comp['min_r'],
                     'min_c': comp['min_c'],
                     'pattern_color': pattern_color,
                     'pattern_coords': pattern_coords
                 })

    # If no valid containers with patterns found, return original grid
    if not containers:
        return output_grid

    # 3. Order containers by top-left corner (row, then col)
    containers.sort(key=lambda c: (c['min_r'], c['min_c']))

    # 4. Determine N and the color permutation
    N = len(containers)
    original_colors = [c['pattern_color'] for c in containers]
    new_colors = [0] * N # Initialize with a placeholder

    if N == 3:
        # 1 gets color of 2, 2 gets color of 3, 3 gets color of 1
        # Indices: 0->1, 1->2, 2->0
        new_colors[0] = original_colors[1]
        new_colors[1] = original_colors[2]
        new_colors[2] = original_colors[0]
    elif N == 4:
        # 1 gets color of 3, 2 gets color of 1, 3 gets color of 4, 4 gets color of 2
        # Indices: 0->2, 1->0, 2->3, 3->1
        new_colors[0] = original_colors[2]
        new_colors[1] = original_colors[0]
        new_colors[2] = original_colors[3]
        new_colors[3] = original_colors[1]
    else:
        # If N is not 3 or 4, return the original grid as permutation is unknown
        # Or potentially handle other cases if more examples were provided
        # For now, just copy original colors if N is not 3 or 4
         print(f"Warning: Unhandled number of containers (N={N}). Returning input.")
         return output_grid # Or could return original_colors if no swap needed

    # 5. Construct Output Grid
    # Iterate through the *ordered* containers and apply the *new* colors
    for i in range(N):
        container = containers[i]
        new_color = new_colors[i]
        pattern_coords = container['pattern_coords']
        
        # Update the output grid at the pattern coordinates with the new color
        for r, c in pattern_coords:
             # Safety check for coordinates being within bounds (should always be)
             if 0 <= r < rows and 0 <= c < cols:
                 output_grid[r, c] = new_color

    return output_grid
```