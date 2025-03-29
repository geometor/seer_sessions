
Previous Code:
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
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 0 0 2 0 2 0 0 0
0 0 0 4 0 0 0 0 2 0 0 0 0
0 0 4 4 4 0 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 3 0 3 0 0
0 0 0 0 0 0 0 0 3 3 0 0 0
0 0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 0 0 0 0 0 0
1 4 1 1 1 8 1 0 0 0 0 0 0
1 1 1 1 1 1 1 0 0 0 8 0 0
1 1 1 1 1 1 1 0 0 8 0 8 0
1 1 1 1 1 1 1 0 0 0 8 0 0
1 3 1 1 1 2 1 0 0 0 0 0 0
1 1 1 1 1 1 1 0 0 0 0 0 0
```
Expected Output:
```
0 4 0 0 0 8 0
4 4 4 0 8 0 8
0 4 0 0 0 8 0
0 0 0 0 0 0 0
3 0 3 0 2 2 0
3 3 0 0 2 0 2
0 3 0 0 0 2 0
```
Transformed Output:
```
0 4 0 0 8
4 4 4 0 0
0 4 0 0 0
0 0 0 0 0
3 0 0 0 2
```
Match: False
Pixels Off: None
Size Correct: False
Color Palette Correct: True
Color Count Correct: False
Score: None

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1
0 0 0 0 2 0 0 0 0 0 1 2 1 1 1 4 1
0 0 2 2 2 0 0 0 0 0 1 1 1 1 1 1 1
0 0 0 2 2 0 0 0 0 0 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 1 6 1 1 1 3 1
0 0 0 0 0 0 0 0 0 0 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 0 6 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 6 0 0 0 0 0 0 0 0 3 3 0 0 0
0 0 6 6 6 0 0 0 0 0 0 0 3 0 3 0 0
0 0 0 0 0 0 0 0 8 0 0 0 0 3 0 0 0
0 0 0 0 0 0 0 8 8 8 0 0 0 0 0 0 0
0 0 0 4 0 0 0 0 8 0 0 0 0 0 0 0 0
0 0 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 2 0 0 4 0
2 2 2 0 4 4 4
0 2 2 0 0 4 4
0 0 0 0 0 0 0
6 0 6 0 3 3 0
0 6 0 0 3 0 3
6 6 6 0 0 3 0
```
Transformed Output:
```
0 0 2 0 0 4 0
2 2 2 0 4 4 4
0 2 2 0 0 4 4
0 0 0 0 0 0 0
0 6 0 0 3 0 0
6 6 6 0 0 0 0
```
Match: False
Pixels Off: None
Size Correct: False
Color Palette Correct: True
Color Count Correct: False
Score: None

## Example 3:
Input:
```
1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
1 5 1 1 1 4 1 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 0 0 0 0 0 4 0 0 0 0
1 1 1 1 1 1 1 0 0 0 0 4 0 0 0 0 0
1 1 1 1 1 1 1 0 0 0 4 4 4 0 0 0 0
1 2 1 1 1 3 1 0 0 0 0 0 0 0 0 0 0
1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 6 6 6 0
0 0 0 0 0 0 0 0 0 2 0 0 0 0 6 0 0
0 0 3 0 3 0 0 0 2 0 2 0 0 0 0 0 0
0 0 0 3 3 0 0 0 2 2 2 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 8 0 0 0 0 0 0
0 0 5 0 0 0 0 0 8 8 8 0 0 0 0 0 0
0 5 5 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 5 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 5 0 0 0 0 4
5 5 0 0 0 4 0
0 0 5 0 4 4 4
0 0 0 0 0 0 0
0 2 0 0 3 0 3
2 0 2 0 0 3 3
2 2 2 0 0 0 3
```
Transformed Output:
```
5 0 0 0 0 4 0
0 0 0 0 4 4 4
0 0 0 0 0 0 0
2 0 2 0 0 3 0
2 2 2 0 3 3 0
0 0 0 0 0 3 0
```
Match: False
Pixels Off: None
Size Correct: False
Color Palette Correct: True
Color Count Correct: False
Score: None
## General Assessment

