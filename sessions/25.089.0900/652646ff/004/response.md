**General Assessment and Strategy**

The previous attempt failed significantly, producing outputs that were drastically different in size and content from the expected outputs. The core issue seems to stem from incorrectly identifying the relevant 6x6 regions to extract. The code identified too many potential starting points, likely triggering off individual pixels or small fragments rather than coherent shapes fitting within a 6x6 bounding box.

The strategy needs to be revised to more accurately identify the specific 6x6 patterns/shapes present in the input that correspond to the output subgrids. The key observation from the expected outputs is that they *are* 6x6 grids, each containing a distinct shape derived from the input. The logic should focus on finding contiguous objects in the input whose bounding box is *precisely* 6x6. These bounding boxes directly define the regions to extract, clean, and stack.

**Revised Strategy:**

1.  **Identify Background:** Determine the most frequent color in the input grid.
2.  **Identify Noise:** Define noise colors (5-Gray, 7-Orange, 9-Maroon).
3.  **Find Candidate Objects:** Locate all maximal contiguous regions (objects) composed of any color(s) *except* the background color and the noise colors. Use a method like Breadth-First Search (BFS) or Depth-First Search (DFS) starting from any non-background, non-noise pixel, ensuring visited pixels are marked to avoid redundant searches. Crucially, the search should expand to adjacent pixels regardless of their color, as long as they are not background or noise.
4.  **Filter by Bounding Box:** For each object found, calculate its minimal bounding box (min_row, max_row, min_col, max_col). Keep only those objects where `(max_row - min_row + 1) == 6` AND `(max_col - min_col + 1) == 6`.
5.  **Extract Coordinates:** Collect the top-left corner coordinates (`min_row`, `min_col`) of the bounding boxes for all filtered 6x6 objects.
6.  **Order Coordinates:** Sort these coordinates primarily by row (`min_row`) and secondarily by column (`min_col`).
7.  **Check for Reversal Signal:** Scan the *entire* original input grid for the presence of any Orange (7) pixels.
8.  **Apply Reversal:** If Orange (7) pixels were found, reverse the sorted list of coordinates.
9.  **Extract, Clean, Stack:** Iterate through the final ordered list of coordinates. For each (`r`, `c`):
    *   Extract the 6x6 subgrid from the input starting at `(r, c)`.
    *   Create a cleaned copy of this subgrid, replacing any noise pixels (5, 7, 9) within it with the background color.
    *   Append the cleaned subgrid to a list.
10. **Combine:** Vertically stack the cleaned subgrids in the list to form the final output grid.

**Metrics Gathering**

