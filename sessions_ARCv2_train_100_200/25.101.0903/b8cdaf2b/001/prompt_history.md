
## train_1

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 6 6 6 0
6 1 1 1 6
```


**output:**
```
0 0 0 0 0
0 0 0 0 0
1 0 0 0 1
0 6 6 6 0
6 1 1 1 6
```


## train_2

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
0 0 8 0 0
8 8 3 8 8
```


**output:**
```
0 0 0 0 0
3 0 0 0 3
0 3 0 3 0
0 0 8 0 0
8 8 3 8 8
```


## train_3

**input:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 2 2 2 0 0
2 2 4 4 4 2 2
```


**output:**
```
0 0 0 0 0 0 0
0 0 0 0 0 0 0
0 0 0 0 0 0 0
4 0 0 0 0 0 4
0 4 0 0 0 4 0
0 0 2 2 2 0 0
2 2 4 4 4 2 2
```


## train_4

**input:**
```
0 0 0
0 2 0
2 4 2
```


**output:**
```
4 0 4
0 2 0
2 4 2
```

**Perception**

1.  **Input Structure:** Each input grid contains a single, prominent composite object located at the bottom edge. The background is white (0).
2.  **Object Composition:** The object appears to consist of two main parts/colors: an outer "frame" or "shell" and an inner "content" or "core". In some examples, the uppermost part of the frame acts like a "stem". The content color is typically found directly below the stem, on the lowest row(s) of the object, and often horizontally centered within the frame.
3.  **Transformation:** The transformation involves adding new pixels to the grid above the original object. The original object remains unchanged in the output grid.
4.  **Added Pixels:** The added pixels always take the color of the "content" part of the original object. They are placed symmetrically with respect to the object's vertical axis.
5.  **Placement Pattern:** The placement of the added pixels follows one of two distinct symmetrical patterns (Pattern A or Pattern B), determined by properties of the original object.
    *   **Pattern A** (Examples 1, 4): Two pixels are added. They are located `H` rows above the object's lowest row (`r_base`), aligned vertically with the leftmost (`c_min`) and rightmost (`c_max`) extent of the object on its lowest row. Coordinates: `(r_base - H, c_min)` and `(r_base - H, c_max)`.
    *   **Pattern B** (Examples 2, 3): Four pixels are added in two pairs.
        *   Pair 1: Located `H+1` rows above the object's lowest row, aligned vertically with the object's horizontal extent on that row. Coordinates: `(r_base - H - 1, c_min)` and `(r_base - H - 1, c_max)`.
        *   Pair 2: Located `H` rows above the object's lowest row, horizontally inset by one pixel from the edges. Coordinates: `(r_base - H, c_min + 1)` and `(r_base - H, c_max - 1)`.
6.  **Pattern Selection Condition:** The choice between Pattern A and Pattern B depends on the color of the object's corners on its lowest row (`CornerC`) and potentially the object's width on that row (`BaseWidth`).
    *   If `CornerC` is Magenta (6), use Pattern A.
    *   If `CornerC` is Azure (8), use Pattern B.
    *   If `CornerC` is Red (2), check `BaseWidth`: if `BaseWidth <= 3`, use Pattern A; if `BaseWidth > 3`, use Pattern B.

**Facts**


```yaml
# Overall Task Structure
task_type: object_transformation
background_color: 0 # white
objects_per_input: 1
output_relation: adds_pixels_preserves_input_object

# Object Properties
object_location: touches_bottom_edge
object_connectivity: contiguous_non_background_pixels
object_components:
  - frame: outer_pixels
  - content: inner_pixels_on_lowest_rows # Color used for added pixels
object_attributes:
  - height: H # number of rows spanned by the object
  - lowest_row: r_base # row index of the lowest part of the object
  - base_extent: # min/max columns on the lowest row
      min_col: c_min
      max_col: c_max
  - base_width: W = c_max - c_min + 1
  - corner_color: CornerC = color at (r_base, c_min) # also (r_base, c_max) due to symmetry

# Transformation Details
added_pixel_color: content_color C
added_pixel_placement: symmetrical_pattern_above_object
patterns:
  - pattern_A: # Used if (CornerC == 6) OR (CornerC == 2 AND W <= 3)
      pixels:
        - [(r_base - H, c_min), C]
        - [(r_base - H, c_max), C]
  - pattern_B: # Used if (CornerC == 8) OR (CornerC == 2 AND W > 3)
      pixels:
        - [(r_base - H - 1, c_min), C]
        - [(r_base - H - 1, c_max), C]
        - [(r_base - H, c_min + 1), C]
        - [(r_base - H, c_max - 1), C]

# Relationships
- relationship: pattern_selection_depends_on_corner_color_and_base_width
```


**Natural Language Program**

1.  Initialize the output grid as a copy of the input grid.
2.  Identify the single connected block of non-background pixels touching the bottom edge of the input grid. This is the "object".
3.  Determine the object's properties:
    a.  Find the lowest row index `r_base` where the object exists.
    b.  Find the minimum column index `c_min` and maximum column index `c_max` of the object on row `r_base`.
    c.  Calculate the object's base width `W = c_max - c_min + 1`.
    d.  Determine the object's total height `H` (number of rows it spans).
    e.  Identify the color `CornerC` of the pixels at `(r_base, c_min)` and `(r_base, c_max)`.
    f.  Identify the "content color" `C`. This is the color of the pixel(s) on row `r_base` located strictly between `c_min` and `c_max`, OR if no such pixels exist, the color of the pixel directly centered below the object's highest point ("stem"). Find the color C of the pixels at `(r_base, c)` where `c_min < c < c_max`. (Assume this identifies the content color based on examples).
4.  Determine which placement pattern to use based on `CornerC` and `W`:
    a.  If `CornerC` is Magenta (6), select Pattern A.
    b.  If `CornerC` is Azure (8), select Pattern B.
    c.  If `CornerC` is Red (2):
        i.  If `W <= 3`, select Pattern A.
        ii. If `W > 3`, select Pattern B.
5.  Apply the selected pattern to add pixels of color `C` to the output grid:
    a.  If Pattern A: Add color `C` at `(r_base - H, c_min)` and `(r_base - H, c_max)`.
    b.  If Pattern B: Add color `C` at `(r_base - H - 1, c_min)`, `(r_base - H - 1, c_max)`, `(r_base - H, c_min + 1)`, and `(r_base - H, c_max - 1)`. (Ensure coordinates are within grid bounds, though this seems implicit).
6.  Return the modified output grid.