The previous code successfully identified the core components: the blue frame, key pixels within the frame, and target shapes outside the frame. It also correctly matched keys to targets based on color. However, the code fails in reconstructing the output grid accurately. The primary issues appear to be:

1.  **Incorrect Output Dimensions:** The calculated height and sometimes width of the output grid are incorrect, often resulting in smaller grids than expected. This suggests flaws in how the maximum dimensions per row/column and the spacing are calculated or applied.
2.  **Incomplete Shapes:** Shapes in the transformed output are often missing pixels compared to the expected output. This could stem from errors during shape extraction (`get_relative_shape`), shape pasting (`paste_shape`), or potentially from the incorrect grid dimensions causing clipping.
3.  **Missing Shapes:** Example 1 completely misses the azure shape, indicating a potential issue in identifying all target shapes or in the matching/placement logic.
4.  **Relative Positioning:** The current implementation uses absolute coordinates for key pixels to determine the output layout. It's more likely that the *relative* positions of the key pixels *within the inner area* of the frame dictate the arrangement of the corresponding shapes in the output grid.

The strategy for resolving these errors involves:
1.  Recalculating key pixel positions relative to the frame's inner top-left corner.
2.  Revising the algorithm for calculating the output grid dimensions based on the maximum height/width of shapes in each *relative* row/column derived from the key pixels.
3.  Ensuring the shape extraction and pasting functions preserve the integrity of the shapes.
4.  Verifying that all relevant target shapes are identified and matched.

## Metrics and Analysis

Let's gather specific metrics for each example.



*code_execution:*
```python
import numpy as np

def analyze_example(example_num, expected_list, transformed_list):
    expected_np = np.array(expected_list)
    transformed_np = np.array(transformed_list) if transformed_list else np.array([[]])

    expected_shape = expected_np.shape
    transformed_shape = transformed_np.shape

    expected_colors = {}
    transformed_colors = {}

    if expected_np.size > 0:
        unique_expected, counts_expected = np.unique(expected_np[expected_np != 0], return_counts=True)
        expected_colors = dict(zip(unique_expected, counts_expected))

    if transformed_np.size > 0:
        unique_transformed, counts_transformed = np.unique(transformed_np[transformed_np != 0], return_counts=True)
        transformed_colors = dict(zip(unique_transformed, counts_transformed))

    print(f"--- Example {example_num} ---")
    print(f"Expected Shape: {expected_shape}")
    print(f"Transformed Shape: {transformed_shape}")
    print(f"Shape Match: {expected_shape == transformed_shape}")
    print(f"Expected Colors (Count): {expected_colors}")
    print(f"Transformed Colors (Count): {transformed_colors}")
    print(f"Color Count Match: {expected_colors == transformed_colors}")
    print("-" * 20)

# Example 1 Data
expected_1 = [
    [0, 4, 0, 0, 0, 8, 0],
    [4, 4, 4, 0, 8, 0, 8],
    [0, 4, 0, 0, 0, 8, 0],
    [0, 0, 0, 0, 0, 0, 0],
    [3, 0, 3, 0, 2, 2, 0],
    [3, 3, 0, 0, 2, 0, 2],
    [0, 3, 0, 0, 0, 2, 0]
]
transformed_1 = [
    [0, 4, 0, 0, 8],
    [4, 4, 4, 0, 0],
    [0, 4, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [3, 0, 0, 0, 2]
]
analyze_example(1, expected_1, transformed_1)

# Example 2 Data
expected_2 = [
    [0, 0, 2, 0, 0, 4, 0],
    [2, 2, 2, 0, 4, 4, 4],
    [0, 2, 2, 0, 0, 4, 4],
    [0, 0, 0, 0, 0, 0, 0],
    [6, 0, 6, 0, 3, 3, 0],
    [0, 6, 0, 0, 3, 0, 3],
    [6, 6, 6, 0, 0, 3, 0]
]
transformed_2 = [
    [0, 0, 2, 0, 0, 4, 0],
    [2, 2, 2, 0, 4, 4, 4],
    [0, 2, 2, 0, 0, 4, 4],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 6, 0, 0, 3, 0, 0],
    [6, 6, 6, 0, 0, 0, 0]
]
analyze_example(2, expected_2, transformed_2)

# Example 3 Data
expected_3 = [
    [0, 5, 0, 0, 0, 0, 4],
    [5, 5, 0, 0, 0, 4, 0],
    [0, 0, 5, 0, 4, 4, 4],
    [0, 0, 0, 0, 0, 0, 0],
    [0, 2, 0, 0, 3, 0, 3],
    [2, 0, 2, 0, 0, 3, 3],
    [2, 2, 2, 0, 0, 0, 3]
]
transformed_3 = [
    [5, 0, 0, 0, 0, 4, 0],
    [0, 0, 0, 0, 4, 4, 4],
    [0, 0, 0, 0, 0, 0, 0],
    [2, 0, 2, 0, 0, 3, 0],
    [2, 2, 2, 0, 3, 3, 0],
    [0, 0, 0, 0, 0, 3, 0]
]
analyze_example(3, expected_3, transformed_3)
```

