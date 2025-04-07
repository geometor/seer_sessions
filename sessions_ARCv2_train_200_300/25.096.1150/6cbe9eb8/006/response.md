Warning: Response generation stopped. Finish Reason: FINISH_REASON_UNSPECIFIED (0)
Partial text available:
---
## General Assessment

The previous attempt failed because it incorrectly identified the area for the output grid and the rule for preservation versus replacement with zero. The core issues were:

1.  **Bounding Box Definition:** The bounding box was calculated based on *all* non-background elements, whereas the examples show the output area is defined by the bounding box of a specific "framing" shape.
2.  **Frame Identification:** The concept of "framing cells" being non-background elements on the perimeter of the *global* bounding box was incorrect. The frame is a distinct connected shape within the input.
3.  **Background Definition:** Using a fixed set like {0, 1, 2, 3} for background digits conflicts with Example 2, where '3' forms the frame. The background needs to be defined relative to the identified frame.

**Strategy for Resolution:**

1.  Implement a robust method to identify the primary "framing" shape/component in the input. The most promising heuristic seems to be the largest connected component of non-zero digits.
2.  Determine the bounding box based *only* on this identified framing component.
3.  Define background digits dynamically: 0 is always background, and {1, 2, 3} are background *unless* they are the digit making up the frame.
4.  Apply the transformation: within the frame's bounding box, replace background digits with 0, *unless* the cell is part of the frame component itself. Keep all other digits (frame digits and other non-background digits).

## Metrics and Analysis

Let's gather metrics to confirm the new strategy.


