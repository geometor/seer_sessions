**Correction:** My manual analysis of Example 3 was incorrect regarding the number of green objects. The `find_objects` function identifies *all* connected green pixels as a single object if they touch cardinally. In Example 3, the two apparent rectangles are connected by pixels like (5,4) and (6,4), forming one large object. The code output confirms this: "Number of Green Objects: 1", with BBox `(3, 4, 7, 9)`. This simplifies the "main object" selection as there's only one. The rest of the analysis holds.

The metrics confirm the initial bounding boxes and external markers used in the previous logic. The core issue remains the handling of the *content* within the frame during resizing.

## General Assessment

The provided code successfully identifies the main green frame object and calculates the correct expanded bounding box based on external magenta markers in all examples. Example 1 succeeded because the original frame was hollow, so drawing only the new border was sufficient. Examples 2 and 3 failed because the original frames contained internal patterns (non-green pixels) which were discarded by the code. The code only drew the *new* hollow green frame and the magenta markers, omitting the original content.

The strategy to resolve this is to modify the transformation process:
1.  Identify the main green frame and its initial bounding box (`initial_bbox`).
2.  Identify external magenta markers and calculate the new bounding box (`new_bbox`).
3.  Create an empty output grid.
4.  Copy the rectangular region defined by `initial_bbox` from the input grid to the same coordinates in the output grid.
5.  Draw the *perimeter* of the `new_bbox` onto the output grid using the green color (color 3). This will overwrite any pixels from the previous step that fall on the new border.
6.  Draw all original magenta markers onto the output grid at their original positions.

## Metrics

| Example | Input Shape | Output Shape | Main Green Initial BBox | External Markers | Pixels Off (Previous Code) | Failure Reason                                     |
| :------ | :---------- | :----------- | :---------------------- | :--------------- | :------------------------- | :------------------------------------------------- |
| 1       | 11x15       | 11x15        | (2, 4, 4, 6)            | [(3, 1), (9, 5)] | 0                          | N/A (Success)                                      |
| 2       | 8x17        | 8x17         | (1, 1, 4, 6)            | [(2, 11), (6, 4)] | 3                          | Original frame content (white pixels) not copied.  |
| 3       | 15x15       | 15x15        | (3, 4, 7, 9)            | [(4, 12), (6, 1), (14, 7)] | 16                         | Original frame content (white pixels) not copied. |

*Note: The BBoxes are (min_row, min_col, max_row, max_col), inclusive.*
*Note: The code analysis confirmed only one green object was found in Example 3, with BBox (3, 4, 7, 9).*

## Facts


```yaml
task_description: "Resize a green frame based on the location of external magenta markers, preserving the original content within the frame's initial area."

grid_properties:
  - size: Variable (up to 30x30)
  - background_color: white (0)

objects:
  - type: frame
    color: green (3)
    definition: A connected component of green pixels. May be hollow or contain other colors.
    properties:
      - bounding_box: The smallest rectangle enclosing the object.
      - main_frame: If multiple green objects exist, the one with the largest bounding box area. Ties broken by top-most, then left-most bounding box corner. (In observed examples, only one green object exists).
  - type: marker
    color: magenta (6)
    definition: Single pixels of magenta color.
    properties:
      - location: (row, col) coordinates.
      - classification:
          - internal: Located within or on the border of the main_frame's initial bounding box.
          - external: Located strictly outside the main_frame's initial bounding box.

actions:
  - 1_find_markers: Identify the coordinates of all magenta markers.
  - 2_find_frame: Identify all connected green objects and determine the main_frame and its initial bounding box (`initial_bbox`).
  - 3_classify_markers: Identify which magenta markers are external to `initial_bbox`.
  - 4_calculate_new_bbox: Determine the target expansion boundaries based on external markers:
      - target_top: Row below the lowest external marker above `initial_bbox`.
      - target_bottom: Row above the highest external marker below `initial_bbox`.
      - target_left: Column right of the rightmost external marker left of `initial_bbox`.
      - target_right: Column left of the leftmost external marker right of `initial_bbox`.
      - The final new bounding box (`new_bbox`) is the union of `initial_bbox` and the area defined by the target boundaries, clamped to grid dimensions.
  - 5_create_output: Initialize an output grid of the same size as the input, filled with white (0).
  - 6_copy_content: Copy the rectangular region defined by `initial_bbox` from the input grid to the output grid at the same coordinates.
  - 7_draw_new_frame: Draw a hollow rectangle using green (3) along the perimeter defined by `new_bbox` onto the output grid.
  - 8_draw_markers: Draw all original magenta markers (both internal and external) onto the output grid at their original coordinates.

edge_cases:
  - No green frame found: Output should contain only the magenta markers on a white background.
  - No external markers found: The frame is not resized (`new_bbox` equals `initial_bbox`). Content is copied, frame border is redrawn (potentially changing internal green pixels to border green pixels if the original wasn't hollow), markers are drawn.
  - Markers only on some sides: Frame expands only in the directions indicated by external markers.
```


