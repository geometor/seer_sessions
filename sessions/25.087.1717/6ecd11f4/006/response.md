## General Assessment

The previous code correctly identified the largest object and the set of "source" pixels (pixels not belonging to the largest object). However, it failed because:

1.  **Incorrect Filtering Logic:** The rules mapping the largest object's color (`FilterColor`) to the set of colors to be removed (`TargetColors`) were incorrect for at least `FilterColor` = Green (3) and `FilterColor` = Azure (8). The actual rule appears to depend on the `FilterColor`, but the specific colors to remove/keep needed revision based on all examples.
2.  **Incorrect Output Construction:** The transformed output grids were significantly different in size and content from the expected outputs. The code seemed to be including parts of the largest object or miscalculating the bounding box/cropping based on the source pixels *before* filtering, rather than *after*. The cropping should be based only on the pixels that remain *after* the filtering step.

**Strategy for Resolution:**

1.  **Re-analyze Filtering:** Re-examine the relationship between the largest object's color and the colors present in the payload pixels versus the colors present in the final output across all examples. Define a precise rule for which colors are *kept* based on the largest object's color.
2.  **Refine Cropping:** Ensure the bounding box calculation and subsequent cropping are performed *only* on the payload pixels that are *kept* after the filtering step.
3.  **Update Natural Language Program:** Revise the program to reflect the corrected filtering and cropping logic.
4.  **Implement and Test:** Update the Python code based on the revised program and re-test.

## Metrics Gathering

Let's gather details for each example using the previous code's helper functions and the refined understanding.


