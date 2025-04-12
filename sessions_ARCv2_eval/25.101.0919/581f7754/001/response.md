```python
import numpy as np
from collections import Counter, deque

"""
Identifies a background color, movable objects (multi-pixel components), and potential marker pixels (single-pixel components).
Determines a reference column based on the top-most, left-most marker pixel.
Shifts all movable objects and all marker pixels horizontally so that their center column aligns with the reference column.
The internal structure of objects is preserved during the shift.
"""

def find_connected_components(grid: np.ndarray, background_color: int) -> list[list[tuple[int, int]]]:
    """
    Finds all connected components of non-background pixels.
    Uses Breadth-First Search (BFS).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []

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
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               grid[nr, nc] != background_color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                
                if component_pixels:
                    components.append(component_pixels)
    return components

def get_component_center_col(component_pixels: list[tuple[int, int]]) -> int:
    """Calculates the approximate center column of a component."""
    if not component_pixels:
        return -1 # Should not happen for valid components
    cols = [c for r, c in component_pixels]
    # Using integer division for center calculation, consistent with grid indices
    # Alternative: round(np.mean(cols)) 
    # Using median might be more robust to outliers if shapes are complex/skewed
    # Using (min_col + max_col) // 2 is another option
    center_col = int(np.median(cols)) 
    # Let's use average rounded for potentially better centering
    center_col = int(round(np.mean(cols))) 
    return center_col
    

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Shifts non-background objects horizontally to align with a reference marker column.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # 1. Identify background color (most frequent color)
    colors, counts = np.unique(input_np, return_counts=True)
    background_color = colors[np.argmax(counts)]

    # 2. Find all connected components of non-background colors
    all_components_pixels = find_connected_components(input_np, background_color)

    if not all_components_pixels:
        # No non-background elements, return input as is
        return input_grid

    # 3. Separate components into markers (single-pixel) and objects (multi-pixel)
    marker_components = []
    object_components = []
    for comp_pixels in all_components_pixels:
        if len(comp_pixels) == 1:
            marker_components.append(comp_pixels)
        else:
            object_components.append(comp_pixels)

    # 4. Determine the reference marker column
    ref_col = -1
    if marker_components:
        # Sort markers by row, then column to find the top-most, left-most
        marker_components.sort() 
        ref_marker_pixel = marker_components[0][0] # The single pixel (r, c)
        ref_col = ref_marker_pixel[1]
    else:
        # Fallback if no single-pixel markers? 
        # Based on examples, this seems unlikely for this specific task pattern.
        # If needed, could try using the center of the top-most object, etc.
        # For now, if no markers, maybe no movement? Return input.
         return input_grid # Or define alternative reference logic

    # 5. Initialize output grid with background color
    output_np = np.full_like(input_np, background_color)

    # 6. Process and move all components (markers and objects)
    all_components_to_move = marker_components + object_components
    
    for comp_pixels in all_components_to_move:
        # a. Get original colors and calculate center column
        original_colors = {pixel: input_np[pixel] for pixel in comp_pixels}
        comp_center_col = get_component_center_col(comp_pixels)
        
        # b. Calculate horizontal shift
        dx = ref_col - comp_center_col
        
        # c. Apply shift and draw onto output grid
        for (r, c) in comp_pixels:
            new_c = c + dx
            # Ensure the new position is within grid bounds
            if 0 <= r < rows and 0 <= new_c < cols:
                output_np[r, new_c] = original_colors[(r, c)]
            # else: pixel moves off-grid (discarded)

    # 7. Convert back to list of lists and return
    return output_np.tolist()
```