## Natural Language Program

1.  Initialize an output grid of the same dimensions as the input grid, filled with the background color (white, 0).
2.  Find all coordinates of magenta (6) pixels (markers).
3.  Find all connected components of green (3) pixels. If multiple components exist, identify the "main" component as the one with the largest bounding box area (breaking ties by selecting the component whose bounding box has the minimum row index, then minimum column index). If no green component exists, skip to step 7.
4.  Calculate the initial bounding box (`initial_bbox`) of the main green component.
5.  Copy the rectangular region defined by `initial_bbox` from the input grid to the corresponding region in the output grid.
6.  Determine the "new" bounding box (`new_bbox`):
    a.  Identify magenta markers that lie strictly outside `initial_bbox`.
    b.  Calculate target expansion boundaries based on these external markers:
        i.  The top boundary expands upwards towards the lowest external marker *above* the `initial_bbox`, stopping one row below it.
        ii. The bottom boundary expands downwards towards the highest external marker *below* the `initial_bbox`, stopping one row above it.
        iii.The left boundary expands leftwards towards the rightmost external marker *left* of the `initial_bbox`, stopping one column to its right.
        iv. The right boundary expands rightwards towards the leftmost external marker *right* of the `initial_bbox`, stopping one column to its left.
    c.  `new_bbox` is the union of `initial_bbox` and the target expansion area (defined by the calculated boundaries), ensuring coordinates stay within the grid limits. If there are no external markers in a given direction (e.g., no markers above), the boundary does not expand in that direction.
    d.  Draw the perimeter of `new_bbox` on the output grid using green (3), overwriting any pixels previously copied in step 5 that fall on this perimeter.
7.  Draw all magenta markers found in step 2 onto the output grid at their original coordinates, overwriting any existing pixels at those locations.
8.  Return the final output grid.## General Assessment

The previous code successfully identified the primary green object (frame) and the external magenta markers, correctly calculating the dimensions and position of the resized frame based on these markers. The code worked for Example 1 where the original frame content was effectively hollow or irrelevant. However, it failed on Examples 2 and 3 because it only drew the *new* frame's border and markers, neglecting to preserve the content that was originally inside the frame's initial bounding box.

The core issue is the omission of copying the original frame's content area into the new grid before drawing the resized frame border. The strategy is to insert a step where the content within the original frame's bounding box is copied to the output grid, *then* draw the new, potentially larger, frame border, and finally redraw the markers.

## Metrics

Metrics gathered using `tool_code` confirm the analysis:

| Example | Input Shape | Output Shape | Main Green Initial BBox | External Markers           | Pixels Off (Previous Code) | Failure Reason (Previous Code)                     |
| :------ | :---------- | :----------- | :---------------------- | :------------------------- | :------------------------- | :------------------------------------------------- |
| 1       | 11x15       | 11x15        | (2, 4, 4, 6)            | [(3, 1), (9, 5)]           | 0                          | N/A (Success)                                      |
| 2       | 8x17        | 8x17         | (1, 1, 4, 6)            | [(2, 11), (6, 4)]          | 3                          | Original frame content (white pixels) not copied.  |
| 3       | 15x15       | 15x15        | (3, 4, 7, 9)            | [(4, 12), (6, 1), (14, 7)] | 16                         | Original frame content (white pixels) not copied. |

*Note: BBoxes are (min_row, min_col, max_row, max_col), inclusive.*
*Note: In Example 3, although visually appearing as two rectangles, the green pixels form a single connected component.*

## Facts