``` python
import numpy as np
from collections import Counter

def analyze_example(input_data, output_data):
    input_grid = np.array(input_data)
    output_grid = np.array(output_data)
    
    # Input analysis
    i_rows, i_cols = input_grid.shape
    i_colors, i_counts = np.unique(input_grid, return_counts=True)
    i_bg_color = i_colors[np.argmax(i_counts)]
    i_non_bg_noise_pixels = np.where((input_grid != i_bg_color) & (input_grid != 5) & (input_grid != 7) & (input_grid != 9))
    i_noise_pixels = np.where((input_grid == 5) | (input_grid == 7) | (input_grid == 9))
    has_orange = np.any(input_grid == 7)

    # Output analysis
    o_rows, o_cols = output_grid.shape if output_grid.size > 0 else (0, 0)
    num_subgrids = o_rows // 6 if o_cols == 6 and o_rows > 0 else 0

    return {
        "input_dims": (i_rows, i_cols),
        "output_dims": (o_rows, o_cols),
        "input_bg_color": int(i_bg_color),
        "input_unique_colors": sorted(i_colors.tolist()),
        "input_non_bg_noise_coords": list(zip(i_non_bg_noise_pixels[0].tolist(), i_non_bg_noise_pixels[1].tolist())),
        "input_noise_coords": list(zip(i_noise_pixels[0].tolist(), i_noise_pixels[1].tolist())),
        "has_orange_signal": has_orange,
        "expected_num_subgrids": num_subgrids,
        "expected_output_width": o_cols
    }

# Example Data (as provided in the problem description)
train_1_in = [[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 5, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 4, 4, 2, 2, 2, 8, 8, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 4, 2, 2, 4, 2, 8, 2, 2, 8, 2, 3, 3, 2, 2, 2, 2, 2, 2], [2, 4, 2, 2, 2, 2, 4, 5, 2, 2, 2, 8, 2, 2, 3, 2, 2, 2, 2, 2], [2, 4, 2, 9, 2, 2, 4, 2, 2, 2, 3, 8, 2, 9, 2, 3, 2, 2, 2, 2], [2, 2, 4, 2, 2, 4, 2, 8, 2, 2, 8, 2, 2, 2, 2, 3, 2, 2, 2, 2], [2, 2, 2, 4, 4, 2, 2, 2, 8, 8, 2, 3, 2, 2, 3, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 5, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]]
train_1_out = [[2, 2, 4, 4, 2, 2], [2, 4, 2, 2, 4, 2], [4, 2, 2, 2, 2, 4], [4, 2, 2, 2, 2, 4], [2, 4, 2, 2, 4, 2], [2, 2, 4, 4, 2, 2], [2, 2, 8, 8, 2, 2], [2, 8, 2, 2, 8, 2], [8, 2, 2, 2, 2, 8], [8, 2, 2, 2, 2, 8], [2, 8, 2, 2, 8, 2], [2, 2, 8, 8, 2, 2], [2, 2, 3, 3, 2, 2], [2, 3, 2, 2, 3, 2], [3, 2, 2, 2, 2, 3], [3, 2, 2, 2, 2, 3], [2, 3, 2, 2, 3, 2], [2, 2, 3, 3, 2, 2]]
train_2_in = [[3, 3, 3, 3, 3, 3, 3, 3, 3, 3], [5, 3, 3, 4, 4, 3, 3, 3, 3, 3], [3, 3, 4, 3, 8, 4, 3, 3, 3, 3], [3, 4, 3, 8, 3, 3, 4, 3, 3, 3], [3, 4, 8, 1, 3, 3, 4, 8, 3, 3], [3, 1, 4, 3, 1, 4, 3, 8, 3, 3], [1, 3, 3, 4, 4, 1, 8, 3, 3, 3], [1, 3, 5, 3, 8, 8, 3, 3, 3, 3], [3, 1, 3, 3, 1, 3, 3, 3, 3, 3], [3, 3, 1, 1, 3, 3, 5, 3, 3, 3]]
train_2_out = [[3, 3, 4, 4, 3, 3], [3, 4, 3, 3, 4, 3], [4, 3, 3, 3, 3, 4], [4, 3, 3, 3, 3, 4], [3, 4, 3, 3, 4, 3], [3, 3, 4, 4, 3, 3], [3, 3, 8, 8, 3, 3], [3, 8, 3, 3, 8, 3], [8, 3, 3, 3, 3, 8], [8, 3, 3, 3, 3, 8], [3, 8, 3, 3, 8, 3], [3, 3, 8, 8, 3, 3], [3, 3, 1, 1, 3, 3], [3, 1, 3, 3, 1, 3], [1, 3, 3, 3, 3, 1], [1, 3, 3, 3, 3, 1], [3, 1, 3, 3, 1, 3], [3, 3, 1, 1, 3, 3]]
train_3_in = [[4, 4, 4, 4, 4, 5, 4, 4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 7, 4], [4, 4, 2, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4], [4, 2, 4, 4, 2, 4, 4, 4, 4, 4, 4, 4, 4], [2, 4, 4, 7, 4, 2, 4, 4, 4, 4, 4, 4, 4], [2, 4, 4, 4, 4, 8, 8, 4, 4, 5, 4, 4, 4], [4, 2, 4, 4, 8, 4, 4, 8, 4, 4, 4, 4, 4], [4, 4, 2, 8, 4, 4, 4, 4, 8, 4, 4, 4, 4], [4, 4, 4, 8, 4, 4, 4, 4, 3, 3, 4, 4, 4], [4, 4, 4, 4, 8, 4, 4, 3, 4, 4, 3, 4, 4], [4, 5, 4, 4, 4, 8, 3, 4, 4, 4, 4, 3, 4], [4, 4, 7, 4, 4, 4, 3, 4, 4, 5, 4, 3, 4], [4, 4, 4, 4, 4, 4, 4, 3, 4, 4, 3, 4, 4]]
train_3_out = [[4, 4, 3, 3, 4, 4], [4, 3, 4, 4, 3, 4], [3, 4, 4, 4, 4, 3], [3, 4, 4, 4, 4, 3], [4, 3, 4, 4, 3, 4], [4, 4, 3, 3, 4, 4], [4, 4, 8, 8, 4, 4], [4, 8, 4, 4, 8, 4], [8, 4, 4, 4, 4, 8], [8, 4, 4, 4, 4, 8], [4, 8, 4, 4, 8, 4], [4, 4, 8, 8, 4, 4], [4, 4, 2, 2, 4, 4], [4, 2, 4, 4, 2, 4], [2, 4, 4, 4, 4, 2], [2, 4, 4, 4, 4, 2], [4, 2, 4, 4, 2, 4], [4, 4, 2, 2, 4, 4]]
train_4_in = [[8, 8, 8, 8, 8, 8, 8, 8, 5, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 4, 4, 8, 3, 3, 8, 8], [8, 8, 4, 8, 8, 4, 8, 8, 3, 8], [8, 4, 2, 8, 3, 8, 4, 8, 8, 3], [8, 4, 8, 8, 3, 8, 4, 8, 8, 3], [8, 8, 4, 8, 8, 4, 8, 8, 3, 8], [8, 8, 8, 4, 4, 8, 3, 3, 8, 8], [8, 5, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 2, 8, 8]]
train_4_out = [[8, 8, 4, 4, 8, 8], [8, 4, 8, 8, 4, 8], [4, 8, 8, 8, 8, 4], [4, 8, 8, 8, 8, 4], [8, 4, 8, 8, 4, 8], [8, 8, 4, 4, 8, 8], [8, 8, 3, 3, 8, 8], [8, 3, 8, 8, 3, 8], [3, 8, 8, 8, 8, 3], [3, 8, 8, 8, 8, 3], [8, 3, 8, 8, 3, 8], [8, 8, 3, 3, 8, 8]]

results = {}
results["train_1"] = analyze_example(train_1_in, train_1_out)
results["train_2"] = analyze_example(train_2_in, train_2_out)
results["train_3"] = analyze_example(train_3_in, train_3_out)
results["train_4"] = analyze_example(train_4_in, train_4_out)

import json
print(json.dumps(results, indent=2))
```
``` failed
Traceback (most recent call last):
  File "<string>", line 49, in <module>
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
TypeError: Object of type bool is not JSON serializable

```
**Revised Metrics Gathering (Correcting JSON serialization)**

