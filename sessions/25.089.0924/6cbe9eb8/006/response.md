**General Assessment**

The previous attempt failed because the frame identification logic was flawed. It relied on finding perfect, single-color rectangles using `np.argwhere` and bounding boxes, which failed when the frame wasn't perfectly rectangular (Ex 2) or when multiple potential rectangular shapes existed (Ex 1, Ex 3 - finding inner shapes or incorrect frames). The background filtering was dependent on the correctly identified frame and its adjacent external colors, leading to further errors.

The new strategy focuses on:
1.  Defining a fixed set of background colors {white:0, blue:1, red:2, green:3}.
2.  Identifying the area of interest by finding the bounding box of *all* non-background pixels.
3.  Determining the frame color by checking which single, non-background color forms a 1-pixel border around this bounding box.
4.  Extracting the content within this frame (bounding box minus the 1-pixel border).
5.  Filtering this extracted content by replacing pixels matching the background colors {0, 1, 2, 3} with white (0).
6.  Constructing the output grid with the identified frame color as the border and the filtered content inside.

This revised approach correctly handles all three examples conceptually and aligns with the observed input-output transformations.

**Metrics Analysis**

*   **Example 1:**
    *   `input_shape`: (14, 22), `output_shape`: (12, 11)
    *   `input_colors`: {0, 1, 2, 3, 4, 5, 6, 8} (white, blue, red, green, yellow, gray, magenta, azure)
    *   `output_colors`: {0, 4, 5, 6, 8} (white, yellow, gray, magenta, azure)
    *   `non_background_bbox`: (r=1, c=1) -> (r=12, c=18)
    *   *Failure*: Incorrect frame ID led to wrong size (6, 7) and content (only yellow/gray kept, border missing).
    *   *Correction Need*: Identify frame based on non-background bbox (1,1)-(12,18). Check perimeter for single color. Azure (8) forms the relevant border sections. Inner area (2,2)-(11,17). Filter using {0,1,2,3}.

*   **Example 2:**
    *   `input_shape`: (13, 23), `output_shape`: (9, 12)
    *   `input_colors`: {0, 1, 2, 3, 4, 6, 8} (white, blue, red, green, yellow, magenta, azure)
    *   `output_colors`: {0, 3, 4, 6, 8} (white, green, yellow, magenta, azure)
    *   `non_background_bbox`: (r=0, c=14) -> (r=5, c=18). *Wait*, the code output for this bbox is wrong. Let's re-run the calculation mentally. Non-background = {3, 4, 6, 8}. Coords for 3: (3,5)-(3,13), (11,5)-(11,16), (4,5)-(10,5), ... BBox should be much larger. The code used `invert=True` on `np.isin` - maybe that's only checking *not* 0, 1, 2, *or* 3? Yes. Correct non-bg set {4, 5, 6, 8} for Ex 1, {4, 6, 8} for Ex 2, {4, 8} for Ex 3. Let's recalculate the bboxes based on these sets.
        *   Ex 1: {4,5,6,8}. Min/Max Rs: 1, 12. Min/Max Cs: 1, 18. BBox: (1,1) -> (12,18). Correct.
        *   Ex 2: {4,6,8}. Min/Max Rs: 1, 5. Min/Max Cs: 14, 18. BBox: (1,14) -> (5,18). Correct.
        *   Ex 3: {4,8}. Min/Max Rs: 2, 7. Min/Max Cs: 3, 14. BBox: (2,3) -> (7,14). Correct.
    *   *Failure*: Frame finding failed entirely (returned input).
    *   *Correction Need*: Identify frame based on non-background bbox (1,14)-(5,18). The actual frame uses Green(3). This contradicts the non-background definition.

