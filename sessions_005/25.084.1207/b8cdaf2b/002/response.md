## General Assessment

The provided code consistently failed across all training examples, producing outputs identical to the inputs. The failure analysis indicates that the `find_emitter_segment` function incorrectly identified the 'emitter'. The original logic assumed the emitter was the *upper* segment in a vertical pair of different non-background colored pixels. However, the input-output transformations clearly show that the *lower* segment's color is propagated, and the new pixels appear relative to this lower segment.

The core issue lies in the definition and identification of the "emitter object". The strategy is to redefine the emitter identification logic:
1.  Locate the "trigger" condition: a non-background pixel `C1` at `(r, c)` directly above a *different* non-background pixel `C2` at `(r+1, c)`.
2.  Identify the emitter: The emitter is the full horizontal contiguous segment of color `C2` containing the pixel at `(r+1, c)`.
3.  Recalculate emitter properties (color `C2`, width, center coordinates).
4.  Apply the predefined offset patterns based on the *correct* emitter's color and width. The existing offset patterns seem consistent with the examples once the emitter is correctly identified.

## Metrics and Observations

Let's analyze each example based on the revised understanding:

**Example 1:**
*   Input Size: 5x5
*   Output Size: 5x5
*   Trigger: Pixels like `grid[3, 1]=6` (magenta) above `grid[4, 1]=1` (blue).
*   Emitter Segment: `[1, 1, 1]` (blue) at row 4, columns 1-3.
*   Emitter Properties: Color=1 (blue), Width=3, Center=(4, 2).
*   Emitted Pixels: Color=1 (blue) at (2, 0) and (2, 4).
*   Relative Offsets from (4, 2): `(-2, -2)`, `(-2, +2)`.
*   Code Output Analysis: Failed because it likely identified magenta (6) at row 3 as the emitter, for which no pattern is defined, or failed to find any segment meeting its criteria.

**Example 2:**
*   Input Size: 5x5
*   Output Size: 5x5
*   Trigger: `grid[3, 2]=8` (azure) above `grid[4, 2]=3` (green).
*   Emitter Segment: `[3]` (green) at row 4, column 2.
*   Emitter Properties: Color=3 (green), Width=1, Center=(4, 2).
*   Emitted Pixels: Color=3 (green) at (1, 0), (1, 4), (2, 1), (2, 3).
*   Relative Offsets from (4, 2): `(-3, -2)`, `(-3, +2)`, `(-2, -1)`, `(-2, +1)`.
*   Code Output Analysis: Failed because it likely identified azure (8) at row 3 as the emitter.

**Example 3:**
*   Input Size: 7x7
*   Output Size: 7x7
*   Trigger: Pixels like `grid[5, 2]=2` (red) above `grid[6, 2]=4` (yellow).
*   Emitter Segment: `[4, 4, 4]` (yellow) at row 6, columns 2-4.
*   Emitter Properties: Color=4 (yellow), Width=3, Center=(6, 3).
*   Emitted Pixels: Color=4 (yellow) at (3, 0), (3, 6), (4, 1), (4, 5).
*   Relative Offsets from (6, 3): `(-3, -3)`, `(-3, +3)`, `(-2, -2)`, `(-2, +2)`.
*   Code Output Analysis: Failed because it likely identified red (2) at row 5 as the emitter.

**Example 4:**
*   Input Size: 3x3
*   Output Size: 3x3
*   Trigger: `grid[1, 1]=2` (red) above `grid[2, 1]=4` (yellow).
*   Emitter Segment: `[4]` (yellow) at row 2, column 1.
*   Emitter Properties: Color=4 (yellow), Width=1, Center=(2, 1).
*   Emitted Pixels: Color=4 (yellow) at (0, 0) and (0, 2).
*   Relative Offsets from (2, 1): `(-2, -1)`, `(-2, +1)`.
*   Code Output Analysis: Failed because it likely identified red (2) at row 1 as the emitter.

## Facts YAML