*code_execution_result:*
outcome: OUTCOME_OK
```
--- Example 1 ---
Expected Shape: (7, 7)
Transformed Shape: (5, 5)
Shape Match: False
Expected Colors (Count): {np.int64(2): np.int64(5), np.int64(3): np.int64(5), np.int64(4): np.int64(5), np.int64(8): np.int64(4)}
Transformed Colors (Count): {np.int64(2): np.int64(1), np.int64(3): np.int64(1), np.int64(4): np.int64(5), np.int64(8): np.int64(1)}
Color Count Match: False
--------------------
--- Example 2 ---
Expected Shape: (7, 7)
Transformed Shape: (6, 7)
Shape Match: False
Expected Colors (Count): {np.int64(2): np.int64(6), np.int64(3): np.int64(5), np.int64(4): np.int64(6), np.int64(6): np.int64(6)}
Transformed Colors (Count): {np.int64(2): np.int64(6), np.int64(3): np.int64(1), np.int64(4): np.int64(6), np.int64(6): np.int64(4)}
Color Count Match: False
--------------------
--- Example 3 ---
Expected Shape: (7, 7)
Transformed Shape: (6, 7)
Shape Match: False
Expected Colors (Count): {np.int64(2): np.int64(6), np.int64(3): np.int64(5), np.int64(4): np.int64(5), np.int64(5): np.int64(4)}
Transformed Colors (Count): {np.int64(2): np.int64(5), np.int64(3): np.int64(4), np.int64(4): np.int64(4), np.int64(5): np.int64(1)}
Color Count Match: False
--------------------

```
**Analysis Summary:**

*   **Shape Mismatch:** Confirmed in all examples. Example 1 is significantly smaller (5x5 vs 7x7), while Examples 2 & 3 are one row shorter (6x7 vs 7x7).
*   **Color Count Mismatch:** Confirmed in all examples. The counts for specific colors are consistently lower in the transformed outputs, supporting the observation of incomplete or missing shapes.
    *   Ex 1: Major discrepancies in red(2), green(3), and azure(8). Yellow(4) count is correct, but visual inspection shows it's incomplete, suggesting placement/clipping issues.
    *   Ex 2: Discrepancies in green(3) and magenta(6).
    *   Ex 3: Discrepancies in red(2), green(3), yellow(4), and gray(5).

## Documented Facts (YAML)