**Revised Revised Hypothesis:**
The background isn't *just* {0,1,2,3}. The *frame* color is also not part of the "content".
1.  Identify the single color `C` that forms a 1-pixel thick perimeter enclosing some area. This must be the frame identification step. Use the `_find_potential_frames` logic, but maybe simplify the thickness check. Find the largest such frame.
2.  Let the frame color be `frame_color` and its outer bounding box be `(min_r, min_c) -> (max_r, max_c)`.
3.  Identify background colors: {0} plus any colors adjacent *outside* the frame's bounding box. `bg_colors = {0}.union(_get_adjacent_outside_colors(grid, min_r, min_c, max_r, max_c))`
4.  Extract inner region: `grid[min_r+1:max_r, min_c+1:max_c]`
5.  Filter: Replace pixels in `bg_colors` with 0.
6.  Construct output.

Let's re-test this on the failures:
*   **Ex 1:** Largest frame is Azure(8) at (1,1)-(12,11). `frame_color=8`. Adjacent outside colors = {0, 1, 2, 3}. `bg_colors = {0, 1, 2, 3}`. Inner region `grid[2:12, 2:11]` contains {0,1,2,3,4,5,6}. Filter {0,1,2,3} -> 0. Keep {4,5,6}. Looks correct.
*   **Ex 2:** Frame finding failed previously. Why? The Green(3) object isn't a perfect rectangle defined by its min/max coords. The `_find_potential_frames` check `np.all(grid[min_r, min_c:max_c + 1] == color)` fails because the top edge has 0s/1s/2s interspersed. Frame finding needs to be more robust - perhaps find largest connected component of a single color, check if it's 1 pixel thick and encloses other colors.
*   **Ex 3:** Previous code found Green(3) at (1,2)-(8,9). Adjacent outside = {0, 1}. `bg_colors = {0, 1}`. Inner region `grid[2:8, 3:9]` contains only {8}. Filtering keeps {8}. The Yellow(4) object at `grid[4:7, 12:15]` is *outside* this frame. This means the frame found (1,2)-(8,9) is *wrong*. The *intended* frame must enclose the 4s as well.

**Conclusion:** The core difficulty is robustly identifying the correct "frame" and the "content" it encloses, especially when the frame isn't a simple rectangle or when multiple potential frames exist. The definition of "background" also seems tied to what's *outside* the true frame.

**Final Approach Attempt:**
1.  Find *all* potential frames using the `_find_potential_frames` logic (single color, 1-pixel thick, hollow rectangle based on its own bounding box).
2.  For each potential frame `F` with color `C_F` and outer bounds `B_F`:
    *   Define its inner region `I_F`.
    *   Define background colors `BG_F = {0} + colors adjacent outside B_F`.
    *   Create a candidate output by filtering `I_F` (replace `BG_F` colors with 0) and adding `C_F` border.
3.  Select the candidate output that seems "best" - perhaps largest size, or most non-white pixels? Compare against expected outputs. All expected outputs are rectangular and contain non-background colors.
4.  Try selecting the frame that encloses the largest number of non-zero pixels that are *not* the frame color and *not* the adjacent background colors.


```yaml
elements:
  - element: background_pixels
    description: Pixels considered part of the background noise or pattern, primarily located outside the main frame. Often consists of low-value colors (0, 1, 2, 3 in examples) in a repeating pattern. White (0) is always considered background. The exact set can also include colors found immediately adjacent to the outside of the identified frame.
    properties:
      - low_value_colors (often 0, 1, 2, 3)
      - repetitive_pattern (often)
      - located_outside_frame (primarily)
      - includes_white (0)
      - includes_colors_adjacent_outside_frame
  - element: frame
    description: A hollow, rectangular structure, exactly one pixel thick, made of a single non-background color. It encloses the 'content_pixels'. Identified as the largest valid frame object in the input.
    properties:
      - rectangular_shape
      - hollow
      - thickness_1_pixel
      - single_color
      - non_background_color
      - encloses_content_pixels
      - largest_valid_frame (heuristic)
  - element: content_pixels
    description: Pixels located spatially inside the 'frame'. These include the actual objects of interest and potentially some 'background_pixels' that need filtering.
    properties:
      - located_inside_frame
      - may_include_objects_of_interest
      - may_include_background_pixels

actions:
  - action: identify_candidate_frames
    description: Find all single-colored, non-white, 1-pixel thick, hollow rectangular structures in the input grid based on their own bounding boxes.
  - action: select_main_frame
    description: From the candidates, select the 'best' frame. Heuristic likely involves selecting the largest frame (by area or perimeter). Record its color (`frame_color`) and outer bounding box (`frame_bounds`).
  - action: determine_background_colors
    description: Create a set of background colors consisting of white (0) plus all unique colors found immediately adjacent to the *outside* perimeter defined by `frame_bounds`.
  - action: extract_inner_content
    description: Select the portion of the input grid located strictly inside the `frame_bounds` (i.e., excluding the frame itself).
  - action: filter_background_from_content
    description: Within the extracted inner content, replace any pixel whose color belongs to the determined background color set with white (0).
  - action: construct_output
    description: Create a new grid sized to fit the inner content plus a 1-pixel border. Draw the border using `frame_color`. Place the filtered inner content into the center.

relationships:
  - relationship: containment
    description: The selected 'frame' contains the 'content_pixels'.
  - relationship: adjacency
    description: The 'background_pixels' used for filtering are determined by adjacency to the outside of the selected 'frame'.
  - relationship: filtering
    description: Pixels within the 'content_pixels' are checked against the 'background_colors'. If a match occurs, the pixel is replaced with white (0) in the output; otherwise, it's preserved.
```


