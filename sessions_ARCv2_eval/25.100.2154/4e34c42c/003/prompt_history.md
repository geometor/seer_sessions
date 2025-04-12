
## train_1

**input:**
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 9 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 1 1 8 8 2 8 2 3 3 3 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 4 1 1 1 2 2 2 3 2 3 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 1 1 8 8 2 8 2 3 3 3 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 9 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 6 8 9 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 6 1 1 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 6 1 4 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 6 1 1 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 6 8 9 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 3 3 3 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 3 2 3 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 3 3 3 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```


**output:**
```
6 8 9 8 8 8 8 8 8 8 8 8
6 1 1 1 8 8 2 8 2 3 3 3
6 1 4 1 1 1 2 2 2 3 2 3
6 1 1 1 8 8 2 8 2 3 3 3
6 8 9 8 8 8 8 8 8 8 8 8
```

Okay, analyzing the first example pair.

**Initial Perception:**

The input is a large grid primarily filled with the digit '8', which appears to be a background color. Scattered within this background are three distinct "objects" or clusters formed by other digits (1, 2, 3, 4, 6, 9). Two of these objects (one located roughly top-center, the other middle-right) seem to share a common height (5 rows), while the third object (bottom-left) has a different height (3 rows).

The output is a smaller grid. Its content strongly resembles a combination of the two input objects that share the same height (5 rows). Specifically, it looks like the rightmost 5-row-high object is placed first, followed by a modified version (missing the first column) of the leftmost 5-row-high object. The 3-row-high object seems to be ignored in the transformation.

**Observed Facts (YAML):**

```yaml
task_type: grid_transformation
input_properties:
  - grid_representation: matrix of digits
  - background_digit: 8
  - foreground_elements: clusters of non-8 digits
objects:
  - id: C1 # Cluster 1 (leftmost, 5-high)
    location: roughly rows 6-10, cols 6-15
    height: 5
    width: 10 # Based on bounding box of non-8s
    content: subgrid containing digits 1, 2, 3, 4, 9 and background 8s
    bounding_box: rows 6-10, cols 6-15
  - id: C2 # Cluster 2 (rightmost, 5-high)
    location: roughly rows 11-15, cols 20-22
    height: 5
    width: 3 # Based on bounding box of non-8s
    content: subgrid containing digits 1, 4, 6, 9 and background 8s
    bounding_box: rows 11-15, cols 20-22
  - id: C3 # Cluster 3 (ignored?)
    location: roughly rows 18-20, cols 3-5
    height: 3
    width: 3
    content: subgrid containing digits 2, 3
    bounding_box: rows 18-20, cols 3-5
relationships:
  - type: height_match
    objects: [C1, C2]
    value: 5
  - type: relative_horizontal_position
    objects: [C1, C2]
    relation: C1 is to the left of C2 (based on min column index)
output_properties:
  - grid_representation: matrix of digits
  - dimensions: 5 rows, 12 columns (matches height of C1/C2, width is width(C2) + width(C1) - 1)
  - content_origin: derived from C1 and C2
transformation:
  - action: identify_objects
    criteria: connected components of non-background (non-8) digits
  - action: filter_objects
    criteria: select objects with matching height (height=5 in this case), resulting in C1 and C2
  - action: order_objects
    criteria: horizontal position (min column index), C1 (left), C2 (right)
  - action: extract_content
    source: C1 -> Content_Left
    source: C2 -> Content_Right
  - action: slice_content
    source: Content_Left
    operation: remove first column -> Sliced_Content_Left
  - action: concatenate_content
    part1: Content_Right
    part2: Sliced_Content_Left
    axis: horizontal
    result: output grid
