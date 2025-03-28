**Correction:** The code execution output reveals a critical mistake in my analysis of Example 3.
*   The input grid for Example 3 only contains *one* green frame, not two as I initially perceived. The structure `3 0 0 3 0 3` within the bounding box made it look like two separate frames visually, but `find_objects` correctly identifies it as a single connected component.
*   The expected output also contains only *one* frame.
*   The `Calculated New BBox` (3, 1, 14, 12) does not match the `Expected New BBox` (3, 2, 13, 11).
*   Crucially, the check `Checking if Expected Output Frames are Hollow` reports `False`. Looking closely at the expected output grid, the frame *is* hollow, but there's a green line `expected_output_grid_3[5, 2:12] = 3` and `expected_output_grid_3[4:14, 7] = 3` *inside* the main bounding box. This internal structure seems preserved or somehow derived from the input's internal structure.

**Revised Hypothesis:**
1.  The transformation identifies green "frame" objects. A frame might not be a perfect hollow rectangle initially.
2.  It identifies magenta markers.
3.  It calculates an *outer* bounding box for the output frame based on the initial frame's bounding box and the locations of *all* magenta markers outside that initial box. The calculation seems to be:
    *   `new_min_r = min(initial_min_r, min(marker_r for markers above))` - This doesn't match the code output. Let's re-evaluate.
    *   The code calculates: `new_min_r = min(marker_r for markers above)` *if* markers_above exist, otherwise `new_min_r = initial_min_r`. Similarly for other directions.
    *   Example 3 calculation:
        *   Initial bbox: (3, 4, 7, 9)
        *   Markers: (4, 12) [Right], (6, 1) [Left], (14, 7) [Below]
        *   `markers_above = []` -> `new_min_r = 3`
        *   `markers_below = [14]` -> `new_max_r = 14`
        *   `markers_left = [1]` -> `new_min_c = 1`
        *   `markers_right = [12]` -> `new_max_c = 12`
        *   Calculated `new_bbox`: (3, 1, 14, 12) - This matches the code execution result.
    *   Expected `new_bbox`: (3, 2, 13, 11) - This is different!
        *   Expected `new_min_r = 3` (matches initial)
        *   Expected `new_max_r = 13` (one less than marker row 14)
        *   Expected `new_min_c = 2` (one more than marker col 1)
        *   Expected `new_max_c = 11` (one less than marker col 12)

    *   **New Rule Idea:** The new boundary aligns *one step inside* the outermost marker's row/column. Or perhaps, it aligns *with* the marker row/column, but the drawing function is off by one? Let's check Example 1.
        *   Initial bbox: (2, 4, 4, 6)
        *   Markers: (3, 1) [Left], (9, 5) [Below]
        *   Calculated `new_bbox`: (2, 1, 9, 6)
        *   Expected `new_bbox`: Need to determine this from the expected output grid.

