
## train_1

**input:**
```
0 8 0 0 0 0 0 0 0 0 0
0 0 8 0 0 0 8 0 0 0 8
0 0 0 0 0 0 0 0 0 8 8
0 0 8 0 0 0 0 0 8 0 0
8 0 5 0 0 0 0 0 5 0 0
0 0 5 0 0 8 8 0 5 0 0
0 0 5 0 0 0 0 0 5 0 0
0 0 8 0 8 0 0 0 8 0 0
0 8 0 0 0 0 0 0 8 8 0
```


**output:**
```
8 0 0 0 0 0 8
5 0 0 0 0 0 5
5 0 0 8 8 0 5
5 0 0 0 0 0 5
8 0 8 0 0 0 8
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0
0 8 0 0 0 8 0 0 8
0 5 0 0 0 5 0 0 0
0 5 0 8 0 5 0 8 0
0 5 0 0 0 5 0 0 0
0 8 0 0 0 8 0 0 0
0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 8 0
0 8 0 0 0 0 0 0 0
```


**output:**
```
8 0 0 0 8
5 0 0 0 5
5 0 8 0 5
5 0 0 0 5
8 0 0 0 8
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 8 8 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 0 0 0 8 0 0 0 0 0
0 0 0 5 0 0 0 5 0 8 0 0 0
0 0 8 5 0 8 0 5 0 0 0 0 0
0 0 0 5 0 0 0 5 8 0 0 0 0
0 0 8 5 0 8 0 5 0 0 0 0 0
0 0 0 8 0 0 0 8 0 0 8 0 0
0 0 0 0 0 0 0 0 0 0 8 0 0
0 0 8 8 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 8 0 0 0 0
```


**output:**
```
8 0 0 0 8
5 0 0 0 5
5 0 8 0 5
5 0 0 0 5
5 0 8 0 5
8 0 0 0 8
```

Okay, let's analyze the task examples.

**Perception:**

1.  **Input/Output Colors:** Both input and output grids primarily use white (0), gray (5), and azure (8) pixels.
2.  **Grid Size:** The output grid is consistently smaller than the input grid.
3.  **Key Feature - Gray Pixels:** The gray (5) pixels in the input appear crucial. They seem to form vertical structures, often pairs of lines or segments.
4.  **Key Feature - Azure Pixels:** Azure (8) pixels are also present, often appearing near the gray structures or scattered elsewhere.
5.  **Transformation:** The output seems to be a cropped section of the input grid. The cropping region appears centered around the gray pixels.
6.  **Bounding Box:** Let's consider the bounding box containing *only* the gray (5) pixels in the input.
    *   Example 1: Gray pixels are in rows 4-6, columns 2-8. BBox height=3, width=7. Output is 5x7.
    *   Example 2: Gray pixels are in rows 2-4, columns 1-5. BBox height=3, width=5. Output is 5x5.
    *   Example 3: Gray pixels are in rows 3-6, columns 3-7. BBox height=4, width=5. Output is 6x5.
7.  **Pattern:** The output width matches the width of the gray pixel bounding box (`max_col_gray - min_col_gray + 1`). The output height is consistently 2 rows larger than the height of the gray pixel bounding box (`max_row_gray - min_row_gray + 1 + 2`).
8.  **Cropping Rule:** The output appears to be the subgrid extracted from the input using the column range defined by the gray bounding box (`min_col_gray` to `max_col_gray`) and a row range expanded by one row above and one row below the gray bounding box (`min_row_gray - 1` to `max_row_gray + 1`).

**Facts:**


```yaml
task_elements:
  - item: grids
    description: Input and output are 2D grids of pixels with colors 0 (white), 5 (gray), and 8 (azure).
  - item: gray_pixels
    properties:
      - color_value: 5
      - role: Defines the core region of interest for the transformation.
    relationships:
      - determines the column boundaries of the output grid.
      - determines the central rows of the output grid region.
  - item: azure_pixels
    properties:
      - color_value: 8
    relationships:
      - They are included in the output if they fall within the extracted region defined by the gray pixels.
  - item: white_pixels
    properties:
      - color_value: 0
      - role: Background color.
    relationships:
      - They are included in the output if they fall within the extracted region.
transformation:
  - action: identify_gray_pixels
    input: input_grid
    output: coordinates of all gray (5) pixels.
  - action: calculate_gray_bounding_box
    input: coordinates of gray pixels
    output: min_row_gray, max_row_gray, min_col_gray, max_col_gray
    description: Find the minimum and maximum row and column indices containing gray pixels.
  - action: determine_output_boundaries
    input: min_row_gray, max_row_gray, min_col_gray, max_col_gray
    output: start_row, end_row, start_col, end_col
    logic:
      - start_row = min_row_gray - 1
      - end_row = max_row_gray + 1
      - start_col = min_col_gray
      - end_col = max_col_gray
  - action: extract_subgrid
    input: input_grid, start_row, end_row, start_col, end_col
    output: output_grid
    description: Select the portion of the input grid defined by the calculated row and column boundaries.
output_characteristics:
  - property: width
    derivation: max_col_gray - min_col_gray + 1
  - property: height
    derivation: (max_row_gray - min_row_gray + 1) + 2
  - property: content
    derivation: A direct sub-section of the input grid based on the expanded gray bounding box.

```


**Natural Language Program:**

1.  Identify all pixels in the input grid that have the color gray (5).
2.  Determine the minimum row index (`min_r`), maximum row index (`max_r`), minimum column index (`min_c`), and maximum column index (`max_c`) occupied by these gray pixels. If no gray pixels exist, the behavior is undefined by these examples (but assume they always exist).
3.  Define the row range for extraction as starting from `min_r - 1` and ending at `max_r + 1` (inclusive).
4.  Define the column range for extraction as starting from `min_c` and ending at `max_c` (inclusive).
5.  Extract the subgrid from the input grid using these calculated row and column ranges.
6.  The extracted subgrid is the final output grid.
