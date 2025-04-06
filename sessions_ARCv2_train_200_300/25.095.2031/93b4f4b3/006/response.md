**General Assessment and Strategy**

The previous code attempt correctly identified the core structure of the task: splitting the input grid, using the left half as a mask/frame, and filling the zeros in the mask with values derived from the right half. The code also implemented a mapping logic based on analyzing the unique non-zero values in the right half (content keys) relative to all non-zero values in the input.

However, the comparison between the `transformed_output` and the `expected_output` showed discrepancies, specifically unexpected zeros in the `transformed_output` where the frame value should have been preserved or where a mapped content value should have appeared.

The analysis suggests:
1.  The mapping rules identified by the analysis script (`Reverse` for Example 1, `Cyclic Shift` for Example 2) seem to correctly correspond to the transformations seen in the *expected* outputs.
2.  The previous code's logic for *selecting* between Reverse and Cyclic Shift (based on whether the smallest content key is the overall smallest non-zero value) appears consistent with the examples.
3.  The failure likely occurred during the *execution* or implementation details of the previous code, potentially overwriting parts of the frame from the left grid incorrectly before or during the mapping application, despite the code appearing logically sound.

The strategy is to refine the documentation and natural language program to be extremely clear about preserving the left grid's frame and only modifying its zero cells, then re-implement the python code based on this refined understanding, ensuring the initialization and update steps are correct.

**Metrics Analysis**