**Natural Language Program**

1.  **Scan** the input grid to find all possible candidate "frames". A candidate frame must be a perfectly rectangular, hollow shape, exactly one pixel thick, composed of a single color (not white), based on the bounding box of that color's pixels.
2.  **Select** the "main frame" from the candidates. Use a heuristic: choose the frame with the largest area (height * width). Record its color (`frame_color`) and its outer bounding box coordinates (`min_r`, `min_c`, `max_r`, `max_c`). If no candidate frames are found, return the original input grid.
3.  **Determine** the set of `background_colors`. This set initially contains only white (0). Then, examine all pixels immediately adjacent to the *outside* of the main frame's bounding box (pixels at `r=min_r-1`, `r=max_r+1`, `c=min_c-1`, `c=max_c+1` where they exist within grid bounds and border the frame). Add all unique colors found in these adjacent positions to the `background_colors` set.
4.  **Calculate** the dimensions of the region strictly inside the main frame: `inner_height = max_r - min_r - 1`, `inner_width = max_c - min_c - 1`.
5.  **Create** a new output grid initialized with white (0), with dimensions `(inner_height + 2) x (inner_width + 2)`.
6.  **Draw** a border, one pixel thick, around the edge of the output grid using the `frame_color`.
7.  **Iterate** through each pixel `(r_in, c_in)` within the inner region of the input grid (from `r = min_r + 1` to `max_r - 1`, and `c = min_c + 1` to `max_c - 1`). Let the color of this input pixel be `P`.
8.  **Calculate** the corresponding position `(r_out, c_out)` in the output grid's interior (`r_out = r_in - min_r`, `c_out = c_in - min_c`).
9.  **Check** if the input pixel color `P` is present in the `background_colors` set.
10. **If** `P` is *not* in `background_colors`, set the pixel at `(r_out, c_out)` in the output grid to `P`. (Otherwise, leave it as the initialized white color).
11. **Output** the completed grid.**General Assessment**

The previous code failed primarily due to an incorrect frame identification strategy and, consequently, incorrect background color determination.
*   **Example 1:** Identified an inner yellow shape as the frame instead of the outer azure one.
*   **Example 2:** Failed to identify any frame because the correct green frame wasn't a perfect rectangle fill within its bounding box. The frame-finding logic (`_find_potential_frames`) required all pixels on the perimeter defined by `min_r, min_c, max_r, max_c` to be the frame color, which wasn't true here.
*   **Example 3:** Identified a smaller green frame, excluding the yellow object which should have been part of the content. This again stemmed from the frame identification logic selecting the wrong candidate.

The core issues are:
1.  **Frame Identification:** The logic must correctly identify the single, intended frame object, even if it's not a perfect rectangle or if other shapes exist. The heuristic of selecting the largest frame by area seems promising based on the examples.
2.  **Background Definition:** The background colors to be filtered from the inside seem to be defined by white (0) plus whatever colors are immediately adjacent to the *outside* of the correctly identified frame.