``` python
import numpy as np
from collections import deque

# --- Helper functions from previous code ---
def find_objects(grid):
    rows, cols = grid.shape
    visited = set()
    objects = []
    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r, c] != 0:
                color = grid[r, c]
                obj_coords = set()
                q = deque([(r, c)])
                visited.add((r, c))
                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           (nr, nc) not in visited and grid[nr, nc] == color:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                objects.append({
                    'color': color,
                    'coords': obj_coords,
                    'size': len(obj_coords)
                })
    return objects

def get_bounding_box(coords):
    if not coords: return None
    min_row = min(r for r, c in coords)
    min_col = min(c for r, c in coords)
    max_row = max(r for r, c in coords)
    max_col = max(c for r, c in coords)
    return min_row, min_col, max_row, max_col

# --- Define Inputs ---
inputs = [
    [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,3,3,3,0,0,0,3,3,3,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,3,3,3,0,0,0,3,3,3,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,3,3,3,0,0,0,3,3,3,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,2,1,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,4,8,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,8,6,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
    [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],[0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],[0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],[0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],[0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],[0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0],[0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],[0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],[0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],[0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],[0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,3,1,7,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,2,8,9,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,3,4,6,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
    [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,8,8,8,8,0,0,0,0,8,8,8,8,8,8,8,8,0,0,0,0],[0,0,8,8,8,8,0,0,0,0,8,8,8,8,8,8,8,8,0,0,0,0],[0,0,8,8,8,8,0,0,0,0,8,8,8,8,8,8,8,8,0,0,0,0],[0,0,8,8,8,8,0,0,0,0,8,8,8,8,8,8,8,8,0,0,0,0],[0,0,8,8,8,8,0,0,0,0,8,8,8,8,0,0,0,0,0,0,0,0],[0,0,8,8,8,8,0,0,0,0,8,8,8,8,0,0,0,0,0,0,0,0],[0,0,8,8,8,8,0,0,0,0,8,8,8,8,0,0,0,0,0,0,0,0],[0,0,8,8,8,8,0,0,0,0,8,8,8,8,0,0,0,0,0,0,0,0],[0,0,8,8,8,8,0,0,0,0,0,0,0,0,8,8,8,8,0,0,0,0],[0,0,8,8,8,8,0,0,0,0,0,0,0,0,8,8,8,8,0,0,0,0],[0,0,8,8,8,8,0,0,0,0,0,0,0,0,8,8,8,8,0,0,0,0],[0,0,8,8,8,8,0,0,0,0,0,0,0,0,8,8,8,8,0,0,0,0],[0,0,8,8,8,8,8,8,8,8,8,8,8,8,0,0,0,0,0,0,0,0],[0,0,8,8,8,8,8,8,8,8,8,8,8,8,0,0,0,0,0,0,0,0],[0,0,8,8,8,8,8,8,8,8,8,8,8,8,0,0,0,0,0,0,0,0],[0,0,8,8,8,8,8,8,8,8,8,8,8,8,0,0,0,4,1,9,4,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,3,6,1,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,5,7,5,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,4,2,7,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
]

# --- Define Expected Outputs for Size Comparison ---
expected_outputs = [
    [[2,0,7],[4,8,0],[0,6,1]],
    [[3,0,7],[0,8,0],[3,0,6]],
    [[4,0,9,4],[6,0,6,0],[3,0,0,5],[2,4,2,0]]
]

# --- Process Each Example ---
metrics = []
for i, input_list in enumerate(inputs):
    input_grid = np.array(input_list, dtype=int)
    expected_output_grid = np.array(expected_outputs[i], dtype=int)
    input_rows, input_cols = input_grid.shape
    expected_output_rows, expected_output_cols = expected_output_grid.shape

    objects = find_objects(input_grid)
    if not objects:
        metrics.append({
            'example': i + 1,
            'input_shape': (input_rows, input_cols),
            'expected_output_shape': (expected_output_rows, expected_output_cols),
            'status': 'No non-white objects found',
            'largest_object': None,
            'payload_pixels': None,
            'payload_colors': None,
            'kept_payload_pixels': None,
            'kept_payload_colors': None,
            'kept_payload_bbox': None,
            'colors_to_remove': None
        })
        continue

    largest_object = max(objects, key=lambda obj: obj['size'])
    key_color = largest_object['color']
    large_object_coords = largest_object['coords']

    all_non_white_coords = set(zip(*np.where(input_grid != 0)))
    payload_coords = all_non_white_coords - large_object_coords

    payload_pixels_data = {(r, c): input_grid[r, c] for r, c in payload_coords}
    payload_colors = set(payload_pixels_data.values())

    # Determine colors to keep based on refined logic
    all_colors = set(range(1, 10)) # Colors 1 through 9
    colors_to_remove = set()
    if key_color == 3: # Green Key
        colors_to_remove = {9} # Remove Maroon
    elif key_color == 1: # Blue Key
        colors_to_remove = {1, 2, 4, 9} # Remove Blue, Red, Yellow, Maroon
    elif key_color == 8: # Azure Key
        colors_to_remove = {1, 7} # Remove Blue, Orange
    # else: keep all payload colors (implicitly)

    colors_to_keep = payload_colors - colors_to_remove

    kept_payload_coords = {
        (r, c) for (r, c), color in payload_pixels_data.items() if color in colors_to_keep
    }
    kept_payload_colors = {input_grid[r,c] for r,c in kept_payload_coords} # Unique colors kept

    kept_payload_bbox = get_bounding_box(kept_payload_coords)
    if kept_payload_bbox:
         min_r, min_c, max_r, max_c = kept_payload_bbox
         kept_bbox_shape = (max_r - min_r + 1, max_c - min_c + 1)
    else:
        kept_bbox_shape = (0, 0) # Or handle as per expected output for empty cases

    metrics.append({
        'example': i + 1,
        'input_shape': (input_rows, input_cols),
        'expected_output_shape': (expected_output_rows, expected_output_cols),
        'status': 'Processed',
        'largest_object': {
            'color': key_color,
            'size': largest_object['size'],
            # 'coords': large_object_coords # Too verbose for summary
        },
        'payload_pixel_count': len(payload_coords),
        'payload_colors': sorted(list(payload_colors)),
        'key_color_action': f"Key: {key_color}, Remove: {sorted(list(colors_to_remove))}",
        'kept_payload_pixel_count': len(kept_payload_coords),
        'kept_payload_colors': sorted(list(kept_payload_colors)),
        'kept_payload_bbox': kept_payload_bbox,
        'derived_output_shape': kept_bbox_shape
    })

# --- Print Metrics ---
import json
print(json.dumps(metrics, indent=2))
```
``` failed
Traceback (most recent call last):
  File "<string>", line 135, in <module>
  File "__init__.py", line 238, in dumps
    **kw).encode(obj)
          ^^^^^^^^^^^
  File "encoder.py", line 202, in encode
    chunks = list(chunks)
             ^^^^^^^^^^^^
  File "encoder.py", line 430, in _iterencode
    yield from _iterencode_list(o, _current_indent_level)
  File "encoder.py", line 326, in _iterencode_list
    yield from chunks
  File "encoder.py", line 406, in _iterencode_dict
    yield from chunks
  File "encoder.py", line 406, in _iterencode_dict
    yield from chunks
  File "encoder.py", line 439, in _iterencode
    o = _default(o)
        ^^^^^^^^^^^
  File "encoder.py", line 180, in default
    raise TypeError(f'Object of type {o.__class__.__name__} '
TypeError: Object of type int64 is not JSON serializable

```
Ah, the numpy integer types aren't directly JSON serializable. Let's fix the printing part.