``` python
import numpy as np
from scipy import ndimage
from collections import Counter

def analyze_example(input_grid_list, output_grid_list):
    input_grid = np.array(input_grid_list, dtype=int)
    output_grid = np.array(output_grid_list, dtype=int)
    
    in_rows, in_cols = input_grid.shape
    out_rows, out_cols = output_grid.shape
    
    unique_in = sorted(list(np.unique(input_grid)))
    unique_out = sorted(list(np.unique(output_grid)))
    
    # --- Identify Frame Component (Largest non-zero component) ---
    non_zero_mask = input_grid != 0
    labeled_array, num_features = ndimage.label(non_zero_mask, structure=np.ones((3,3), dtype=bool))
    
    largest_component_size = 0
    frame_component_label = -1
    frame_digit = -1
    frame_coords = set()
    component_sizes = Counter(labeled_array.flatten())

    for label in range(1, num_features + 1):
        size = component_sizes[label]
        if size > largest_component_size:
            coords = list(zip(*np.where(labeled_array == label)))
            # Check if component has uniform digit (often true for frames)
            digits_in_comp = {input_grid[r, c] for r, c in coords}
            if len(digits_in_comp) == 1: # Assume frame has uniform digit
                 largest_component_size = size
                 frame_component_label = label
                 frame_digit = digits_in_comp.pop()
                 frame_coords = set(coords) # Use set for efficiency

    if frame_component_label == -1: # Fallback if no uniform large component? Find largest regardless.
        largest_component_size = 0
        for label in range(1, num_features + 1):
           size = component_sizes[label]
           if size > largest_component_size:
               largest_component_size = size
               frame_component_label = label
        if frame_component_label != -1:
             coords = list(zip(*np.where(labeled_array == label)))
             frame_coords = set(coords)
             # Determine frame_digit (maybe most common in coords?) - Less reliable
             digits_in_comp = [input_grid[r,c] for r,c in coords]
             if digits_in_comp:
                  frame_digit = Counter(digits_in_comp).most_common(1)[0][0]


    # --- Calculate Bounding Box of Frame Component ---
    if frame_coords:
        min_r = min(r for r, c in frame_coords)
        max_r = max(r for r, c in frame_coords)
        min_c = min(c for r, c in frame_coords)
        max_c = max(c for r, c in frame_coords)
        frame_bbox = (min_r, min_c, max_r, max_c)
        calculated_out_dims = (max_r - min_r + 1, max_c - min_c + 1)
    else:
        frame_bbox = None
        calculated_out_dims = (0, 0)
        
    # --- Determine Background Digits ---
    potential_low_bg = {1, 2, 3}
    background_digits = {0}
    if frame_digit != -1:
       background_digits.update(potential_low_bg - {frame_digit})
    else: # If no frame found, assume default background?
       background_digits.update(potential_low_bg) # Less safe

    # --- Compare with Expected Output ---
    output_dims_match = (calculated_out_dims == (out_rows, out_cols))

    return {
        "input_dims": (in_rows, in_cols),
        "output_dims": (out_rows, out_cols),
        "unique_in": unique_in,
        "unique_out": unique_out,
        "identified_frame_digit": frame_digit,
        "identified_frame_component_label": frame_component_label,
        "identified_frame_num_pixels": len(frame_coords),
        "frame_component_bbox": frame_bbox,
        "calculated_output_dims": calculated_out_dims,
        "output_dims_match_frame_bbox": output_dims_match,
        "identified_background_digits": sorted(list(background_digits))
    }

# Example Data (truncated for brevity in output)
train_1_input = [[0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1],[1,8,8,8,8,8,8,8,8,8,8,8,1,2,3,0,1,2,3,0,1,2],[0,8,2,3,0,1,2,3,0,1,2,8,0,1,2,3,0,1,2,3,0,1],[1,8,3,0,1,2,3,0,4,4,4,4,4,4,4,0,1,2,3,0,1,2],[0,8,2,3,0,1,2,3,4,5,5,5,5,5,4,3,0,1,2,3,0,1],[1,8,3,0,1,2,3,0,4,5,5,5,5,5,4,0,1,2,3,0,1,2],[0,8,2,3,0,1,2,3,4,5,5,5,5,5,4,3,0,1,2,3,0,1],[1,8,3,0,1,2,3,0,4,5,5,5,5,5,4,0,1,2,3,0,1,2],[0,8,2,3,0,1,2,3,4,4,4,4,4,4,4,3,0,6,6,3,0,1],[1,8,3,0,1,2,3,0,1,2,3,8,1,2,3,0,1,6,6,0,1,2],[0,8,2,3,0,1,2,3,0,1,2,8,0,1,2,3,0,1,2,3,0,1],[1,8,3,0,1,2,3,0,1,2,3,8,1,2,3,0,1,2,3,0,1,2],[0,8,8,8,8,8,8,8,8,8,8,8,0,1,2,3,0,1,2,3,0,1],[1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1,2]]
train_1_output = [[8,8,8,8,8,8,8,8,8,8,8],[8,0,0,0,0,0,0,0,0,0,8],[8,0,0,0,0,0,0,0,0,0,8],[8,0,0,0,0,0,0,0,0,0,8],[8,0,0,0,0,0,0,0,0,0,8],[8,4,4,4,4,4,4,4,0,0,8],[8,4,5,5,5,5,5,4,0,0,8],[8,4,5,5,5,5,5,4,0,0,8],[8,4,6,6,5,5,5,4,0,0,8],[8,4,6,6,5,5,5,4,0,0,8],[8,4,4,4,4,4,4,4,0,0,8],[8,8,8,8,8,8,8,8,8,8,8]]

train_2_input = [[0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,4,4,1,2,0,1],[1,2,0,1,2,0,1,2,0,1,2,0,1,2,8,8,8,4,4,2,0,1,2],[1,2,0,1,2,0,1,2,0,1,2,0,1,2,8,6,6,6,8,2,0,1,2],[0,1,2,0,1,3,3,3,3,3,3,3,3,3,8,6,6,6,8,1,2,0,1],[1,2,0,1,2,3,1,2,0,1,2,0,1,2,8,6,6,6,8,2,0,1,2],[1,2,0,1,2,3,1,2,0,1,2,0,1,2,8,8,8,8,8,2,0,1,2],[0,1,2,0,1,3,0,1,2,0,1,2,0,1,2,0,3,2,0,1,2,0,1],[1,2,0,1,2,3,1,2,0,1,2,0,1,2,0,1,3,0,1,2,0,1,2],[1,2,0,1,2,3,1,2,0,1,2,0,1,2,0,1,3,0,1,2,0,1,2],[0,1,2,0,1,3,0,1,2,0,1,2,0,1,2,0,3,2,0,1,2,0,1],[1,2,0,1,2,3,1,2,0,1,2,0,1,2,0,1,3,0,1,2,0,1,2],[1,2,0,1,2,3,3,3,3,3,3,3,3,3,3,3,3,0,1,2,0,1,2],[0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1]]
train_2_output = [[3,3,3,3,3,3,3,3,3,3,3,3],[3,0,0,0,0,0,0,0,0,0,0,3],[3,0,0,0,0,0,0,0,0,0,0,3],[3,8,8,8,8,8,0,0,0,0,0,3],[3,8,6,6,6,8,0,0,0,0,0,3],[3,8,4,4,6,8,0,0,0,0,0,3],[3,8,4,4,6,8,0,0,0,0,0,3],[3,8,8,8,8,8,0,0,0,0,0,3],[3,3,3,3,3,3,3,3,3,3,3,3]]

train_3_input = [[0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],[1,0,3,3,3,3,3,3,3,3,1,0,1,0,1,0,1,0,1,0,1,0,1],[0,1,3,8,8,8,8,8,8,3,0,1,0,1,0,1,0,1,0,1,0,1,0],[1,0,3,8,8,8,8,8,8,3,1,0,1,0,1,0,1,0,1,0,1,0,1],[0,1,3,8,8,8,8,8,8,3,0,1,4,4,4,1,0,1,0,1,0,1,0],[1,0,3,8,8,8,8,8,8,3,1,0,4,4,4,0,1,0,1,0,1,0,1],[0,1,3,8,8,8,8,8,8,3,0,1,4,4,4,1,0,1,0,1,0,1,0],[1,0,3,8,8,8,8,8,8,3,1,0,1,0,1,0,1,0,1,0,1,0,1],[0,1,3,3,3,3,3,3,3,3,0,1,0,1,0,1,0,1,0,1,0,1,0],[1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],[0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],[1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],[0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],[1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],[0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],[1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1]]
train_3_output = [[3,3,3,3,3,3,3,3],[3,8,8,8,8,8,8,3],[3,8,8,8,8,8,8,3],[3,8,8,8,8,8,8,3],[3,4,4,4,8,8,8,3],[3,4,4,4,8,8,8,3],[3,4,4,4,8,8,8,3],[3,3,3,3,3,3,3,3]]

results = {}
results["train_1"] = analyze_example(train_1_input, train_1_output)
results["train_2"] = analyze_example(train_2_input, train_2_output)
results["train_3"] = analyze_example(train_3_input, train_3_output)

import json
print(json.dumps(results, indent=2))
```
``` failed
Traceback (most recent call last):
  File "<string>", line 106, in <module>
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
  File "encoder.py", line 326, in _iterencode_list
    yield from chunks
  File "encoder.py", line 439, in _iterencode
    o = _default(o)
        ^^^^^^^^^^^
  File "encoder.py", line 180, in default
    raise TypeError(f'Object of type {o.__class__.__name__} '
TypeError: Object of type int64 is not JSON serializable

```
Ah, the numpy integers are causing JSON serialization issues. Let's cast them to standard Python ints.