``` python
import numpy as np

def get_bounding_box_from_grid(grid, color):
    rows, cols = grid.shape
    coords = []
    for r in range(rows):
        for c in range(cols):
            if grid[r,c] == color:
                coords.append((r,c))
    if not coords: return None
    min_row = min(r for r, c in coords)
    min_col = min(c for r, c in coords)
    max_row = max(r for r, c in coords)
    max_col = max(c for r, c in coords)
    return min_row, min_col, max_row, max_col

# Example 1 Expected Output
expected_output_grid_1 = np.array([
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,3,3,3,3,3,0,0,0,0,0,0,0,0],
    [0,6,3,0,0,0,3,0,0,0,0,0,0,0,0],
    [0,0,3,0,0,0,3,0,0,0,0,0,0,0,0],
    [0,0,3,0,0,0,3,0,0,0,0,0,0,0,0],
    [0,0,3,0,0,0,3,0,0,0,0,0,0,0,0],
    [0,0,3,0,0,0,3,0,0,0,0,0,0,0,0],
    [0,0,3,3,3,3,3,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,6,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
], dtype=int)

expected_bbox_1 = get_bounding_box_from_grid(expected_output_grid_1, 3)
print(f"Example 1 Expected BBox: {expected_bbox_1}")

# Example 2 Expected Output
expected_output_grid_2 = np.array([
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0,0],
    [0,3,0,3,0,0,0,0,0,0,3,6,0,0,0,0,0],
    [0,3,0,3,0,0,0,0,0,0,3,0,0,0,0,0,0],
    [0,3,0,3,0,0,0,0,0,0,3,0,0,0,0,0,0],
    [0,3,3,3,3,3,3,3,3,3,3,0,0,0,0,0,0],
    [0,0,0,0,6,0,0,0,0,0,0,0,0,0,0,0,0],
    [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
], dtype=int)

expected_bbox_2 = get_bounding_box_from_grid(expected_output_grid_2, 3)
print(f"Example 2 Expected BBox: {expected_bbox_2}")
```
```
Example 1 Expected BBox: (2, 2, 8, 6)
Example 2 Expected BBox: (1, 1, 5, 10)

```
*   **Example 1 Analysis:**
    *   Initial bbox: (2, 4, 4, 6)
    *   Markers: (3, 1) [Left], (9, 5) [Below]
    *   Calculated `new_bbox`: (2, 1, 9, 6)
    *   Expected `new_bbox`: (2, 2, 8, 6)
    *   Comparison:
        *   `new_min_r`: Calculated=2, Expected=2 (Matches initial)
        *   `new_max_r`: Calculated=9, Expected=8 (Expected is one less than marker row 9)
        *   `new_min_c`: Calculated=1, Expected=2 (Expected is one more than marker col 1)
        *   `new_max_c`: Calculated=6, Expected=6 (Matches initial)

*   **Example 2 Analysis:**
    *   Initial bbox: (1, 1, 4, 6)
    *   Markers: (2, 11) [Right], (6, 4) [Below]
    *   Calculated `new_bbox`: (1, 1, 6, 11)
    *   Expected `new_bbox`: (1, 1, 5, 10)
    *   Comparison:
        *   `new_min_r`: Calculated=1, Expected=1 (Matches initial)
        *   `new_max_r`: Calculated=6, Expected=5 (Expected is one less than marker row 6)
        *   `new_min_c`: Calculated=1, Expected=1 (Matches initial)
        *   `new_max_c`: Calculated=11, Expected=10 (Expected is one less than marker col 11)

**Consistent Pattern:** The new bounding box seems to extend *towards* the relevant external markers, but stops *one step short* of the marker's row/column.
*   New Top Row = `min(initial_min_r, min(marker_r + 1 for markers above))` -> Actually, looks like `new_min_r = initial_min_r` if no markers above, otherwise `min(marker_r + 1 for markers above)`. But wait, if `marker_r < initial_min_r`, then `marker_r + 1` could still be less than `initial_min_r`. Let's simplify:
    *   `target_min_r = min(marker_r + 1 for markers above)` if markers above exist, else `rows`
    *   `new_min_r = min(initial_min_r, target_min_r)`

*   New Bottom Row = `max(initial_max_r, max(marker_r - 1 for markers below))`
    *   `target_max_r = max(marker_r - 1 for markers below)` if markers below exist, else `-1`
    *   `new_max_r = max(initial_max_r, target_max_r)`

*   New Left Col = `min(initial_min_c, min(marker_c + 1 for markers left))`
    *   `target_min_c = min(marker_c + 1 for markers left)` if markers left exist, else `cols`
    *   `new_min_c = min(initial_min_c, target_min_c)`

*   New Right Col = `max(initial_max_c, max(marker_c - 1 for markers right))`
    *   `target_max_c = max(marker_c - 1 for markers right)` if markers right exist, else `-1`
    *   `new_max_c = max(initial_max_c, target_max_c)`

Let's re-test this logic on the examples:

*   **Example 1:** Initial(2, 4, 4, 6), Markers(3, 1)[L], (9, 5)[B]
    *   Above: None -> `target_min_r = rows` -> `new_min_r = min(2, rows) = 2`
    *   Below: `max(9-1) = 8` -> `target_max_r = 8` -> `new_max_r = max(4, 8) = 8`
    *   Left: `min(1+1) = 2` -> `target_min_c = 2` -> `new_min_c = min(4, 2) = 2`
    *   Right: None -> `target_max_c = -1` -> `new_max_c = max(6, -1) = 6`
    *   Result: (2, 2, 8, 6). **Matches Expected!**

*   **Example 2:** Initial(1, 1, 4, 6), Markers(2, 11)[R], (6, 4)[B]
    *   Above: None -> `new_min_r = 1`
    *   Below: `max(6-1) = 5` -> `target_max_r = 5` -> `new_max_r = max(4, 5) = 5`
    *   Left: None -> `new_min_c = 1`
    *   Right: `max(11-1) = 10` -> `target_max_c = 10` -> `new_max_c = max(6, 10) = 10`
    *   Result: (1, 1, 5, 10). **Matches Expected!**

*   **Example 3:** Initial(3, 4, 7, 9), Markers(4, 12)[R], (6, 1)[L], (14, 7)[B]
    *   Above: None -> `new_min_r = 3`
    *   Below: `max(14-1) = 13` -> `target_max_r = 13` -> `new_max_r = max(7, 13) = 13`
    *   Left: `min(1+1) = 2` -> `target_min_c = 2` -> `new_min_c = min(4, 2) = 2`
    *   Right: `max(12-1) = 11` -> `target_max_c = 11` -> `new_max_c = max(9, 11) = 11`
    *   Result: (3, 2, 13, 11). **Matches Expected!**

This bounding box calculation seems correct.

**Remaining Issues:**
1.  **Drawing the Hollow Frame:** The code needs to draw only the perimeter defined by the *new* bounding box.
2.  **Internal Structure (Example 3):** The expected output for Example 3 has internal green lines `(5, 2)-(5, 11)` and `(3, 7)-(13, 7)`. These correspond to row 5 and column 7 within the new bounding box (3, 2, 13, 11). Looking at the *input* grid and the *initial* bounding box (3, 4, 7, 9), row 5 and column 7 contain green pixels within that initial frame: `input[5, 4:10]` is `[3,3,3,3,3,3]` and `input[3:8, 7]` is `[3, 3, 3, 3, 3]`. It looks like any row or column that contained *any* green pixel within the *initial* frame gets "extended" to fill the width/height of the *new* frame. This needs careful implementation.

**Refined Drawing Logic:**
1.  Create a blank output grid.
2.  Calculate the `new_bbox`.
3.  Draw the outer perimeter of the `new_bbox` in green.
4.  Identify rows within the `initial_bbox` that contain green pixels: `initial_rows_with_green = {r for r, c in initial_frame_coords}`.
5.  Identify columns within the `initial_bbox` that contain green pixels: `initial_cols_with_green = {c for r, c in initial_frame_coords}`.
6.  For each `r` in `initial_rows_with_green`, draw a green horizontal line in the output grid at row `r` spanning from `new_min_c` to `new_max_c`.
7.  For each `c` in `initial_cols_with_green`, draw a green vertical line in the output grid at column `c` spanning from `new_min_r` to `new_max_r`.
8.  Redraw the magenta markers.

Let's dry run this refined logic for Example 1:
*   Initial bbox: (2, 4, 4, 6). New bbox: (2, 2, 8, 6).
*   Initial frame coords contain rows {2, 3, 4} and cols {4, 5, 6}.
*   Output grid initialized to white.
*   Draw outer frame (2, 2, 8, 6).
*   Draw horizontal lines: row 2 (cols 2-6), row 3 (cols 2-6), row 4 (cols 2-6).
*   Draw vertical lines: col 4 (rows 2-8), col 5 (rows 2-8), col 6 (rows 2-8).
*   Redraw markers (3, 1) and (9, 5).
*   Does this match expected output 1?
    *   Expected frame: (2, 2, 8, 6). Outer frame is correct.
    *   Expected interior: Only white.
    *   My dry run fills the *entire* new bounding box with green! This is wrong.