```yaml
Task: Reconstruct shapes based on key locations within a frame.

Input_Objects:
  - Object: Frame
    Properties:
      - Color: Blue (1)
      - Shape: Typically a hollow rectangle, 1 pixel thick.
      - Role: Defines a spatial boundary and contains Key_Pixels.
  - Object: Key_Pixel
    Properties:
      - Color: Any color except White (0) or Blue (1).
      - Location: Inside the Frame's inner boundary.
      - Role: Acts as a positional marker, color-matched to a Target_Shape.
  - Object: Target_Shape
    Properties:
      - Color: Any color except White (0).
      - Location: Outside the Frame's bounding box.
      - Shape: A contiguous block of non-White pixels of a single color.
      - Role: The content to be placed in the output grid.

Derived_Objects:
  - Object: Inner_Frame_Area
    Properties:
      - Boundary: Defined by the pixels adjacent to the inside edge of the Frame.
      - Role: The area where Key_Pixels' relative positions are determined.
  - Object: Relative_Key_Grid
    Properties:
      - Structure: A conceptual grid based on the unique row and column offsets of Key_Pixels relative to the Inner_Frame_Area's top-left corner.
      - Role: Defines the layout structure (rows and columns) of the output grid.
  - Object: Output_Grid
    Properties:
      - Background: White (0)
      - Dimensions: Determined by the sum of maximum shape heights/widths in each row/column of the Relative_Key_Grid, plus spacing.
      - Content: Composed of Target_Shapes placed according to the Relative_Key_Grid.

Actions:
  - Action: Identify_Frame
    Input: Input Grid
    Output: Pixel coordinates of the Blue Frame.
  - Action: Identify_Key_Pixels
    Input: Input Grid, Frame coordinates
    Output: List of Key_Pixels (color, absolute position).
    Refinement: Key pixels must be strictly *inside* the hollow frame, not part of the frame itself.
  - Action: Identify_Target_Shapes
    Input: Input Grid, Frame bounding box
    Output: List of Target_Shapes (color, relative shape grid, dimensions).
    Refinement: Target shapes must be entirely *outside* the Frame's bounding box.
  - Action: Calculate_Relative_Key_Positions
    Input: Key_Pixels, Frame coordinates
    Output: Map of Key_Pixel absolute position to relative (row_offset, col_offset) from the frame's inner top-left corner (e.g., `frame_min_row + 1`, `frame_min_col + 1`).
  - Action: Determine_Output_Layout
    Input: Relative_Key_Positions, Matched Target_Shapes' dimensions
    Output: Output grid dimensions, placement coordinates for each shape.
    Refinement:
      - Identify unique relative rows and columns from key positions.
      - Calculate max height for shapes corresponding to keys in each relative row.
      - Calculate max width for shapes corresponding to keys in each relative column.
      - Sum max heights + (num_rows - 1) * spacing for total height.
      - Sum max widths + (num_cols - 1) * spacing for total width.
      - Spacing is 1 white pixel.
  - Action: Match_Keys_To_Targets
    Input: Key_Pixels, Target_Shapes
    Output: Mapping between Key_Pixels and Target_Shapes based on matching colors. Assume one-to-one mapping.
  - Action: Construct_Output_Grid
    Input: Output grid dimensions, Matched Target_Shapes, Placement coordinates.
    Output: Final Output Grid.
    Refinement: Paste shapes accurately at calculated top-left coordinates within the output grid. Ensure no clipping occurs due to miscalculated dimensions or pasting logic.

Observations_From_Failures:
  - Output grid dimensions calculation needs correction, particularly height.
  - Relative positioning of keys within the frame's *inner* area is crucial for layout.
  - Shape integrity must be maintained during extraction and pasting.
  - Spacing between shapes in the output grid is consistently 1 white pixel.
```


## Natural Language Program