``` python
import numpy as np
from scipy import ndimage
from collections import Counter
import json

# Helper to convert numpy types for JSON
def convert_numpy_types(obj):
    if isinstance(obj, (np.int_, np.intc, np.intp, np.int8,
                      np.int16, np.int32, np.int64, np.uint8,
                      np.uint16, np.uint32, np.uint64)):
        return int(obj)
    elif isinstance(obj, (np.float_, np.float16, np.float32, 
                      np.float64)):
        return float(obj)
    elif isinstance(obj, (np.ndarray,)): # if obj is an ndarray
        return obj.tolist() # or map(convert_numpy_types, obj) depending on what you need
    elif isinstance(obj, set):
        return list(obj) # Convert sets to lists for JSON
    elif isinstance(obj, dict):
        return {k: convert_numpy_types(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convert_numpy_types(x) for x in obj]
    return obj


def analyze_example(input_grid_list, output_grid_list):
    input_grid = np.array(input_grid_list, dtype=int)
    output_grid = np.array(output_grid_list, dtype=int)
    
    in_rows, in_cols = input_grid.shape
    out_rows, out_cols = output_grid.shape
    
    unique_in = sorted(list(np.unique(input_grid)))
    unique_out = sorted(list(np.unique(output_grid)))
    
    # --- Identify Frame Component (Largest non-zero component with uniform digit) ---
    non_zero_mask = input_grid != 0
    labeled_array, num_features = ndimage.label(non_zero_mask, structure=np.ones((3,3), dtype=bool))
    
    largest_component_size = 0
    frame_component_label = -1
    frame_digit = -1
    frame_coords = set()
    component_sizes = Counter(labeled_array.flatten())
    component_sizes.pop(0, None) # Remove background label 0 count

    candidate_labels = sorted(component_sizes, key=component_sizes.get, reverse=True)

    for label in candidate_labels: # Iterate from largest component downwards
        coords = list(zip(*np.where(labeled_array == label)))
        if not coords: continue
        
        digits_in_comp = {input_grid[r, c] for r, c in coords}
        
        # Prioritize largest *uniform* component as frame
        if len(digits_in_comp) == 1: 
            frame_component_label = label
            frame_digit = digits_in_comp.pop()
            frame_coords = set(coords)
            break # Found the best candidate

    # Fallback if no uniform component found: Use largest overall (less ideal)
    if frame_component_label == -1 and candidate_labels:
         frame_component_label = candidate_labels[0] # Largest component label
         coords = list(zip(*np.where(labeled_array == frame_component_label)))
         frame_coords = set(coords)
         # Determine frame_digit (most common in coords?)
         digits_in_comp = [input_grid[r,c] for r,c in coords]
         if digits_in_comp:
              frame_digit = Counter(digits_in_comp).most_common(1)[0][0]
         else:
             frame_digit = -1 # Should not happen if coords exist


    # --- Calculate Bounding Box of Frame Component ---
    if frame_coords:
        min_r = min(r for r, c in frame_coords)
        max_r = max(r for r, c in frame_coords)
        min_c = min(c for r, c in frame_coords)
        max_c = max(c for r, c in frame_coords)
        frame_bbox = (min_r, min_c, max_r, max_c)
        calculated_out_dims = (max_r - min_r + 1, max_c - min_c + 1)
    else:
        frame_bbox = None
        calculated_out_dims = (0, 0)
        frame_digit = -1 # Ensure frame digit is reset if no frame found
        
    # --- Determine Background Digits ---
    potential_low_bg = {1, 2, 3}
    background_digits = {0}
    if frame_digit != -1:
       # Only consider 1,2,3 background if they are NOT the frame digit
       background_digits.update(d for d in potential_low_bg if d != frame_digit and d in unique_in)
    else: 
       # If no frame identified, assume standard 1,2,3 are background if present
       background_digits.update(d for d in potential_low_bg if d in unique_in)

    # --- Compare with Expected Output ---
    output_dims_match = (calculated_out_dims == (out_rows, out_cols))

    # Convert results using helper function before returning
    return convert_numpy_types({
        "input_dims": (in_rows, in_cols),
        "output_dims": (out_rows, out_cols),
        "unique_in": unique_in,
        "unique_out": unique_out,
        "identified_frame_digit": frame_digit,
        "identified_frame_component_label": frame_component_label,
        "identified_frame_num_pixels": len(frame_coords),
        "frame_component_bbox": frame_bbox,
        "calculated_output_dims": calculated_out_dims,
        "output_dims_match_frame_bbox": output_dims_match,
        "identified_background_digits": sorted(list(background_digits))
    })

# Example Data (truncated for brevity in output)
train_1_input = [[0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1],[1,8,8,8,8,8,8,8,8,8,8,8,1,2,3,0,1,2,3,0,1,2],[0,8,2,3,0,1,2,3,0,1,2,8,0,1,2,3,0,1,2,3,0,1],[1,8,3,0,1,2,3,0,4,4,4,4,4,4,4,0,1,2,3,0,1,2],[0,8,2,3,0,1,2,3,4,5,5,5,5,5,4,3,0,1,2,3,0,1],[1,8,3,0,1,2,3,0,4,5,5,5,5,5,4,0,1,2,3,0,1,2],[0,8,2,3,0,1,2,3,4,5,5,5,5,5,4,3,0,1,2,3,0,1],[1,8,3,0,1,2,3,0,4,5,5,5,5,5,4,0,1,2,3,0,1,2],[0,8,2,3,0,1,2,3,4,4,4,4,4,4,4,3,0,6,6,3,0,1],[1,8,3,0,1,2,3,0,1,2,3,8,1,2,3,0,1,6,6,0,1,2],[0,8,2,3,0,1,2,3,0,1,2,8,0,1,2,3,0,1,2,3,0,1],[1,8,3,0,1,2,3,0,1,2,3,8,1,2,3,0,1,2,3,0,1,2],[0,8,8,8,8,8,8,8,8,8,8,8,0,1,2,3,0,1,2,3,0,1],[1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1,2]]
train_1_output = [[8,8,8,8,8,8,8,8,8,8,8],[8,0,0,0,0,0,0,0,0,0,8],[8,0,0,0,0,0,0,0,0,0,8],[8,0,0,0,0,0,0,0,0,0,8],[8,0,0,0,0,0,0,0,0,0,8],[8,4,4,4,4,4,4,4,0,0,8],[8,4,5,5,5,5,5,4,0,0,8],[8,4,5,5,5,5,5,4,0,0,8],[8,4,6,6,5,5,5,4,0,0,8],[8,4,6,6,5,5,5,4,0,0,8],[8,4,4,4,4,4,4,4,0,0,8],[8,8,8,8,8,8,8,8,8,8,8]]

train_2_input = [[0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,4,4,1,2,0,1],[1,2,0,1,2,0,1,2,0,1,2,0,1,2,8,8,8,4,4,2,0,1,2],[1,2,0,1,2,0,1,2,0,1,2,0,1,2,8,6,6,6,8,2,0,1,2],[0,1,2,0,1,3,3,3,3,3,3,3,3,3,8,6,6,6,8,1,2,0,1],[1,2,0,1,2,3,1,2,0,1,2,0,1,2,8,6,6,6,8,2,0,1,2],[1,2,0,1,2,3,1,2,0,1,2,0,1,2,8,8,8,8,8,2,0,1,2],[0,1,2,0,1,3,0,1,2,0,1,2,0,1,2,0,3,2,0,1,2,0,1],[1,2,0,1,2,3,1,2,0,1,2,0,1,2,0,1,3,0,1,2,0,1,2],[1,2,0,1,2,3,1,2,0,1,2,0,1,2,0,1,3,0,1,2,0,1,2],[0,1,2,0,1,3,0,1,2,0,1,2,0,1,2,0,3,2,0,1,2,0,1],[1,2,0,1,2,3,1,2,0,1,2,0,1,2,0,1,3,0,1,2,0,1,2],[1,2,0,1,2,3,3,3,3,3,3,3,3,3,3,3,3,0,1,2,0,1,2],[0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1]]
train_2_output = [[3,3,3,3,3,3,3,3,3,3,3,3],[3,0,0,0,0,0,0,0,0,0,0,3],[3,0,0,0,0,0,0,0,0,0,0,3],[3,8,8,8,8,8,0,0,0,0,0,3],[3,8,6,6,6,8,0,0,0,0,0,3],[3,8,4,4,6,8,0,0,0,0,0,3],[3,8,4,4,6,8,0,0,0,0,0,3],[3,8,8,8,8,8,0,0,0,0,0,3],[3,3,3,3,3,3,3,3,3,3,3,3]]

train_3_input = [[0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],[1,0,3,3,3,3,3,3,3,3,1,0,1,0,1,0,1,0,1,0,1,0,1],[0,1,3,8,8,8,8,8,8,3,0,1,0,1,0,1,0,1,0,1,0,1,0],[1,0,3,8,8,8,8,8,8,3,1,0,1,0,1,0,1,0,1,0,1,0,1],[0,1,3,8,8,8,8,8,8,3,0,1,4,4,4,1,0,1,0,1,0,1,0],[1,0,3,8,8,8,8,8,8,3,1,0,4,4,4,0,1,0,1,0,1,0,1],[0,1,3,8,8,8,8,8,8,3,0,1,4,4,4,1,0,1,0,1,0,1,0],[1,0,3,8,8,8,8,8,8,3,1,0,1,0,1,0,1,0,1,0,1,0,1],[0,1,3,3,3,3,3,3,3,3,0,1,0,1,0,1,0,1,0,1,0,1,0],[1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],[0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],[1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],[0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],[1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],[0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],[1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1]]
train_3_output = [[3,3,3,3,3,3,3,3],[3,8,8,8,8,8,8,3],[3,8,8,8,8,8,8,3],[3,8,8,8,8,8,8,3],[3,4,4,4,8,8,8,3],[3,4,4,4,8,8,8,3],[3,4,4,4,8,8,8,3],[3,3,3,3,3,3,3,3]]

results = {}
results["train_1"] = analyze_example(train_1_input, train_1_output)
results["train_2"] = analyze_example(train_2_input, train_2_output)
results["train_3"] = analyze_example(train_3_input, train_3_output)

# Convert the entire results dict using the helper
results_converted = convert_numpy_types(results)

print(json.dumps(results_converted, indent=2))
```
``` failed
Traceback (most recent call last):
  File "<string>", line 127, in <module>
  File "<string>", line 102, in analyze_example
  File "<string>", line 12, in convert_numpy_types
  File "__init__.py", line 400, in __getattr__
    raise AttributeError(
AttributeError: `np.float_` was removed in the NumPy 2.0 release. Use `np.float64` instead.

```
Okay, numpy 2.0 removed `np.float_`. Updating the type checking.