**Alternative Internal Structure Hypothesis:** Maybe the internal structure is simply copied from the input frame, shifted? No, the dimensions change.

Let's reconsider the "hollow frame" idea. The previous code failed because it drew solid lines using slicing `output_grid[r1, c1:c2+1] = 3`. A correct hollow frame drawing should only set the pixels *on* the perimeter.


```python
# Corrected drawing for hollow frame
output_grid[new_min_r, new_min_c:new_max_c+1] = 3  # Top
output_grid[new_max_r, new_min_c:new_max_c+1] = 3  # Bottom
output_grid[new_min_r:new_max_r+1, new_min_c] = 3  # Left
output_grid[new_min_r:new_max_r+1, new_max_c] = 3  # Right
```

This looks correct for drawing a hollow rectangle.

Why did Example 3's expected output have internal lines? Let's re-examine `expected_output_grid_3`.
Rows 3, 4, 5... 13. Cols 2, 3, 4... 11. Bbox (3, 2, 13, 11).
Internal pixels:
`expected_output_grid_3[4, 7] == 3`
`expected_output_grid_3[5, 2:12] == 3` (all 3s except marker at [5,11]?) No, marker is at (4,12) outside. `expected_output_grid_3[5, 2:12]` should be `[3, 3, 3, 3, 3, 3, 3, 3, 3, 3]`.
`expected_output_grid_3[6:13, 7] == 3`

Okay, the internal structure *is* present in Example 3's expected output.
Where did it come from? Input frame BBox (3, 4, 7, 9).
Internal structure input:
Row 4: `input[4, 5:9]` = `[0, 0, 3, 0]`
Row 5: `input[5, 4:10]` = `[3, 3, 3, 3, 3, 3]`
Row 6: `input[6, 5:9]` = `[0, 0, 3, 0]`
Col 4: `input[4:7, 4]` = `[3, 3, 3]`
Col 7: `input[4:7, 7]` = `[3, 3, 3]`
Col 9: `input[4:7, 9]` = `[3, 3, 3]`

Compare input internal structure rows/cols with output internal structure rows/cols:
Output internal green is on row 5 and col 7.
Input internal green exists on rows {4, 5, 6} and cols {4, 7, 9}.
Row 5 and Col 7 are common.

**Hypothesis 3 (Internal Structure):**
1. Find the initial green frame object and its bounding box (`initial_bbox`).
2. Find magenta markers.
3. Calculate the new bounding box (`new_bbox`) using the "stop one step short" logic.
4. Create a blank output grid.
5. Draw the hollow rectangle defined by `new_bbox` onto the output grid using green.
6. Identify the "internal" coordinates of the *initial* green frame object: `internal_coords = {(r, c) for (r, c) in initial_frame_coords if initial_min_r < r < initial_max_r and initial_min_c < c < initial_max_c}`.
7. Determine the relative offset of these internal coordinates within the `initial_bbox`: `relative_internal_coords = {(r - initial_min_r, c - initial_min_c) for (r, c) in internal_coords}`.
8. Map these relative coordinates to the `new_bbox` and draw them green on the output grid: `for rel_r, rel_c in relative_internal_coords: output_r = new_min_r + rel_r; output_c = new_min_c + rel_c; if new_min_r < output_r < new_max_r and new_min_c < output_c < new_max_c: output_grid[output_r, output_c] = 3`. This assumes a simple scaling/translation, which might be wrong if the aspect ratio changes significantly.

