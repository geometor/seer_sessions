*   **Perception**
    *   The input grids contain two distinct solid rectangular blocks of color, set against a white background (color 0).
    *   The two colored blocks are separated by a region of white pixels, either horizontally or vertically.
    *   The output grids are identical to the input grids, with the addition of a new solid rectangular block of azure color (color 8).
    *   This new azure block is always located in the white space directly between the two original colored blocks.
    *   The position and size of the azure block depend on the relative positions and dimensions of the original two blocks.
    *   If the original blocks are separated horizontally (different column ranges, overlapping row ranges), the azure block fills the horizontal gap between them and is vertically centered within the row range where the original blocks overlap.
    *   If the original blocks are separated vertically (different row ranges, overlapping column ranges), the azure block fills the vertical gap between them and is horizontally centered within the column range where the original blocks overlap.
    *   The original blocks remain unchanged in the output.

*   **Facts**
    
```yaml
    task_type: object_manipulation
    objects:
      - object_type: rectangle
        count: 2
        color: non-white (variable)
        properties:
          - solid_fill
          - fixed_position_in_input
          - fixed_color_in_input
      - object_type: background
        color: white (0)
      - object_type: rectangle # Added in output
        count: 1
        color: azure (8)
        properties:
          - solid_fill
          - derived_position
          - derived_size
    relationships:
      - type: spatial_separation
        object1: rectangle_1
        object2: rectangle_2
        dimension: horizontal_or_vertical
        gap: region_of_white_pixels
      - type: spatial_overlap
        object1: rectangle_1
        object2: rectangle_2
        dimension: vertical_if_horizontal_separation_else_horizontal
    actions:
      - action: identify_objects
        target: non-white_rectangles
        result: bounding_boxes
      - action: determine_separation_and_overlap
        input: bounding_boxes
        output: separation_dimension, gap_range, overlap_dimension, overlap_range
      - action: calculate_new_block_properties
        input: gap_range, overlap_range
        output: new_block_position, new_block_size
        details: |
          If separation is horizontal:
            new_block_cols = gap_range
            new_block_height = size_of_gap_range (width) # Based on train_1, size is determined by gap width, not height? Let's re-check train_1. Azure block is 3x3. Gap width 3. Overlap height 5. Centered height is 3. It seems size in the overlap dimension is also determined by the gap dimension size. Let's assume square based on train_1? No, train_2 is 3x2, train_3 is 5x4.
            Let's refine:
            If horizontal separation:
              new_block_cols = gap_columns
              new_block_rows = center(size=width_of_gap_columns, within=overlap_rows)
            If vertical separation:
              new_block_rows = gap_rows
              new_block_cols = center(size=height_of_gap_rows, within=overlap_columns)
      - action: draw_new_block
        target: output_grid
        color: azure (8)
        position: new_block_position
        size: new_block_size
    ```