``` python
import numpy as np
from collections import Counter
import json

# Custom JSON encoder to handle numpy types
class NpEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.integer):
            return int(obj)
        if isinstance(obj, np.floating):
            return float(obj)
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        if isinstance(obj, np.bool_):
            return bool(obj)
        return super(NpEncoder, self).default(obj)

def analyze_example(input_data, output_data):
    input_grid = np.array(input_data)
    output_grid = np.array(output_data)
    
    # Input analysis
    i_rows, i_cols = input_grid.shape
    i_colors, i_counts = np.unique(input_grid, return_counts=True)
    i_bg_color = i_colors[np.argmax(i_counts)] if i_counts.size > 0 else -1 # Handle empty grid case
    i_non_bg_noise_pixels = np.where((input_grid != i_bg_color) & (input_grid != 5) & (input_grid != 7) & (input_grid != 9))
    i_noise_pixels = np.where((input_grid == 5) | (input_grid == 7) | (input_grid == 9))
    has_orange = np.any(input_grid == 7)

    # Output analysis
    o_rows, o_cols = output_grid.shape if output_grid.size > 0 else (0, 0)
    num_subgrids = o_rows // 6 if o_cols == 6 and o_rows > 0 else 0

    return {
        "input_dims": (i_rows, i_cols),
        "output_dims": (o_rows, o_cols),
        "input_bg_color": i_bg_color,
        "input_unique_colors": sorted(i_colors.tolist()),
        "input_non_bg_noise_coords_count": len(i_non_bg_noise_pixels[0]),
        "input_noise_coords_count": len(i_noise_pixels[0]),
        "has_orange_signal": has_orange,
        "expected_num_subgrids": num_subgrids,
        "expected_output_width": o_cols
    }

# Example Data (as provided in the problem description)
train_1_in = [[2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 5, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 4, 4, 2, 2, 2, 8, 8, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 4, 2, 2, 4, 2, 8, 2, 2, 8, 2, 3, 3, 2, 2, 2, 2, 2, 2], [2, 4, 2, 2, 2, 2, 4, 5, 2, 2, 2, 8, 2, 2, 3, 2, 2, 2, 2, 2], [2, 4, 2, 9, 2, 2, 4, 2, 2, 2, 3, 8, 2, 9, 2, 3, 2, 2, 2, 2], [2, 2, 4, 2, 2, 4, 2, 8, 2, 2, 8, 2, 2, 2, 2, 3, 2, 2, 2, 2], [2, 2, 2, 4, 4, 2, 2, 2, 8, 8, 2, 3, 2, 2, 3, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 3, 3, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 5, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2], [5, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2, 2]]
train_1_out = [[2, 2, 4, 4, 2, 2], [2, 4, 2, 2, 4, 2], [4, 2, 2, 2, 2, 4], [4, 2, 2, 2, 2, 4], [2, 4, 2, 2, 4, 2], [2, 2, 4, 4, 2, 2], [2, 2, 8, 8, 2, 2], [2, 8, 2, 2, 8, 2], [8, 2, 2, 2, 2, 8], [8, 2, 2, 2, 2, 8], [2, 8, 2, 2, 8, 2], [2, 2, 8, 8, 2, 2], [2, 2, 3, 3, 2, 2], [2, 3, 2, 2, 3, 2], [3, 2, 2, 2, 2, 3], [3, 2, 2, 2, 2, 3], [2, 3, 2, 2, 3, 2], [2, 2, 3, 3, 2, 2]]
train_2_in = [[3, 3, 3, 3, 3, 3, 3, 3, 3, 3], [5, 3, 3, 4, 4, 3, 3, 3, 3, 3], [3, 3, 4, 3, 8, 4, 3, 3, 3, 3], [3, 4, 3, 8, 3, 3, 4, 3, 3, 3], [3, 4, 8, 1, 3, 3, 4, 8, 3, 3], [3, 1, 4, 3, 1, 4, 3, 8, 3, 3], [1, 3, 3, 4, 4, 1, 8, 3, 3, 3], [1, 3, 5, 3, 8, 8, 3, 3, 3, 3], [3, 1, 3, 3, 1, 3, 3, 3, 3, 3], [3, 3, 1, 1, 3, 3, 5, 3, 3, 3]]
train_2_out = [[3, 3, 4, 4, 3, 3], [3, 4, 3, 3, 4, 3], [4, 3, 3, 3, 3, 4], [4, 3, 3, 3, 3, 4], [3, 4, 3, 3, 4, 3], [3, 3, 4, 4, 3, 3], [3, 3, 8, 8, 3, 3], [3, 8, 3, 3, 8, 3], [8, 3, 3, 3, 3, 8], [8, 3, 3, 3, 3, 8], [3, 8, 3, 3, 8, 3], [3, 3, 8, 8, 3, 3], [3, 3, 1, 1, 3, 3], [3, 1, 3, 3, 1, 3], [1, 3, 3, 3, 3, 1], [1, 3, 3, 3, 3, 1], [3, 1, 3, 3, 1, 3], [3, 3, 1, 1, 3, 3]]
train_3_in = [[4, 4, 4, 4, 4, 5, 4, 4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 4, 7, 4], [4, 4, 2, 2, 4, 4, 4, 4, 4, 4, 4, 4, 4], [4, 2, 4, 4, 2, 4, 4, 4, 4, 4, 4, 4, 4], [2, 4, 4, 7, 4, 2, 4, 4, 4, 4, 4, 4, 4], [2, 4, 4, 4, 4, 8, 8, 4, 4, 5, 4, 4, 4], [4, 2, 4, 4, 8, 4, 4, 8, 4, 4, 4, 4, 4], [4, 4, 2, 8, 4, 4, 4, 4, 8, 4, 4, 4, 4], [4, 4, 4, 8, 4, 4, 4, 4, 3, 3, 4, 4, 4], [4, 4, 4, 4, 8, 4, 4, 3, 4, 4, 3, 4, 4], [4, 5, 4, 4, 4, 8, 3, 4, 4, 4, 4, 3, 4], [4, 4, 7, 4, 4, 4, 3, 4, 4, 5, 4, 3, 4], [4, 4, 4, 4, 4, 4, 4, 3, 4, 4, 3, 4, 4]]
train_3_out = [[4, 4, 3, 3, 4, 4], [4, 3, 4, 4, 3, 4], [3, 4, 4, 4, 4, 3], [3, 4, 4, 4, 4, 3], [4, 3, 4, 4, 3, 4], [4, 4, 3, 3, 4, 4], [4, 4, 8, 8, 4, 4], [4, 8, 4, 4, 8, 4], [8, 4, 4, 4, 4, 8], [8, 4, 4, 4, 4, 8], [4, 8, 4, 4, 8, 4], [4, 4, 8, 8, 4, 4], [4, 4, 2, 2, 4, 4], [4, 2, 4, 4, 2, 4], [2, 4, 4, 4, 4, 2], [2, 4, 4, 4, 4, 2], [4, 2, 4, 4, 2, 4], [4, 4, 2, 2, 4, 4]]
train_4_in = [[8, 8, 8, 8, 8, 8, 8, 8, 5, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 4, 4, 8, 3, 3, 8, 8], [8, 8, 4, 8, 8, 4, 8, 8, 3, 8], [8, 4, 2, 8, 3, 8, 4, 8, 8, 3], [8, 4, 8, 8, 3, 8, 4, 8, 8, 3], [8, 8, 4, 8, 8, 4, 8, 8, 3, 8], [8, 8, 8, 4, 4, 8, 3, 3, 8, 8], [8, 5, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 2, 8, 8]]
train_4_out = [[8, 8, 4, 4, 8, 8], [8, 4, 8, 8, 4, 8], [4, 8, 8, 8, 8, 4], [4, 8, 8, 8, 8, 4], [8, 4, 8, 8, 4, 8], [8, 8, 4, 4, 8, 8], [8, 8, 3, 3, 8, 8], [8, 3, 8, 8, 3, 8], [3, 8, 8, 8, 8, 3], [3, 8, 8, 8, 8, 3], [8, 3, 8, 8, 3, 8], [8, 8, 3, 3, 8, 8]]

results = {}
results["train_1"] = analyze_example(train_1_in, train_1_out)
results["train_2"] = analyze_example(train_2_in, train_2_out)
results["train_3"] = analyze_example(train_3_in, train_3_out)
results["train_4"] = analyze_example(train_4_in, train_4_out)

print(json.dumps(results, indent=2, cls=NpEncoder))
```
```
{
  "train_1": {
    "input_dims": [
      20,
      20
    ],
    "output_dims": [
      18,
      6
    ],
    "input_bg_color": 2,
    "input_unique_colors": [
      2,
      3,
      4,
      5,
      8,
      9
    ],
    "input_non_bg_noise_coords_count": 32,
    "input_noise_coords_count": 7,
    "has_orange_signal": false,
    "expected_num_subgrids": 3,
    "expected_output_width": 6
  },
  "train_2": {
    "input_dims": [
      10,
      10
    ],
    "output_dims": [
      18,
      6
    ],
    "input_bg_color": 3,
    "input_unique_colors": [
      1,
      3,
      4,
      5,
      8
    ],
    "input_non_bg_noise_coords_count": 30,
    "input_noise_coords_count": 3,
    "has_orange_signal": false,
    "expected_num_subgrids": 3,
    "expected_output_width": 6
  },
  "train_3": {
    "input_dims": [
      13,
      13
    ],
    "output_dims": [
      18,
      6
    ],
    "input_bg_color": 4,
    "input_unique_colors": [
      2,
      3,
      4,
      5,
      7,
      8
    ],
    "input_non_bg_noise_coords_count": 28,
    "input_noise_coords_count": 7,
    "has_orange_signal": true,
    "expected_num_subgrids": 3,
    "expected_output_width": 6
  },
  "train_4": {
    "input_dims": [
      10,
      10
    ],
    "output_dims": [
      12,
      6
    ],
    "input_bg_color": 8,
    "input_unique_colors": [
      2,
      3,
      4,
      5,
      8
    ],
    "input_non_bg_noise_coords_count": 24,
    "input_noise_coords_count": 2,
    "has_orange_signal": false,
    "expected_num_subgrids": 2,
    "expected_output_width": 6
  }
}

```
**YAML Facts Block**


