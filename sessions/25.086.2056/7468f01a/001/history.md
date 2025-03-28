
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 4 0 0 0 0 0 0 0 0
0 0 0 4 4 4 4 4 0 0 0 0 0 0 0 0
0 0 0 4 1 1 4 4 0 0 0 0 0 0 0 0
0 0 0 4 4 1 1 4 0 0 0 0 0 0 0 0
0 0 0 4 4 1 4 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
4 4 4 4 4
4 4 4 4 4
4 4 1 1 4
4 1 1 4 4
4 4 1 4 4
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 8 8 8 8 8 8 2 8 0 0 0 0 0
0 0 8 2 2 8 8 8 8 8 0 0 0 0 0
0 0 8 8 2 2 8 8 8 8 0 0 0 0 0
0 0 8 8 8 8 8 8 8 8 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
8 2 8 8 8 8 8 8
8 8 8 8 8 2 2 8
8 8 8 8 2 2 8 8
8 8 8 8 8 8 8 8
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 6 6 6 3 6 6 0 0 0 0 0 0 0 0 0
0 0 6 3 3 3 6 6 0 0 0 0 0 0 0 0 0
0 0 6 6 6 6 3 6 0 0 0 0 0 0 0 0 0
0 0 6 6 6 6 3 6 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
6 6 3 6 6 6
6 6 3 3 3 6
6 3 6 6 6 6
6 3 6 6 6 6
```

**Perception**

1.  **Input Grid Structure:** Each input grid consists primarily of a background color, which is white (0).
2.  **Foreground Object:** Within the white background, there is a single, contiguous block of non-white pixels. This block forms an "object".
3.  **Object Composition:** The object itself may contain pixels of different non-white colors. It appears to be a primary "outer" color forming the main shape, with other colors potentially appearing inside.
4.  **Output Grid Structure:** The output grid is significantly smaller than the input grid and contains only the non-white pixels observed in the input. The background white pixels are removed.
5.  **Transformation:** The transformation involves isolating the non-white object from the input grid and cropping the grid to the smallest possible rectangle (bounding box) that contains this object. The relative positions of the pixels within the object are preserved.

**Facts**


```yaml
task_elements:
  - item: input_grid
    attributes:
      - contains a background color (white, 0)
      - contains a single connected object composed of non-white pixels
  - item: non_white_object
    attributes:
      - composed of one or more non-white colors
      - located somewhere within the input grid
      - forms a contiguous shape
  - item: output_grid
    attributes:
      - represents the extracted non_white_object
      - dimensions are determined by the bounding box of the non_white_object
      - contains only the pixels from the non_white_object in their original relative arrangement
actions:
  - action: identify_pixels
    actor: system
    target: input_grid
    condition: pixel color is not white (0)
    result: set of non-white pixel coordinates
  - action: calculate_bounding_box
    actor: system
    target: set of non-white pixel coordinates
    computation: find minimum and maximum row and column indices
    result: coordinates of the top-left and bottom-right corners of the bounding box
  - action: extract_subgrid
    actor: system
    target: input_grid
    using: bounding box coordinates
    result: output_grid
```


**Natural Language Program**

1.  Scan the input grid to find all pixels that are not white (color value 0).
2.  Determine the minimum and maximum row indices among these non-white pixels.
3.  Determine the minimum and maximum column indices among these non-white pixels.
4.  These minimum/maximum row and column indices define the bounding box of the non-white object.
5.  Create a new grid (the output grid) whose dimensions match the height (max_row - min_row + 1) and width (max_col - min_col + 1) of the bounding box.
6.  Copy the pixels from the input grid within the calculated bounding box (from `min_row`, `min_col` to `max_row`, `max_col`) into the corresponding positions in the new output grid.