The refined strategy is to find all candidate rectangular frames, select the largest one by area, determine background colors based on its exterior adjacency, and then filter the content within that frame.

**Metrics Analysis**

``` python
import numpy as np

def get_metrics(input_grid_list, output_grid_list, transformed_grid_list, example_num):
    input_grid = np.array(input_grid_list)
    output_grid = np.array(output_grid_list)
    transformed_grid = np.array(transformed_grid_list) if transformed_grid_list else np.array([[]])

    metrics = {}
    metrics['example'] = example_num
    metrics['input_shape'] = input_grid.shape
    metrics['output_shape'] = output_grid.shape
    metrics['transformed_shape'] = transformed_grid.shape if transformed_grid.size > 0 else (0, 0)

    metrics['input_colors'] = sorted(list(np.unique(input_grid)))
    metrics['output_colors'] = sorted(list(np.unique(output_grid)))
    metrics['transformed_colors'] = sorted(list(np.unique(transformed_grid))) if transformed_grid.size > 0 else []

    metrics['output_size_correct'] = (metrics['output_shape'] == metrics['transformed_shape'])
    metrics['output_colors_correct'] = (metrics['output_colors'] == metrics['transformed_colors'])

    if metrics['output_size_correct']:
        match = np.array_equal(output_grid, transformed_grid)
        metrics['match'] = bool(match)
        metrics['pixels_off'] = int(np.sum(output_grid != transformed_grid)) if not match else 0
    else:
        metrics['match'] = False
        metrics['pixels_off'] = None # Cannot compare pixels if shapes differ

    print(metrics)

# --- Example 1 Data ---
input_1 = [[0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1],[1,8,8,8,8,8,8,8,8,8,8,8,1,2,3,0,1,2,3,0,1,2],[0,8,2,3,0,1,2,3,0,1,2,8,0,1,2,3,0,1,2,3,0,1],[1,8,3,0,1,2,3,0,4,4,4,4,4,4,4,0,1,2,3,0,1,2],[0,8,2,3,0,1,2,3,4,5,5,5,5,5,4,3,0,1,2,3,0,1],[1,8,3,0,1,2,3,0,4,5,5,5,5,5,4,0,1,2,3,0,1,2],[0,8,2,3,0,1,2,3,4,5,5,5,5,5,4,3,0,1,2,3,0,1],[1,8,3,0,1,2,3,0,4,5,5,5,5,5,4,0,1,2,3,0,1,2],[0,8,2,3,0,1,2,3,4,4,4,4,4,4,4,3,0,6,6,3,0,1],[1,8,3,0,1,2,3,0,1,2,3,8,1,2,3,0,1,6,6,0,1,2],[0,8,2,3,0,1,2,3,0,1,2,8,0,1,2,3,0,1,2,3,0,1],[1,8,3,0,1,2,3,0,1,2,3,8,1,2,3,0,1,2,3,0,1,2],[0,8,8,8,8,8,8,8,8,8,8,8,0,1,2,3,0,1,2,3,0,1],[1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1,2,3,0,1,2]]
output_1 = [[8,8,8,8,8,8,8,8,8,8,8],[8,0,0,0,0,0,0,0,0,0,8],[8,0,0,0,0,0,0,0,0,0,8],[8,0,0,0,0,0,0,0,0,0,8],[8,0,0,0,0,0,0,0,0,0,8],[8,4,4,4,4,4,4,4,0,0,8],[8,4,5,5,5,5,5,4,0,0,8],[8,4,5,5,5,5,5,4,0,0,8],[8,4,6,6,5,5,5,4,0,0,8],[8,4,6,6,5,5,5,4,0,0,8],[8,4,4,4,4,4,4,4,0,0,8],[8,8,8,8,8,8,8,8,8,8,8]]
# Previous transformed output was based on incorrect frame ID
transformed_1 = [[4,4,4,4,4,4,4],[4,5,5,5,5,5,4],[4,5,5,5,5,5,4],[4,5,5,5,5,5,4],[4,5,5,5,5,5,4],[4,4,4,4,4,4,4]]
print("--- Example 1 Metrics (Previous Run) ---")
get_metrics(input_1, output_1, transformed_1, 1)

# --- Example 2 Data ---
input_2 = [[0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,4,4,1,2,0,1],[1,2,0,1,2,0,1,2,0,1,2,0,1,2,8,8,8,4,4,2,0,1,2],[1,2,0,1,2,0,1,2,0,1,2,0,1,2,8,6,6,6,8,2,0,1,2],[0,1,2,0,1,3,3,3,3,3,3,3,3,3,8,6,6,6,8,1,2,0,1],[1,2,0,1,2,3,1,2,0,1,2,0,1,2,8,6,6,6,8,2,0,1,2],[1,2,0,1,2,3,1,2,0,1,2,0,1,2,8,8,8,8,8,2,0,1,2],[0,1,2,0,1,3,0,1,2,0,1,2,0,1,2,0,3,2,0,1,2,0,1],[1,2,0,1,2,3,1,2,0,1,2,0,1,2,0,1,3,0,1,2,0,1,2],[1,2,0,1,2,3,1,2,0,1,2,0,1,2,0,1,3,0,1,2,0,1,2],[0,1,2,0,1,3,0,1,2,0,1,2,0,1,2,0,3,2,0,1,2,0,1],[1,2,0,1,2,3,1,2,0,1,2,0,1,2,0,1,3,0,1,2,0,1,2],[1,2,0,1,2,3,3,3,3,3,3,3,3,3,3,3,3,0,1,2,0,1,2],[0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1,2,0,1]]
output_2 = [[3,3,3,3,3,3,3,3,3,3,3,3],[3,0,0,0,0,0,0,0,0,0,0,3],[3,0,0,0,0,0,0,0,0,0,0,3],[3,8,8,8,8,8,0,0,0,0,0,3],[3,8,6,6,6,8,0,0,0,0,0,3],[3,8,4,4,6,8,0,0,0,0,0,3],[3,8,4,4,6,8,0,0,0,0,0,3],[3,8,8,8,8,8,0,0,0,0,0,3],[3,3,3,3,3,3,3,3,3,3,3,3]]
# Previous transformed output was original input because no frame found
transformed_2 = input_2
print("\n--- Example 2 Metrics (Previous Run) ---")
get_metrics(input_2, output_2, transformed_2, 2)

# --- Example 3 Data ---
input_3 = [[0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],[1,0,3,3,3,3,3,3,3,3,1,0,1,0,1,0,1,0,1,0,1,0,1],[0,1,3,8,8,8,8,8,8,3,0,1,0,1,0,1,0,1,0,1,0,1,0],[1,0,3,8,8,8,8,8,8,3,1,0,1,0,1,0,1,0,1,0,1,0,1],[0,1,3,8,8,8,8,8,8,3,0,1,4,4,4,1,0,1,0,1,0,1,0],[1,0,3,8,8,8,8,8,8,3,1,0,4,4,4,0,1,0,1,0,1,0,1],[0,1,3,8,8,8,8,8,8,3,0,1,4,4,4,1,0,1,0,1,0,1,0],[1,0,3,8,8,8,8,8,8,3,1,0,1,0,1,0,1,0,1,0,1,0,1],[0,1,3,3,3,3,3,3,3,3,0,1,0,1,0,1,0,1,0,1,0,1,0],[1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],[0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],[1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],[0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],[1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1],[0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0],[1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1,0,1]]
output_3 = [[3,3,3,3,3,3,3,3],[3,8,8,8,8,8,8,3],[3,8,8,8,8,8,8,3],[3,8,8,8,8,8,8,3],[3,4,4,4,8,8,8,3],[3,4,4,4,8,8,8,3],[3,4,4,4,8,8,8,3],[3,3,3,3,3,3,3,3]]
# Previous transformed output was based on incorrect frame ID, missing the yellow part
transformed_3 = [[3,3,3,3,3,3,3,3],[3,8,8,8,8,8,8,3],[3,8,8,8,8,8,8,3],[3,8,8,8,8,8,8,3],[3,8,8,8,8,8,8,3],[3,8,8,8,8,8,8,3],[3,8,8,8,8,8,8,3],[3,3,3,3,3,3,3,3]]
print("\n--- Example 3 Metrics (Previous Run) ---")
get_metrics(input_3, output_3, transformed_3, 3)
```
```
--- Example 1 Metrics (Previous Run) ---
{'example': 1, 'input_shape': (14, 22), 'output_shape': (12, 11), 'transformed_shape': (6, 7), 'input_colors': [np.int64(0), np.int64(1), np.int64(2), np.int64(3), np.int64(4), np.int64(5), np.int64(6), np.int64(8)], 'output_colors': [np.int64(0), np.int64(4), np.int64(5), np.int64(6), np.int64(8)], 'transformed_colors': [np.int64(4), np.int64(5)], 'output_size_correct': False, 'output_colors_correct': False, 'match': False, 'pixels_off': None}

--- Example 2 Metrics (Previous Run) ---
{'example': 2, 'input_shape': (13, 23), 'output_shape': (9, 12), 'transformed_shape': (13, 23), 'input_colors': [np.int64(0), np.int64(1), np.int64(2), np.int64(3), np.int64(4), np.int64(6), np.int64(8)], 'output_colors': [np.int64(0), np.int64(3), np.int64(4), np.int64(6), np.int64(8)], 'transformed_colors': [np.int64(0), np.int64(1), np.int64(2), np.int64(3), np.int64(4), np.int64(6), np.int64(8)], 'output_size_correct': False, 'output_colors_correct': False, 'match': False, 'pixels_off': None}

--- Example 3 Metrics (Previous Run) ---
{'example': 3, 'input_shape': (16, 23), 'output_shape': (8, 8), 'transformed_shape': (8, 8), 'input_colors': [np.int64(0), np.int64(1), np.int64(3), np.int64(4), np.int64(8)], 'output_colors': [np.int64(3), np.int64(4), np.int64(8)], 'transformed_colors': [np.int64(3), np.int64(8)], 'output_size_correct': True, 'output_colors_correct': False, 'match': False, 'pixels_off': 9}

```
**YAML Facts**


