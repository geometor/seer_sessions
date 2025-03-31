*   **Assessment and Strategy:**
    *   The initial code correctly identified the core components: background color, non-background colors, bounding boxes, and the idea of filling based on adjacency. However, it failed because it performed a single pass check based *only* on the original input grid's neighbours.
    *   The results show that the filling process is iterative or expanding. A background pixel within the bounding box should be filled if it becomes adjacent to the target color *at any point* during the filling process for that color, not just based on the initial state.
    *   The strategy is to modify the transformation logic for each non-background color. After identifying the bounding box, we need to repeatedly scan the pixels within the box. In each scan (or iteration), we identify background pixels adjacent to *currently* colored pixels (of the target color) and change them. This process repeats until a scan finds no more pixels to change for that specific color. This ensures the "spreading" or "filling" effect observed in the examples.

*   **Metrics:**
    
``` python
    import numpy as np
    from collections import Counter

    def find_background_color(grid):
        unique, counts = np.unique(grid, return_counts=True)
        return unique[np.argmax(counts)]

    def find_pixels_of_color(grid, color):
        rows, cols = np.where(grid == color)
        return list(zip(rows, cols))

    def calculate_bounding_box(coords):
        if not coords: return None
        min_row = min(r for r, c in coords)
        min_col = min(c for r, c in coords)
        max_row = max(r for r, c in coords)
        max_col = max(c for r, c in coords)
        return min_row, min_col, max_row, max_col

    # Example 1 Data
    input_1 = np.array([
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 1, 3, 3, 3],
        [3, 3, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 3, 3, 4, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 3, 3, 3, 3, 3],
        [3, 3, 3, 4, 3, 3, 3, 3, 4, 4, 4, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    ])

    # Example 2 Data
    input_2 = np.array([
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 3, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 3, 3, 3, 3, 3, 3, 3, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 3, 3, 3, 3, 3, 3, 3, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 3, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
    ])

    # Example 3 Data
    input_3 = np.array([
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 8, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 1, 1, 1],
        [1, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 1, 1, 1],
        [1, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 8, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ])

    metrics = {}

    for i, input_grid in enumerate([input_1, input_2, input_3], 1):
        bg_color = find_background_color(input_grid)
        unique_colors = np.unique(input_grid)
        non_bg_colors = [c for c in unique_colors if c != bg_color]
        
        bounding_boxes = {}
        for color in non_bg_colors:
            coords = find_pixels_of_color(input_grid, color)
            bounding_boxes[color] = calculate_bounding_box(coords)
            
        metrics[f'example_{i}'] = {
            'background_color': bg_color,
            'non_background_colors': non_bg_colors,
            'bounding_boxes': bounding_boxes
        }

    import json
    print(json.dumps(metrics, indent=2))
```
``` failed
Traceback (most recent call last):
  File "<string>", line 108, in <module>
  File "__init__.py", line 238, in dumps
    **kw).encode(obj)
          ^^^^^^^^^^^
  File "encoder.py", line 202, in encode
    chunks = list(chunks)
             ^^^^^^^^^^^^
  File "encoder.py", line 432, in _iterencode
    yield from _iterencode_dict(o, _current_indent_level)
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
*   **Assessment and Strategy:** (As stated previously)
    *   The initial code failed due to performing only a single-pass check based on the original input grid's neighbors.
    *   The filling process requires iteration: background pixels within a color's bounding box are filled if they become adjacent to that color *during* the filling process.
    *   The updated strategy involves iteratively scanning within each color's bounding box, changing background pixels adjacent to the target color (in the *current* grid state), and repeating until no more pixels change for that color.

*   **Metrics:**
    
``` python
    import numpy as np
    from collections import Counter
    import json

    # Helper function to convert numpy types to Python types for JSON serialization
    def convert_types(obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            return {k: convert_types(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            return [convert_types(i) for i in obj]
        return obj

    def find_background_color(grid):
        unique, counts = np.unique(grid, return_counts=True)
        return unique[np.argmax(counts)]

    def find_pixels_of_color(grid, color):
        rows, cols = np.where(grid == color)
        return list(zip(rows, cols))

    def calculate_bounding_box(coords):
        if not coords: return None
        min_row = min(r for r, c in coords)
        min_col = min(c for r, c in coords)
        max_row = max(r for r, c in coords)
        max_col = max(c for r, c in coords)
        return min_row, min_col, max_row, max_col

    # Example 1 Data
    input_1 = np.array([
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 1, 3, 3, 3],
        [3, 3, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 3, 3, 4, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 3, 3, 3, 3, 3],
        [3, 3, 3, 4, 3, 3, 3, 3, 4, 4, 4, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    ])

    # Example 2 Data
    input_2 = np.array([
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 3, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 3, 3, 3, 3, 3, 3, 3, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 3, 3, 3, 3, 3, 3, 3, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 3, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
    ])

    # Example 3 Data
    input_3 = np.array([
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 8, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 1, 1, 1],
        [1, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 1, 1, 1],
        [1, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 8, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ])

    metrics = {}

    for i, input_grid in enumerate([input_1, input_2, input_3], 1):
        bg_color = find_background_color(input_grid)
        unique_colors = np.unique(input_grid)
        non_bg_colors = [c for c in unique_colors if c != bg_color]
        
        bounding_boxes = {}
        for color in non_bg_colors:
            coords = find_pixels_of_color(input_grid, color)
            bounding_boxes[color] = calculate_bounding_box(coords)
            
        metrics[f'example_{i}'] = {
            'background_color': bg_color,
            'non_background_colors': non_bg_colors,
            'bounding_boxes': bounding_boxes
        }

    # Convert numpy types before printing
    metrics_converted = convert_types(metrics)
    print(json.dumps(metrics_converted, indent=2))
```
``` failed
Traceback (most recent call last):
  File "<string>", line 124, in <module>
  File "__init__.py", line 238, in dumps
    **kw).encode(obj)
          ^^^^^^^^^^^
  File "encoder.py", line 202, in encode
    chunks = list(chunks)
             ^^^^^^^^^^^^
  File "encoder.py", line 432, in _iterencode
    yield from _iterencode_dict(o, _current_indent_level)
  File "encoder.py", line 406, in _iterencode_dict
    yield from chunks
  File "encoder.py", line 406, in _iterencode_dict
    yield from chunks
  File "encoder.py", line 377, in _iterencode_dict
    raise TypeError(f'keys must be str, int, float, bool or None, '
TypeError: keys must be str, int, float, bool or None, not int64

```
*   **Assessment and Strategy:** (As stated previously)
    *   The core issue is the lack of iterative filling within each color's bounding box.
    *   The updated strategy involves a loop for each non-background color that repeatedly fills adjacent background pixels within the bounding box until no more changes occur.

*   **Metrics:**
    
``` python
    import numpy as np
    from collections import Counter
    import json

    # Helper function to convert numpy types to Python types for JSON serialization
    # Now also handles keys in dictionaries
    def convert_types(obj):
        if isinstance(obj, np.integer):
            return int(obj)
        elif isinstance(obj, np.floating):
            return float(obj)
        elif isinstance(obj, np.ndarray):
            return obj.tolist()
        elif isinstance(obj, dict):
            # Convert keys and values
            return {convert_types(k): convert_types(v) for k, v in obj.items()}
        elif isinstance(obj, (list, tuple)):
            # Convert elements in lists/tuples
            # Special handling for bounding box tuples (don't iterate into them)
            if len(obj) == 4 and all(isinstance(x, np.integer) for x in obj):
                 return tuple(int(x) for x in obj)
            return [convert_types(i) for i in obj]
        return obj

    def find_background_color(grid):
        unique, counts = np.unique(grid, return_counts=True)
        return unique[np.argmax(counts)]

    def find_pixels_of_color(grid, color):
        rows, cols = np.where(grid == color)
        return list(zip(rows, cols))

    def calculate_bounding_box(coords):
        if not coords: return None
        min_row = min(r for r, c in coords)
        min_col = min(c for r, c in coords)
        max_row = max(r for r, c in coords)
        max_col = max(c for r, c in coords)
        # Return numpy integers initially, conversion happens later
        return np.int64(min_row), np.int64(min_col), np.int64(max_row), np.int64(max_col)

    # Example 1 Data
    input_1 = np.array([
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 1, 3, 3, 3],
        [3, 3, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 1, 1, 1, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 3, 3, 4, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 3, 3, 3, 3, 3],
        [3, 3, 3, 4, 3, 3, 3, 3, 4, 4, 4, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 4, 4, 4, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]
    ])

    # Example 2 Data
    input_2 = np.array([
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 3, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 3, 3, 3, 3, 3, 3, 3, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 3, 3, 3, 3, 3, 3, 3, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 3, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]
    ])

    # Example 3 Data
    input_3 = np.array([
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 8, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 8, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 1, 1, 1],
        [1, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 1, 1, 1],
        [1, 1, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 8, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]
    ])

    metrics = {}

    for i, input_grid in enumerate([input_1, input_2, input_3], 1):
        bg_color = find_background_color(input_grid)
        unique_colors = np.unique(input_grid)
        non_bg_colors = [c for c in unique_colors if c != bg_color]
        
        bounding_boxes = {}
        for color in non_bg_colors:
            coords = find_pixels_of_color(input_grid, color)
            bounding_boxes[color] = calculate_bounding_box(coords)
            
        metrics[f'example_{i}'] = {
            'background_color': bg_color,
            'non_background_colors': non_bg_colors,
            'bounding_boxes': bounding_boxes # Will be converted below
        }

    # Convert numpy types before printing
    metrics_converted = convert_types(metrics)
    print(json.dumps(metrics_converted, indent=2))