*   **Natural Language Program**
    1.  Identify the two distinct non-white, solid rectangular objects in the input grid. Determine their bounding boxes (top-left and bottom-right coordinates).
    2.  Determine if the objects are separated primarily horizontally or vertically by examining their bounding boxes.
        *   If their row ranges overlap, but their column ranges do not, they are separated horizontally.
        *   If their column ranges overlap, but their row ranges do not, they are separated vertically.
    3.  **If separated horizontally:**
        *   Define the `gap_columns` as the range of columns strictly between the right edge of the left object and the left edge of the right object.
        *   Define the `overlap_rows` as the intersection of the row ranges of the two objects.
        *   Calculate the `new_block_width` as the number of columns in `gap_columns`.
        *   Calculate the `new_block_height` based on centering within `overlap_rows`. The height should be equal to the `new_block_width`. Calculate the starting row for the new block by finding the row that centers a block of `new_block_height` within the `overlap_rows`.
        *   The `new_block_start_col` is the first column in `gap_columns`.
    4.  **If separated vertically:**
        *   Define the `gap_rows` as the range of rows strictly between the bottom edge of the top object and the top edge of the bottom object.
        *   Define the `overlap_columns` as the intersection of the column ranges of the two objects.
        *   Calculate the `new_block_height` as the number of rows in `gap_rows`.
        *   Calculate the `new_block_width` based on centering within `overlap_columns`. The width should be equal to the `new_block_height`. Calculate the starting column for the new block by finding the column that centers a block of `new_block_width` within the `overlap_columns`.
        *   The `new_block_start_row` is the first row in `gap_rows`.
    5.  Create the output grid by copying the input grid.
    6.  Fill the rectangle defined by the calculated starting row/column and the calculated height/width with azure color (8) in the output grid.

    *Self-Correction during NL Program generation:* My initial YAML logic for size was slightly off. Re-examining train_1 (3x3 azure for 3-wide gap), train_2 (3x2 azure for 3-high gap), and train_3 (5x4 azure for 5-high gap) suggests the size of the new block in the *overlap* dimension might not simply be equal to the size of the gap dimension.
    *   Train 1: Gap width 3, Overlap height 5 -> Azure 3x3. Height is `gap_width`. Centered in 5.
    *   Train 2: Gap height 3, Overlap width 4 -> Azure 3x2. Width is NOT `gap_height`. Width is centered (size 2) in 4.
    *   Train 3: Gap height 5, Overlap width 6 -> Azure 5x4. Width is NOT `gap_height`. Width is centered (size 4) in 6.

    *Revised Natural Language Program:*
    1.  Identify the two distinct non-white, solid rectangular objects and their bounding boxes.
    2.  Determine if separation is horizontal (row overlap, column gap) or vertical (column overlap, row gap).
    3.  **If separated horizontally:**
        *   Identify `gap_columns` and `overlap_rows`.
        *   The new block's columns are `gap_columns`.
        *   The new block's height is the width of `gap_columns`.
        *   The new block's rows are determined by centering a block of this height within `overlap_rows`.
    4.  **If separated vertically:**
        *   Identify `gap_rows` and `overlap_columns`.
        *   The new block's rows are `gap_rows`.
        *   The new block's width is the height of `gap_rows`.
        *   The new block's columns are determined by centering a block of this width within `overlap_columns`.
    5.  Create the output grid by copying the input grid.
    6.  Fill the calculated rectangular area for the new block with azure color (8).

    *Final check on revised logic:*
    *   Train 1: Horiz sep. Gap cols 4-6 (width 3). Overlap rows 3-7 (height 5). -> Azure cols 4-6. Azure height = gap width = 3. Center height 3 in rows 3-7: offset (5-3)//2=1. Start row 3+1=4. Rows 4-6. -> Azure block (4,4) to (6,6). Correct.
    *   Train 2: Vert sep. Gap rows 4-6 (height 3). Overlap cols 1-4 (width 4). -> Azure rows 4-6. Azure width = gap height = 3. Center width 3 in cols 1-4: offset (4-3)//2=0 (integer division). Start col 1+0=1. Cols 1-3. -> Azure block (4,1) to (6,3). **Incorrect.** Output is (4,2) to (6,3), width 2.
    *   Train 3: Vert sep. Gap rows 3-7 (height 5). Overlap cols 3-8 (width 6). -> Azure rows 3-7. Azure width = gap height = 5. Center width 5 in cols 3-8: offset (6-5)//2=0. Start col 3+0=3. Cols 3-7. -> Azure block (3,3) to (7,7). **Incorrect.** Output is (3,4) to (7,7), width 4.

    Let's rethink the size calculation in the overlap dimension. It's not equal to the gap dimension size. It seems related to centering.
    *   Train 1: Center 3x? in rows 3-7 (height 5), cols 4-6 (width 3). Fills cols -> width=3. Center height 3 in 5 rows -> rows 4-6. Size 3x3.
    *   Train 2: Center ?x? in rows 4-6 (height 3), cols 1-4 (width 4). Fills rows -> height=3. Center width ? in 4 cols. Output width is 2. Center 2 in 4 -> offset 1 -> cols 2-3. Size 3x2.
    *   Train 3: Center ?x? in rows 3-7 (height 5), cols 3-8 (width 6). Fills rows -> height=5. Center width ? in 6 cols. Output width is 4. Center 4 in 6 -> offset 1 -> cols 4-7. Size 5x4.

    Okay, the dimension *along* the gap is filled completely. The dimension *across* the gap (the overlap dimension) seems to be centered, but what determines its size? It's not constant, not related to the gap size. Could it be related to the overlap size?
    *   Train 1: Overlap height 5. Azure height 3. Center 3 in 5.
    *   Train 2: Overlap width 4. Azure width 2. Center 2 in 4.
    *   Train 3: Overlap width 6. Azure width 4. Center 4 in 6.

    It looks like the size in the overlap dimension is `overlap_size - 2`?
    *   Train 1: Overlap height 5 -> Azure height 5-2=3. Correct.
    *   Train 2: Overlap width 4 -> Azure width 4-2=2. Correct.
    *   Train 3: Overlap width 6 -> Azure width 6-2=4. Correct.

    *Final Revised Natural Language Program:*
    1.  Identify the two distinct non-white, solid rectangular objects and their bounding boxes.
    2.  Determine if separation is horizontal (row overlap, column gap) or vertical (column overlap, row gap).
    3.  **If separated horizontally:**
        *   Identify `gap_columns` and `overlap_rows`.
        *   The new block's columns span the `gap_columns`.
        *   The new block's height is `height(overlap_rows) - 2`.
        *   The new block's rows are determined by centering a block of this calculated height within `overlap_rows`.
    4.  **If separated vertically:**
        *   Identify `gap_rows` and `overlap_columns`.
        *   The new block's rows span the `gap_rows`.
        *   The new block's width is `width(overlap_columns) - 2`.
        *   The new block's columns are determined by centering a block of this calculated width within `overlap_columns`.
    5.  Create the output grid by copying the input grid.
    6.  Fill the calculated rectangular area for the new block with azure color (8).