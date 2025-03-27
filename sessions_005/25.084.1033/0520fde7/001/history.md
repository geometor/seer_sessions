
## train_1

**input:**
```
1 1 0 5 0 1 0
0 0 1 5 1 1 1
1 1 0 5 0 1 0
```


**output:**
```
0 2 0
0 0 2
0 2 0
```


## train_2

**input:**
```
1 0 0 5 0 1 0
0 1 0 5 1 1 1
1 0 0 5 0 0 0
```


**output:**
```
0 0 0
0 2 0
0 0 0
```


## train_3

**input:**
```
0 0 1 5 0 0 0
1 1 0 5 1 0 1
0 1 1 5 1 0 1
```


**output:**
```
0 0 0
2 0 0
0 0 2
```

Okay, let's break down this task.

## Perception

1.  **Input Grid Structure**: The input grids consistently have a height of 3 and a width of 7.
2.  **Key Feature**: There's a distinct vertical column of gray (5) pixels always located at the center column (index 3). This column appears to act as an axis or separator.
3.  **Symmetry**: The task seems to involve comparing the left side of the grid (columns 0-2) with the right side (columns 4-6) relative to the central gray column.
4.  **Pixel Colors**: The input primarily uses blue (1) and white (0) pixels on either side of the gray column.
5.  **Output Grid Structure**: The output grids have the same height (3) as the input but a width of 3, matching the width of the left (or right) section of the input grid.
6.  **Output Colors**: The output grids only contain red (2) and white (0) pixels.
7.  **Transformation Logic**: The placement of red pixels in the output corresponds to locations on the *left side* of the input grid. Comparing the input examples, a red pixel appears in the output at position `(r, c)` if the pixel at `input[r][c]` *matches* the pixel symmetrically opposite it on the right side, `input[r][6-c]`, *and* if that matching pixel is *not* white (0). If the pixels don't match, or if they match but are white (0), the corresponding output pixel is white (0).

## Facts


```yaml
task_description: Compare pixels symmetrically across a central gray vertical line and mark non-white matches.

elements:
  - name: input_grid
    type: grid
    properties:
      height: 3
      width: 7
      pixels:
        colors: [white, blue, gray] # 0, 1, 5
        distribution:
          - color: gray (5)
            location: Forms a vertical line at the central column (index 3).
          - color: blue (1) / white (0)
            location: Occupy the remaining cells to the left and right of the gray line.
  - name: output_grid
    type: grid
    properties:
      height: 3
      width: 3 # Matches the width of the input grid's left section
      pixels:
        colors: [white, red] # 0, 2

relationships:
  - type: symmetry_axis
    source: input_grid
    target: gray_column
    details: The column containing only gray (5) pixels acts as a vertical axis of symmetry. In the examples, this is column index 3.
  - type: pixel_comparison
    source: input_grid
    target: output_grid
    details: |
      Each pixel `(r, c)` in the output grid corresponds to a pixel `(r, c)` in the left section (columns 0 to axis_col - 1) of the input grid.
      The value of `output[r][c]` depends on comparing `input[r][c]` with its symmetrical counterpart `input[r][width - 1 - c]` across the gray axis.
  - type: color_mapping
    source: pixel_comparison result
    target: output_grid pixel value
    details: |
      If `input[r][c]` equals `input[r][width - 1 - c]` AND `input[r][c]` is not white (0), then `output[r][c]` is red (2).
      Otherwise, `output[r][c]` is white (0).

constants:
  - name: axis_color
    value: gray (5)
  - name: background_color
    value: white (0)
  - name: primary_input_color
    value: blue (1)
  - name: output_match_color
    value: red (2)

assumptions:
  - The input grid will always have an odd number of columns.
  - There will always be exactly one column consisting entirely of the axis color (gray).
```


## Natural Language Program

1.  **Identify the Axis**: Find the vertical column in the input grid that consists entirely of gray (5) pixels. Let the index of this column be `axis_col`.
2.  **Determine Output Size**: The output grid will have the same number of rows as the input grid and a number of columns equal to `axis_col`.
3.  **Initialize Output**: Create a new grid for the output with the determined dimensions, filling it entirely with white (0) pixels.
4.  **Compare Symmetrically**: Iterate through each row `r` from 0 to `height - 1` and each column `c` from 0 to `axis_col - 1` of the input grid.
5.  **Check Condition**: For each position `(r, c)`, compare the pixel value `input[r][c]` with the pixel value symmetrically opposite the axis, which is `input[r][(axis_col * 2) - c]`.
6.  **Set Output Pixel**: If the two pixel values (`input[r][c]` and `input[r][(axis_col * 2) - c]`) are identical *and* this value is *not* white (0), then set the corresponding pixel in the output grid `output[r][c]` to red (2). Otherwise, leave `output[r][c]` as white (0).
7.  **Return Output**: The completed grid is the result.