``` python
import numpy as np
import json

def analyze_example(input_grid_str, output_grid_str):
    # Parse grids
    input_grid = np.array([[int(x) for x in row.split()] for row in input_grid_str.strip().split('\n')])
    expected_output_grid = np.array([[int(x) for x in row.split()] for row in output_grid_str.strip().split('\n')])

    # Get dimensions
    rows, cols = input_grid.shape
    mid_col = cols // 2

    # Split input
    left_grid = input_grid[:, :mid_col]
    right_grid = input_grid[:, mid_col:]

    # Analyze frame
    left_non_zeros = left_grid[left_grid != 0]
    frame_value = 0
    if left_non_zeros.size > 0:
        unique_left, counts_left = np.unique(left_non_zeros, return_counts=True)
        frame_value = int(unique_left[np.argmax(counts_left)]) # Convert to standard int

    # Analyze content keys
    right_non_zeros = right_grid[right_grid != 0]
    content_keys = sorted([int(x) for x in np.unique(right_non_zeros)]) # Convert to standard int list

    min_key = min(content_keys) if content_keys else None
    max_key = max(content_keys) if content_keys else None

    # Analyze all non-zeros
    all_non_zeros = sorted([int(x) for x in np.unique(input_grid[input_grid != 0])])

    # Determine expected mapping
    expected_map = {}
    mapping_consistent = True
    map_found = False
    if content_keys:
        temp_map = {}
        for r in range(rows):
            for c in range(mid_col):
                if left_grid[r, c] == 0:
                    right_val = int(right_grid[r, c])
                    expected_val = int(expected_output_grid[r, c])
                    if right_val != 0:
                        if right_val not in temp_map:
                           temp_map[right_val] = expected_val
                           map_found = True
                        elif temp_map[right_val] != expected_val:
                           mapping_consistent = False
                           break
            if not mapping_consistent: break

        if map_found and mapping_consistent:
            expected_map = {k: v for k, v in temp_map.items()}
            # Determine map type string
            key_list = content_keys
            n_keys = len(key_list)
            # Check Identity
            is_identity = all(k == v for k, v in expected_map.items())
            # Check Cyclic
            is_cyclic = False
            if not is_identity and len(expected_map) == n_keys:
                is_cyclic = all(expected_map.get(key_list[i]) == key_list[(i + 1) % n_keys] for i in range(n_keys))
            # Check Reverse
            is_reverse = False
            if not is_identity and not is_cyclic and len(expected_map) == n_keys:
                 is_reverse = all(expected_map.get(key_list[i]) == key_list[n_keys - 1 - i] for i in range(n_keys))

            if is_identity: expected_mapping_type = "Identity"
            elif is_cyclic: expected_mapping_type = "Cyclic Shift"
            elif is_reverse: expected_mapping_type = "Reverse"
            else: expected_mapping_type = "Other"
        elif not mapping_consistent:
            expected_mapping_type = "Inconsistent"
            expected_map = {}
        else:
             expected_mapping_type = "N/A (No mapping found)"
    else:
        expected_mapping_type = "N/A (No content keys)"

    # Determine rule trigger condition
    rule_trigger_condition = "N/A"
    smallest_content_key_is_overall_smallest = False
    if content_keys and all_non_zeros:
        smallest_content_key_is_overall_smallest = (content_keys[0] == all_non_zeros[0])
        rule_trigger_condition = f"Smallest content key ({content_keys[0]}) == Smallest overall non-zero ({all_non_zeros[0]})? -> {smallest_content_key_is_overall_smallest}"


    return {
        "dimensions_input": f"{rows}x{cols}",
        "dimensions_output": f"{expected_output_grid.shape[0]}x{expected_output_grid.shape[1]}",
        "frame_value": frame_value,
        "content_keys": content_keys,
        "all_non_zero_values": all_non_zeros,
        "rule_trigger_condition": rule_trigger_condition,
        "expected_mapping_type": expected_mapping_type,
        "derived_expected_map": expected_map
    }

# Example 1 Data
input_1 = """
5 5 5 5 5 5 0 0 0 0 0 0
5 5 0 0 0 5 0 3 0 0 3 0
5 5 5 0 0 5 0 3 0 0 3 0
5 5 5 5 0 5 0 3 3 3 3 0
5 5 5 5 5 5 0 0 0 0 0 0
5 0 0 0 5 5 0 2 2 2 0 0
5 0 0 5 5 5 0 2 2 0 0 0
5 0 5 5 5 5 0 2 0 0 0 0
5 5 5 5 5 5 0 0 0 0 0 0
5 0 5 5 0 5 0 0 1 1 1 0
5 0 5 5 0 5 0 0 0 1 1 0
5 0 0 0 0 5 0 0 0 0 1 0
5 5 5 5 5 5 0 0 0 0 0 0
"""
output_1 = """
5 5 5 5 5 5
5 5 1 1 1 5
5 5 5 1 1 5
5 5 5 5 1 5
5 5 5 5 5 5
5 2 2 2 5 5
5 2 2 5 5 5
5 2 5 5 5 5
5 5 5 5 5 5
5 3 5 5 3 5
5 3 5 5 3 5
5 3 3 3 3 5
5 5 5 5 5 5
"""

# Example 2 Data
input_2 = """
1 1 1 1 1 1 0 0 0 0 0 0
1 1 0 0 1 1 0 0 2 2 0 0
1 0 0 0 0 1 0 0 2 2 0 0
1 1 1 1 1 1 0 0 0 0 0 0
1 0 0 0 0 1 0 0 3 3 0 0
1 1 0 0 1 1 0 3 3 3 3 0
1 1 1 1 1 1 0 0 0 0 0 0
1 1 0 0 1 1 0 6 6 6 6 0
1 1 0 0 1 1 0 0 6 6 0 0
1 1 1 1 1 1 0 0 0 0 0 0
"""
output_2 = """
1 1 1 1 1 1
1 1 3 3 1 1
1 3 3 3 3 1
1 1 1 1 1 1
1 6 6 6 6 1
1 1 6 6 1 1
1 1 1 1 1 1
1 1 2 2 1 1
1 1 2 2 1 1
1 1 1 1 1 1
"""

results = {}
results["example1"] = analyze_example(input_1, output_1)
results["example2"] = analyze_example(input_2, output_2)

# Print results as JSON
print(json.dumps(results, indent=2))

```
```
{
  "example1": {
    "dimensions_input": "13x12",
    "dimensions_output": "13x6",
    "frame_value": 5,
    "content_keys": [
      1,
      2,
      3
    ],
    "all_non_zero_values": [
      1,
      2,
      3,
      5
    ],
    "rule_trigger_condition": "Smallest content key (1) == Smallest overall non-zero (1)? -> True",
    "expected_mapping_type": "Reverse",
    "derived_expected_map": {
      "3": 1,
      "2": 2,
      "1": 3
    }
  },
  "example2": {
    "dimensions_input": "10x12",
    "dimensions_output": "10x6",
    "frame_value": 1,
    "content_keys": [
      2,
      3,
      6
    ],
    "all_non_zero_values": [
      1,
      2,
      3,
      6
    ],
    "rule_trigger_condition": "Smallest content key (2) == Smallest overall non-zero (1)? -> False",
    "expected_mapping_type": "Cyclic Shift",
    "derived_expected_map": {
      "2": 3,
      "3": 6,
      "6": 2
    }
  }
}

```
**YAML Fact Documentation**


