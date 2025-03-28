## General Assessment

The provided code successfully solves Example 1 but fails on Example 2.
- Example 1 involves a non-background pattern (azure '8') that *does not* touch the top edge (`min_r = 3`). The code correctly identifies this, extracts the rows containing the pattern (`rows 3-4`), flips this block vertically, and places it at the top of the grid (`rows 0-1`). The rest of the grid seems implicitly copied, which matches the expected output.
- Example 2 involves a non-background pattern (red '2') that *does* touch the top edge (`min_r = 0`) but not the left edge (`min_c = 4`). The code attempts a cyclic horizontal shift based on the previous logic, but the *expected output* is identical to the *input grid*. This indicates that the condition `min_r == 0` might trigger a "no change" operation, regardless of `min_c`.

The strategy is to revise the transformation rule to account for the observation in Example 2: if the pattern touches the top row, the grid remains unchanged. The transformation (vertical flip and move to top) should only occur if the pattern does *not* touch the top row.

## Metrics

Let's gather specific metrics for each example.


``` python
import numpy as np

def get_grid_metrics(grid_list):
    if not grid_list:
        return {"error": "Empty grid provided"}
    grid = np.array(grid_list, dtype=int)
    height, width = grid.shape
    bg_pixel = 0
    non_bg_coords = np.argwhere(grid != bg_pixel)

    metrics = {
        "shape": (height, width),
        "non_bg_pixels_present": non_bg_coords.size > 0
    }

    if non_bg_coords.size > 0:
        min_r = int(non_bg_coords[:, 0].min())
        max_r = int(non_bg_coords[:, 0].max())
        min_c = int(non_bg_coords[:, 1].min())
        max_c = int(non_bg_coords[:, 1].max())
        pattern_height = max_r - min_r + 1
        pattern_width = max_c - min_c + 1
        non_bg_colors = sorted(list(np.unique(grid[grid != bg_pixel])))

        metrics.update({
            "min_r": min_r,
            "max_r": max_r,
            "min_c": min_c,
            "max_c": max_c,
            "pattern_bounding_box": ((min_r, min_c), (max_r, max_c)),
            "pattern_row_span_height": pattern_height,
            "touches_top_edge": min_r == 0,
            "touches_left_edge": min_c == 0,
            "non_bg_colors": non_bg_colors,
        })
    else:
         metrics.update({
            "min_r": None, "max_r": None, "min_c": None, "max_c": None,
            "pattern_bounding_box": None, "pattern_row_span_height": 0,
            "touches_top_edge": None, "touches_left_edge": None,
            "non_bg_colors": []
        })

    return metrics

# Example 1 Data
input1 = [
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0],
    [8, 8, 0, 8, 8],
    [0, 8, 0, 8, 0]
]
output1_expected = [
    [0, 8, 0, 8, 0],
    [8, 8, 0, 8, 8],
    [0, 0, 0, 0, 0],
    [8, 8, 0, 8, 8],
    [0, 8, 0, 8, 0]
]
output1_transformed = [
    [0, 8, 0, 8, 0],
    [8, 8, 0, 8, 8],
    [0, 0, 0, 0, 0],
    [8, 8, 0, 8, 8],
    [0, 8, 0, 8, 0]
]


# Example 2 Data
input2 = [
    [0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 0],
    [0, 0, 0, 0, 2, 2, 2, 0, 2, 2, 2],
    [0, 0, 0, 0, 2, 2, 2, 0, 2, 2, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 2, 2, 0, 2, 2, 2],
    [0, 0, 0, 0, 2, 2, 2, 0, 2, 2, 2],
    [0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 0]
]
output2_expected = [
    [0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 0],
    [0, 0, 0, 0, 2, 2, 2, 0, 2, 2, 2],
    [0, 0, 0, 0, 2, 2, 2, 0, 2, 2, 2],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 0, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 2, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 2, 2, 2, 0, 2, 2, 2],
    [0, 0, 0, 0, 2, 2, 2, 0, 2, 2, 2],
    [0, 0, 0, 0, 2, 0, 2, 0, 2, 2, 0]
]
output2_transformed = [
    [2, 0, 2, 0, 2, 2, 0, 0, 0, 0, 0],
    [2, 2, 2, 0, 2, 2, 2, 0, 0, 0, 0],
    [2, 2, 2, 0, 2, 2, 2, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 0, 0, 0, 0, 0, 0, 0, 0],
    [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
    [2, 2, 2, 0, 2, 2, 2, 0, 0, 0, 0],
    [2, 2, 2, 0, 2, 2, 2, 0, 0, 0, 0],
    [2, 0, 2, 0, 2, 2, 0, 0, 0, 0, 0]
]


metrics1_in = get_grid_metrics(input1)
metrics1_out_expected = get_grid_metrics(output1_expected)
metrics1_out_transformed = get_grid_metrics(output1_transformed)

metrics2_in = get_grid_metrics(input2)
metrics2_out_expected = get_grid_metrics(output2_expected)
metrics2_out_transformed = get_grid_metrics(output2_transformed)


print("--- Example 1 ---")
print(f"Input Metrics: {metrics1_in}")
print(f"Expected Output Metrics: {metrics1_out_expected}")
print(f"Transformed Output Metrics: {metrics1_out_transformed}")
print(f"Match: {np.array_equal(output1_expected, output1_transformed)}")

print("\n--- Example 2 ---")
print(f"Input Metrics: {metrics2_in}")
print(f"Expected Output Metrics: {metrics2_out_expected}")
print(f"Transformed Output Metrics: {metrics2_out_transformed}")
print(f"Match: {np.array_equal(output2_expected, output2_transformed)}")
```
```
--- Example 1 ---
Input Metrics: {'shape': (5, 5), 'non_bg_pixels_present': True, 'min_r': 3, 'max_r': 4, 'min_c': 0, 'max_c': 4, 'pattern_bounding_box': ((3, 0), (4, 4)), 'pattern_row_span_height': 2, 'touches_top_edge': False, 'touches_left_edge': True, 'non_bg_colors': [np.int64(8)]}
Expected Output Metrics: {'shape': (5, 5), 'non_bg_pixels_present': True, 'min_r': 0, 'max_r': 4, 'min_c': 0, 'max_c': 4, 'pattern_bounding_box': ((0, 0), (4, 4)), 'pattern_row_span_height': 5, 'touches_top_edge': True, 'touches_left_edge': True, 'non_bg_colors': [np.int64(8)]}
Transformed Output Metrics: {'shape': (5, 5), 'non_bg_pixels_present': True, 'min_r': 0, 'max_r': 4, 'min_c': 0, 'max_c': 4, 'pattern_bounding_box': ((0, 0), (4, 4)), 'pattern_row_span_height': 5, 'touches_top_edge': True, 'touches_left_edge': True, 'non_bg_colors': [np.int64(8)]}
Match: True

--- Example 2 ---
Input Metrics: {'shape': (11, 11), 'non_bg_pixels_present': True, 'min_r': 0, 'max_r': 10, 'min_c': 4, 'max_c': 10, 'pattern_bounding_box': ((0, 4), (10, 10)), 'pattern_row_span_height': 11, 'touches_top_edge': True, 'touches_left_edge': False, 'non_bg_colors': [np.int64(2)]}
Expected Output Metrics: {'shape': (11, 11), 'non_bg_pixels_present': True, 'min_r': 0, 'max_r': 10, 'min_c': 4, 'max_c': 10, 'pattern_bounding_box': ((0, 4), (10, 10)), 'pattern_row_span_height': 11, 'touches_top_edge': True, 'touches_left_edge': False, 'non_bg_colors': [np.int64(2)]}
Transformed Output Metrics: {'shape': (11, 11), 'non_bg_pixels_present': True, 'min_r': 0, 'max_r': 10, 'min_c': 0, 'max_c': 6, 'pattern_bounding_box': ((0, 0), (10, 6)), 'pattern_row_span_height': 11, 'touches_top_edge': True, 'touches_left_edge': True, 'non_bg_colors': [np.int64(2)]}
Match: False

```
## Facts


