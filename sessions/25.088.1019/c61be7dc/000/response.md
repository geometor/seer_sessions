## Perception

1.  **Input Structure:** Each input grid consists primarily of an orange (7) background. A key feature is a pair of parallel white (0) lines, which can be either horizontal or vertical. Located geometrically between these two white lines is a shape composed of gray (5) pixels. There might be other white pixels present, sometimes forming lines perpendicular to the main pair (e.g., train_1 row 5).
2.  **Output Structure:** The output grid retains the orange background. The pair of parallel white lines from the input have moved one step inwards (closer to each other). The gray shape from the input is replaced by a single straight line segment (either horizontal or vertical) of gray pixels.
3.  **Transformation Core Logic:** The transformation centers around the pair of parallel white lines and the gray object situated between them.
    *   The white lines act as dynamic boundaries. They move one step towards each other in the output.
    *   The gray object enclosed by the original lines is transformed into a new gray line segment in the output.
    *   The orientation of the output gray line matches the orientation of the input white lines (vertical white lines yield a vertical gray line; horizontal white lines yield a horizontal gray line).
    *   The *position* of the output gray line is centered within the new, narrower region defined by the moved white lines.
    *   The *length* of the output gray line depends on the orientation of the input white lines:
        *   If the input white lines are *vertical*, the output gray line is vertical, and its length is equal to the total height of the grid minus 2. It is centered vertically.
        *   If the input white lines are *horizontal*, the output gray line is horizontal, and its length is equal to the *number of gray pixels* in the original input object. It is centered horizontally.
4.  **Color Preservation/Changes:** The background remains orange. The moving white lines retain their white color at their new positions. The transformed gray shape becomes a gray line. The area between the original white lines that was not the gray object becomes orange background in the output (unless it's part of the new gray line). Areas outside the original white lines remain unchanged (orange).

## Facts


```yaml
objects:
  - type: background
    color: orange (7)
    scope: entire_grid
  - type: boundary_lines
    count: 2
    color: white (0)
    arrangement: parallel (either horizontal or vertical)
    properties:
      - orientation (horizontal or vertical)
      - position (row or column indices)
      - distance_between
  - type: enclosed_object
    color: gray (5)
    location: geometrically between the boundary_lines
    properties:
      - shape (variable, can be line, square, T-shape)
      - pixel_count
      - bounding_box
      - horizontal_span
      - vertical_span
  - type: output_line
    color: gray (5)
    properties:
      - orientation (matches boundary_lines orientation)
      - length (depends on boundary_lines orientation)
      - position (centered between moved boundary_lines)

actions:
  - identify: find the pair of parallel white boundary_lines
  - identify: determine the orientation of boundary_lines
  - identify: find the gray enclosed_object between the boundary_lines
  - calculate: count the pixels of the enclosed_object (N)
  - transform: move the boundary_lines one step inwards
  - calculate: determine the center row/column index (C_idx) of the region between the moved lines
  - calculate: determine the orientation of the output_line (matches boundary_lines orientation)
  - calculate: determine the length of the output_line:
      - if boundary_lines are vertical: length = grid_height - 2
      - if boundary_lines are horizontal: length = N
  - calculate: determine the position (start row/col) of the output_line by centering it within the grid dimension perpendicular to its orientation.
  - construct: create the output grid with the background, moved boundary_lines, and the calculated output_line.

relationships:
  - enclosed_object is spatially located between the boundary_lines in the input.
  - The orientation of the output_line is determined by the orientation of the input boundary_lines.
  - The length of the output_line depends on the orientation of the boundary_lines (either grid dimension or pixel count).
  - The output_line is positioned centrally between the moved boundary_lines along one axis and centrally within the grid along the other axis.
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid, or filled with the background color (orange, 7).
2.  Scan the input grid to locate the unique pair of parallel white (0) lines (either two horizontal lines or two vertical lines). Record their orientation (horizontal/vertical) and their positions (row/column indices `idx1`, `idx2`, where `idx1 < idx2`).
3.  Identify all gray (5) pixels located between these two lines (i.e., for rows/columns strictly between `idx1` and `idx2`). Let this set of pixels be the 'input object'.
4.  Count the total number of pixels (`N`) in the 'input object'.
5.  Calculate the new positions for the white lines by moving them one step inwards: `new_idx1 = idx1 + 1`, `new_idx2 = idx2 - 1`.
6.  Determine the central row/column index (`C_idx`) for the output line. This is the midpoint between `new_idx1` and `new_idx2`. `C_idx = floor((new_idx1 + new_idx2) / 2)`.
7.  Determine the orientation and length of the output gray line:
    *   If the original white lines were **vertical** (at columns `idx1`, `idx2`):
        *   The output line orientation is **vertical**.
        *   The output line length (`Length`) is `grid_height - 2`.
        *   The output line will be placed in column `C_idx`.
        *   Calculate the starting row: `Start_Row = floor((grid_height - Length) / 2)`.
        *   Draw the vertical gray line in the output grid at column `C_idx`, from `Start_Row` to `Start_Row + Length - 1`.
    *   If the original white lines were **horizontal** (at rows `idx1`, `idx2`):
        *   The output line orientation is **horizontal**.
        *   The output line length (`Length`) is `N` (the count of gray pixels in the input object).
        *   The output line will be placed in row `C_idx`.
        *   Calculate the starting column: `Start_Col = floor((grid_width - Length) / 2)`.
        *   Draw the horizontal gray line in the output grid at row `C_idx`, from `Start_Col` to `Start_Col + Length - 1`.
8.  Ensure the moved white lines are drawn in the output grid at their new positions (`new_idx1` and `new_idx2`).
9.  Fill the remaining pixels of the output grid:
    *   Pixels occupied by the new gray line are gray (5).
    *   Pixels occupied by the moved white lines are white (0).
    *   All other pixels are the background color (orange, 7).