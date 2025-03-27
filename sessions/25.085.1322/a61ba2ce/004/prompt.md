
Previous Code:
```python
import numpy as np

"""
Identifies four 3-pixel L-shaped objects in the input grid.
Extracts the 2x2 pattern defined by each object's bounding box.
Assigns each pattern to a quadrant (TL, TR, BL, BR) in a 4x4 output grid based on the object colors sorted numerically (1st color -> TL, 2nd -> TR, 3rd -> BL, 4th -> BR).
Determines the vertical center line of the input grid (between column index floor(width/2) and floor(width/2) + 1).
Checks if the bounding box of either the object assigned to TL or the object assigned to TR crosses this vertical center line (crossing means min_col <= floor(width/2) AND max_col >= floor(width/2) + 1).
If the crossing condition is met, swaps the patterns placed in the TL and TR quadrants of the output grid. Otherwise, places them according to the sorted color order.
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
                pixels = []
                q = [(r, c)]
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                component_pixels = [] # Track pixels in the current connected component

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

                # Check if the found object is an L-shape (3 pixels and 2x2 bbox)
                if len(component_pixels) == 3 and (max_r - min_r == 1) and (max_c - min_c == 1):
                    bbox = (min_r, min_c, max_r, max_c)
                    # Extract the 2x2 pattern directly using the bounding box
                    pattern = grid[min_r:min_r+2, min_c:min_c+2]
                    
                    # Ensure pattern is exactly 2x2, padding if necessary (unlikely for valid L)
                    if pattern.shape != (2, 2):
                         padded_pattern = np.zeros((2, 2), dtype=int)
                         rows_p, cols_p = pattern.shape
                         padded_pattern[0:rows_p, 0:cols_p] = pattern
                         pattern = padded_pattern

                    objects.append({
                        'color': color,
                        'pixels': component_pixels,
                        'bbox': bbox,
                        'pattern': pattern
                    })
    return objects


def transform(input_grid):
    """
    Transforms the input grid according to the specified L-shape pattern assembly rule.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    height, width = input_grid_np.shape

    # 1. Find the four L-shaped objects
    objects = find_l_objects(input_grid_np)

    # Ensure exactly four objects are found
    if len(objects) != 4:
        # Return default 4x4 grid if object count is wrong
        print(f"Warning: Expected 4 objects, but found {len(objects)}. Returning default grid.")
        return np.zeros((4, 4), dtype=int).tolist()

    # 2. Sort objects by color index (ascending)
    objects.sort(key=lambda obj: obj['color'])

    # 3. Assign objects conceptually to quadrants based on sorted order
    # obj_tl (lowest color), obj_tr (2nd), obj_bl (3rd), obj_br (highest color)
    obj_tl = objects[0]
    obj_tr = objects[1]
    obj_bl = objects[2]
    obj_br = objects[3]

    # 4. Determine the vertical center line indices
    # The line is conceptually between center_col_idx and center_col_idx_plus_1
    center_col_idx = (width - 1) // 2
    center_col_idx_plus_1 = center_col_idx + 1 # The index of the column just right of the midline

    # 5. Check the swap condition
    swap_top_quadrants = False
    # Check if TL object's bbox crosses the center line
    tl_bbox = obj_tl['bbox']
    if tl_bbox[1] <= center_col_idx and tl_bbox[3] >= center_col_idx_plus_1:
        swap_top_quadrants = True

    # Check if TR object's bbox crosses the center line (only need one to cross)
    if not swap_top_quadrants:
        tr_bbox = obj_tr['bbox']
        if tr_bbox[1] <= center_col_idx and tr_bbox[3] >= center_col_idx_plus_1:
            swap_top_quadrants = True

    # 6. Construct the 4x4 output grid
    output_grid = np.zeros((4, 4), dtype=int)

    # Place bottom patterns (always fixed relative to sorted order)
    output_grid[2:4, 0:2] = obj_bl['pattern']
    output_grid[2:4, 2:4] = obj_br['pattern']

    # Place top patterns based on swap condition
    if swap_top_quadrants:
        # Swap: TR pattern goes to TL output, TL pattern goes to TR output
        output_grid[0:2, 0:2] = obj_tr['pattern']
        output_grid[0:2, 2:4] = obj_tl['pattern']
    else:
        # No swap: TL pattern goes to TL output, TR pattern goes to TR output
        output_grid[0:2, 0:2] = obj_tl['pattern']
        output_grid[0:2, 2:4] = obj_tr['pattern']

    # 7. Return as list of lists
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
1 1 0 2
1 0 2 2
4 0 8 8
4 4 0 8
```
Match: False
Pixels Off: 8
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 50.0

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
0 1 2 2
1 1 0 2
3 0 8 8
3 3 8 0
```
Match: False
Pixels Off: 8
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 50.0