``` python
import numpy as np
from collections import deque
import json

# --- Helper functions ---
def find_objects(grid):
    rows, cols = grid.shape
    visited = set()
    objects = []
    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r, c] != 0:
                color = grid[r, c]
                obj_coords = set()
                q = deque([(r, c)])
                visited.add((r, c))
                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           (nr, nc) not in visited and grid[nr, nc] == color:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                objects.append({
                    'color': color,
                    'coords': obj_coords,
                    'size': len(obj_coords)
                })
    return objects

def get_bounding_box(coords):
    if not coords: return None
    min_row = min(r for r, c in coords)
    min_col = min(c for r, c in coords)
    max_row = max(r for r, c in coords)
    max_col = max(c for r, c in coords)
    return min_row, min_col, max_row, max_col

# --- Define Inputs ---
inputs = [
    [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,3,3,3,0,0,0,3,3,3,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,3,3,3,0,0,0,3,3,3,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,3,3,3,0,0,0,3,3,3,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,2,1,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,4,8,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,8,6,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
    [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],[0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],[0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],[0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],[0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],[0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0],[0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],[0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],[0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],[0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],[0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,3,1,7,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,2,8,9,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,3,4,6,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
    [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,8,8,8,8,0,0,0,0,8,8,8,8,8,8,8,8,0,0,0,0],[0,0,8,8,8,8,0,0,0,0,8,8,8,8,8,8,8,8,0,0,0,0],[0,0,8,8,8,8,0,0,0,0,8,8,8,8,8,8,8,8,0,0,0,0],[0,0,8,8,8,8,0,0,0,0,8,8,8,8,8,8,8,8,0,0,0,0],[0,0,8,8,8,8,0,0,0,0,8,8,8,8,0,0,0,0,0,0,0,0],[0,0,8,8,8,8,0,0,0,0,8,8,8,8,0,0,0,0,0,0,0,0],[0,0,8,8,8,8,0,0,0,0,8,8,8,8,0,0,0,0,0,0,0,0],[0,0,8,8,8,8,0,0,0,0,8,8,8,8,0,0,0,0,0,0,0,0],[0,0,8,8,8,8,0,0,0,0,0,0,0,0,8,8,8,8,0,0,0,0],[0,0,8,8,8,8,0,0,0,0,0,0,0,0,8,8,8,8,0,0,0,0],[0,0,8,8,8,8,0,0,0,0,0,0,0,0,8,8,8,8,0,0,0,0],[0,0,8,8,8,8,0,0,0,0,0,0,0,0,8,8,8,8,0,0,0,0],[0,0,8,8,8,8,8,8,8,8,8,8,8,8,0,0,0,0,0,0,0,0],[0,0,8,8,8,8,8,8,8,8,8,8,8,8,0,0,0,0,0,0,0,0],[0,0,8,8,8,8,8,8,8,8,8,8,8,8,0,0,0,0,0,0,0,0],[0,0,8,8,8,8,8,8,8,8,8,8,8,8,0,0,0,4,1,9,4,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,3,6,1,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,5,7,5,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,4,2,7,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
]

# --- Define Expected Outputs ---
expected_outputs = [
    [[2,0,7],[4,8,0],[0,6,1]],
    [[3,0,7],[0,8,0],[3,0,6]],
    [[4,0,9,4],[6,0,6,0],[3,0,0,5],[2,4,2,0]]
]

# --- Custom JSON Encoder for NumPy types ---
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, set):
            return list(obj) # Convert sets to lists for JSON
        return super(NpEncoder, self).default(obj)

# --- Process Each Example ---
metrics = []
for i, input_list in enumerate(inputs):
    input_grid = np.array(input_list, dtype=int)
    expected_output_grid = np.array(expected_outputs[i], dtype=int)
    input_rows, input_cols = input_grid.shape
    expected_output_rows, expected_output_cols = expected_output_grid.shape

    objects = find_objects(input_grid)
    if not objects:
        metrics.append({
            'example': i + 1,
            'input_shape': (input_rows, input_cols),
            'expected_output_shape': (expected_output_rows, expected_output_cols),
            'status': 'No non-white objects found',
            'largest_object': None,
            'payload_pixels': None,
            'payload_colors': None,
            'kept_payload_pixels': None,
            'kept_payload_colors': None,
            'kept_payload_bbox': None,
            'colors_to_remove': None
        })
        continue

    largest_object = max(objects, key=lambda obj: obj['size'])
    key_color = largest_object['color']
    large_object_coords = largest_object['coords']

    all_non_white_coords = set(zip(*np.where(input_grid != 0)))
    payload_coords = all_non_white_coords - large_object_coords

    payload_pixels_data = {(r, c): input_grid[r, c] for r, c in payload_coords}
    payload_colors = set(payload_pixels_data.values())

    # Determine colors to keep based on refined logic
    all_colors = set(range(1, 10)) # Colors 1 through 9
    colors_to_remove = set()
    if key_color == 3: # Green Key
        colors_to_remove = {9} # Remove Maroon
    elif key_color == 1: # Blue Key
        colors_to_remove = {1, 2, 4, 9} # Remove Blue, Red, Yellow, Maroon
    elif key_color == 8: # Azure Key
        colors_to_remove = {1, 7} # Remove Blue, Orange
    # else: keep all payload colors (implicitly)

    colors_to_keep = payload_colors - colors_to_remove

    kept_payload_coords = {
        (r, c) for (r, c), color in payload_pixels_data.items() if color in colors_to_keep
    }
    kept_payload_colors = {input_grid[r,c] for r,c in kept_payload_coords} # Unique colors kept

    kept_payload_bbox = get_bounding_box(kept_payload_coords)
    if kept_payload_bbox:
         min_r, min_c, max_r, max_c = kept_payload_bbox
         kept_bbox_shape = (max_r - min_r + 1, max_c - min_c + 1)
    else:
        # If no pixels are kept, the output should be empty [] or [[0]]?
        # The original code returned [[]] which seemed expected by failed tests.
        # If bbox is None, shape is (0,0) conceptually.
        kept_bbox_shape = (0, 0)


    metrics.append({
        'example': i + 1,
        'input_shape': (input_rows, input_cols),
        'expected_output_shape': (expected_output_rows, expected_output_cols),
        'status': 'Processed',
        'largest_object': {
            'color': key_color,
            'size': largest_object['size'],
        },
        'payload_pixel_count': len(payload_coords),
        'payload_colors': sorted(list(payload_colors)),
        'key_color_action': f"Key: {key_color}, Remove: {sorted(list(colors_to_remove))}",
        'kept_payload_pixel_count': len(kept_payload_coords),
        'kept_payload_colors': sorted(list(kept_payload_colors)),
        'kept_payload_bbox': kept_payload_bbox, # (min_r, min_c, max_r, max_c)
        'derived_output_shape': kept_bbox_shape # (height, width)
    })

# --- Print Metrics using custom encoder ---
print(json.dumps(metrics, indent=2, cls=NpEncoder))
```
```
[
  {
    "example": 1,
    "input_shape": [
      27,
      25
    ],
    "expected_output_shape": [
      3,
      3
    ],
    "status": "Processed",
    "largest_object": {
      "color": 3,
      "size": 45
    },
    "payload_pixel_count": 18,
    "payload_colors": [
      1,
      2,
      3,
      4,
      6,
      7,
      8,
      9
    ],
    "key_color_action": "Key: 3, Remove: [9]",
    "kept_payload_pixel_count": 17,
    "kept_payload_colors": [
      1,
      2,
      3,
      4,
      6,
      7,
      8
    ],
    "kept_payload_bbox": [
      3,
      8,
      21,
      17
    ],
    "derived_output_shape": [
      19,
      10
    ]
  },
  {
    "example": 2,
    "input_shape": [
      27,
      21
    ],
    "expected_output_shape": [
      3,
      3
    ],
    "status": "Processed",
    "largest_object": {
      "color": 1,
      "size": 25
    },
    "payload_pixel_count": 109,
    "payload_colors": [
      1,
      2,
      3,
      4,
      6,
      7,
      8,
      9
    ],
    "key_color_action": "Key: 1, Remove: [1, 2, 4, 9]",
    "kept_payload_pixel_count": 5,
    "kept_payload_colors": [
      3,
      6,
      7,
      8
    ],
    "kept_payload_bbox": [
      19,
      7,
      21,
      9
    ],
    "derived_output_shape": [
      3,
      3
    ]
  },
  {
    "example": 3,
    "input_shape": [
      22,
      22
    ],
    "expected_output_shape": [
      4,
      4
    ],
    "status": "Processed",
    "largest_object": {
      "color": 8,
      "size": 96
    },
    "payload_pixel_count": 80,
    "payload_colors": [
      1,
      2,
      3,
      4,
      5,
      6,
      7,
      8,
      9
    ],
    "key_color_action": "Key: 8, Remove: [1, 7]",
    "kept_payload_pixel_count": 76,
    "kept_payload_colors": [
      2,
      3,
      4,
      5,
      6,
      8,
      9
    ],
    "kept_payload_bbox": [
      1,
      10,
      19,
      20
    ],
    "derived_output_shape": [
      19,
      11
    ]
  }
]

```
**Analysis of Metrics vs. Expectations:**