Let's test Hypothesis 3 on Example 3:
*   `initial_bbox` = (3, 4, 7, 9)
*   `new_bbox` = (3, 2, 13, 11)
*   `initial_frame_coords`: {(3,4), (3,5)... (4,4), (4,7), (4,9), (5,4)...(5,9), (6,4), (6,7), (6,9), (7,4)...(7,9)}
*   `internal_coords`: {(4,7), (5,5), (5,6), (5,7), (5,8), (6,7)} - Only pixels strictly inside the bbox. Let's check input: (4,7)=3, (5,5)=3, (5,6)=3, (5,7)=3, (5,8)=3, (6,7)=3. Yes.
*   `relative_internal_coords`: {(1,3), (2,1), (2,2), (2,3), (2,4), (3,3)} (relative to (3,4))
*   Map to `new_bbox`:
    *   (1,3) -> (3+1, 2+3) = (4, 5) -> `output[4, 5] = 3`
    *   (2,1) -> (3+2, 2+1) = (5, 3) -> `output[5, 3] = 3`
    *   (2,2) -> (3+2, 2+2) = (5, 4) -> `output[5, 4] = 3`
    *   (2,3) -> (3+2, 2+3) = (5, 5) -> `output[5, 5] = 3`
    *   (2,4) -> (3+2, 2+4) = (5, 6) -> `output[5, 6] = 3`
    *   (3,3) -> (3+3, 2+3) = (6, 5) -> `output[6, 5] = 3`
*   This does *not* match the expected internal structure (row 5, col 7).

**Hypothesis 4 (Internal Structure):**
Perhaps the rule isn't about individual pixels but about preserving the *topology* or *features* like lines.
Input frame has horizontal line segments at rows 3, 5, 7 and vertical segments at cols 4, 7, 9.
Output frame has horizontal segments at rows 3, 5, 6, 13 and vertical segments at cols 2, 7, 11. (Derived from expected output grid).
This doesn't seem right either.

Let's revisit the idea of extending rows/columns containing green.
1. Calculate `new_bbox` = (3, 2, 13, 11)
2. Find all coordinates of the original green object: `initial_obj_coords`.
3. Create blank output grid.
4. For each `(r, c)` in `initial_obj_coords`:
    *   Draw a horizontal green line segment in the output at row `r` from `new_min_c` to `new_max_c`.
    *   Draw a vertical green line segment in the output at column `c` from `new_min_r` to `new_max_r`.
5. Redraw magenta markers.

Test Hypothesis 4 on Example 1:
*   `new_bbox` = (2, 2, 8, 6)
*   `initial_obj_coords` include rows {2, 3, 4} and cols {4, 5, 6}.
*   Draw H-lines at r=2, 3, 4 (cols 2-6).
*   Draw V-lines at c=4, 5, 6 (rows 2-8).
*   This *still* fills the entire box green.

**Hypothesis 5 (Simplest):**
The transformation calculates the new bounding box and draws *only* a hollow rectangle. The internal structure in Example 3's expected output might be an anomaly or misinterpreted. Let's assume the goal is *always* a hollow rectangle based on the expanded bounds. This matches Examples 1 & 2 perfectly if the drawing is corrected. Example 3's expected output might be wrong in the problem description, or there's a nuance missed. But given the failures across the board seem related to filling vs hollow, fixing the drawing and the bounding box calculation seems primary.

Let's proceed with the "hollow rectangle" assumption, using the corrected bounding box logic.

**Final Check on Logic:**
1. Identify green objects (frames) and get their coordinates.
2. For each frame, get its initial bounding box (`initial_bbox`).
3. Identify all magenta markers.
4. For each frame, calculate its `new_bbox` based on `initial_bbox` and *all* magenta markers *outside* the `initial_bbox`, using the "stop one step short" rule:
    * `target_min_r = min(m_r + 1 for m in markers if m_r < initial_min_r)` or `rows`
    * `new_min_r = min(initial_min_r, target_min_r)`
    * `target_max_r = max(m_r - 1 for m in markers if m_r > initial_max_r)` or `-1`
    * `new_max_r = max(initial_max_r, target_max_r)`
    * `target_min_c = min(m_c + 1 for m in markers if m_c < initial_min_c)` or `cols`
    * `new_min_c = min(initial_min_c, target_min_c)`
    * `target_max_c = max(m_c - 1 for m in markers if m_c > initial_max_c)` or `-1`
    * `new_max_c = max(initial_max_c, target_max_c)`