```yaml
task_name: map_content_onto_mask_conditional
description: Overlays content from the right half of an input grid onto the zero-valued cells of the left half (mask), applying a conditional mapping to the content values.
grid_properties:
  input_width_relation: twice the output width
  input_height_relation: same as output height
  cell_values: non-negative integers (0 is background/fill target, others are frame or content)

components:
  - id: input_grid
    type: Grid
    properties:
      - even number of columns
  - id: left_mask_grid
    type: Grid
    derivation: Left half of input_grid (columns 0 to width/2 - 1)
    properties:
      - contains a frame defined by a non-zero value (frame_value)
      - contains target areas defined by zero (fill_target_value: 0)
  - id: right_content_grid
    type: Grid
    derivation: Right half of input_grid (columns width/2 to width - 1)
    properties:
      - contains content keys defined by non-zero values (content_keys)
      - contains empty areas defined by zero (background_value: 0)
  - id: output_grid
    type: Grid
    derivation: Combination of left_mask_grid and mapped right_content_grid.
  - id: all_non_zeros
    type: List[int]
    derivation: Sorted unique non-zero values from the entire input_grid.
  - id: content_keys_sorted
    type: List[int]
    derivation: Sorted unique non-zero values from the right_content_grid.
  - id: value_map
    type: Dict[int, int]
    derivation: Mapping from content_keys to output values based on a conditional rule.

actions:
  - Split: Divide input_grid vertically into left_mask_grid and right_content_grid.
  - Analyze:
      - Identify fill_target_value (0) in left_mask_grid.
      - Extract frame_value from left_mask_grid (typically the most frequent non-zero value).
      - Extract content_keys from right_content_grid.
      - Generate content_keys_sorted list.
      - Generate all_non_zeros list from input_grid.
  - Determine Map Rule:
      - Condition: Check if content_keys_sorted is not empty AND if content_keys_sorted[0] is equal to all_non_zeros[0].
      - If True: Set mapping type to "Reverse".
      - If False (or content_keys_sorted is empty): Set mapping type to "Cyclic Shift".
  - Build Map:
      - If mapping type is "Reverse": Create value_map where content_keys_sorted[i] maps to content_keys_sorted[n-1-i].
      - If mapping type is "Cyclic Shift": Create value_map where content_keys_sorted[i] maps to content_keys_sorted[(i+1) % n].
      - If content_keys_sorted is empty: value_map is empty.
  - Construct Output:
      - Initialize output_grid as a deep copy of left_mask_grid.
      - Iterate through each cell (r, c) of output_grid.
      - Condition: Check if output_grid[r][c] equals fill_target_value (0).
      - If True:
          - Get the content_key = right_content_grid[r][c].
          - If content_key is non-zero:
              - mapped_value = value_map[content_key].
              - Set output_grid[r][c] = mapped_value.
          - (If content_key is 0, output_grid[r][c] remains 0).
      - If False (cell is part of the frame): Keep the original frame_value.

relationships:
  - output_grid dimensions match left_mask_grid dimensions.
  - The choice between Reverse and Cyclic Shift mapping depends on whether the smallest content key is also the smallest non-zero value in the entire input grid.
  - Only cells that are 0 in the left_mask_grid are potentially modified in the output_grid.
  - The modification value depends on the corresponding cell in the right_content_grid and the derived value_map.
```


**Natural Language Program**

1.  Read the input grid and determine its dimensions (rows `R`, total columns `C`).
2.  Calculate the midpoint column index `M = C / 2`.
3.  Split the input grid vertically into two sub-grids:
    *   `left_grid`: Columns 0 to `M-1`.
    *   `right_grid`: Columns `M` to `C-1`.
4.  Find all unique non-zero integer values present in the entire `input_grid`. Sort them to get the `all_non_zeros_sorted` list.
5.  Find all unique non-zero integer values present in the `right_grid`. Sort them to get the `content_keys_sorted` list.
6.  Determine the mapping rule:
    *   Initialize `use_reverse_mapping` to `False`.
    *   If `content_keys_sorted` is not empty AND `all_non_zeros_sorted` is not empty AND the first element of `content_keys_sorted` is equal to the first element of `all_non_zeros_sorted`, set `use_reverse_mapping` to `True`.
7.  Create an empty dictionary `value_map` to store the mapping from content keys to output values.
8.  If `content_keys_sorted` is not empty:
    *   Let `n = length` of `content_keys_sorted`.
    *   If `use_reverse_mapping` is `True`:
        *   For each index `i` from 0 to `n-1`, add an entry to `value_map`: `content_keys_sorted[i]` maps to `content_keys_sorted[n - 1 - i]`.
    *   Else (`use_reverse_mapping` is `False`, implying Cyclic Shift):
        *   For each index `i` from 0 to `n-1`, add an entry to `value_map`: `content_keys_sorted[i]` maps to `content_keys_sorted[(i + 1) % n]`.
9.  Create the `output_grid` by making a deep copy of the `left_grid`.
10. Iterate through each cell of the `output_grid` using its row index `r` (from 0 to `R-1`) and column index `c` (from 0 to `M-1`).
11. For the current cell `(r, c)`:
    *   Check if the value `output_grid[r][c]` is 0.
    *   If it is 0:
        *   Get the corresponding value from the `right_grid`: `content_key = right_grid[r][c]`.
        *   If `content_key` exists as a key in the `value_map` (meaning it was a non-zero value in the right grid):
            *   Set `output_grid[r][c]` to the mapped value: `value_map[content_key]`.
        *   (If `content_key` is 0, `output_grid[r][c]` remains 0).
    *   If `output_grid[r][c]` is not 0, leave it unchanged (it's part of the frame).
12. Return the final `output_grid`.