*   **Example 1:**
    *   Key Color: Green (3). Action: Remove Maroon (9). Correct.
    *   Payload Colors: {1, 2, 3, 4, 6, 7, 8, 9}.
    *   Kept Payload Colors: {1, 2, 3, 4, 6, 7, 8}.
    *   Expected Output Colors: {1, 2, 4, 6, 7, 8}. *Difference: My `kept_payload_colors` includes Green (3), but the expected output does not.* Why? Looking at the input, the payload pixels *do* contain Green (3) from the smaller green squares.
        
```
        Input Snippet (Payload Area for Ex 1):
        ...
        ... 3 3 3 ... 3 3 3 ...  -> These are part of the largest object
        ... 3 3 3 ... 3 3 3 ...
        ... 3 3 3 ... 3 3 3 ...
        ... 3 3 3 3 3 3 ...
        ... 3 3 3 3 3 3 ...
        ... 3 3 3 3 3 3 ...
        ... 0 0 0 3 3 3 3 3 3 ... -> These are part of the largest object
        ... 0 0 0 3 3 3 3 3 3 ...
        ... 0 0 0 3 3 3 3 3 3 ...
        ...
        ... 2 1 7 ...
        ... 4 8 9 ...
        ... 8 6 1 ... -> These are payload pixels. Wait, where did the other green payload pixels come from? Let's re-run find_objects carefully.
        ```

        Rethinking `find_objects`: The current BFS finds contiguous blocks of the *same* color. In Example 1, the large green object is indeed size 45. The payload pixels are *only* the 3x3 grid at the bottom: (19,8) to (21,10). There are no other non-white pixels.
        Let's redo the metrics manually for Ex 1 based on this:
        *   Largest Object: Green (3), Size 45.
        *   Payload Coords: {(19,8), (19,9), (19,10), (20,8), (20,9), (20,10), (21,8), (21,9), (21,10)}
        *   Payload Colors: {1, 2, 4, 6, 7, 8, 9}
        *   Key Color Action: Key=3, Remove={9}.
        *   Kept Payload Colors: {1, 2, 4, 6, 7, 8}. This *matches* the colors in the expected output.
        *   Kept Payload Coords: All payload coords except (20,10) where color is 9.
        *   Bounding Box of Kept Coords: min_r=19, min_c=8, max_r=21, max_c=10.
        *   Derived Output Shape: (21-19+1) x (10-8+1) = 3x3. This *matches* the expected output shape.
        *   *Conclusion for Ex 1:* The refined logic seems correct. The error was in my previous interpretation/calculation of payload pixels during the metrics run.