```yaml
task_description: Extract specific 6x6 shapes from an input grid, clean noise pixels from them, and stack them vertically in an order determined by their position and the presence of an orange signal pixel.

elements:
  - element: grid
    role: input/output container
    properties:
      - background_color: The most frequent color in the input grid. (e.g., Red=2, Green=3, Yellow=4, Azure=8)
      - dimensions: Variable for input (up to 30x30). Output width is always 6. Output height is 6 * N, where N is the number of identified shapes.

  - element: target_shape_object
    role: The primary structure to identify and extract.
    properties:
      - composition: A maximal contiguous block of one or more pixels whose colors are NOT the background color and NOT noise colors. Adjacency is defined by side-sharing (not diagonal).
      - size_constraint: The minimal bounding box containing all pixels of the object MUST be exactly 6x6 pixels.
      - location: Defined by the top-left corner (min_row, min_col) of its 6x6 bounding box in the input grid.

  - element: noise_pixel
    role: Irrelevant data or control signal.
    properties:
      - colors: [Gray (5), Orange (7), Maroon (9)]
      - location: Can appear anywhere in the input grid.
      - significance:
          - Gray (5), Maroon (9): Ignored during object identification. If located within an extracted 6x6 shape region, they are replaced by the background color in the output subgrid.
          - Orange (7): Presence *anywhere* in the input grid acts as a control signal, reversing the default stacking order of the output subgrids. Also replaced by the background color if within an extracted 6x6 region.

actions:
  - action: identify_background_color
    description: Find the most frequent pixel color in the input grid.
  - action: identify_noise_colors
    description: Define the set of noise colors {5, 7, 9}.
  - action: find_potential_objects
    description: >
      Perform a search (e.g., BFS) starting from every unvisited pixel that is not background and not noise.
      Expand the search to adjacent (up, down, left, right) pixels that are also not background and not noise, marking them as visited.
      Group all pixels visited during a single search into one potential object.
  - action: filter_objects_by_bbox
    description: >
      For each potential object found:
      1. Calculate its minimal bounding box (min_row, max_row, min_col, max_col).
      2. Check if the height (max_row - min_row + 1) is exactly 6.
      3. Check if the width (max_col - min_col + 1) is exactly 6.
      4. If both conditions are true, record the top-left corner (min_row, min_col) of this bounding box.
  - action: determine_order
    description: >
      Collect all recorded top-left corners from the filtered objects.
      Sort these corners first by row index, then by column index (top-to-bottom, left-to-right).
      Scan the original input grid for any Orange (7) pixel.
      If an Orange (7) pixel is found, reverse the sorted order of corners.
  - action: extract_clean_stack
    description: >
      Initialize an empty list for output subgrids.
      For each corner (r, c) in the final determined order:
      1. Extract the 6x6 region from the input grid starting at (r, c).
      2. Create a cleaned copy of this 6x6 region: Replace every pixel with a noise color (5, 7, or 9) with the background color.
      3. Append the cleaned 6x6 subgrid to the list.
      Vertically concatenate (stack) all subgrids in the list to create the final output grid.

relationships:
  - relation: object_defines_extraction_window
    subject: target_shape_object
    object: 6x6_subgrid
    description: The exact 6x6 bounding box of a valid target shape object defines the 6x6 window to be extracted from the input.
  - relation: noise_removal
    subject: noise_pixel
    object: extracted_6x6_subgrid
    description: Noise pixels within an extracted 6x6 subgrid are replaced by the background color.
  - relation: order_determination
    subject: target_shape_object location (top-left corner)
    object: stacking_order
    description: The relative positions (row, then column) of the top-left corners of the valid 6x6 objects determine their default stacking order.
  - relation: order_reversal_signal
    subject: Orange (7) pixel presence (anywhere in input)
    object: stacking_order
    description: The presence of any Orange (7) pixel reverses the default stacking order.
```