``` python
import numpy as np
from scipy import ndimage
from collections import Counter
import json

# Helper to convert numpy types for JSON (updated for NumPy 2.0)
def convert_numpy_types(obj):
    if isinstance(obj, (np.integer)): # Generic integer check
        return int(obj)
    elif isinstance(obj, (np.floating)): # Generic float check
        return float(obj)
    elif isinstance(obj, (np.ndarray,)): # if obj is an ndarray
        return obj.tolist() 
    elif isinstance(obj, set):
        return sorted(list(obj)) # Convert sets to sorted lists for consistent JSON
    elif isinstance(obj, dict):
        return {k: convert_numpy_types(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convert_numpy_types(x) for x in obj]
    return obj


def analyze_example(input_grid_list, output_grid_list):
    input_grid = np.array(input_grid_list, dtype=int)
    output_grid = np.array(output_grid_list, dtype=int)
    
    in_rows, in_cols = input_grid.shape
    out_rows, out_cols = output_grid.shape
    
    unique_in = sorted(list(np.unique(input_grid)))
    unique_out = sorted(list(np.unique(output_grid)))
    
    # --- Identify Frame Component (Largest non-zero component with uniform digit) ---
    non_zero_mask = input_grid != 0
    labeled_array, num_features = ndimage.label(non_zero_mask, structure=np.ones((3,3), dtype=bool))
    
    largest_component_size = 0
    frame_component_label = -1
    frame_digit = -1
    frame_coords = set()
    component_sizes = Counter(labeled_array.flatten())
    component_sizes.pop(0, None) # Remove background label 0 count

    candidate_labels = sorted(component_sizes, key=component_sizes.get, reverse=True)

    for label in candidate_labels: # Iterate from largest component downwards
        coords = list(zip(*np.where(labeled_array == label)))
        if not coords: continue
        
        digits_in_comp = {input_grid[r, c] for r, c in coords}
        
        # Prioritize largest *uniform* component as frame
        if len(digits_in_comp) == 1: 
            frame_component_label = label
            frame_digit = digits_in_comp.pop()
            frame_coords = set(coords)
            break # Found the best candidate

    # Fallback if no uniform component found: Use largest overall (less ideal)
    if frame_component_label == -1 and candidate_labels:
         frame_component_label = candidate_labels[0] # Largest component label
         coords = list(zip(*np.where(labeled_array == frame_component_label)))
         frame_coords = set(coords)
         # Determine frame_digit (most common in coords?)
         digits_in_comp = [input_grid[r,c] for r,c in coords]
         if digits_in_comp:
              frame_digit = Counter(digits_in_comp).most_common(1)[0][0]
         else:
             frame_digit = -1 # Should not happen if coords exist


    # --- Calculate Bounding Box of Frame Component ---
    if frame_coords:
        min_r = min(r for r, c in frame_coords)
        max_r = max(r for r, c in frame_coords)
        min_c = min(c for r, c in frame_coords)
        max_c = max(c for r, c in frame_coords)
        frame_bbox = (min_r, min_c, max_r, max_c)
        calculated_out_dims = (max_r - min_r + 1, max_c - min_c + 1)
    else:
        frame_bbox = None
        calculated_out_dims = (0, 0)
        frame_digit = -1 # Ensure frame digit is reset if no frame found
        
    # --- Determine Background Digits ---
    potential_low_bg = {1, 2, 3}
    background_digits = {0}
    if frame_digit != -1:
       # Only consider 1,2,3 background if they are NOT the frame digit
       background_digits.update(d for d in potential_low_bg if d != frame_digit and d in unique_in)
    else: 
       # If no frame identified, assume standard 1,2,3 are background if present
       background_digits.update(d for d in potential_low_bg if d in unique_in)

    # --- Compare with Expected Output ---
    output_dims_match = (calculated_out_dims == (out_rows, out_cols))

    # Convert results using helper function before returning
    return convert_numpy_types({
        "input_dims": (in_rows, in_cols),
        "output_dims": (out_rows, out_cols),
        "unique_in": unique_in,
        "unique_out": unique_out,
        "identified_frame_digit": frame_digit,
        "identified_frame_component_label": frame_component_label,
        "identified_frame_num_pixels": len(frame_coords),
        "frame_component_bbox": frame_bbox,
        "calculated_output_dims": calculated_out_dims,
        "output_dims_match_frame_bbox": output_dims_match,
        "identified_background_digits": sorted(list(background_digits)) # Sort for consistent output
    })

# Example Data (truncated for brevity in output)
train_1_input = [[0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1],[1,8,8,8,8,8,8,8,8,8,8,8,1,2,3,0,1,2,3,0,1,2],[0,8,2,3,0,1,2,3,0,1,2,8,0,1,2,3,0,1,2,3,0,1],[1,8,3,0,1,2,3,0,4,4,4,4,4,4,4,0,1,2,3,0,1,2],[0,8,2,3,0,1,2,3,4,5,5,5,5,5,4,3,0,1,2,3,0,1],[1,8,3,0,1,2,3,0,4,5,5,5,5,5,4,0,1,2,3,0,1,2],[0,8,2,3,0,1,2,3,4,5,5,5,5,5,4,3,0,1,2,3,0,1],[1,8,3,0,1,2,3,0,4,5,5,5,5,5,4,0,1,2,3,0,1,2],[0,8,2,3,0,1,2,3,4,4,4,4,4,4,4,3,0,6,6,3,0,1],[1,8,3,0,1,2,3,0,1,2,3,8,1,2,3,0,1,6,6,0,1,2],[0,8,2,3,0,1,2,3,0,1,2,8,0,1,2,3,0,1,2,3,0,1],[1,8,3,0,1,2,3,0,1,2,3,8,1,2,3,0,1,2,3,0,1,2],[0,8,8,8,8,8,8,8,8,8,8,8,0,1,2,3,0,1,2,3,0,1],[1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1,2]]
train_1_output = [[8,8,8,8,8,8,8,8,8,8,8],[8,0,0,0,0,0,0,0,0,0,8],[8,0,0,0,0,0,0,0,0,0,8],[8,0,0,0,0,0,0,0,0,0,8],[8,0,0,0,0,0,0,0,0,0,8],[8,4,4,4,4,4,4,4,0,0,8],[8,4,5,5,5,5,5,4,0,0,8],[8,4,5,5,5,5,5,4,0,0,8],[8,4,6,6,5,5,5,4,0,0,8],[8,4,6,6,5,5,5,4,0,0,8],[8,4,4,4,4,4,4,4,0,0,8],[8,8,8,8,8,8,8,8,8,8,8]]

train_2_input = [[0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,4,4,1,2,0,1],[1,2,0,1,2,0,1,2,0,1,2,0,1,2,8,8,8,4,4,2,0,1,2],[1,2,0,1,2,0,1,2,0,1,2,0,1,2,8,6,6,6,8,2,0,1,2],[0,1,2,0,1,3,3,3,3,3,3,3,3,3,8,6,6,6,8,1,2,0,1],[1,2,0,1,2,3,1,2,0,1,2,0,1,2,8,6,6,6,8,2,0,1,2],[1,2,0,1,2,3,1,2,0,1,2,0,1,2,8,8,8,8,8,2,0,1,2],[0,1,2,0,1,3,0,1,2,0,1,2,0,1,2,0,3,2,0,1,2,0,1],[1,2,0,1,2,3,1,2,0,1,2,0,1,2,0,1,3,0,1,2,0,1,2],[1,2,0,1,2,3,1,2,0,1,2,0,1,2,0,1,3,0,1,2,0,1,2],[0,1,2,0,1,3,0,1,2,0,1,2,0,1,2,0,3,2,0,1,2,0,1],[1,2,0,1,2,3,1,2,0,1,2,0,1,2,0,1,3,0,1,2,0,1,2],[1,2,0,1,2,3,3,3,3,3,3,3,3,3,3,3,3,0,1,2,0,1,2],[0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1]]
train_2_output = [[3,3,3,3,3,3,3,3,3,3,3,3],[3,0,0,0,0,0,0,0,0,0,0,3],[3,0,0,0,0,0,0,0,0,0,0,3],[3,8,8,8,8,8,0,0,0,0,0,3],[3,8,6,6,6,8,0,0,0,0,0,3],[3,8,4,4,6,8,0,0,0,0,0,3],[3,8,4,4,6,8,0,0,0,0,0,3],[3,8,8,8,8,8,0,0,0,0,0,3],[3,3,3,3,3,3,3,3,3,3,3,3]]

train_3_input = [[0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],[1,0,3,3,3,3,3,3,3,3,1,0,1,0,1,0,1,0,1,0,1,0,1],[0,1,3,8,8,8,8,8,8,3,0,1,0,1,0,1,0,1,0,1,0,1,0],[1,0,3,8,8,8,8,8,8,3,1,0,1,0,1,0,1,0,1,0,1,0,1],[0,1,3,8,8,8,8,8,8,3,0,1,4,4,4,1,0,1,0,1,0,1,0],[1,0,3,8,8,8,8,8,8,3,1,0,4,4,4,0,1,0,1,0,1,0,1],[0,1,3,8,8,8,8,8,8,3,0,1,4,4,4,1,0,1,0,1,0,1,0],[1,0,3,8,8,8,8,8,8,3,1,0,1,0,1,0,1,0,1,0,1,0,1],[0,1,3,3,3,3,3,3,3,3,0,1,0,1,0,1,0,1,0,1,0,1,0],[1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],[0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],[1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],[0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],[1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],[0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],[1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1]]
train_3_output = [[3,3,3,3,3,3,3,3],[3,8,8,8,8,8,8,3],[3,8,8,8,8,8,8,3],[3,8,8,8,8,8,8,3],[3,4,4,4,8,8,8,3],[3,4,4,4,8,8,8,3],[3,4,4,4,8,8,8,3],[3,3,3,3,3,3,3,3]]

results = {}
results["train_1"] = analyze_example(train_1_input, train_1_output)
results["train_2"] = analyze_example(train_2_input, train_2_output)
results["train_3"] = analyze_example(train_3_input, train_3_output)

# Convert the entire results dict using the helper
results_converted = convert_numpy_types(results)

print(json.dumps(results_converted, indent=2))
```
```
{
  "train_1": {
    "input_dims": [
      14,
      22
    ],
    "output_dims": [
      12,
      11
    ],
    "unique_in": [
      0,
      1,
      2,
      3,
      4,
      5,
      6,
      8
    ],
    "unique_out": [
      0,
      4,
      5,
      6,
      8
    ],
    "identified_frame_digit": 1,
    "identified_frame_component_label": 1,
    "identified_frame_num_pixels": 247,
    "frame_component_bbox": [
      0,
      0,
      13,
      21
    ],
    "calculated_output_dims": [
      14,
      22
    ],
    "output_dims_match_frame_bbox": false,
    "identified_background_digits": [
      0,
      2,
      3
    ]
  },
  "train_2": {
    "input_dims": [
      13,
      23
    ],
    "output_dims": [
      9,
      12
    ],
    "unique_in": [
      0,
      1,
      2,
      3,
      4,
      6,
      8
    ],
    "unique_out": [
      0,
      3,
      4,
      6,
      8
    ],
    "identified_frame_digit": 1,
    "identified_frame_component_label": 1,
    "identified_frame_num_pixels": 226,
    "frame_component_bbox": [
      0,
      0,
      12,
      22
    ],
    "calculated_output_dims": [
      13,
      23
    ],
    "output_dims_match_frame_bbox": false,
    "identified_background_digits": [
      0,
      2,
      3
    ]
  },
  "train_3": {
    "input_dims": [
      16,
      23
    ],
    "output_dims": [
      8,
      8
    ],
    "unique_in": [
      0,
      1,
      3,
      4,
      8
    ],
    "unique_out": [
      3,
      4,
      8
    ],
    "identified_frame_digit": 1,
    "identified_frame_component_label": 1,
    "identified_frame_num_pixels": 221,
    "frame_component_bbox": [
      0,
      0,
      15,
      22
    ],
    "calculated_output_dims": [
      16,
      23
    ],
    "output_dims_match_frame_bbox": false,
    "identified_background_digits": [
      0,
      3
    ]
  }
}

```
The metrics calculation seems flawed. The `ndimage.label` on `non_zero_mask` is creating one giant component for *all* non-zero digits combined, including the background digits 1, 2, 3. This is not correctly identifying distinct objects. The frame digit is consistently identified as '1' because '1' is present everywhere and connects all other non-zero elements.