5. Create a blank (white) output grid.
6. For each calculated `new_bbox`, draw a hollow green rectangle on the output grid using the perimeter coordinates.
7. Draw all original magenta markers onto the output grid.


This seems the most consistent approach covering the first two examples perfectly and matching the *bounding box* of the third example. The discrepancy is the internal structure in Example 3's expected output vs the hollow frame produced by this logic. Given the simple hollow frames in Ex1 and Ex2 outputs, this revised logic is the most probable general rule.

---
## General Assessment

The previous code failed primarily because:
1.  **Incorrect Bounding Box Calculation:** The expansion logic extended the frame boundaries *to* the row/column of the outermost markers, whereas the examples show the expansion stops *one step before* the marker's row/column.
2.  **Incorrect Frame Drawing:** The code drew filled lines or potentially filled the entire new bounding box area with green, instead of drawing only the hollow perimeter of the new frame. The expected outputs for Examples 1 and 2 clearly show hollow frames (interior remains white). Example 3's expected output is ambiguous as it shows some internal green structure, but the primary error across all examples points towards fixing the bounding box calculation and ensuring a hollow frame is drawn.

The strategy is to:
1.  Correct the calculation of the new bounding box dimensions based on the "stop one step short" observation.
2.  Implement drawing logic that strictly draws only the perimeter of the calculated new bounding box.
3.  Assume the transformation produces a hollow rectangle, pending further evidence contradicting this for Example 3.
4.  Ensure magenta markers are correctly preserved by drawing them last.

## Metrics

Based on code execution analysis (`code_output` blocks above):

**Example 1:**
*   Input Grid: 11x15
*   Input Green Frame: 1 object, BBox=(2, 4, 4, 6)
*   Input Magenta Markers: [(3, 1), (9, 5)]
*   Expected Output Green Frame BBox: (2, 2, 8, 6)
*   Calculated New BBox (Original Code): (2, 1, 9, 6) - Incorrect
*   Calculated New BBox (Revised Logic): (2, 2, 8, 6) - **Matches Expected**
*   Expected Output Markers: [(3, 1), (9, 5)] (Match Input)
*   Expected Output Frame: Hollow

**Example 2:**
*   Input Grid: 8x17
*   Input Green Frame: 1 object, BBox=(1, 1, 4, 6)
*   Input Magenta Markers: [(2, 11), (6, 4)]
*   Expected Output Green Frame BBox: (1, 1, 5, 10)
*   Calculated New BBox (Original Code): (1, 1, 6, 11) - Incorrect
*   Calculated New BBox (Revised Logic): (1, 1, 5, 10) - **Matches Expected**
*   Expected Output Markers: [(2, 11), (6, 4)] (Match Input)
*   Expected Output Frame: Hollow

**Example 3:**
*   Input Grid: 15x15
*   Input Green Frame: 1 object, BBox=(3, 4, 7, 9)
*   Input Magenta Markers: [(4, 12), (6, 1), (14, 7)]
*   Expected Output Green Frame BBox: (3, 2, 13, 11)
*   Calculated New BBox (Original Code): (3, 1, 14, 12) - Incorrect
*   Calculated New BBox (Revised Logic): (3, 2, 13, 11) - **Matches Expected**
*   Expected Output Markers: [(4, 12), (6, 1), (14, 7)] (Match Input)
*   Expected Output Frame: Shows internal structure (Row 5, Col 7), not strictly hollow based on visual inspection and the `is_hollow=False` check previously run (though that check might be too simple if internal structures are allowed). **Discrepancy:** Revised logic produces a hollow frame.

## Facts


