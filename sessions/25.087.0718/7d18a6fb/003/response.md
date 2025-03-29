```python
import numpy as np
from collections import deque, defaultdict

"""
Identifies a blue frame in the input grid. Finds 'key' pixels (non-white, non-blue) inside the frame's inner area.
Finds 'target' shapes (non-white components) outside the frame's bounding box.
Matches key pixels to target shapes based on color.
Calculates the relative positions of key pixels within the frame's inner area.
Determines the output grid layout based on these relative positions and the dimensions of the matched target shapes, maintaining a 1-pixel white spacing.
Constructs the output grid by placing the matched target shapes according to the determined layout.
"""

# === Helper Functions (Mostly from previous attempt, verified/slightly refined) ===

def find_connected_components(grid, colors_to_find=None, mask=None, connectivity=4):
    """
    Finds connected components of specified colors in the grid.

    Args:
        grid (np.ndarray): The input grid.
        colors_to_find (set, optional): A set of colors to include in components.
                                        If None, finds components of any non-zero color.
        mask (np.ndarray, optional): A boolean grid of the same shape as grid.
                                     Only cells where mask is True will be considered.
        connectivity (int): 4 or 8 for neighbor connectivity. Defaults to 4.

    Returns:
        list: A list of components. Each component is a tuple:
              (color, set of (row, col) tuples).
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    components = []

    if connectivity == 4:
        deltas = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    elif connectivity == 8:
        deltas = [(dr, dc) for dr in [-1, 0, 1] for dc in [-1, 0, 1] if not (dr == 0 and dc == 0)]
    else:
        raise ValueError("Connectivity must be 4 or 8")

    for r in range(height):
        for c in range(width):
            # Apply mask if provided
            if mask is not None and not mask[r, c]:
                continue

            # Check if visited
            if visited[r, c]:
                continue

            color = grid[r, c]
            # Check if it's a target color
            is_target_color = False
            if colors_to_find is None:
                if color != 0: # Any non-background color
                    is_target_color = True
            elif color in colors_to_find:
                is_target_color = True

            if not is_target_color:
                continue

            # Start BFS for a new component
            component_pixels = set()
            q = deque([(r, c)])
            visited[r, c] = True
            component_color = color # All pixels in a component must have the same color

            while q:
                row, col = q.popleft()
                component_pixels.add((row, col))

                # Check neighbors
                for dr, dc in deltas:
                    nr, nc = row + dr, col + dc

                    if 0 <= nr < height and 0 <= nc < width:
                        # Check mask for neighbor
                        if mask is not None and not mask[nr, nc]:
                            continue

                        neighbor_color = grid[nr, nc]
                        if not visited[nr, nc] and neighbor_color == component_color:
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
    """ Extracts the shape details: shape grid, top-left absolute coord, height, width. """
    if not pixels:
        return None, None, 0, 0

    min_r, min_c, max_r, max_c = get_bounding_box(pixels)
    height = max_r - min_r + 1
    width = max_c - min_c + 1

    shape_grid = np.zeros((height, width), dtype=int)
    for r, c in pixels:
        shape_grid[r - min_r, c - min_c] = color

    return shape_grid, (min_r, min_c), height, width


def paste_shape(target_grid, shape_grid, top_left_r, top_left_c):
    """ Pastes a shape_grid onto the target_grid at the specified top-left corner. """
    shape_h, shape_w = shape_grid.shape
    target_h, target_w = target_grid.shape

    for r_rel in range(shape_h):
        for c_rel in range(shape_w):
            # Only paste non-background pixels of the shape
            if shape_grid[r_rel, c_rel] != 0:
                abs_r = top_left_r + r_rel
                abs_c = top_left_c + c_rel
                # Check bounds before pasting
                if 0 <= abs_r < target_h and 0 <= abs_c < target_w:
                    target_grid[abs_r, abs_c] = shape_grid[r_rel, c_rel]

# === Main Transformation Logic ===

def transform(input_grid):
    """
    Transforms the input grid by identifying key pixels within a blue frame,
    matching them to corresponding colored shapes outside the frame, and
    arranging these shapes in an output grid based on the relative positions
    of the key pixels, separated by 1 white pixel.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # 1. Identify the Frame (largest blue component)
    blue_components = find_connected_components(input_np, colors_to_find={1})
    if not blue_components:
        return np.array([[]]).tolist() # No frame found

    frame_pixels = max(blue_components, key=lambda item: len(item[1]))[1]
    frame_bb = get_bounding_box(frame_pixels)
    if frame_bb is None:
         return np.array([[]]).tolist() # Should not happen if frame_pixels exist
    fr_min_r, fr_min_c, fr_max_r, fr_max_c = frame_bb
    
    # Define inner frame boundaries (where keys can exist)
    inner_min_r, inner_min_c = fr_min_r + 1, fr_min_c + 1
    inner_max_r, inner_max_c = fr_max_r - 1, fr_max_c - 1

    # 2. Identify Key Pixels (inside the inner frame area)
    key_pixels_data = []
    for r in range(inner_min_r, inner_max_r + 1):
        for c in range(inner_min_c, inner_max_c + 1):
            color = input_np[r, c]
            # Key condition: Inside inner bounds and not white (0) or blue (1)
            if color not in [0, 1]:
                 key_pixels_data.append({'color': color, 'abs_pos': (r, c)})

    if not key_pixels_data:
        return np.array([[]]).tolist() # No keys found

    # 3. Identify Target Shapes (outside frame's bounding box)
    outside_mask = np.ones_like(input_np, dtype=bool)
    outside_mask[fr_min_r:fr_max_r+1, fr_min_c:fr_max_c+1] = False
    
    # Find all non-white components outside the frame
    potential_target_components = find_connected_components(input_np, colors_to_find=None, mask=outside_mask)

    target_shapes_data = []
    for color, pixels in potential_target_components:
        shape_grid, _, shape_h, shape_w = get_relative_shape(pixels, color)
        if shape_grid is not None:
            target_shapes_data.append({
                'color': color,
                'shape': shape_grid,
                'height': shape_h,
                'width': shape_w
            })

    # 4. Match Keys to Targets by color (one-to-one)
    matched_keys = [] # Store key info along with matched shape data
    available_targets = defaultdict(list)
    for shape_data in target_shapes_data:
        available_targets[shape_data['color']].append(shape_data)

    key_colors_used = defaultdict(int)
    for key in key_pixels_data:
        key_color = key['color']
        if key_color in available_targets and len(available_targets[key_color]) > key_colors_used[key_color]:
            target_shape = available_targets[key_color][key_colors_used[key_color]]
            matched_keys.append({
                'abs_pos': key['abs_pos'],
                'color': key_color,
                'target': target_shape
            })
            key_colors_used[key_color] += 1 # Mark this target as used for this color

    if not matched_keys:
        return np.array([[]]).tolist() # No matches found

    # 5. Determine Relative Key Positions (relative to inner frame top-left)
    relative_key_info = []
    for key in matched_keys:
        abs_r, abs_c = key['abs_pos']
        rel_r = abs_r - inner_min_r
        rel_c = abs_c - inner_min_c
        relative_key_info.append({
            'rel_pos': (rel_r, rel_c),
            'target': key['target']
        })

    # 6. Define Output Grid Structure based on relative positions
    unique_rel_rows = sorted(list(set(r for r, c in [k['rel_pos'] for k in relative_key_info])))
    unique_rel_cols = sorted(list(set(c for r, c in [k['rel_pos'] for k in relative_key_info])))

    # Map relative row/col to grid index (0, 1, 2...)
    rel_row_to_grid_idx = {r: i for i, r in enumerate(unique_rel_rows)}
    rel_col_to_grid_idx = {c: i for i, c in enumerate(unique_rel_cols)}

    num_grid_rows = len(unique_rel_rows)
    num_grid_cols = len(unique_rel_cols)

    # Store target shape by grid index for easy lookup
    shape_by_grid_idx = {}
    for key_info in relative_key_info:
        rel_r, rel_c = key_info['rel_pos']
        grid_r_idx = rel_row_to_grid_idx[rel_r]
        grid_c_idx = rel_col_to_grid_idx[rel_c]
        shape_by_grid_idx[(grid_r_idx, grid_c_idx)] = key_info['target']

    # 7. Calculate Output Grid Dimensions
    spacing = 1 # Space between shapes
    max_h_per_grid_row = defaultdict(int)
    max_w_per_grid_col = defaultdict(int)

    for (grid_r_idx, grid_c_idx), target_data in shape_by_grid_idx.items():
        max_h_per_grid_row[grid_r_idx] = max(max_h_per_grid_row[grid_r_idx], target_data['height'])
        max_w_per_grid_col[grid_c_idx] = max(max_w_per_grid_col[grid_c_idx], target_data['width'])

    # Calculate total height and width
    total_h = sum(max_h_per_grid_row[i] for i in range(num_grid_rows)) + max(0, num_grid_rows - 1) * spacing
    total_w = sum(max_w_per_grid_col[i] for i in range(num_grid_cols)) + max(0, num_grid_cols - 1) * spacing

    # 8. Construct Output Grid
    output_grid = np.zeros((total_h, total_w), dtype=int)

    current_output_r = 0
    for grid_r_idx in range(num_grid_rows):
        current_output_c = 0
        row_h = max_h_per_grid_row[grid_r_idx] # Max height for this conceptual row

        for grid_c_idx in range(num_grid_cols):
            col_w = max_w_per_grid_col[grid_c_idx] # Max width for this conceptual col

            # Check if a shape belongs in this grid cell
            if (grid_r_idx, grid_c_idx) in shape_by_grid_idx:
                target_data = shape_by_grid_idx[(grid_r_idx, grid_c_idx)]
                shape_to_paste = target_data['shape']
                # Paste the shape at the current calculated top-left corner
                paste_shape(output_grid, shape_to_paste, current_output_r, current_output_c)

            # Move to the next column position, including spacing
            current_output_c += col_w + spacing

        # Move to the next row position, including spacing
        current_output_r += row_h + spacing

    # 9. Return the final grid as a list of lists
    return output_grid.tolist()
```