```yaml
elements:
  - element: potential_background_pattern
    description: Pixels often composed of low-value colors (e.g., white, blue, red, green - 0, 1, 2, 3) sometimes forming a repeating pattern, primarily outside the main frame.
    properties:
      - low_value_colors
      - often_repetitive
      - primarily_outside_frame
  - element: frame_object
    description: A structure, typically rectangular but not always perfectly filled, exactly one pixel thick, composed of a single non-white color. It encloses the content objects. It's identified as the 'best' candidate frame, often the largest by area.
    properties:
      - hollow_structure
      - thickness_1_pixel
      - single_color (non-white)
      - encloses_content_objects
      - identified_via_heuristics (e.g., largest area among valid candidates)
  - element: content_objects
    description: Discrete shapes or blocks of pixels located spatially inside the frame_object, whose colors are distinct from the frame color and typically distinct from the colors identified as background for filtering purposes.
    properties:
      - located_inside_frame
      - colors_distinct_from_frame
      - colors_distinct_from_filtered_background
      - contiguous_shapes (usually)
  - element: filtered_background_colors
    description: A set of colors dynamically determined for filtering. Always includes white (0). Also includes all unique colors found immediately adjacent to the *outside* border of the identified frame_object.
    properties:
      - includes_white_0
      - includes_colors_adjacent_to_outside_of_frame

actions:
  - action: identify_candidate_frames
    description: Find all single-colored, non-white, 1-pixel thick, hollow rectangular structures based on their individual bounding boxes. Check for perimeter completeness, hollowness, and external thickness=1 relative to *that color*.
  - action: select_main_frame
    description: Choose the best frame from the candidates, typically the one with the largest area (height * width). Record its color (`frame_color`) and outer bounding box (`frame_bounds`). Handle cases where no valid frame is found.
  - action: determine_filtering_colors
    description: Identify the set of `filtered_background_colors` by taking white (0) and adding any unique colors adjacent to the outside perimeter defined by `frame_bounds`.
  - action: extract_inner_region
    description: Get the grid portion strictly inside `frame_bounds`.
  - action: filter_content
    description: Create a copy of the inner region. Replace pixels whose color is in `filtered_background_colors` with white (0).
  - action: construct_output
    description: Create a new grid sized for the filtered content plus a 1-pixel border. Draw the border using `frame_color`. Place the filtered content inside.

relationships:
  - relationship: enclosure
    description: The selected 'frame_object' spatially encloses the 'content_objects' and potentially some pixels matching 'filtered_background_colors'.
  - relationship: adjacency_based_filtering
    description: The set of 'filtered_background_colors' is determined by adjacency to the selected 'frame_object', linking the frame choice to the filtering process.
  - relationship: preservation_vs_removal
    description: Within the area defined by the frame, pixels matching 'filtered_background_colors' are removed (set to white), while other pixels ('content_objects') are preserved.
```