```yaml
task_description: Transforms input grids containing green frame-like objects and magenta markers into output grids with resized green frames and original markers.

grid_properties:
  - background_color: 0 (white)
  - dimensions: variable (up to 30x30)

objects:
  - object_type: frame
    color: 3 (green)
    properties:
      - represents a connected component of green pixels, often resembling a rectangle but may have internal gaps or structures.
      - characterized by an initial bounding box (min_row, min_col, max_row, max_col).
  - object_type: marker
    color: 6 (magenta)
    properties:
      - single pixels.
      - location relative to frames determines the transformation.

transformation:
  - action: identify_objects
    inputs: [input_grid]
    outputs: [green_frames (coordinates sets), magenta_markers (coordinate list)]
  - action: calculate_initial_bboxes
    inputs: [green_frames]
    outputs: [initial_bboxes (list of tuples)]
  - action: calculate_new_bboxes
    inputs: [initial_bboxes, magenta_markers, grid_dims]
    outputs: [new_bboxes (list of tuples)]
    rule: |
      For each initial_bbox (min_r, min_c, max_r, max_c):
      Find markers strictly outside the initial_bbox.
      Determine target boundaries based on these external markers, stopping one step short:
        target_min_r = min(m_r + 1 for markers above initial_bbox) if any, else grid_height
        target_max_r = max(m_r - 1 for markers below initial_bbox) if any, else -1
        target_min_c = min(m_c + 1 for markers left of initial_bbox) if any, else grid_width
        target_max_c = max(m_c - 1 for markers right of initial_bbox) if any, else -1
      Calculate the new_bbox:
        new_min_r = min(initial_min_r, target_min_r)
        new_max_r = max(initial_max_r, target_max_r)
        new_min_c = min(initial_min_c, target_min_c)
        new_max_c = max(initial_max_c, target_max_c)
  - action: create_output_grid
    inputs: [input_grid_dims]
    outputs: [output_grid (initialized to white)]
  - action: draw_frames
    inputs: [output_grid, new_bboxes]
    outputs: [output_grid (modified)]
    rule: For each new_bbox, draw a hollow green rectangle on the output_grid corresponding to its perimeter.
  - action: draw_markers
    inputs: [output_grid, magenta_markers]
    outputs: [output_grid (modified)]
    rule: Draw each magenta marker at its original coordinates on the output_grid.

uncertainties:
  - The exact drawing rule for Example 3's output. The expected output shows internal green lines not accounted for by a simple hollow rectangle rule. Assuming hollow rectangle for now as it fits Examples 1 & 2.
```


## Natural Language Program

1.  Initialize an empty output grid with the same dimensions as the input grid, filled with the background color (white, 0).
2.  Identify all magenta (6) pixels (markers) and store their coordinates.
3.  Identify all distinct connected green (3) objects (frames).
4.  For each green frame object:
    a.  Determine its initial bounding box (the smallest rectangle enclosing all its pixels).
    b.  Find all magenta markers located strictly outside this initial bounding box.
    c.  Calculate the target expansion boundaries based *only* on these external markers:
        i.  `target_top_row`: If there are markers above the initial box, find the row of the lowest such marker and add 1. Otherwise, use a value outside the grid (e.g., grid height).
        ii. `target_bottom_row`: If there are markers below the initial box, find the row of the highest such marker and subtract 1. Otherwise, use a value outside the grid (e.g., -1).
        iii. `target_left_col`: If there are markers left of the initial box, find the column of the rightmost such marker and add 1. Otherwise, use a value outside the grid (e.g., grid width).
        iv. `target_right_col`: If there are markers right of the initial box, find the column of the leftmost such marker and subtract 1. Otherwise, use a value outside the grid (e.g., -1).
    d.  Determine the final new bounding box for the frame by taking the union of the initial bounding box and the area defined by the target boundaries:
        i.  `new_top_row` = minimum of `initial_top_row` and `target_top_row`.
        ii. `new_bottom_row` = maximum of `initial_bottom_row` and `target_bottom_row`.
        iii. `new_left_col` = minimum of `initial_left_col` and `target_left_col`.
        iv. `new_right_col` = maximum of `initial_right_col` and `target_right_col`.
    e.  Draw a hollow green rectangle on the output grid using the `new_top_row`, `new_bottom_row`, `new_left_col`, and `new_right_col` as the perimeter coordinates.
5.  After processing all green frames, redraw all the original magenta markers at their initial coordinates onto the output grid (potentially overwriting green pixels from the drawn frames if a marker falls on a new perimeter).
6.  Return the final output grid.