```yaml
task_description: "Resize a green frame based on the location of external magenta markers, preserving the original content within the frame's initial area."

grid_properties:
  - size: Variable (up to 30x30)
  - background_color: white (0)

objects:
  - type: frame
    color: green (3)
    definition: A connected component of green pixels. May contain pixels of other colors within its bounding box.
    properties:
      - bounding_box: The smallest rectangle enclosing all the object's green pixels (`initial_bbox`).
      - main_frame: If multiple disjoint green objects exist, the one with the largest `initial_bbox` area. Ties broken by top-most, then left-most corner of `initial_bbox`. (In observed examples, only one connected green object exists).
      - content_area: The rectangular region defined by `initial_bbox`.
  - type: marker
    color: magenta (6)
    definition: Single pixels of magenta color.
    properties:
      - location: (row, col) coordinates.
      - classification:
          - internal: Located within or on the border of the `initial_bbox`.
          - external: Located strictly outside the `initial_bbox`.

actions:
  - 1_find_markers: Identify the coordinates of all magenta markers.
  - 2_find_frame: Identify all connected green objects. If any exist, determine the `main_frame` and its `initial_bbox`. If no green frame exists, proceed to step 8.
  - 3_classify_markers: Identify which magenta markers are `external` relative to `initial_bbox`.
  - 4_calculate_new_bbox: Determine the target expansion boundaries based on `external` markers:
      - target_top_boundary: Row index `r` such that `r = min(marker_row) + 1` for all external markers with `marker_row < initial_bbox.min_row`. Default is `initial_bbox.min_row`.
      - target_bottom_boundary: Row index `r` such that `r = max(marker_row) - 1` for all external markers with `marker_row > initial_bbox.max_row`. Default is `initial_bbox.max_row`.
      - target_left_boundary: Column index `c` such that `c = max(marker_col) + 1` for all external markers with `marker_col < initial_bbox.min_col`. Default is `initial_bbox.min_col`.
      - target_right_boundary: Column index `c` such that `c = min(marker_col) - 1` for all external markers with `marker_col > initial_bbox.max_col`. Default is `initial_bbox.max_col`.
      - The final new bounding box (`new_bbox`) encompasses the area from `min(initial_bbox.min_row, target_top_boundary)` to `max(initial_bbox.max_row, target_bottom_boundary)` and `min(initial_bbox.min_col, target_left_boundary)` to `max(initial_bbox.max_col, target_right_boundary)`, clamped to grid dimensions (0 to rows-1, 0 to cols-1).
  - 5_create_output: Initialize an output grid of the same size as the input, filled with white (0).
  - 6_copy_content: Copy the rectangular region defined by `initial_bbox` from the input grid to the output grid, placing it at the same `(row, col)` coordinates.
  - 7_draw_new_frame_border: Draw a hollow rectangle using green (3) along the perimeter defined by `new_bbox` onto the output grid. This overwrites any pixels previously copied in step 6 that lie on this new perimeter.
  - 8_draw_markers: Draw all magenta markers (found in step 1) onto the output grid at their original coordinates, overwriting any existing pixels.

edge_cases:
  - No green frame found: Output grid contains only the original magenta markers on a white background.
  - No external markers found: `new_bbox` equals `initial_bbox`. The content is copied, the frame border is redrawn with green (potentially overwriting original non-border green pixels if the frame wasn't hollow), and markers are drawn.
  - Markers only on some sides: Frame expands only in the directions indicated by external markers.
```


## Natural Language Program

1.  Create an output grid with the same dimensions as the input grid, initialized with white (0) pixels.
2.  Locate all magenta (6) pixels in the input grid and store their coordinates.
3.  Identify all distinct connected components of green (3) pixels in the input grid.
4.  If no green components are found, proceed directly to step 9.
5.  If one or more green components are found, determine the "main" green component: select the component whose bounding box has the largest area. If there's a tie in area, select the component whose bounding box has the minimum top-row index; if there's still a tie, select the one with the minimum left-column index. Let the bounding box of this main component be `initial_bbox`.
6.  Copy the rectangular region defined by `initial_bbox` (from `initial_bbox.min_row` to `initial_bbox.max_row`, and `initial_bbox.min_col` to `initial_bbox.max_col`) from the input grid to the *same corresponding region* in the output grid.
7.  Identify the subset of magenta markers that lie strictly *outside* the `initial_bbox`.
8.  Calculate the boundaries of a new bounding box, `new_bbox`, based on the `initial_bbox` and the locations of these *external* markers:
    *   The top edge of `new_bbox` is the minimum of `initial_bbox.min_row` and `r+1` for the lowest external marker above the box (where `r` is the marker's row). If no markers are above, the top edge is `initial_bbox.min_row`.
    *   The bottom edge of `new_bbox` is the maximum of `initial_bbox.max_row` and `r-1` for the highest external marker below the box (where `r` is the marker's row). If no markers are below, the bottom edge is `initial_bbox.max_row`.
    *   The left edge of `new_bbox` is the minimum of `initial_bbox.min_col` and `c+1` for the rightmost external marker left of the box (where `c` is the marker's column). If no markers are left, the left edge is `initial_bbox.min_col`.
    *   The right edge of `new_bbox` is the maximum of `initial_bbox.max_col` and `c-1` for the leftmost external marker right of the box (where `c` is the marker's column). If no markers are right, the right edge is `initial_bbox.max_col`.
    *   Ensure all `new_bbox` coordinates are clamped within the grid's bounds (0 to height-1, 0 to width-1).
    *   Draw the perimeter (top, bottom, left, right edges) of this `new_bbox` onto the output grid using the green (3) color. This overwrites any pixels previously copied at these border locations.
9.  Iterate through the stored coordinates of *all* magenta markers (from step 2) and set the corresponding pixels in the output grid to magenta (6), overwriting any color previously present at those locations.
10. Return the completed output grid.