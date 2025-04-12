## Perception

1.  **Input/Output Structure:** Each example consists of an 8x8 input grid and a corresponding 8x8 output grid. The grids contain pixels colored white (0) and two other distinct non-white colors.
2.  **Object Identification:** In each example, there are typically two main non-white objects. One object appears to act as a frame, boundary, or central line (Red plus, Yellow rectangle, Magenta line), while the second object is located inside or adjacent to the first (Blue rectangle, Green rectangle, Orange shape).
3.  **Core Transformation:** The transformation involves modifying the 'inner' or 'adjacent' object (let's call it Object A) based on its relationship with the 'outer' or 'boundary' object (Object B). Specifically, Object A undergoes a horizontal expansion or filling.
4.  **Expansion Logic:**
    *   In `train_1` and `train_2`, Object B (Red plus, Yellow rectangle) forms clear vertical boundaries. Object A (Blue, Green) expands horizontally to fill the entire space between these vertical boundaries, but only on the rows where Object A was originally present. The color used for filling is the color of Object A. Pixels originally belonging to Object B within the fill area are overwritten.
    *   In `train_3`, Object B (Magenta line) is *between* parts of Object A (Orange shape). Object A expands horizontally to connect its leftmost and rightmost points *within each row it occupies*, overwriting Object B where they intersect.
5.  **Color Preservation:** The color of Object B generally remains unchanged outside the fill area. The color of Object A is used for the fill operation. Background (white) pixels within the fill area are colored. Pixels of Object B within the fill area are also recolored with Object A's color.

## Facts


```yaml
task_type: object_transformation
grid_properties:
  size: 8x8
  colors_used: 3 per example (white background + 2 object colors)

objects:
  - id: A # The 'inner' object that expands/fills
    properties:
      - color: variable (Blue, Green, Orange in examples)
      - shape: variable (rectangle, complex shape)
      - role: fill_source
  - id: B # The 'outer' object that defines boundaries or is overwritten
    properties:
      - color: variable (Red, Yellow, Magenta in examples)
      - shape: variable (plus, rectangle, line)
      - role: boundary_or_intersected

relationships:
  - type: spatial
    description: Object A is spatially related to Object B (inside, adjacent, surrounding).
  - type: boundary_definition
    description: Object B either defines vertical boundaries for Object A's horizontal expansion, or Object A's own horizontal extent per row defines the expansion.

actions:
  - name: horizontal_fill
    parameters:
      - fill_color: color of Object A
      - target_rows: rows where Object A is present
      - target_columns:
          conditional:
            - if: Object B provides left/right boundaries enclosing A
              then: columns between and including B's boundaries
            - else: columns between and including A's min/max extent per row
    output: Modifies a copy of the input grid by applying the fill.
```


## Natural Language Program

1.  Initialize the output grid as a copy of the input grid.
2.  Identify the two distinct non-background colored objects present in the input grid. Designate them as Object A (the one that will expand/fill) and Object B (the reference/boundary object). Determine the color of Object A.
3.  Determine the set of rows (`rows_A`) where Object A exists.
4.  Analyze the spatial relationship: Check if Object B forms consistent vertical boundaries (left and right) that enclose Object A across `rows_A`.
5.  **If** Object B forms enclosing vertical boundaries:
    a.  Find the column index of the leftmost boundary (`col_left`) and the rightmost boundary (`col_right`) defined by Object B relevant to Object A.
    b.  For each row `r` in `rows_A`:
        i.  Iterate through the columns from `col_left` to `col_right` (inclusive).
        ii. Set the color of the pixel at `(r, col)` in the output grid to the color of Object A.
6.  **Else** (Object B does not form enclosing boundaries, e.g., it's between parts of A):
    a.  For each row `r` in `rows_A`:
        i.  Find the minimum column index (`min_col_A`) and the maximum column index (`max_col_A`) occupied by Object A *in this specific row r*.
        ii. Iterate through the columns from `min_col_A` to `max_col_A` (inclusive).
        iii. Set the color of the pixel at `(r, col)` in the output grid to the color of Object A.
7.  Return the final output grid.