**Natural Language Program**

1.  Identify the single background color by finding the most frequent color in the input grid.
2.  Define the set of noise colors as Gray (5), Orange (7), and Maroon (9).
3.  Find all distinct, maximal, contiguous groups of pixels (objects) in the input grid where each pixel in the group is *neither* the background color *nor* a noise color. Use 4-way adjacency (up, down, left, right) to determine contiguity.
4.  For each object found, calculate its minimal bounding box (the smallest rectangle enclosing all its pixels).
5.  Filter these objects, keeping only those whose bounding box dimensions are exactly 6 pixels high and 6 pixels wide.
6.  Create a list containing the top-left corner coordinates (row, column) of the bounding boxes for these filtered 6x6 objects.
7.  Sort this list of coordinates. The primary sort key is the row index (ascending), and the secondary sort key is the column index (ascending). This establishes the default top-to-bottom, left-to-right order.
8.  Check the *entire original input grid* to see if it contains *any* pixel with the Orange (7) color.
9.  If an Orange (7) pixel was found anywhere in the input, reverse the order of the sorted list of coordinates.
10. Initialize an empty list to hold the final 6x6 output subgrids.
11. Iterate through the list of coordinates in their final (potentially reversed) order. For each coordinate pair (R, C):
    a.  Extract the 6x6 block of pixels from the input grid starting at row R, column C.
    b.  Create a cleaned version of this 6x6 block: Iterate through its pixels. If a pixel's color is one of the noise colors (5, 7, or 9), change its color to the background color identified in step 1. Keep all other pixels as they are.
    c.  Add this cleaned 6x6 block to the list of output subgrids.
12. Vertically stack the cleaned 6x6 blocks in the order they were added to the list. This final stacked grid is the output. If no 6x6 objects were found in step 5, the output is an empty grid.