```python
import numpy as np
from collections import deque

"""
Identifies a blue frame in the input grid. Finds 'key' pixels (non-white, non-blue) inside the frame's bounding box.
Finds 'target' shapes (non-white components) outside the frame's bounding box.
Matches key pixels to target shapes based on color.
Arranges the matched target shapes in the output grid according to the relative positions of their corresponding key pixels within the frame, maintaining a 1-pixel white spacing between adjacent shapes.
"""

def find_connected_components(grid, colors_to_find=None, mask=None):
    """
    Finds connected components of specified colors in the grid.

    Args:
        grid (np.ndarray): The input grid.
        colors_to_find (set, optional): A set of colors to include in components. 
                                        If None, finds components of any non-zero color.
        mask (np.ndarray, optional): A boolean grid of the same shape as grid. 
                                     Only cells where mask is True will be considered.

    Returns:
        list: A list of components. Each component is a tuple:
              (color, set of (row, col) tuples).
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    for r in range(height):
        for c in range(width):
            # Check mask if provided
            if mask is not None and not mask[r, c]:
                continue
                
            # Check if visited or not a target color
            color = grid[r, c]
            is_target_color = False
            if colors_to_find is None:
                 if color != 0: # Any non-background color if colors_to_find is None
                     is_target_color = True
            elif color in colors_to_find:
                 is_target_color = True

            if visited[r, c] or not is_target_color:
                continue

            # Start BFS to find a new component
            component_pixels = set()
            q = deque([(r, c)])
            visited[r, c] = True
            component_color = color # All pixels in a component must have the same color in ARC

            while q:
                row, col = q.popleft()
                component_pixels.add((row, col))

                # Check neighbors (4-way connectivity)
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = row + dr, col + dc

                    if 0 <= nr < height and 0 <= nc < width:
                         # Check mask if provided
                        if mask is not None and not mask[nr, nc]:
                            continue
                            
                        # Check if valid neighbor
                        neighbor_color = grid[nr, nc]
                        if not visited[nr, nc] and neighbor_color == component_color:
                             # Check mask if provided for the neighbor as well
                            if mask is None or mask[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
            
            if component_pixels:
                 components.append((component_color, component_pixels))

    return components

def get_bounding_box(pixels):
    """Calculates the bounding box (min_r, min_c, max_r, max_c) for a set of pixels."""
    if not pixels:
        return None
    min_r = min(r for r, c in pixels)
    min_c = min(c for r, c in pixels)
    max_r = max(r for r, c in pixels)
    max_c = max(c for r, c in pixels)
    return min_r, min_c, max_r, max_c

def get_relative_shape(pixels, color):
    """ Extracts the shape details: relative coordinates, color, height, width. """
    if not pixels:
        return None, None, 0, 0
    
    min_r, min_c, max_r, max_c = get_bounding_box(pixels)
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    
    relative_pixels = set()
    for r, c in pixels:
        relative_pixels.add((r - min_r, c - min_c))
        
    shape_grid = np.zeros((height, width), dtype=int)
    for r_rel, c_rel in relative_pixels:
        shape_grid[r_rel, c_rel] = color
        
    return shape_grid, (min_r, min_c), height, width


def paste_shape(target_grid, shape_grid, top_left_r, top_left_c):
    """ Pastes a shape_grid onto the target_grid at the specified top-left corner. """
    h, w = shape_grid.shape
    target_h, target_w = target_grid.shape
    
    for r in range(h):
        for c in range(w):
            tr, tc = top_left_r + r, top_left_c + c
            if 0 <= tr < target_h and 0 <= tc < target_w:
                # Only paste non-background pixels of the shape
                if shape_grid[r, c] != 0:
                    target_grid[tr, tc] = shape_grid[r, c]


def transform(input_grid):
    """
    Transforms the input grid based on the described logic.
    """
    input_np = np.array(input_grid)
    height, width = input_np.shape

    # 1. Find the blue frame and its bounding box
    blue_components = find_connected_components(input_np, colors_to_find={1})
    if not blue_components:
        # Handle cases with no blue frame if necessary, maybe return input or empty?
        # Based on examples, a frame is always present. Let's assume this.
         return np.array([[]]) # Or raise error? Return empty for now.

    # Assume largest blue component is the frame
    frame_pixels = max(blue_components, key=lambda item: len(item[1]))[1]
    frame_bb = get_bounding_box(frame_pixels)
    if frame_bb is None:
         return np.array([[]]) # Error case
    fr_min_r, fr_min_c, fr_max_r, fr_max_c = frame_bb

    # 2. Find Key Pixels inside the frame's bounding box
    key_pixels_data = []
    for r in range(fr_min_r, fr_max_r + 1):
        for c in range(fr_min_c, fr_max_c + 1):
            color = input_np[r, c]
            # Check if it's inside the bounding box AND not blue (1) or white (0)
            if color not in [0, 1]:
                 # Check if it's truly inside the frame area (not part of the frame itself)
                 # A simple check: ensure it's not part of the found frame pixels
                 if (r, c) not in frame_pixels:
                     # Store color and absolute coordinates
                     key_pixels_data.append({'color': color, 'pos': (r, c)})
                         
    if not key_pixels_data:
        return np.array([[]]) # No keys found

    # 3. Find Target Shapes outside the frame's bounding box
    outside_mask = np.ones_like(input_np, dtype=bool)
    if frame_bb: # If a frame was found, mask its bounding box
        outside_mask[fr_min_r:fr_max_r+1, fr_min_c:fr_max_c+1] = False

    potential_target_components = find_connected_components(input_np, mask=outside_mask)
    
    target_shapes_data = []
    for color, pixels in potential_target_components:
        # Ensure the component is entirely outside the frame's bounding box
        # (The mask already mostly ensures this, but double check for safety)
        is_fully_outside = True
        if frame_bb:
            for r, c in pixels:
                if fr_min_r <= r <= fr_max_r and fr_min_c <= c <= fr_max_c:
                    is_fully_outside = False
                    break
        
        if is_fully_outside:
            shape_grid, _, shape_h, shape_w = get_relative_shape(pixels, color)
            if shape_grid is not None:
                target_shapes_data.append({
                    'color': color, 
                    'shape': shape_grid, 
                    'height': shape_h,
                    'width': shape_w
                })

    # 4. Match Key Pixels to Target Shapes by color
    matched_targets = {} # Map key position -> target shape details
    available_targets = {s['color']: s for s in target_shapes_data}
    
    keys_to_process = [] # Store keys that have a matching shape
    for key in key_pixels_data:
        color = key['color']
        pos = key['pos']
        if color in available_targets:
            matched_targets[pos] = available_targets[color]
            keys_to_process.append(key)
            # Remove target to prevent reuse (assuming 1-to-1 mapping)
            del available_targets[color] 
            
    if not keys_to_process:
         return np.array([[]]) # No matches found

    # 5. Determine relative arrangement of Key Pixels
    key_coords = sorted([k['pos'] for k in keys_to_process]) # Sort by row, then col
    
    # Find unique rows and columns used by keys
    unique_rows = sorted(list(set(r for r, c in key_coords)))
    unique_cols = sorted(list(set(c for r, c in key_coords)))
    
    # Map absolute key position to grid index (row_idx, col_idx)
    key_grid_indices = {}
    row_map = {r: i for i, r in enumerate(unique_rows)}
    col_map = {c: i for i, c in enumerate(unique_cols)}
    for r, c in key_coords:
        key_grid_indices[(r, c)] = (row_map[r], col_map[c])

    num_grid_rows = len(unique_rows)
    num_grid_cols = len(unique_cols)

    # 6. Calculate output grid dimensions
    spacing = 1 # Space between shapes
    
    # Find max height per grid row and max width per grid col
    grid_row_max_h = {i: 0 for i in range(num_grid_rows)}
    grid_col_max_w = {i: 0 for i in range(num_grid_cols)}

    for key_pos, target_data in matched_targets.items():
        grid_r_idx, grid_c_idx = key_grid_indices[key_pos]
        grid_row_max_h[grid_r_idx] = max(grid_row_max_h[grid_r_idx], target_data['height'])
        grid_col_max_w[grid_c_idx] = max(grid_col_max_w[grid_c_idx], target_data['width'])

    # Calculate total height and width
    output_h = sum(grid_row_max_h.values()) + max(0, num_grid_rows - 1) * spacing
    output_w = sum(grid_col_max_w.values()) + max(0, num_grid_cols - 1) * spacing

    # 7. Initialize output grid
    output_grid = np.zeros((output_h, output_w), dtype=int)

    # 8. Place shapes onto the output grid
    current_r = 0
    for grid_r_idx in range(num_grid_rows):
        current_c = 0
        max_h_this_row = grid_row_max_h[grid_r_idx]
        for grid_c_idx in range(num_grid_cols):
            max_w_this_col = grid_col_max_w[grid_c_idx]
            
            # Find the key/shape corresponding to this grid cell (if any)
            found_key_pos = None
            for key_pos, (gr, gc) in key_grid_indices.items():
                if gr == grid_r_idx and gc == grid_c_idx:
                    found_key_pos = key_pos
                    break
            
            if found_key_pos and found_key_pos in matched_targets:
                target_data = matched_targets[found_key_pos]
                shape_to_paste = target_data['shape']
                # Paste the shape at the current calculated position
                paste_shape(output_grid, shape_to_paste, current_r, current_c)

            # Move to the next column position
            current_c += max_w_this_col + spacing
            
        # Move to the next row position
        current_r += max_h_this_row + spacing

    return output_grid.tolist() # Convert back to list of lists for ARC standard
```