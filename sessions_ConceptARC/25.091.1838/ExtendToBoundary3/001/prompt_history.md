
## train_1

**input:**
```
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 4
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
0 0 4 4 4 4 4 4 4 4 4 4
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 5 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 0 7 0 7 0 7 0 7 0 7 0 7 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0
7 0 7 0 7 0 7 0 7 0 7 0 7 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 3 0 0 0 0
```


**output:**
```
3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 3 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 3 0 0 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 3 0 0 0 0
```

Okay, let's break down the task based on the provided examples.

**Perception**

Across the training examples, I observe the following:

1.  **Background:** The grids predominantly use white (0) as the background color.
2.  **Key Elements:** Each input grid contains two distinct non-background elements:
    *   A **Reference Structure**: This is usually a set of pixels forming a simple geometric pattern (a vertical partial line in Ex1, a horizontal dashed line in Ex2, a diagonal line in Ex3). These pixels may or may not be contiguous but follow a clear rule. They often consist of a single color (gray in Ex1, orange in Ex2, green in Ex3).
    *   A **Marker Pixel**: This is typically a single, isolated pixel distinct from the background and often distinct in color or location from the Reference Structure (yellow in Ex1, orange in Ex2, red in Ex3). Notably, in Ex2, the Marker Pixel has the same color as the Reference Structure but is spatially isolated from it.
3.  **Transformation:** The core transformation involves drawing a new line or path on the grid. The properties of this new line (color, orientation, start/end points) are determined by the relationship between the Marker Pixel and the Reference Structure.
4.  **Output Grid:** The output grid contains all the elements from the input grid plus the newly drawn line.
5.  **Line Drawing Logic:**
    *   The **color** of the new line always matches the color of the Marker Pixel.
    *   The **orientation** and **extent** of the line depend on the relative positions and orientations of the Marker Pixel and the Reference Structure:
        *   In Ex1 (Vertical Reference Structure): A horizontal line is drawn *from* near the Reference Structure's column *towards* the Marker Pixel's column, aligned with the Marker Pixel's row.
        *   In Ex2 (Horizontal Reference Structure): A vertical line is drawn *from* near the Reference Structure's row *towards* the Marker Pixel's row, aligned with the Marker Pixel's column.
        *   In Ex3 (Diagonal Reference Structure): A diagonal path is drawn *from* the Marker Pixel *towards* the Reference Structure, stopping just before "colliding" with the column occupied by a Reference Structure pixel.

**Facts**


```yaml
# General observations across examples
task_type: drawing_completion
background_color: 0 # white
elements:
  - role: reference_structure
    description: A pattern of non-background pixels (line, dashed line, diagonal).
    properties:
      - color: Varies (gray, orange, green)
      - shape: Line-like (vertical, horizontal, diagonal)
      - count: Multiple pixels
  - role: marker_pixel
    description: A single, isolated non-background pixel.
    properties:
      - color: Varies (yellow, orange, red)
      - shape: Single pixel
      - count: 1
transformation:
  action: draw_line
  properties:
    color: Determined by marker_pixel.color
    orientation: Determined by reference_structure.shape and relative position to marker_pixel
    start_point: Near reference_structure, aligned with marker_pixel
    end_point: Near marker_pixel, aligned with reference_structure (or stops based on collision rule)
relationship: The new line connects the 'area' of the reference structure to the 'area' of the marker pixel, following specific alignment and stopping rules based on the reference structure's orientation.

# Example-specific observations
example_1:
  reference_structure:
    color: 5 # gray
    location: Column 1, various rows
    orientation: Vertical
  marker_pixel:
    color: 4 # yellow
    location: (5, 11)
  drawn_line:
    color: 4 # yellow
    orientation: Horizontal
    row: 5
    start_col: 2 # col after reference + 1
    end_col: 11 # marker_pixel column

example_2:
  reference_structure:
    color: 7 # orange
    location: Row 1, various columns
    orientation: Horizontal
  marker_pixel:
    color: 7 # orange
    location: (7, 8)
  drawn_line:
    color: 7 # orange
    orientation: Vertical
    col: 8
    start_row: 2 # row after reference + 1
    end_row: 7 # marker_pixel row

example_3:
  reference_structure:
    color: 3 # green
    location: Diagonal ((0,0), (2,2), (4,4), (6,6))
    orientation: Diagonal (top-left to bottom-right)
  marker_pixel:
    color: 2 # red
    location: (6, 0)
  drawn_line:
    color: 2 # red
    orientation: Diagonal path (up-right)
    start_pos: (6, 0) # marker_pixel position (path originates here)
    path_points_added: [(5, 1), (4, 2)]
    stop_condition: Next step's column (col 2) contains a reference_structure pixel (at row 2).

```


**Natural Language Program**

1.  **Identify Background:** Determine the background color (typically the most frequent color, usually white/0).
2.  **Identify Objects:**
    *   Find all non-background pixels.
    *   Group these pixels into connected components (considering pixels of the same color adjacent or diagonally adjacent as connected) or distinct color groups.
    *   Identify the component consisting of a single pixel; this is the `Marker Pixel`. Record its `marker_color` and `marker_position` (row, col).
    *   Identify the component representing a line or regular pattern; this is the `Reference Structure`. Record its pixels' coordinates (`reference_coordinates`) and determine its primary orientation (Vertical, Horizontal, or Diagonal).
3.  **Prepare Output:** Create a copy of the input grid.
4.  **Execute Drawing Rule based on Reference Structure Orientation:**
    *   **If Vertical Reference:**
        *   Find the column index (`ref_col`) occupied by the `Reference Structure` pixels (if they span multiple columns, use the minimum column index).
        *   Draw a horizontal line in the output grid using `marker_color`.
        *   The line is drawn in the row `marker_position.row`.
        *   The line extends from column `ref_col + 1` up to `marker_position.col` (inclusive).
    *   **If Horizontal Reference:**
        *   Find the row index (`ref_row`) occupied by the `Reference Structure` pixels (if they span multiple rows, use the minimum row index).
        *   Draw a vertical line in the output grid using `marker_color`.
        *   The line is drawn in the column `marker_position.col`.
        *   The line extends from row `ref_row + 1` down to `marker_position.row` (inclusive).
    *   **If Diagonal Reference:**
        *   Determine the primary direction (e.g., up-right, down-left) from the `marker_position` towards the `Reference Structure`. Define this as a step (`dr`, `dc`).
        *   Initialize `current_position` = `marker_position`.
        *   Initialize an empty list `path_to_draw`.
        *   Loop:
            *   Calculate `next_position` = (`current_position.row + dr`, `current_position.col + dc`).
            *   Check if `next_position` is within grid bounds. If not, stop looping.
            *   Check if the column `next_position.col` contains any pixel whose coordinates are in `reference_coordinates`.
            *   If yes, stop looping.
            *   If no, add `next_position` to `path_to_draw`, update `current_position` = `next_position`, and continue looping.
        *   For each `pos` in `path_to_draw`, set the color of the pixel at `pos` in the output grid to `marker_color`.
5.  **Return Output:** Return the modified grid.
