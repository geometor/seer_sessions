
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 2 2 0 2 2 0 2 2
0 2 2 0 2 2 0 2 2 0 2 2
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
1 1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 0 2 2 0 2 2 0 2 2
0 2 2 0 2 2 0 2 2 0 2 2
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 3 0 0 0 0 0
0 0 0 3 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 3 0 0 0 0 0
0 0 0 3 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 3 3 3 3 0 0 0 0 0
0 0 0 3 3 3 3 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
1 0 0 0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0 0 0 0
1 0 0 3 3 3 3 0 0 0 0 0
1 0 0 3 3 3 3 0 0 0 0 0
1 0 0 0 0 0 0 0 0 0 0 0
1 0 0 3 3 3 3 0 0 0 0 0
1 0 0 3 3 3 3 0 0 0 0 0
1 0 0 0 0 0 0 0 0 0 0 0
1 0 0 3 3 3 3 0 0 0 0 0
1 0 0 3 3 3 3 0 0 0 0 0
1 0 0 0 0 0 0 0 0 0 0 0
1 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 4 0 0 0 4 0 0
0 0 0 0 4 4 4 0 4 4 4 0
0 0 0 0 0 4 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
1 1 1 1 1 1 1 1 1 1 1 1
0 0 0 0 0 4 0 0 0 4 0 0
0 0 0 0 4 4 4 0 4 4 4 0
0 0 0 0 0 4 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```

**Perception:**

The task involves modifying either the first row or the first column of the input grid based on the spatial extent of the non-white shapes present. The input grid contains one or more shapes made of a single color (red, green, or yellow in the examples) on a white background. The output grid is identical to the input, except for either the entire first row or the entire first column being changed to blue. The decision of whether to modify the row or the column depends on the overall dimensions (width vs. height) of the area occupied by the non-white shapes.

**Facts:**


```yaml
task_context:
  - The input grid contains a white background (0) and one or more objects composed of a single non-white color.
  - The output grid is derived from the input grid by modifying either the first row or the first column.
  - The modification involves changing all pixels in the selected row or column to blue (1).
  - The choice between modifying the first row or the first column depends on the geometry of the non-white shapes.

input_elements:
  - background: white pixels (0)
  - objects: contiguous groups of non-white pixels (colors 2, 3, 4 in examples)

transformation_logic:
  - Identify all non-white pixels in the input grid.
  - Determine the minimum bounding box that encloses all these non-white pixels.
  - Calculate the width (number of columns) and height (number of rows) of this bounding box.
  - condition:
      - if width > height:
          - target: first row (row index 0)
      - else (if height >= width):
          - target: first column (column index 0)
  - action:
      - Copy the input grid to the output grid.
      - Change all pixels in the target row or column to blue (1).

output_elements:
  - modified_grid: The input grid with either the first row or first column changed to blue (1).
```


**Natural Language Program:**

1.  Create a copy of the input grid. This copy will become the output grid.
2.  Find the coordinates (row, column) of all pixels in the input grid that are not white (color 0).
3.  If no non-white pixels are found, return the unmodified copy of the input grid.
4.  If non-white pixels exist, determine the minimum row index (`min_row`), maximum row index (`max_row`), minimum column index (`min_col`), and maximum column index (`max_col`) among these pixels.
5.  Calculate the height of the bounding box: `height = max_row - min_row + 1`.
6.  Calculate the width of the bounding box: `width = max_col - min_col + 1`.
7.  Compare the width and height:
    *   If `width` is greater than `height`, iterate through all columns of the first row (row 0) in the output grid and set their color to blue (1).
    *   Otherwise (if `height` is greater than or equal to `width`), iterate through all rows of the first column (column 0) in the output grid and set their color to blue (1).
8.  Return the modified output grid.