1.  **Identify the Frame:** Locate the largest connected component of blue (1) pixels in the input grid. Determine its bounding box (`fr_min_r`, `fr_min_c`, `fr_max_r`, `fr_max_c`).
2.  **Identify Key Pixels:** Find all non-white (0) and non-blue (1) pixels located strictly within the inner area of the frame (i.e., row index `r` is between `fr_min_r + 1` and `fr_max_r - 1`, and column index `c` is between `fr_min_c + 1` and `fr_max_c - 1`). Record the color and absolute position (`r`, `c`) of each key pixel.
3.  **Identify Target Shapes:** Find all connected components of non-white (0) pixels located entirely outside the frame's bounding box. For each component, record its color and extract its shape as a relative grid of pixels. Store the shape's grid, color, height, and width.
4.  **Match Keys to Targets:** Create a one-to-one mapping between key pixels and target shapes based on matching colors. Discard any keys or targets that do not have a match.
5.  **Determine Relative Key Positions:** For each matched key pixel at absolute position (`r`, `c`), calculate its relative position (`rel_r`, `rel_c`) with respect to the frame's inner top-left corner: `rel_r = r - (fr_min_r + 1)`, `rel_c = c - (fr_min_c + 1)`. Store these relative positions along with their corresponding matched target shape data.
6.  **Define Output Grid Structure:**
    *   Identify the set of unique relative row indices (`unique_rel_rows`) and unique relative column indices (`unique_rel_cols`) from the matched key positions. Sort these unique indices.
    *   Create mappings from the unique relative row/column indices to output grid indices (0, 1, 2,...).
    *   Assign a grid index pair (`grid_row_idx`, `grid_col_idx`) to each key based on its `rel_r` and `rel_c` using the mappings.
7.  **Calculate Output Grid Dimensions:**
    *   Initialize dictionaries `max_h_per_grid_row` and `max_w_per_grid_col` to zero for each grid row/column index.
    *   For each matched key and its corresponding target shape:
        *   Find its `grid_row_idx` and `grid_col_idx`.
        *   Update `max_h_per_grid_row[grid_row_idx]` with the maximum height seen so far for that grid row (using the target shape's height).
        *   Update `max_w_per_grid_col[grid_col_idx]` with the maximum width seen so far for that grid column (using the target shape's width).
    *   Calculate the total output height: Sum of all values in `max_h_per_grid_row` + (`number_of_unique_relative_rows` - 1) * 1 (for spacing).
    *   Calculate the total output width: Sum of all values in `max_w_per_grid_col` + (`number_of_unique_relative_cols` - 1) * 1 (for spacing).
8.  **Construct Output Grid:**
    *   Create an empty output grid filled with white (0) pixels, using the calculated dimensions.
    *   Initialize `current_output_r = 0`.
    *   Iterate through the sorted `unique_rel_rows` (or equivalently, `grid_row_idx` from 0 to `num_rows - 1`):
        *   Initialize `current_output_c = 0`.
        *   Get the maximum height for this grid row: `row_h = max_h_per_grid_row[grid_row_idx]`.
        *   Iterate through the sorted `unique_rel_cols` (or equivalently, `grid_col_idx` from 0 to `num_cols - 1`):
            *   Get the maximum width for this grid column: `col_w = max_w_per_grid_col[grid_col_idx]`.
            *   Find if there is a key pixel associated with the current (`grid_row_idx`, `grid_col_idx`).
            *   If a key exists, retrieve its matched target shape grid.
            *   Paste the target shape grid onto the output grid at the top-left position (`current_output_r`, `current_output_c`). Ensure the pasting respects the shape's dimensions and does not overwrite outside its bounds within the allocated cell space defined by `row_h` and `col_w`. (Note: Pasting only requires the top-left corner; the dimension calculation already accounts for the space needed).
            *   Update `current_output_c = current_output_c + col_w + 1` (add spacing).
        *   Update `current_output_r = current_output_r + row_h + 1` (add spacing).
9.  **Return:** Return the constructed output grid.
