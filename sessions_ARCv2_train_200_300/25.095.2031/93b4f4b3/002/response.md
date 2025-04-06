## General Assessment

The initial analysis correctly identified the basic structure: splitting the input grid and using the left half as a base or mask, with the right half providing content. However, the initial code assumed a direct overlay (copying values from the right grid into the 0-valued cells of the left grid). The provided results clearly show this is incorrect. The values appearing in the output grid's filled areas are *different* from the corresponding values in the right input grid.

The key insight missed initially is a **value mapping** step. The non-zero values present in the right grid (`content values`) are transformed into different non-zero values (`fill values`) before being placed into the output grid. The analysis of the discrepancies between the `transformed_output` (from the initial code) and the `expected_output` reveals a consistent mapping within each example, but the mapping rule itself differs between examples.

**Strategy for Resolution:**

1.  **Identify Mapping Keys:** Determine the set of unique non-zero values present in the right half of the input grid. These are the "keys" for the mapping.
2.  **Determine Mapping Rule:** Analyze the relationship between the input keys and the output fill values for each example. The code execution and analysis reveal two distinct mapping rules: a "Reverse" mapping and a "Cyclic Shift" mapping applied to the sorted list of input keys.
3.  **Identify Rule Trigger:** Determine what property of the input grid dictates which mapping rule (Reverse or Cyclic) to use. The analysis suggests the rule depends on whether the index `0` is present in the list of indices derived by locating the right-grid non-zero values within the sorted list of all non-zero input values. Specifically, if index 0 is present, use Reverse; otherwise, use Cyclic Shift.
4.  **Apply Mapping:** Implement the logic: split the grid, determine the mapping keys (`V_in`), determine the rule, create the specific value map, initialize the output grid from the left half, and iterate through the output grid, replacing 0s with the *mapped* value from the corresponding right-grid cell.

## Metrics and Analysis

The `tool_code` execution provides detailed metrics confirming the refined hypothesis:

*   **Example 1:**
    *   `frame_value`: 5
    *   `all_non_zeros (A)`: `[1, 2, 3, 5]`
    *   `right_non_zeros (V_in)`: `[1, 2, 3]`
    *   `indices (Idx)`: `[0, 1, 2]` (Indices of `V_in` within `A`)
    *   `observed_mapping`: `{1: 3, 2: 2, 3: 1}`
    *   `rule_applied`: Reverse (Matches `expected_mapping_reverse`)
    *   `hypothesis_rule (0 in Idx?)`: Reverse
    *   `hypothesis_matches_applied`: True

*   **Example 2:**
    *   `frame_value`: 1
    *   `all_non_zeros (A)`: `[1, 2, 3, 6]`
    *   `right_non_zeros (V_in)`: `[2, 3, 6]`
    *   `indices (Idx)`: `[1, 2, 3]` (Indices of `V_in` within `A`)
    *   `observed_mapping`: `{2: 3, 3: 6, 6: 2}`
    *   `rule_applied`: Cyclic (Matches `expected_mapping_cyclic`)
    *   `hypothesis_rule (0 in Idx?)`: Cyclic
    *   `hypothesis_matches_applied`: True

**Conclusion from Metrics:** The analysis strongly supports the hypothesis that the mapping rule (Reverse vs. Cyclic) applied to the unique non-zero values from the right grid (`V_in`) is determined by whether the indices of these values within the sorted list of all unique non-zero input values (`A`) include the index `0`.

## YAML Fact Documentation


