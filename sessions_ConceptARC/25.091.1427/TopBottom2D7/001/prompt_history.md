
## train_1

**input:**
```
1 1 1 1 1 1 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 3 3 3 3 3
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
1 1 1 1 1 1
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 3 3 3 0 0 0 0
0 0 0 1 1 1 1 1
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
3 3 3
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 1 1 1 1 0 0 0
0 0 0 0 0 0 0 0
0 0 3 3 3 3 3 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
1 1 1 1
```


## train_4

**input:**
```
0 0 0 3 3 3 0 0
0 0 0 3 3 3 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 1 1 0 0 0 0 0
0 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
3 3 3
3 3 3
```


## train_5

**input:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
1
```

*   **Perception**: The input grids are 8x8 and contain a white background (0) with exactly two distinct non-white objects: one blue (1) and one green (3). These objects vary in shape (lines, rectangles, single pixels) and position. The output grid is smaller than the input and contains only one of the two colored objects from the input. The key transformation seems to be selecting one of the two objects based on a positional criterion and then cropping the grid to the minimal bounding box of the selected object. By comparing the objects' positions across examples, the object whose top-most pixel appears highest in the grid (minimum row index) is selected for the output. If both objects started on the same row (not shown in examples, but a logical consideration), the one starting further to the left (minimum column index) would likely be chosen. The output grid perfectly frames the selected object.

*   **YAML Facts**:
    
```yaml
    task_description: "Select one of two colored objects (blue or green) based on its vertical position and output its minimal bounding box."
    grid_properties:
      size: 8x8 (input), variable (output)
      background_color: white (0)
    objects:
      - id: object_1
        color: blue (1)
        shape: variable (contiguous block of pixels)
        count_in_input: 1
      - id: object_2
        color: green (3)
        shape: variable (contiguous block of pixels)
        count_in_input: 1
    properties_per_object:
      - pixels: List of coordinates for each pixel belonging to the object.
      - bounding_box: Defined by min_row, max_row, min_col, max_col.
      - top_row: The minimum row index occupied by any pixel of the object.
      - left_col_at_top_row: The minimum column index among pixels in the top_row.
    selection_rule:
      primary_criterion: Select the object with the minimum `top_row`.
      secondary_criterion (tie-breaker): If `top_row` values are equal, select the object with the minimum `left_col_at_top_row`.
    output_generation:
      action: Extract the subgrid defined by the `bounding_box` of the selected object.
      content: Contains only the pixels of the selected object, preserving their original color.
    ```


*   **Natural Language Program**:
    1.  Identify all distinct contiguous blocks of non-white pixels in the input grid. There will be exactly two such blocks (objects): one blue and one green.
    2.  For each identified object, determine its spatial extent, specifically finding the row index of its top-most pixel(s).
    3.  Compare the top-most row indices of the blue and green objects.
    4.  Select the object whose top-most row index is smaller (i.e., the object appearing higher in the grid).
    5.  (If the top-most row indices are identical, determine the column index of the left-most pixel in that top row for each object, and select the object with the smaller column index).
    6.  Determine the minimal bounding box (minimum row, maximum row, minimum column, maximum column) that encloses all pixels of the selected object.
    7.  Create the output grid by extracting the subgrid corresponding to this bounding box from the input grid, containing only the pixels of the selected object.