```

**Natural Language Program:**

1.  Identify the background digit ('8').
2.  Find all distinct connected groups (objects) of non-background digits in the input grid.
3.  Determine the bounding box and height for each object.
4.  Find the height value `H` that is shared by exactly two objects.
5.  Select the two objects (Object_A, Object_B) that have height `H`.
6.  Identify which object is horizontally positioned to the left (Object_Left) and which is to the right (Object_Right) based on their minimum column indices.
7.  Extract the subgrid corresponding to the bounding box of Object_Left (Content_Left).
8.  Extract the subgrid corresponding to the bounding box of Object_Right (Content_Right).
9.  Create a new subgrid, Sliced_Content_Left, by taking all columns of Content_Left *except* the first column.
10. Construct the output grid by horizontally concatenating Content_Right and Sliced_Content_Left, placing Content_Right on the left and Sliced_Content_Left on the right.

## train_2

**input:**
```
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 1 1 1 1 4 4 4
4 4 4 4 4 4 4 4 4 4 8 1 1 1 3 3 1 4 4 4
4 1 1 1 4 4 4 4 4 4 8 4 4 1 4 4 1 4 4 4
4 1 2 1 4 4 4 4 4 4 8 1 1 1 3 3 1 4 4 4
4 1 1 1 4 4 4 4 4 4 4 4 4 1 1 1 1 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 1 1 1 4 4 4 4 4 4 4 5 3 5 4 4
4 4 4 4 4 1 2 1 3 3 3 3 3 3 3 3 5 3 4 4
4 4 4 4 4 1 1 1 4 4 4 4 4 4 4 5 3 5 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 6 6 6 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 5 3 5 6 6 8 4 4 4 4 4 4 4 4 4 4 4 4
4 4 3 5 3 6 6 8 4 4 4 4 4 4 4 4 4 4 4 4
4 4 5 3 5 6 6 8 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 6 6 6 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4
```


**output:**
```
4 4 4 4 4 4 4 4 4 4 4 6 6 6 4 4 4 4 1 1 1 1
1 1 1 4 4 4 4 4 4 4 5 3 5 6 6 8 1 1 1 3 3 1
1 2 1 3 3 3 3 3 3 3 3 5 3 6 6 8 4 4 1 4 4 1
1 1 1 4 4 4 4 4 4 4 5 3 5 6 6 8 1 1 1 3 3 1
4 4 4 4 4 4 4 4 4 4 4 6 6 6 4 4 4 4 1 1 1 1
```

**Refined Perception:**

The core task involves identifying exactly two objects within the input grid that share the same height, `H`. The transformation rule used to construct the output depends on the properties of the *other* objects (those not having height `H`).

There appear to be two distinct transformation pathways:

1.  **Simple Concatenation:** If none of the "ignored" objects (height != `H`) are wider than the rightmost object of the selected pair, the output is formed by taking the content of the rightmost object of the pair and concatenating it with a sliced version (first column removed) of the leftmost object of the pair. The output dimensions are `H` rows by `Width(Right) + Width(Left) - 1` columns. (`train_1` follows this path).
2.  **Complex Assembly with Padding:** If there exists an "ignored" object `C` that is wider than the rightmost object of the selected pair, a more complex assembly is used. The output includes padding derived from the widest such ignored object `C`, followed by sliced portions of the selected pair (Left object `A`, Right object `B`). Specifically, the output seems to be constructed from:
    *   Padding based on `C`'s content (specifically, `C`'s content truncated to width `Width(C)-2` and vertically centered to height `H`).
    *   A slice of `A` (removing the first two columns).
    *   A reordered version of `B` (moving its column 2 to the beginning of its contribution).
    The output width in this case is `(Width(C)-2) + (Width(A)-2) + Width(B)`. (`train_2` follows this path).

The background digit varies between examples and is used for padding when required. Object identification relies on connected components of non-background digits. The relative horizontal position (left/right) of the selected pair is crucial for applying the rules.

**Updated YAML:**

```yaml
task_type: conditional_grid_transformation
input_properties:
  - grid_representation: matrix of digits
  - background_digit: determined per example (e.g., 8, 4)
  - foreground_elements: clusters of non-background digits