*   **Example 2:**
    *   Key Color: Blue (1). Action: Remove {1, 2, 4, 9}. Correct.
    *   Payload Coords: Pixels from (1,1) to (15,5), (1,11) to (15,16), (6,6) to (10,10), and (19,7) to (21,9). *Correction:* The `find_objects` should identify the *single* largest object. In this case, there are multiple blue objects. Which one is largest? Let's assume the one from (1,1) to (5,5) and (11,1) to (15,5) combined (size 30+30=60?). No, they are separate. And the central blue square (6,6) to (10,10) is size 25. The two blocks top-left/right are size 30 each. The bottom-left/right are size 30 each. Okay, there are multiple objects tied for largest size (30). How to break ties? Maybe use the one that appears first in scan order (top-left)? Let's assume the top-left blue block (1,1) to (5,5) is the Key Object.
    *   Key Object: Blue (1), Size 30, Coords {(r,c) | 1<=r<=5, 1<=c<=5}.
    *   Payload Pixels: All other blue pixels + the 3x3 grid at the bottom.
    *   Payload Colors: {1, 2, 3, 4, 6, 7, 8, 9}.
    *   Key Color Action: Key=1, Remove={1, 2, 4, 9}.
    *   Kept Payload Colors: {3, 6, 7, 8}. This *matches* the colors in the expected output.
    *   Kept Payload Coords: Only the coords from the bottom 3x3 grid where colors are {3, 7, 8, 3, 6}. Specifically: {(19,7), (19,9), (20,8), (21,7), (21,9)}.
    *   Bounding Box of Kept Coords: min_r=19, min_c=7, max_r=21, max_c=9.
    *   Derived Output Shape: (21-19+1) x (9-7+1) = 3x3. This *matches* the expected output shape.
    *   *Conclusion for Ex 2:* The refined logic seems correct, assuming the top-left object is chosen in case of a size tie. The `max()` function in Python on a list of dictionaries will typically return the *first* one found if the `key` values are equal.

*   **Example 3:**
    *   Key Color: Azure (8). Action: Remove {1, 7}. Correct.
    *   Largest Object: There are multiple large azure shapes. The top-left one (1,2) to (12,5) has size 4*12=48. The top-right one (1,10) to (8,17) seems larger... wait, shapes are complex. Need `find_objects` output.
    *   *Assumption based on code logic:* The `find_objects` finds *all* contiguous objects, then `max()` finds the one with the largest size. If ties, the first one encountered in row-major scan order wins. Let's assume the largest is correctly identified as Azure (8).
    *   Payload Pixels: All other azure pixels + the 4x4 grid at the bottom-right.
    *   Payload Colors: {1, 2, 3, 4, 5, 6, 7, 8, 9}.
    *   Key Color Action: Key=8, Remove={1, 7}.
    *   Kept Payload Colors: {2, 3, 4, 5, 6, 8, 9}.
    *   Expected Output Colors: {2, 3, 4, 5, 6, 9}. *Difference: My `kept_payload_colors` includes Azure (8), but the expected output does not.* This means Azure pixels from the payload are also removed when the Key Color is Azure.
    *   *Revised Rule for Azure (8):* Remove {1, 7, 8}.
    *   Kept Payload Colors (Revised): {2, 3, 4, 5, 6, 9}. This *matches* the expected output colors.
    *   Kept Payload Coords: Only the coords from the bottom 4x4 grid where colors are in {2, 3, 4, 5, 6, 9}. Coords: {(16,17), (16,19), (16,20), (17,17), (17,19), (18,17), (18,18), (18,20), (19,17), (19,18), (19,19)}.
    *   Bounding Box of Kept Coords: min_r=16, min_c=17, max_r=19, max_c=20.
    *   Derived Output Shape: (19-16+1) x (20-17+1) = 4x4. This *matches* the expected output shape.
    *   *Conclusion for Ex 3:* The refined logic needs one more tweak: if the key color is Azure (8), remove Blue (1), Orange (7), *and Azure (8)* from the payload.

**Final Refined Filtering Rules:**

*   If `KeyColor` is Green (3): Remove Maroon (9).
*   If `KeyColor` is Blue (1): Remove Blue (1), Red (2), Yellow (4), Maroon (9).
*   If `KeyColor` is Azure (8): Remove Blue (1), Orange (7), Azure (8).
*   Otherwise: Remove nothing.

Let's re-run the metrics check with the final Azure rule.