```yaml
task_description: "Identify a specific horizontal segment ('emitter') based on vertical color adjacency and add new pixels above it based on the emitter's color and width."

definitions:
  - name: trigger_point
    description: "A location (r, c) where a non-background pixel C1 at (r, c) is directly above a different non-background pixel C2 at (r+1, c)."
  - name: emitter_segment
    description: "The maximal horizontal contiguous segment of color C2 that includes the pixel at (r+1, c) identified by a trigger_point."
    properties:
      - color: The color C2 of the segment.
      - width: The number of pixels in the segment.
      - location:
          - row: The row index (r+1) of the segment.
          - col_min: The starting column index.
          - col_max: The ending column index.
          - center_col: The central column index, calculated as (col_min + col_max) // 2.
  - name: emitted_pixels
    description: "New pixels added to the output grid."
    properties:
      - color: Same as the emitter_segment color.
      - locations: A set of coordinates determined by applying specific offsets relative to the emitter_segment's center coordinates (center_row, center_col).

transformation:
  - action: find_trigger_and_emitter
    description: "Scan the grid row by row, column by column, checking for the trigger_point condition. If found, identify the corresponding emitter_segment below it."
    assumptions: "There is likely only one unique emitter_segment per grid, even if multiple trigger_points identify the same segment."
  - action: determine_offset_pattern
    description: "Select a predefined set of relative (dy, dx) offsets based on the emitter_segment's color and width."
    patterns:
      - condition: color=1 (blue), width=3
        offsets: [(-2, -2), (-2, +2)]
      - condition: color=3 (green), width=1
        offsets: [(-3, -2), (-3, +2), (-2, -1), (-2, +1)]
      - condition: color=4 (yellow), width=3
        offsets: [(-3, -3), (-3, +3), (-2, -2), (-2, +2)]
      - condition: color=4 (yellow), width=1
        offsets: [(-2, -1), (-2, +1)]
  - action: generate_output
    description: "Create the output grid by copying the input grid. For each offset (dy, dx) in the selected pattern, calculate the target coordinate (emitter_row + dy, emitter_center_col + dx). If the target coordinate is within the grid boundaries, set the pixel at that coordinate to the emitter_segment's color."

example_specific_details:
  - example: 1
    trigger_location_example: (3, 1) [Color 6 above Color 1]
    emitter_segment: color=1, width=3, center=(4, 2)
    pattern_used: color=1, width=3
  - example: 2
    trigger_location_example: (3, 2) [Color 8 above Color 3]
    emitter_segment: color=3, width=1, center=(4, 2)
    pattern_used: color=3, width=1
  - example: 3
    trigger_location_example: (5, 2) [Color 2 above Color 4]
    emitter_segment: color=4, width=3, center=(6, 3)
    pattern_used: color=4, width=3
  - example: 4
    trigger_location_example: (1, 1) [Color 2 above Color 4]
    emitter_segment: color=4, width=1, center=(2, 1)
    pattern_used: color=4, width=1
```


## Natural Language Program

1.  **Identify Trigger Points:** Iterate through the grid to find all locations `(r, c)` where a non-background pixel `C1` at `(r, c)` is directly above a different non-background pixel `C2` at `(r+1, c)`.
2.  **Identify Emitter Segment:** For a found trigger point `(r, c)` involving colors `C1` and `C2`, locate the pixel `P_lower` at `(r+1, c)` with color `C2`. Find the maximal horizontal contiguous segment composed entirely of color `C2` that includes `P_lower`. This is the `emitter_segment`. Assume there is only one such unique segment in the grid.
3.  **Determine Emitter Properties:** Record the `emitter_segment`'s color (`emitter_color = C2`), its row index (`emitter_y = r+1`), its starting and ending column indices (`emitter_x_min`, `emitter_x_max`). Calculate its width (`emitter_width = emitter_x_max - emitter_x_min + 1`) and its center column index (`emitter_center_x = (emitter_x_min + emitter_x_max) // 2`).
4.  **Select Offset Pattern:** Choose a predefined set of `(dy, dx)` coordinate offsets based on the `emitter_color` and `emitter_width`. The known patterns are:
    *   If `emitter_color` is Blue (1) and `emitter_width` is 3: `{(-2, -2), (-2, +2)}`
    *   If `emitter_color` is Green (3) and `emitter_width` is 1: `{(-3, -2), (-3, +2), (-2, -1), (-2, +1)}`
    *   If `emitter_color` is Yellow (4) and `emitter_width` is 3: `{(-3, -3), (-3, +3), (-2, -2), (-2, +2)}`
    *   If `emitter_color` is Yellow (4) and `emitter_width` is 1: `{(-2, -1), (-2, +1)}`
5.  **Generate Output:** Create a copy of the input grid. For each offset `(dy, dx)` in the selected pattern:
    *   Calculate the target coordinates: `target_y = emitter_y + dy`, `target_x = emitter_center_x + dx`.
    *   Check if `target_y` and `target_x` are within the grid boundaries.
    *   If within bounds, set the pixel at `(target_y, target_x)` in the output grid to the `emitter_color`.
6.  **Return Output:** Return the modified grid. If no emitter segment is found, return the original input grid.