objects:
  - role: selected_pair # Objects A and B
    criteria:
      - find connected components of non-background digits
      - calculate bounding_box and height H for each
      - identify the height H_pair shared by exactly two objects
      - select the two objects (A, B) with height H_pair
    properties:
      - content: subgrid within bounding box
      - height: H_pair
      - width: W_A, W_B
      - position: Left (A), Right (B) based on min column index
  - role: ignored_set # Objects C...
    criteria:
      - all objects not in selected_pair
    properties:
      - content: subgrid within bounding box
      - height: H_C != H_pair
      - width: W_C
relationships:
  - type: width_comparison
    objects: [Widest_Ignored_Object (C_maxW), Right_Selected_Object (B)]
    condition: W_C_maxW > W_B
transformation_logic:
  - condition: W_C_maxW <= W_B (or no ignored objects) # Simple Rule (e.g., train_1)
    steps:
      - extract: Content_A (from Left Object A), Content_B (from Right Object B)
      - slice: Sliced_Content_A = Content_A[:, 1:] # Remove first column
      - concatenate: Output = hstack(Content_B, Sliced_Content_A)
  - condition: W_C_maxW > W_B # Complex Rule (e.g., train_2)
    steps:
      - identify: Widest_Ignored_Object C (content: Content_C, width: W_C)
      - extract: Content_A (from Left Object A, width W_A), Content_B (from Right Object B, width W_B)
      - calculate_pad_width: Pad_W = W_C - 2
      - slice_pad_content: Pad_Content_Base = Content_C[:, :Pad_W]
      - create_padding: Pad = vertically_center(Pad_Content_Base, target_height=H_pair, pad_value=background_digit)
      - slice_left: Slice_A = Content_A[:, 2:] # Remove first two columns
      - slice_right_parts:
          - R_Part1 = Content_B[:, 2:3] # Column 2
          - R_Part2 = Content_B[:, 0:2] # Columns 0, 1
          - R_Part3 = Content_B[:, 3:] # Columns 3 onwards
      - reassemble_right: Slice_B = hstack(R_Part1, R_Part2, R_Part3)
      - concatenate: Output = hstack(Pad, Slice_A, Slice_B)
output_properties:
  - grid_representation: matrix of digits
  - dimensions: H_pair rows, variable width depending on rule applied
  - content_origin: derived from selected_pair objects and potentially widest ignored object
```

**Updated Natural Language Program:**

1.  Identify the most frequent digit in the input grid; this is the background digit (BG).
2.  Find all connected components (objects) of non-BG digits. For each object, determine its bounding box, height (H), and width (W).
3.  Find the height value (`H_pair`) that is the height of exactly two objects. Let these two objects be the `selected_pair`.
4.  Identify the `Left_Object` (A) and `Right_Object` (B) within the `selected_pair` based on their minimum column indices. Let their widths be `W_A` and `W_B`. Extract their content (`Content_A`, `Content_B`).
5.  Identify all other objects as the `ignored_set`.
6.  Find the object `C` in the `ignored_set` with the maximum width (`W_C_maxW`). If the `ignored_set` is empty or no object exists, consider `W_C_maxW` to be 0.
7.  **Conditional Rule Selection:**
    *   **If `W_C_maxW` is greater than `W_B`:**
        *   Apply the **Complex Rule**:
            *   Extract the content of object `C` (`Content_C`).
            *   Calculate the padding width: `Pad_W = W_C_maxW - 2`.
            *   Take the first `Pad_W` columns of `Content_C`.
            *   Create the `Padding` grid by vertically centering this sliced content within a new grid of height `H_pair` and width `Pad_W`, using BG for padding above and below.
            *   Create `Slice_A` by taking all columns of `Content_A` *except* the first two.
            *   Create `Slice_B` by taking column 2 of `Content_B`, followed by columns 0 and 1 of `Content_B`, followed by columns 3 onwards of `Content_B`, and concatenating them horizontally.
            *   Construct the final output grid by horizontally concatenating `Padding`, `Slice_A`, and `Slice_B` in that order.
    *   **Else (`W_C_maxW` is not greater than `W_B`):**
        *   Apply the **Simple Rule**:
            *   Create `Sliced_Content_A` by taking all columns of `Content_A` *except* the first column.
            *   Construct the final output grid by horizontally concatenating `Content_B` and `Sliced_Content_A` in that order.
8.  Return the constructed output grid.
```python
"""
Identifies connected components (objects) of non-background digits in an input grid.
Determines the background digit as the most frequent digit.
Finds the height (H_pair) shared by exactly two objects (selected_pair).
Identifies the left (A) and right (B) objects within the selected_pair.
Finds the widest object (C) among the remaining (ignored) objects.
Applies one of two transformation rules based on whether the width of C (W_C) is greater than the width of B (W_B):
1. Simple Rule (W_C <= W_B): Concatenates the content of B with the content of A (excluding A's first column).
2. Complex Rule (W_C > W_B): 
   - Creates a padding grid by vertically centering the first W_C-2 columns of C's content to height H_pair.
   - Takes the content of A excluding the first two columns (Slice_A).
   - Reorders the columns of B's content: column 2, then columns 0-1, then columns 3+ (Slice_B).
   - Concatenates Padding, Slice_A, and Slice_B horizontally.
Returns the resulting grid.
"""