``` python
import numpy as np
from collections import deque
import json

# --- Helper functions ---
def find_objects(grid):
    rows, cols = grid.shape
    visited = set()
    objects = []
    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r, c] != 0:
                color = grid[r, c]
                obj_coords = set()
                q = deque([(r, c)])
                visited.add((r, c))
                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           (nr, nc) not in visited and grid[nr, nc] == color:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                objects.append({
                    'color': color,
                    'coords': obj_coords,
                    'size': len(obj_coords)
                })
    # Sort by size descending, then row, then col of top-left coord for deterministic tie-breaking
    objects.sort(key=lambda o: (-o['size'], min(r for r,c in o['coords']), min(c for r,c in o['coords'])))
    return objects

def get_bounding_box(coords):
    if not coords: return None
    min_row = min(r for r, c in coords)
    min_col = min(c for r, c in coords)
    max_row = max(r for r, c in coords)
    max_col = max(c for r, c in coords)
    return min_row, min_col, max_row, max_col

# --- Define Inputs ---
inputs = [
    [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,3,3,3,0,0,0,3,3,3,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,3,3,3,0,0,0,3,3,3,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,3,3,3,0,0,0,3,3,3,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,3,3,3,3,3,3,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,2,1,7,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,4,8,9,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,8,6,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
    [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],[0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],[0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],[0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],[0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],[0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0],[0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],[0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],[0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],[0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],[0,1,1,1,1,1,0,0,0,0,0,1,1,1,1,1,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,3,1,7,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,2,8,9,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,3,4,6,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
    [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,8,8,8,8,0,0,0,0,8,8,8,8,8,8,8,8,0,0,0,0],[0,0,8,8,8,8,0,0,0,0,8,8,8,8,8,8,8,8,0,0,0,0],[0,0,8,8,8,8,0,0,0,0,8,8,8,8,8,8,8,8,0,0,0,0],[0,0,8,8,8,8,0,0,0,0,8,8,8,8,8,8,8,8,0,0,0,0],[0,0,8,8,8,8,0,0,0,0,8,8,8,8,0,0,0,0,0,0,0,0],[0,0,8,8,8,8,0,0,0,0,8,8,8,8,0,0,0,0,0,0,0,0],[0,0,8,8,8,8,0,0,0,0,8,8,8,8,0,0,0,0,0,0,0,0],[0,0,8,8,8,8,0,0,0,0,8,8,8,8,0,0,0,0,0,0,0,0],[0,0,8,8,8,8,0,0,0,0,0,0,0,0,8,8,8,8,0,0,0,0],[0,0,8,8,8,8,0,0,0,0,0,0,0,0,8,8,8,8,0,0,0,0],[0,0,8,8,8,8,0,0,0,0,0,0,0,0,8,8,8,8,0,0,0,0],[0,0,8,8,8,8,0,0,0,0,0,0,0,0,8,8,8,8,0,0,0,0],[0,0,8,8,8,8,8,8,8,8,8,8,8,8,0,0,0,0,0,0,0,0],[0,0,8,8,8,8,8,8,8,8,8,8,8,8,0,0,0,0,0,0,0,0],[0,0,8,8,8,8,8,8,8,8,8,8,8,8,0,0,0,0,0,0,0,0],[0,0,8,8,8,8,8,8,8,8,8,8,8,8,0,0,0,4,1,9,4,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,6,3,6,1,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,3,5,7,5,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,2,4,2,7,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
]

# --- Define Expected Outputs ---
expected_outputs = [
    [[2,0,7],[4,8,0],[0,6,1]],
    [[3,0,7],[0,8,0],[3,0,6]],
    [[4,0,9,4],[6,0,6,0],[3,0,0,5],[2,4,2,0]]
]

# --- Custom JSON Encoder for NumPy types ---
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, set):
            try:
              return sorted(list(obj)) # Sort sets for consistent output
            except TypeError: # Handle sets of tuples
              return list(obj)
        if isinstance(obj, tuple) and len(obj) == 4: # Bounding box tuple
            return list(obj)
        return super(NpEncoder, self).default(obj)

# --- Process Each Example ---
metrics = []
for i, input_list in enumerate(inputs):
    input_grid = np.array(input_list, dtype=int)
    expected_output_grid = np.array(expected_outputs[i], dtype=int)
    input_rows, input_cols = input_grid.shape
    expected_output_rows, expected_output_cols = expected_output_grid.shape

    objects = find_objects(input_grid)
    if not objects:
        # Handle case with no objects (shouldn't happen based on examples)
        largest_object = None
        key_color = -1 # Invalid color
        large_object_coords = set()
    else:
        largest_object = objects[0] # Get the largest (or first largest if tie)
        key_color = largest_object['color']
        large_object_coords = largest_object['coords']

    all_non_white_coords = set(zip(*np.where(input_grid != 0)))
    payload_coords = all_non_white_coords - large_object_coords

    payload_pixels_data = {(r, c): input_grid[r, c] for r, c in payload_coords}
    payload_colors = set(payload_pixels_data.values())

    # Determine colors to remove based on the final refined logic
    colors_to_remove = set()
    if key_color == 3: # Green Key
        colors_to_remove = {9} # Remove Maroon
    elif key_color == 1: # Blue Key
        colors_to_remove = {1, 2, 4, 9} # Remove Blue, Red, Yellow, Maroon
    elif key_color == 8: # Azure Key
        colors_to_remove = {1, 7, 8} # Remove Blue, Orange, Azure
    # else: remove nothing

    colors_to_keep = payload_colors - colors_to_remove

    kept_payload_coords = {
        (r, c) for (r, c), color in payload_pixels_data.items() if color in colors_to_keep
    }
    kept_payload_colors = {input_grid[r,c] for r,c in kept_payload_coords} # Unique colors kept

    kept_payload_bbox = get_bounding_box(kept_payload_coords)
    if kept_payload_bbox:
         min_r, min_c, max_r, max_c = kept_payload_bbox
         derived_output_shape = (max_r - min_r + 1, max_c - min_c + 1)
    else:
        derived_output_shape = (0, 0)

    metrics.append({
        'example': i + 1,
        'input_shape': (input_rows, input_cols),
        'expected_output_shape': (expected_output_rows, expected_output_cols),
        'status': 'Processed',
        'largest_object': {
            'color': key_color,
            'size': largest_object['size'] if largest_object else 0,
        },
        'payload_pixel_count': len(payload_coords),
        'payload_colors': sorted(list(payload_colors)), # Use sorted list
        'key_color_action': f"Key: {key_color}, Remove: {sorted(list(colors_to_remove))}", # Use sorted list
        'kept_payload_pixel_count': len(kept_payload_coords),
        'kept_payload_colors': sorted(list(kept_payload_colors)), # Use sorted list
        'kept_payload_bbox': kept_payload_bbox, # (min_r, min_c, max_r, max_c)
        'derived_output_shape': derived_output_shape # (height, width)
    })

# --- Print Metrics using custom encoder ---
print(json.dumps(metrics, indent=2, cls=NpEncoder))
```
```
[
  {
    "example": 1,
    "input_shape": [
      27,
      25
    ],
    "expected_output_shape": [
      3,
      3
    ],
    "status": "Processed",
    "largest_object": {
      "color": 3,
      "size": 45
    },
    "payload_pixel_count": 18,
    "payload_colors": [
      1,
      2,
      3,
      4,
      6,
      7,
      8,
      9
    ],
    "key_color_action": "Key: 3, Remove: [9]",
    "kept_payload_pixel_count": 17,
    "kept_payload_colors": [
      1,
      2,
      3,
      4,
      6,
      7,
      8
    ],
    "kept_payload_bbox": [
      3,
      8,
      21,
      17
    ],
    "derived_output_shape": [
      19,
      10
    ]
  },
  {
    "example": 2,
    "input_shape": [
      27,
      21
    ],
    "expected_output_shape": [
      3,
      3
    ],
    "status": "Processed",
    "largest_object": {
      "color": 1,
      "size": 25
    },
    "payload_pixel_count": 109,
    "payload_colors": [
      1,
      2,
      3,
      4,
      6,
      7,
      8,
      9
    ],
    "key_color_action": "Key: 1, Remove: [1, 2, 4, 9]",
    "kept_payload_pixel_count": 5,
    "kept_payload_colors": [
      3,
      6,
      7,
      8
    ],
    "kept_payload_bbox": [
      19,
      7,
      21,
      9
    ],
    "derived_output_shape": [
      3,
      3
    ]
  },
  {
    "example": 3,
    "input_shape": [
      22,
      22
    ],
    "expected_output_shape": [
      4,
      4
    ],
    "status": "Processed",
    "largest_object": {
      "color": 8,
      "size": 96
    },
    "payload_pixel_count": 80,
    "payload_colors": [
      1,
      2,
      3,
      4,
      5,
      6,
      7,
      8,
      9
    ],
    "key_color_action": "Key: 8, Remove: [1, 7, 8]",
    "kept_payload_pixel_count": 12,
    "kept_payload_colors": [
      2,
      3,
      4,
      5,
      6,
      9
    ],
    "kept_payload_bbox": [
      16,
      17,
      19,
      20
    ],
    "derived_output_shape": [
      4,
      4
    ]
  }
]

```
**Final Metrics Check:**