```
```
{
  "example_1": {
    "background_color": 3,
    "non_background_colors": [
      1,
      4
    ],
    "bounding_boxes": {
      "1": [
        2,
        4,
        9,
        12
      ],
      "4": [
        11,
        3,
        17,
        13
      ]
    }
  },
  "example_2": {
    "background_color": 8,
    "non_background_colors": [
      3
    ],
    "bounding_boxes": {
      "3": [
        1,
        3,
        9,
        9
      ]
    }
  },
  "example_3": {
    "background_color": 1,
    "non_background_colors": [
      8
    ],
    "bounding_boxes": {
      "8": [
        2,
        2,
        17,
        12
      ]
    }
  }
}

```
*   **YAML Fact Sheet:**
    
```yaml
    task_description: Iteratively fill background pixels within the bounding box of each non-background color group if they are adjacent (8-way) to a pixel of that color.

    elements:
      - role: background
        property: most frequent color in the input grid.
        example_1: green (3)
        example_2: azure (8)
        example_3: blue (1)
      - role: objects
        property: groups of contiguous or scattered pixels of the same non-background color C.
        example_1: blue (1), yellow (4)
        example_2: green (3)
        example_3: azure (8)
      - role: bounding_box
        property: the smallest rectangle enclosing all pixels of a specific non-background color C in the original input.
        example_1_color_1: (row_min=2, col_min=4, row_max=9, col_max=12)
        example_1_color_4: (row_min=11, col_min=3, row_max=17, col_max=13)
        example_2_color_3: (row_min=1, col_min=3, row_max=9, col_max=9)
        example_3_color_8: (row_min=2, col_min=2, row_max=17, col_max=12)
      - role: adjacency
        property: includes 8 neighbors (cardinal and diagonal).

    transformation:
      - action: initialize_output
        input: input grid
        output: a mutable copy of the input grid (e.g., numpy array).
      - action: identify_background_color
        input: input grid
        output: background color value.
      - action: identify_non_background_colors
        input: input grid
        output: set of color values present, excluding background.
      - action: process_each_non_background_color
        steps:
          - find_initial_pixels: locate all pixels of the current non-background color C in the input grid.
          - calculate_bounding_box: determine the min/max row/column for pixels of color C based on the initial pixels.
          - iterative_fill_loop:
              - condition: loop continues as long as pixels were changed in the previous pass.
              - pass_setup: create a list to store coordinates of pixels to change in this pass.
              - iterate_within_bounding_box: examine each pixel (r, c) within the calculated box.
              - check_pixel_condition:
                  - condition_1: the pixel (r, c) in the *current output grid* has the background color.
                  - condition_2: the pixel (r, c) has at least one neighbor (8-way adjacency) in the *current output grid* with color C.
              - mark_for_update: if both conditions are met, add (r, c) to the list of pixels to change.
              - update_output_grid: after checking all pixels in the box, change the color of all marked pixels in the output grid to C.
              - update_loop_condition: set a flag if any pixels were changed in this pass.
          - repeat_or_next_color: if pixels were changed, repeat the iterative_fill_loop pass; otherwise, proceed to the next non-background color.
      - action: finalize_output
        input: the modified mutable grid.
        output: the final grid in the required format (e.g., list of lists).

    relationship:
      - A background pixel changes to color C if and only if:
        1. It resides within the bounding box defined by the *initial* positions of all pixels of color C in the input.
        2. It is adjacent (8-way) to at least one pixel that *currently* has color C (either from the input or filled in a previous iteration for this color).
      - This filling process for color C repeats until no more background pixels within its bounding box can be filled based on adjacency to existing C-colored pixels.
    ```


*   **Natural Language Program:**
    1.  Create a mutable copy of the input grid (this will become the output grid).
    2.  Determine the background color by finding the most frequent pixel value in the input grid.
    3.  Identify all unique pixel colors present in the input grid, other than the background color.
    4.  For each unique non-background color `C` found:
        a.  Find the coordinates of all pixels in the *original input* grid that have the color `C`.
        b.  If no pixels of color `C` exist, skip to the next color.
        c.  Calculate the minimum bounding box (minimum row, minimum column, maximum row, maximum column) that encloses all found coordinates for color `C` from the *original input*.
        d.  Start an iterative filling process for color `C`:
            i.  Initialize a flag `pixels_changed_this_pass` to `False`.
            ii. Create an empty list `pixels_to_change` to store coordinates `(r, c)` that should be colored `C` in this pass.
            iii. Iterate through every grid cell `(r, c)` within the calculated bounding box (from minimum row to maximum row, and minimum column to maximum column).
            iv. Check the color of the cell `(r, c)` in the *current state* of the output grid. If it is the background color:
                1.  Examine all 8 neighbors (horizontal, vertical, and diagonal) of the cell `(r, c)`.
                2.  Check if any of these neighbors, in the *current state* of the output grid, have the color `C`.
                3.  If at least one neighbor has color `C`, add the coordinates `(r, c)` to the `pixels_to_change` list.
            v.  After iterating through all cells in the bounding box, check if the `pixels_to_change` list is empty.
                1.  If it is *not* empty, set `pixels_changed_this_pass` to `True`. Then, for every coordinate `(r, c)` in the `pixels_to_change` list, update the output grid by setting the color at `(r, c)` to `C`.
                2.  If it *is* empty, it means no more pixels can be filled for color `C` in this pass, so break out of the iterative filling process (step 4d).
            vi. If `pixels_changed_this_pass` is `True`, repeat the iterative filling process starting from step 4.d.i.
    5.  After processing all non-background colors, return the final state of the output grid.