**Natural Language Program**

1.  **Identify Candidate Frames:** Scan the input grid to find all possible candidate "frames". A candidate frame is defined as the set of all connected pixels of a single color `C` (where `C` is not white/0) that meets these criteria based on its bounding box (`min_r`, `min_c`, `max_r`, `max_c`):
    *   The bounding box must be at least 3x3 (`max_r - min_r >= 2` and `max_c - min_c >= 2`).
    *   All pixels along the perimeter of the bounding box (`grid[min_r, min_c:max_c+1]`, `grid[max_r, min_c:max_c+1]`, `grid[min_r+1:max_r, min_c]`, `grid[min_r+1:max_r, max_c]`) must have color `C`.
    *   No pixels strictly inside the bounding box (`grid[min_r+1:max_r, min_c+1:max_c]`) can have color `C`.
    *   No pixels immediately adjacent to the *outside* of the bounding box perimeter can have color `C` (ensuring thickness 1). Store each valid candidate frame's color and bounding box.
2.  **Select Main Frame:** If no candidate frames were found, return the original input grid. Otherwise, select the candidate frame with the largest area (`(max_r - min_r + 1) * (max_c - min_c + 1)`). Let its color be `frame_color` and its bounding box be (`frame_min_r`, `frame_min_c`, `frame_max_r`, `frame_max_c`).
3.  **Determine Background Colors:** Initialize a set `background_colors` containing only white (0). Examine the pixels immediately adjacent to the outside of the selected frame's bounding box (if they exist within the grid):
    *   Row above: `grid[frame_min_r - 1, frame_min_c : frame_max_c + 1]`
    *   Row below: `grid[frame_max_r + 1, frame_min_c : frame_max_c + 1]`
    *   Column left: `grid[frame_min_r : frame_max_r + 1, frame_min_c - 1]`
    *   Column right: `grid[frame_min_r : frame_max_r + 1, frame_max_c + 1]`
    Add all unique colors found in these adjacent positions to the `background_colors` set.
4.  **Calculate Inner Dimensions:** Determine the height and width of the region inside the frame: `inner_height = frame_max_r - frame_min_r - 1`, `inner_width = frame_max_c - frame_min_c - 1`.
5.  **Create Output Grid:** Create a new grid `output_grid` with dimensions `(inner_height + 2) x (inner_width + 2)`, initialized entirely with white (0).
6.  **Draw Border:** Set the 1-pixel thick border of the `output_grid` to `frame_color`.
7.  **Process Inner Content:** Iterate through the input grid's inner region, from row `r_in = frame_min_r + 1` to `frame_max_r - 1` and column `c_in = frame_min_c + 1` to `frame_max_c - 1`.
    *   Get the color `P = input_grid[r_in, c_in]`.
    *   Calculate the corresponding output coordinates: `r_out = r_in - frame_min_r`, `c_out = c_in - frame_min_c`.
    *   If the color `P` is **not** in the `background_colors` set, set `output_grid[r_out, c_out] = P`.
8.  **Return Output:** Return the completed `output_grid`.