Let's redefine "objects" as connected components of digits *not* in the set {0, 1, 2, 3}. Then find the largest of *these* components.

**Revised Metrics Calculation Plan:**

1.  Define potential background digits P = {0, 1, 2, 3}.
2.  Create a mask where input grid digits are NOT in P.
3.  Find connected components on *this* mask. These are the "non-background objects".
4.  Find the largest component among these objects (by pixel count). This is the likely frame. Record its digit (`frame_digit`) and coordinates (`frame_coords`).
5.  Calculate the bounding box of `frame_coords`. Check if its dimensions match the output dimensions.
6.  Define the actual background digits B = {0} union {d in {1, 2, 3} where d != frame_digit}.
7.  Report the findings.


``` python
import numpy as np
from scipy import ndimage
from collections import Counter
import json

# Helper to convert numpy types for JSON (updated for NumPy 2.0)
def convert_numpy_types(obj):
    if isinstance(obj, (np.integer)): # Generic integer check
        return int(obj)
    elif isinstance(obj, (np.floating)): # Generic float check
        return float(obj)
    elif isinstance(obj, (np.ndarray,)): # if obj is an ndarray
        return obj.tolist() 
    elif isinstance(obj, set):
        return sorted(list(obj)) # Convert sets to sorted lists for consistent JSON
    elif isinstance(obj, dict):
        return {k: convert_numpy_types(v) for k, v in obj.items()}
    elif isinstance(obj, (list, tuple)):
        return [convert_numpy_types(x) for x in obj]
    return obj

def analyze_example(input_grid_list, output_grid_list):
    input_grid = np.array(input_grid_list, dtype=int)
    output_grid = np.array(output_grid_list, dtype=int)
    
    in_rows, in_cols = input_grid.shape
    out_rows, out_cols = output_grid.shape
    
    unique_in = sorted(list(np.unique(input_grid)))
    unique_out = sorted(list(np.unique(output_grid)))
    
    # --- Identify Non-Background Objects ---
    potential_bg_digits = {0, 1, 2, 3}
    # Mask is True for digits NOT in potential_bg_digits
    object_mask = np.isin(input_grid, list(potential_bg_digits), invert=True) 
    
    labeled_array, num_features = ndimage.label(object_mask, structure=np.ones((3,3), dtype=bool))
    
    largest_component_size = 0
    frame_component_label = -1
    frame_digit = -1
    frame_coords = set()
    component_sizes = Counter(labeled_array.flatten())
    component_sizes.pop(0, None) # Remove background label 0 count

    candidate_labels = sorted(component_sizes, key=component_sizes.get, reverse=True)

    # Find the largest component formed by non-background digits
    if candidate_labels:
        frame_component_label = candidate_labels[0] # Label of the largest object
        coords = list(zip(*np.where(labeled_array == frame_component_label)))
        frame_coords = set(coords)
        # Determine the digit of this component (assuming it's uniform, take first coord)
        if frame_coords:
            first_coord = next(iter(frame_coords))
            frame_digit = input_grid[first_coord] 
            # Verify uniformity (optional but good check)
            digits_in_comp = {input_grid[r, c] for r, c in frame_coords}
            if len(digits_in_comp) > 1:
                 # If largest component is not uniform, the heuristic might be wrong
                 # For now, we'll stick with the digit from the first coord, but note this potential issue.
                 print(f"Warning: Largest object (label {frame_component_label}) is not uniform: {digits_in_comp}. Using {frame_digit}.")
        else:
             frame_digit = -1 # Should not happen
    else:
        # No objects found based on initial non-bg definition.
        # This might happen if the frame IS made of 1, 2, or 3.
        # Let's add a fallback for this case - check Ex2 & 3 where frame is 3.
        # Fallback: Find largest *uniform* component among ALL non-zero digits
        print("Initial object finding failed (no digits outside {0,1,2,3}). Trying fallback: largest uniform non-zero component.")
        non_zero_mask = input_grid != 0
        labeled_array_nz, num_features_nz = ndimage.label(non_zero_mask, structure=np.ones((3,3), dtype=bool))
        component_sizes_nz = Counter(labeled_array_nz.flatten())
        component_sizes_nz.pop(0, None)
        candidate_labels_nz = sorted(component_sizes_nz, key=component_sizes_nz.get, reverse=True)
        
        for label in candidate_labels_nz:
             coords = list(zip(*np.where(labeled_array_nz == label)))
             if not coords: continue
             digits_in_comp = {input_grid[r, c] for r, c in coords}
             if len(digits_in_comp) == 1: # Found largest uniform component
                  frame_component_label = label # Use label from this labeling
                  frame_digit = digits_in_comp.pop()
                  frame_coords = set(coords)
                  print(f"Fallback success: Found uniform component of digit {frame_digit}")
                  break # Stop after finding the largest uniform one
        if frame_digit == -1:
            print("Fallback failed: No suitable frame component found.")


    # --- Calculate Bounding Box of Frame Component ---
    if frame_coords:
        min_r = min(r for r, c in frame_coords)
        max_r = max(r for r, c in frame_coords)
        min_c = min(c for r, c in frame_coords)
        max_c = max(c for r, c in frame_coords)
        frame_bbox = (min_r, min_c, max_r, max_c)
        calculated_out_dims = (max_r - min_r + 1, max_c - min_c + 1)
    else:
        frame_bbox = None
        calculated_out_dims = (0, 0)
        frame_digit = -1 # Ensure frame digit is reset if no frame found
        
    # --- Determine Background Digits ---
    # Background = 0 + {1, 2, 3} that are NOT the frame digit
    background_digits = {0}
    present_low_digits = potential_bg_digits.intersection(unique_in) - {0} # {1,2,3} present in input
    
    if frame_digit != -1:
       background_digits.update(d for d in present_low_digits if d != frame_digit)
    else: 
       # If no frame identified, assume all present low digits (1,2,3) are background
       background_digits.update(present_low_digits)

    # --- Compare with Expected Output ---
    output_dims_match = (calculated_out_dims == (out_rows, out_cols))

    # Convert results using helper function before returning
    return convert_numpy_types({
        "input_dims": (in_rows, in_cols),
        "output_dims": (out_rows, out_cols),
        "unique_in": unique_in,
        "unique_out": unique_out,
        "identified_frame_digit": frame_digit,
       # "identified_frame_component_label": frame_component_label, # Label can differ depending on method used
        "identified_frame_num_pixels": len(frame_coords),
        "frame_component_bbox": frame_bbox,
        "calculated_output_dims": calculated_out_dims,
        "output_dims_match_frame_bbox": output_dims_match,
        "identified_background_digits": sorted(list(background_digits)) # Sort for consistent output
    })

# Example Data (as before)
train_1_input = [[0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1],[1,8,8,8,8,8,8,8,8,8,8,8,1,2,3,0,1,2,3,0,1,2],[0,8,2,3,0,1,2,3,0,1,2,8,0,1,2,3,0,1,2,3,0,1],[1,8,3,0,1,2,3,0,4,4,4,4,4,4,4,0,1,2,3,0,1,2],[0,8,2,3,0,1,2,3,4,5,5,5,5,5,4,3,0,1,2,3,0,1],[1,8,3,0,1,2,3,0,4,5,5,5,5,5,4,0,1,2,3,0,1,2],[0,8,2,3,0,1,2,3,4,5,5,5,5,5,4,3,0,1,2,3,0,1],[1,8,3,0,1,2,3,0,4,5,5,5,5,5,4,0,1,2,3,0,1,2],[0,8,2,3,0,1,2,3,4,4,4,4,4,4,4,3,0,6,6,3,0,1],[1,8,3,0,1,2,3,0,1,2,3,8,1,2,3,0,1,6,6,0,1,2],[0,8,2,3,0,1,2,3,0,1,2,8,0,1,2,3,0,1,2,3,0,1],[1,8,3,0,1,2,3,0,1,2,3,8,1,2,3,0,1,2,3,0,1,2],[0,8,8,8,8,8,8,8,8,8,8,8,0,1,2,3,0,1,2,3,0,1],[1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1,2]]
train_1_output = [[8,8,8,8,8,8,8,8,8,8,8],[8,0,0,0,0,0,0,0,0,0,8],[8,0,0,0,0,0,0,0,0,0,8],[8,0,0,0,0,0,0,0,0,0,8],[8,0,0,0,0,0,0,0,0,0,8],[8,4,4,4,4,4,4,4,0,0,8],[8,4,5,5,5,5,5,4,0,0,8],[8,4,5,5,5,5,5,4,0,0,8],[8,4,6,6,5,5,5,4,0,0,8],[8,4,6,6,5,5,5,4,0,0,8],[8,4,4,4,4,4,4,4,0,0,8],[8,8,8,8,8,8,8,8,8,8,8]]
train_2_input = [[0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,4,4,1,2,0,1],[1,2,0,1,2,0,1,2,0,1,2,0,1,2,8,8,8,4,4,2,0,1,2],[1,2,0,1,2,0,1,2,0,1,2,0,1,2,8,6,6,6,8,2,0,1,2],[0,1,2,0,1,3,3,3,3,3,3,3,3,3,8,6,6,6,8,1,2,0,1],[1,2,0,1,2,3,1,2,0,1,2,0,1,2,8,6,6,6,8,2,0,1,2],[1,2,0,1,2,3,1,2,0,1,2,0,1,2,8,8,8,8,8,2,0,1,2],[0,1,2,0,1,3,0,1,2,0,1,2,0,1,2,0,3,2,0,1,2,0,1],[1,2,0,1,2,3,1,2,0,1,2,0,1,2,0,1,3,0,1,2,0,1,2],[1,2,0,1,2,3,1,2,0,1,2,0,1,2,0,1,3,0,1,2,0,1,2],[0,1,2,0,1,3,0,1,2,0,1,2,0,1,2,0,3,2,0,1,2,0,1],[1,2,0,1,2,3,1,2,0,1,2,0,1,2,0,1,3,0,1,2,0,1,2],[1,2,0,1,2,3,3,3,3,3,3,3,3,3,3,3,3,0,1,2,0,1,2],[0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1]]
train_2_output = [[3,3,3,3,3,3,3,3,3,3,3,3],[3,0,0,0,0,0,0,0,0,0,0,3],[3,0,0,0,0,0,0,0,0,0,0,3],[3,8,8,8,8,8,0,0,0,0,0,3],[3,8,6,6,6,8,0,0,0,0,0,3],[3,8,4,4,6,8,0,0,0,0,0,3],[3,8,4,4,6,8,0,0,0,0,0,3],[3,8,8,8,8,8,0,0,0,0,0,3],[3,3,3,3,3,3,3,3,3,3,3,3]]
train_3_input = [[0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],[1,0,3,3,3,3,3,3,3,3,1,0,1,0,1,0,1,0,1,0,1,0,1],[0,1,3,8,8,8,8,8,8,3,0,1,0,1,0,1,0,1,0,1,0,1,0],[1,0,3,8,8,8,8,8,8,3,1,0,1,0,1,0,1,0,1,0,1,0,1],[0,1,3,8,8,8,8,8,8,3,0,1,4,4,4,1,0,1,0,1,0,1,0],[1,0,3,8,8,8,8,8,8,3,1,0,4,4,4,0,1,0,1,0,1,0,1],[0,1,3,8,8,8,8,8,8,3,0,1,4,4,4,1,0,1,0,1,0,1,0],[1,0,3,8,8,8,8,8,8,3,1,0,1,0,1,0,1,0,1,0,1,0,1],[0,1,3,3,3,3,3,3,3,3,0,1,0,1,0,1,0,1,0,1,0,1,0],[1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],[0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],[1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],[0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],[1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],[0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],[1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1]]
train_3_output = [[3,3,3,3,3,3,3,3],[3,8,8,8,8,8,8,3],[3,8,8,8,8,8,8,3],[3,8,8,8,8,8,8,3],[3,4,4,4,8,8,8,3],[3,4,4,4,8,8,8,3],[3,4,4,4,8,8,8,3],[3,3,3,3,3,3,3,3]]

results = {}
results["train_1"] = analyze_example(train_1_input, train_1_output)
results["train_2"] = analyze_example(train_2_input, train_2_output)
results["train_3"] = analyze_example(train_3_input, train_3_output)

# Convert the entire results dict using the helper
results_converted = convert_numpy_types(results)

print(json.dumps(results_converted, indent=2))
```
```
Warning: Largest object (label 1) is not uniform: {np.int64(8), np.int64(4), np.int64(5)}. Using 8.
Warning: Largest object (label 1) is not uniform: {np.int64(8), np.int64(4), np.int64(6)}. Using 6.
{
  "train_1": {
    "input_dims": [
      14,
      22
    ],
    "output_dims": [
      12,
      11
    ],
    "unique_in": [
      0,
      1,
      2,
      3,
      4,
      5,
      6,
      8
    ],
    "unique_out": [
      0,
      4,
      5,
      6,
      8
    ],
    "identified_frame_digit": 8,
    "identified_frame_num_pixels": 78,
    "frame_component_bbox": [
      1,
      1,
      12,
      14
    ],
    "calculated_output_dims": [
      12,
      14
    ],
    "output_dims_match_frame_bbox": false,
    "identified_background_digits": [
      0,
      1,
      2,
      3
    ]
  },
  "train_2": {
    "input_dims": [
      13,
      23
    ],
    "output_dims": [
      9,
      12
    ],
    "unique_in": [
      0,
      1,
      2,
      3,
      4,
      6,
      8
    ],
    "unique_out": [
      0,
      3,
      4,
      6,
      8
    ],
    "identified_frame_digit": 6,
    "identified_frame_num_pixels": 27,
    "frame_component_bbox": [
      0,
      14,
      5,
      18
    ],
    "calculated_output_dims": [
      6,
      5
    ],
    "output_dims_match_frame_bbox": false,
    "identified_background_digits": [
      0,
      1,
      2,
      3
    ]
  },
  "train_3": {
    "input_dims": [
      16,
      23
    ],
    "output_dims": [
      8,
      8
    ],
    "unique_in": [
      0,
      1,
      3,
      4,
      8
    ],
    "unique_out": [
      3,
      4,
      8
    ],
    "identified_frame_digit": 8,
    "identified_frame_num_pixels": 36,
    "frame_component_bbox": [
      2,
      3,
      7,
      8
    ],
    "calculated_output_dims": [
      6,
      6
    ],
    "output_dims_match_frame_bbox": false,
    "identified_background_digits": [
      0,
      1,
      3
    ]
  }
}

```
---