import numpy as np
from scipy.ndimage import label, find_objects
from collections import Counter
import collections

def find_background(grid: np.ndarray) -> int:
    """Finds the most frequent element in the grid."""
    counts = Counter(grid.flatten())
    # Assume the most frequent is the background
    background_digit = counts.most_common(1)[0][0]
    return background_digit

def find_objects(grid: np.ndarray, background_digit: int) -> list[dict]:
    """Finds connected components of non-background digits."""
    mask = grid != background_digit
    labeled_array, num_features = label(mask)
    
    objects = []
    slices = find_objects(labeled_array)
    
    if not slices: # Handle cases with no foreground objects
        return []

    for i, slc in enumerate(slices):
        if slc is None: # Might happen if labels are not contiguous? Skip.
             continue
        obj_id = i + 1 # Labels start from 1
        # Ensure we only consider the actual object, not the bounding box padding
        component_mask = labeled_array[slc] == obj_id
        obj_content_full = grid[slc] # Content within bounding box
        # Extract only the non-background digits for shape calculation (alternative bounding box)
        # rows, cols = np.where(component_mask)
        # min_r, max_r = rows.min(), rows.max()
        # min_c, max_c = cols.min(), cols.max()
        # height = max_r - min_r + 1
        # width = max_c - min_c + 1
        
        # Use bounding box dimensions directly from find_objects slice
        height = slc[0].stop - slc[0].start
        width = slc[1].stop - slc[1].start
        min_row = slc[0].start
        min_col = slc[1].start

        objects.append({
            'id': obj_id,
            'slice': slc,
            'content': obj_content_full,
            'height': height,
            'width': width,
            'min_row': min_row,
            'min_col': min_col
        })
        
    return objects