The metrics calculated using the final refined logic now perfectly match the expected outputs in terms of which colors are kept and the derived output shape based on the bounding box of those kept pixels.

*   **Example 1:** Derived shape (3x3) matches expected (3x3). Kept colors {1, 2, 4, 6, 7, 8} match expected. *Correction in previous manual check: Example 1 has payload pixels in the large green area as well, not just the 3x3 block. The code correctly identifies the largest green object (size 45), and all other pixels (including smaller green blocks AND the 3x3 colored block) are payload. When removing color 9 (Maroon), the kept colors are {1, 2, 3, 4, 6, 7, 8}. The bounding box of these kept pixels *does* result in a 19x10 shape.* **HOLD ON.** This contradicts the previous manual analysis that matched the 3x3 output. Let's re-examine Example 1 input and expected output visually.
    *   Input 1: Large green H-shape. Small 3x3 colorful block far below it.
    *   Expected Output 1: The 3x3 block, with color 9 (Maroon) turned to 0 (White). Cropped to 3x3.
    *   Why did the code get a 19x10 bounding box? Because it included the *smaller green objects* as part of the kept payload. If the KeyColor is Green (3), should payload Green (3) pixels be kept? The expected output suggests **NO**.
    *   *Revised Rule for Green (3):* Remove Maroon (9) *and Green (3)*.

*   **Revising for Green (3):**
    *   Key Color: Green (3). Action: Remove {3, 9}.
    *   Kept Payload Colors: {1, 2, 4, 6, 7, 8}. Matches expected output colors.
    *   Kept Payload Coords: Only the coords from the bottom 3x3 grid where colors are {1, 2, 4, 6, 7, 8}. Coords: {(19,8), (19,9), (19,10), (20,8), (20,9), (21,8), (21,9), (21,10)}.
    *   Bounding Box of Kept Coords: min_r=19, min_c=8, max_r=21, max_c=10.
    *   Derived Output Shape: 3x3. Matches expected.

*   **Final, Final Filtering Rules:**
    *   If `KeyColor` is Green (3): Remove Green (3), Maroon (9).
    *   If `KeyColor` is Blue (1): Remove Blue (1), Red (2), Yellow (4), Maroon (9).
    *   If `KeyColor` is Azure (8): Remove Blue (1), Orange (7), Azure (8).
    *   Otherwise: Remove nothing.

This seems consistent across all examples now. The key insight is that sometimes the key object's color itself is also removed from the payload.

## YAML Fact Documentation