```yaml
task_name: overlay_content_with_mapped_values
description: >
  Combine two halves of an input grid. The left half acts as a mask/frame.
  The non-zero values from the right half dictate which areas in the left half's zero-regions should be filled.
  Crucially, the values used for filling are determined by applying a specific mapping (either reverse order or cyclic shift)
  to the unique non-zero values found in the right half. The choice of mapping rule depends on the relationship between
  the right-half values and all unique non-zero values in the input.

grid_properties:
  input_width_relation: twice the output width
  input_height_relation: same as output height
  cell_values: non-negative integers

components:
  - id: input_grid
    type: Grid
  - id: output_grid
    type: Grid
  - id: left_mask_grid
    type: Grid
    derivation: Left half of input_grid (columns 0 to W/2 - 1)
    properties:
      - contains a frame defined by a non-zero value (mask_value)
      - contains empty areas defined by zero (fill_target_value: 0)
  - id: right_content_grid
    type: Grid
    derivation: Right half of input_grid (columns W/2 to W - 1)
    properties:
      - contains content identifiers defined by non-zero values (content_keys)
      - contains empty areas defined by zero (background_value: 0)
  - id: all_unique_non_zeros
    type: Sorted List
    derivation: Unique non-zero values from the entire input_grid.
  - id: content_keys_unique_sorted
    type: Sorted List
    derivation: Unique non-zero values from right_content_grid.
  - id: content_key_indices
    type: List of Integers
    derivation: Indices of content_keys_unique_sorted within all_unique_non_zeros.
  - id: value_map
    type: Dictionary
    derivation: >
      Maps each value `v` in content_keys_unique_sorted to a target fill value.
      The target value is determined by applying either a 'Reverse' or 'Cyclic Shift' operation
      to the content_keys_unique_sorted list, based on whether 0 is present in content_key_indices.

actions:
  - Split: Divide the input_grid vertically into left_mask_grid and right_content_grid.
  - Analyze Input:
    - Find all_unique_non_zeros.
    - Find content_keys_unique_sorted.
    - Calculate content_key_indices.
  - Determine Mapping Rule: Check if 0 is present in content_key_indices.
    - If yes, rule is 'Reverse'.
    - If no, rule is 'Cyclic Shift'.
  - Create Map: Build value_map based on content_keys_unique_sorted and the determined rule.
    - Reverse: `content_keys_unique_sorted[i]` maps to `content_keys_unique_sorted[N-1-i]`.
    - Cyclic Shift: `content_keys_unique_sorted[i]` maps to `content_keys_unique_sorted[(i+1)%N]`.
  - Initialize: Create the output_grid as a copy of the left_mask_grid.
  - Iterate & Fill: Process each cell (row r, column c) of the output_grid.
    - Condition 1: Check if output_grid[r][c] is equal to fill_target_value (0).
    - Condition 2: Check if the corresponding value in right_content_grid[r][c] is non-zero (is a content_key).
    - Replace: If both conditions are true, update output_grid[r][c] using the value_map applied to right_content_grid[r][c].
    - Keep: Otherwise, keep the original value in output_grid[r][c].

relationships:
  - output_grid dimensions match left_mask_grid dimensions.
  - output_grid combines the structure of left_mask_grid with content derived from right_content_grid after value mapping.
  - The specific value mapping function depends on the set properties of non-zero values across the input grid.
```


## Natural Language Program

1.  Determine the dimensions of the `input_grid`: `R` rows and `C` columns.
2.  Calculate the midpoint column index: `mid = C / 2`.
3.  Extract the `left_grid` (columns 0 to `mid - 1`) and the `right_grid` (columns `mid` to `C - 1`).
4.  Find the sorted list of unique non-zero values present in the entire `input_grid`. Call this list `A`.
5.  Find the sorted list of unique non-zero values present in the `right_grid`. Call this list `V_in`.
6.  If `V_in` is empty, initialize `output_grid` as a copy of `left_grid` and finish.
7.  Determine the indices within `A` for each value in `V_in`. Store these indices in a list `Idx`.
8.  Check if the index `0` is present in the list `Idx`.
9.  Based on the check in step 8, define a `value_map`:
    *   If `0` is in `Idx`: For each `i` from 0 to `len(V_in) - 1`, map the value `V_in[i]` to the value `V_in[len(V_in) - 1 - i]`. (Reverse mapping).
    *   If `0` is not in `Idx`: For each `i` from 0 to `len(V_in) - 1`, map the value `V_in[i]` to the value `V_in[(i + 1) % len(V_in)]`. (Cyclic shift mapping).
10. Initialize the `output_grid` as a direct copy of the `left_grid`.
11. Iterate through each cell of the `output_grid` using its row index `r` (from 0 to `R-1`) and column index `c` (from 0 to `mid - 1`).
12. For the current cell `(r, c)`:
    *   Check if the value `output_grid[r][c]` is 0.
    *   Get the corresponding value from the `right_grid`: `content_key = right_grid[r][c]`.
    *   Check if `content_key` is non-zero (i.e., it's one of the keys in `V_in` and thus in `value_map`).
    *   If `output_grid[r][c]` is 0 AND `content_key` is in `value_map`, replace `output_grid[r][c]` with `value_map[content_key]`.
    *   Otherwise, leave `output_grid[r][c]` unchanged.
13. The final `output_grid` is the result.