def vertically_center(content: np.ndarray, target_height: int, pad_value: int) -> np.ndarray:
    """Centers 'content' vertically within a grid of 'target_height', padding with 'pad_value'."""
    current_height, current_width = content.shape
    if current_height >= target_height:
        # If content is taller or equal, take the central part
        start_row = (current_height - target_height) // 2
        return content[start_row:start_row + target_height, :]

    # Calculate padding needed above and below
    pad_total = target_height - current_height
    pad_top = pad_total // 2
    pad_bottom = pad_total - pad_top

    # Create padding arrays
    top_padding = np.full((pad_top, current_width), pad_value, dtype=content.dtype)
    bottom_padding = np.full((pad_bottom, current_width), pad_value, dtype=content.dtype)

    # Stack them vertically
    centered_content = np.vstack((top_padding, content, bottom_padding))
    return centered_content


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation logic to the input grid.
    """
    grid = np.array(input_grid, dtype=int)
    
    # 1. Find Background Digit
    background_digit = find_background(grid)
    
    # 2. Find Objects
    all_objects = find_objects(grid, background_digit)
    if not all_objects:
        return [] # Or handle as error, return empty grid?

    # 3. Group by height and find the pair height
    height_groups = collections.defaultdict(list)
    for obj in all_objects:
        height_groups[obj['height']].append(obj)
        
    selected_pair = []
    H_pair = -1
    for height, objs in height_groups.items():
        if len(objs) == 2:
            selected_pair = objs
            H_pair = height
            break
            
    if not selected_pair:
        # Handle error: No pair with unique matching height found
        # This case is not covered by the examples, returning empty for now.
        print("Error: No pair of objects with the same unique height found.")
        return []

    # 4. Identify Left/Right in selected_pair
    obj1, obj2 = selected_pair
    if obj1['min_col'] < obj2['min_col']:
        object_A = obj1 # Left
        object_B = obj2 # Right
    else:
        object_A = obj2 # Left
        object_B = obj1 # Right
        
    content_A = object_A['content']
    content_B = object_B['content']
    W_A = object_A['width']
    W_B = object_B['width']

    # 5. Identify Ignored Set
    ignored_set = [obj for obj in all_objects if obj not in selected_pair]

    # 6. Find Widest Ignored Object
    widest_ignored_object = None
    W_C_maxW = 0
    if ignored_set:
        widest_ignored_object = max(ignored_set, key=lambda obj: obj['width'])
        W_C_maxW = widest_ignored_object['width']

    # 7. Apply Conditional Rule Selection
    if widest_ignored_object and W_C_maxW > W_B:
        # Apply the Complex Rule
        content_C = widest_ignored_object['content']
        
        pad_W = W_C_maxW - 2
        if pad_W <= 0:
             # If widest ignored is too thin, maybe default to simple rule or handle error?
             # Based on example 2, C has width 8, B has width 7 -> pad_W = 6.
             # Let's assume pad_W will be positive based on the logic W_C > W_B.
             # If C has width 1 or 2, this rule might behave unexpectedly.
             # If W_C = 3 and W_B = 2, pad_W=1. Seems okay.
             # If W_C = 2 and W_B = 1, pad_W=0. Padding will be empty.
             padding_base = np.empty((content_C.shape[0], 0), dtype=content_C.dtype) # Empty base if pad_W is 0
        else:
             padding_base = content_C[:, :pad_W]

        # Create padding grid
        padding_grid = vertically_center(padding_base, H_pair, background_digit)
        
        # Slice A (remove first two columns)
        if W_A <= 2:
            slice_A = np.empty((H_pair, 0), dtype=content_A.dtype) # Empty slice
        else:
            slice_A = content_A[:, 2:]
            
        # Slice and reassemble B
        parts_B = []
        # Part 1: Column 2 (index 2)
        if W_B > 2:
            parts_B.append(content_B[:, 2:3])
        # Part 2: Columns 0, 1 (index 0, 1)
        if W_B > 0:
             parts_B.append(content_B[:, 0:min(2, W_B)]) # Take up to first 2 cols
        # Part 3: Columns 3 onwards (index 3+)
        if W_B > 3:
            parts_B.append(content_B[:, 3:])
            
        if not parts_B:
             slice_B = np.empty((H_pair, 0), dtype=content_B.dtype) # Empty slice if B is too small
        else:
             slice_B = np.hstack(parts_B)

        # Concatenate final output for complex rule
        output_grid_np = np.hstack((padding_grid, slice_A, slice_B))

    else:
        # Apply the Simple Rule
        # Slice A (remove first column)
        if W_A <= 1:
             sliced_content_A = np.empty((H_pair, 0), dtype=content_A.dtype) # Empty slice
        else:
             sliced_content_A = content_A[:, 1:]
             
        # Concatenate final output for simple rule
        output_grid_np = np.hstack((content_B, sliced_content_A))

    # Convert back to list of lists
    output_grid = output_grid_np.tolist()
    
    return output_grid

```