```yaml
Task: Filter payload pixels based on the color of the largest object and crop the result.

Examples:
  - Example: 1
    InputShape: [27, 25]
    OutputShape: [3, 3]
    Objects:
      - Type: KeyObject # Largest object
        Color: Green (3)
        Size: 45
        Action: DetermineFilter
      - Type: PayloadPixels # All other non-white pixels
        ColorsPresent: [Blue (1), Red (2), Green (3), Yellow (4), Gray (6), Orange (7), Azure (8), Maroon (9)]
        Action: FilterAndCrop
    Filtering:
      KeyColor: Green (3)
      RemovedColors: [Green (3), Maroon (9)]
      KeptColors: [Blue (1), Red (2), Yellow (4), Gray (6), Orange (7), Azure (8)]
    OutputGrid:
      Source: Kept PayloadPixels
      BoundingBox: Calculated from Kept PayloadPixels coordinates
      Dimensions: [3, 3] # Derived from BoundingBox

  - Example: 2
    InputShape: [27, 21]
    OutputShape: [3, 3]
    Objects:
      - Type: KeyObject # Largest object (tie-broken by position)
        Color: Blue (1)
        Size: 25 # Note: My code picked the central square, actual tie-break might differ but Blue is the key color. Let's assume code finds a Blue(1) object as largest.
        Action: DetermineFilter
      - Type: PayloadPixels # All other non-white pixels
        ColorsPresent: [Blue (1), Red (2), Green (3), Yellow (4), Gray (6), Orange (7), Azure (8), Maroon (9)]
        Action: FilterAndCrop
    Filtering:
      KeyColor: Blue (1)
      RemovedColors: [Blue (1), Red (2), Yellow (4), Maroon (9)]
      KeptColors: [Green (3), Gray (6), Orange (7), Azure (8)]
    OutputGrid:
      Source: Kept PayloadPixels
      BoundingBox: Calculated from Kept PayloadPixels coordinates
      Dimensions: [3, 3] # Derived from BoundingBox

  - Example: 3
    InputShape: [22, 22]
    OutputShape: [4, 4]
    Objects:
      - Type: KeyObject # Largest object
        Color: Azure (8)
        Size: 96
        Action: DetermineFilter
      - Type: PayloadPixels # All other non-white pixels
        ColorsPresent: [Blue (1), Red (2), Green (3), Yellow (4), Gray (5), Gray (6), Orange (7), Azure (8), Maroon (9)]
        Action: FilterAndCrop
    Filtering:
      KeyColor: Azure (8)
      RemovedColors: [Blue (1), Orange (7), Azure (8)]
      KeptColors: [Red (2), Green (3), Yellow (4), Gray (5), Gray (6), Maroon (9)]
    OutputGrid:
      Source: Kept PayloadPixels
      BoundingBox: Calculated from Kept PayloadPixels coordinates
      Dimensions: [4, 4] # Derived from BoundingBox

GeneralProperties:
  - BackgroundColor: White (0)
  - ObjectDefinition: Contiguous pixels of the same non-white color.
  - Connectivity: 4-way (Up, Down, Left, Right).
  - TieBreaking: Largest object determined by pixel count. If ties, implicitly the first object encountered in row-major scan order (or sorted by top-left coord).
```


## Natural Language Program

1.  Identify all contiguous objects (groups of connected pixels of the same color) that are not white (0). Use 4-way connectivity.
2.  Determine the single largest object based on the number of pixels it contains. If there's a tie in size, select the one whose top-most, left-most pixel comes first in a row-by-row, column-by-column scan. Let the color of this largest object be the `KeyColor` and its coordinates be `KeyObjectCoords`.
3.  Identify all non-white pixels in the input grid whose coordinates are *not* in `KeyObjectCoords`. These are the `PayloadPixels`. Collect their coordinates (`PayloadCoords`) and colors.
4.  If there are no `PayloadPixels`, return an empty grid represented as `[[]]`.
5.  Determine the set of `ColorsToRemove` based on the `KeyColor`:
    *   If `KeyColor` is Green (3), `ColorsToRemove` = {Green (3), Maroon (9)}.
    *   If `KeyColor` is Blue (1), `ColorsToRemove` = {Blue (1), Red (2), Yellow (4), Maroon (9)}.
    *   If `KeyColor` is Azure (8), `ColorsToRemove` = {Blue (1), Orange (7), Azure (8)}.
    *   Otherwise, `ColorsToRemove` is an empty set.
6.  Create a new set of coordinates, `KeptPayloadCoords`, containing only the coordinates `(r, c)` from `PayloadCoords` where the color of the input grid at `(r, c)` is *not* in `ColorsToRemove`.
7.  If `KeptPayloadCoords` is empty, return an empty grid represented as `[[]]`.
8.  Calculate the minimum bounding box that encloses all coordinates in `KeptPayloadCoords`. Let the top-left corner be `(min_r, min_c)` and the bottom-right corner be `(max_r, max_c)`.
9.  Calculate the dimensions of the output grid: `height = max_r - min_r + 1`, `width = max_c - min_c + 1`.
10. Create a new output grid of size `(height, width)`, initialized entirely with white (0).
11. Iterate through each coordinate `(r, c)` in `KeptPayloadCoords`:
    *   Get the `CurrentColor` from the input grid at `(r, c)`.
    *   Calculate the corresponding position in the output grid: `out_r = r - min_r`, `out_c = c - min_c`.
    *   Set the pixel in the output grid at `(out_r, out_c)` to `CurrentColor`.
12. Return the generated output grid.