```yaml
task_description: Transforms an input grid based on the vertical position of its non-background (non-white) pixels.

definitions:
  - name: background_pixel
    value: 0 # white
  - name: pattern
    description: The set of all non-background pixels in the input grid.
  - name: pattern_present
    description: Boolean indicating if any non-background pixels exist in the grid.
  - name: min_r
    description: The minimum row index containing a pattern pixel. Returns None if no pattern present.
  - name: max_r
    description: The maximum row index containing a pattern pixel. Returns None if no pattern present.
  - name: touches_top_edge
    description: Boolean, True if min_r == 0.

examples:
  - id: 1
    input_metrics:
      shape: [5, 5]
      pattern_present: True
      min_r: 3
      max_r: 4
      touches_top_edge: False
      non_bg_colors: [8] # azure
    output_metrics: # Expected & Transformed match
      shape: [5, 5]
      pattern_present: True
      min_r: 0
      max_r: 4 # Note: The original pattern pixels are now split between top and bottom
      touches_top_edge: True
      non_bg_colors: [8] # azure
    transformation_applied: Yes (Flip & Move)

  - id: 2
    input_metrics:
      shape: [11, 11]
      pattern_present: True
      min_r: 0
      max_r: 10
      touches_top_edge: True
      non_bg_colors: [2] # red
    expected_output_metrics:
      shape: [11, 11]
      pattern_present: True
      min_r: 0
      max_r: 10
      touches_top_edge: True
      non_bg_colors: [2] # red
      # Note: Identical to input metrics
    transformed_output_metrics: # Incorrect output from previous code
      shape: [11, 11]
      pattern_present: True
      min_r: 0
      max_r: 10
      touches_top_edge: True
      non_bg_colors: [2] # red
      # Incorrect geometry due to flawed shift logic
    transformation_applied: No (Should be no change)

conditions:
  - condition: No pattern present (grid is all background pixels)
    action: Return the input grid unchanged.
  - condition: Pattern is present AND touches_top_edge is True (min_r == 0)
    action: Return the input grid unchanged.
  - condition: Pattern is present AND touches_top_edge is False (min_r > 0)
    action: Apply "Flip & Move" transformation.

actions:
  - name: Flip & Move
    steps:
      - Identify the minimum (min_r) and maximum (max_r) row indices containing pattern pixels.
      - Calculate the height of the pattern's row span: `block_height = max_r - min_r + 1`.
      - Extract the block of rows from the input grid spanning `min_r` to `max_r` (inclusive), covering the full width of the grid.
      - Create a vertically flipped copy of this extracted block.
      - Create the output grid as a copy of the input grid.
      - Replace the top `block_height` rows of the output grid (rows 0 to `block_height - 1`) with the flipped block. Ensure not to write past the grid boundaries if the grid height is less than `block_height`.
```


## Natural Language Program

1.  **Analyze the Input Grid**: Check if the input grid contains any non-background pixels (pixels with value != 0).
    *   If no non-background pixels exist, return the input grid unchanged.
2.  **Identify Pattern Position**: Determine the minimum row index (`min_r`) containing any non-background pixel.
3.  **Apply Conditional Transformation**:
    *   **Case 1: Pattern touches the top edge (`min_r == 0`)**: Return the input grid unchanged.
    *   **Case 2: Pattern does not touch the top edge (`min_r > 0`)**:
        a.  Find the maximum row index (`max_r`) containing a non-background pixel.
        b.  Calculate the height of the pattern's row span: `block_height = max_r - min_r + 1`.
        c.  Extract the rectangular block of rows from the input grid spanning `min_r` to `max_r` (inclusive) across the full grid width.
        d.  Create a new block by vertically flipping the extracted block.
        e.  Create the output grid as a copy of the input grid.
        f.  Determine the number of rows to overwrite at the top: `rows_to_overwrite = min(block_height, grid_height)`.
        g.  Replace the content of the output grid from row 0 up to (but not including) `rows_to_overwrite` with the corresponding top rows of the flipped block.
4.  **Return the Output Grid**: Return the resulting transformed grid.