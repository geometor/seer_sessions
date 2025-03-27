
Previous Code:
```python
import numpy as np

"""
Identifies four 3-pixel L-shaped objects in the input grid.
Extracts the 2x2 pattern defined by each object's bounding box.
Determines the spatial quadrant (InTL, InTR, InBL, InBR) of each object based on its bounding box center relative to the input grid's center lines.
Checks if the bounding box of the object in the InTL quadrant OR the object in the InTR quadrant crosses the input grid's vertical center line (crossing: min_col <= floor((W-1)/2) AND max_col >= floor((W-1)/2) + 1).
Constructs a 4x4 output grid by placing the patterns:
  - Pattern from InBL object goes to output BL.
  - Pattern from InBR object goes to output BR.
  - If the crossing condition is true, pattern from InTR goes to output TL, and pattern from InTL goes to output TR.
  - If the crossing condition is false, pattern from InTL goes to output TL, and pattern from InTR goes to output TR.
"""

def find_l_objects(grid):
    """
    Finds all contiguous 3-pixel L-shaped objects of non-background colors.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of dictionaries, each representing an L-shaped object with keys:
              'color': The color of the object's pixels.
              'pixels': A list of (row, col) coordinates of the object's pixels.
              'bbox': A tuple (min_row, min_col, max_row, max_col) of the bounding box (should be 2x2).
              'pattern': A 2x2 numpy array of the pattern within the bbox.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    background_color = 0

    for r in range(height):
        for c in range(width):
            if grid[r, c] != background_color and not visited[r, c]:
                color = grid[r, c]
                q = [(r, c)]
                visited[r, c] = True
                component_pixels = []
                min_r, min_c = r, c
                max_r, max_c = r, c

                # Use BFS to find all connected pixels of the same color
                while q:
                    row, col = q.pop(0)
                    component_pixels.append((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                # Check if the found component is an L-shape (3 pixels and 2x2 bbox)
                if len(component_pixels) == 3 and (max_r - min_r == 1) and (max_c - min_c == 1):
                    bbox = (min_r, min_c, max_r, max_c)
                    # Extract the 2x2 pattern directly using the bounding box
                    pattern = grid[min_r:min_r+2, min_c:min_c+2].copy() # Use copy to avoid view issues

                    # Should always be 2x2 for valid L, but defensive check is ok
                    if pattern.shape != (2, 2):
                         # This case should ideally not happen for valid L-shapes
                         print(f"Warning: Pattern shape incorrect {pattern.shape} for bbox {bbox}. Padding.")
                         padded_pattern = np.zeros((2, 2), dtype=int)
                         rows_p, cols_p = pattern.shape
                         padded_pattern[0:rows_p, 0:cols_p] = pattern
                         pattern = padded_pattern

                    objects.append({
                        'color': color,
                        'pixels': component_pixels,
                        'bbox': bbox,
                        'pattern': pattern # Keep as numpy array
                    })
    return objects


def transform(input_grid):
    """
    Transforms the input grid by identifying four L-shaped objects, determining
    their spatial quadrants, checking a midline crossing condition, and assembling
    their 2x2 patterns into a 4x4 output grid with a potential swap of the top quadrants.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape

    # 1. Identify the four L-shaped objects and their patterns
    objects = find_l_objects(input_grid_np)

    # Ensure exactly four objects are found
    if len(objects) != 4:
        print(f"Warning: Expected 4 L-shaped objects, but found {len(objects)}. Returning default grid.")
        return np.zeros((4, 4), dtype=int).tolist()

    # 2. Determine the input grid center lines coordinates
    center_row_coord = (height - 1) / 2.0
    center_col_coord = (width - 1) / 2.0

    # 3. Classify objects by input quadrant based on bounding box center
    objects_by_quadrant = {'InTL': None, 'InTR': None, 'InBL': None, 'InBR': None}
    quadrant_assignment_count = 0
    for obj in objects:
        min_r, min_c, max_r, max_c = obj['bbox']
        bbox_center_r = (min_r + max_r) / 2.0
        bbox_center_c = (min_c + max_c) / 2.0

        quadrant = ""
        if bbox_center_r < center_row_coord: # Top half
            quadrant += "InT"
        else: # Bottom half (including exact center line)
             quadrant += "InB"

        if bbox_center_c < center_col_coord: # Left half
            quadrant += "L"
        else: # Right half (including exact center line)
            quadrant += "R"

        if quadrant in objects_by_quadrant and objects_by_quadrant[quadrant] is None:
            objects_by_quadrant[quadrant] = obj
            quadrant_assignment_count += 1
        else:
            # Handle error: multiple objects in one quadrant or invalid quadrant
            print(f"Warning: Quadrant assignment issue for object at bbox {obj['bbox']} -> quadrant {quadrant}. Existing: {objects_by_quadrant[quadrant] is not None}")
            return np.zeros((4, 4), dtype=int).tolist() # Return default grid on error

    # Check if all quadrants were assigned exactly one object
    if quadrant_assignment_count != 4:
         print(f"Warning: Not all quadrants assigned correctly. Count: {quadrant_assignment_count}. Returning default grid.")
         return np.zeros((4, 4), dtype=int).tolist()

    # 4. Check the swap condition based on vertical midline crossing
    vertical_center_col_idx = (width - 1) // 2
    vertical_center_col_idx_plus_1 = vertical_center_col_idx + 1

    swap_top_quadrants = False
    obj_intl = objects_by_quadrant['InTL']
    obj_intr = objects_by_quadrant['InTR']

    # Check if InTL object's bbox crosses the vertical center line
    bbox_intl = obj_intl['bbox']
    if bbox_intl[1] <= vertical_center_col_idx and bbox_intl[3] >= vertical_center_col_idx_plus_1:
        swap_top_quadrants = True

    # Check if InTR object's bbox crosses the vertical center line (only need one to cross)
    if not swap_top_quadrants:
        bbox_intr = obj_intr['bbox']
        if bbox_intr[1] <= vertical_center_col_idx and bbox_intr[3] >= vertical_center_col_idx_plus_1:
            swap_top_quadrants = True

    # 5. Construct the 4x4 output grid
    output_grid = np.zeros((4, 4), dtype=int)

    # Place bottom patterns (fixed relative to spatial input quadrant)
    output_grid[2:4, 0:2] = objects_by_quadrant['InBL']['pattern']
    output_grid[2:4, 2:4] = objects_by_quadrant['InBR']['pattern']

    # Place top patterns based on swap condition
    if swap_top_quadrants:
        # Swap: InTR pattern goes to OutTL, InTL pattern goes to OutTR
        output_grid[0:2, 0:2] = obj_intr['pattern']
        output_grid[0:2, 2:4] = obj_intl['pattern']
    else:
        # No swap: InTL pattern goes to OutTL, InTR pattern goes to OutTR
        output_grid[0:2, 0:2] = obj_intl['pattern']
        output_grid[0:2, 2:4] = obj_intr['pattern']

    # 6. Return as list of lists
    return output_grid.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 8 8 0 0 0
0 0 0 0 0 0 0 0 0 8 0 0 0
0 0 1 1 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 2 0 0 0 0
0 0 0 0 0 0 0 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 4 0 0 0 0 0 0 0 0
0 0 0 0 4 4 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
1 1 8 8
1 0 0 8
4 0 0 2
4 4 2 2
```
Transformed Output:
```
0 0 0 0
0 0 0 0
0 0 0 0
0 0 0 0
```
Match: False
Pixels Off: 12
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 150.0

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 8 8 0 0 0 0 0
0 0 0 0 0 0 8 0 0 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 0 0 0 0
0 0 0 0 0 0 0 1 1 0 0 0 0
0 0 0 3 0 0 0 0 0 0 0 0 0
0 0 0 3 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
8 8 2 2
8 0 0 2
3 0 0 1
3 3 1 1
```
Transformed Output:
```
8 8 2 2
8 0 0 2
3 0 0 1
3 3 1 1
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0
