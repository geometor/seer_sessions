
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0 0 0
0 0 1 1 0 0 0 0 0 0 0 0
0 0 0 1 0 0 0 0 0 0 0 0
0 0 1 1 1 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
1 0 0
1 1 0
0 1 0
1 1 1
0 0 1
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 0 0 0 0 0
0 0 0 0 0 2 0 0 0 0 0 0
0 0 0 2 2 2 0 0 0 0 0 0
0 0 0 2 0 2 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 2 2 2
0 0 2 0
2 2 2 0
2 0 2 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 8 0 8 0 0 0 0 0
0 0 0 8 8 8 8 0 0 0 0 0
0 0 0 0 0 0 8 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 8 0 8 0
8 8 8 8 0
0 0 0 8 8
```

Okay, let's break down this task.

**Perception of Elements:**

1.  **Input Grid:** Each input grid is relatively large and mostly consists of white pixels (0).
2.  **Object:** Within each input grid, there is a single contiguous object composed of non-white pixels (blue=1 in train\_1, red=2 in train\_2, azure=8 in train\_3). The object's shape varies across examples.
3.  **Output Grid:** The output grid is smaller than the input grid. It contains the *exact* shape and color of the object from the input grid, plus any white pixels that were immediately adjacent to the object within the minimal bounding box enclosing the object.
4.  **Transformation:** The process appears to be one of localization and extraction. The core colored object is identified, and then the smallest rectangular region containing this object is cropped from the input grid to form the output grid.

**YAML Facts:**


```yaml
task_name: crop_object
description: Extract the minimal bounding box containing the single non-white object from the input grid.

examples:
  train_1:
    input:
      grid_size: [11, 12]
      objects:
        - color: 1 # blue
          pixels: [[1, 2], [2, 2], [2, 3], [3, 3], [4, 2], [4, 3], [4, 4], [5, 4]]
          bounding_box: # Calculated [min_row, min_col, max_row, max_col]
            rows: [1, 5]
            cols: [2, 4]
      background_color: 0 # white
    output:
      grid_size: [5, 3] # (max_row - min_row + 1, max_col - min_col + 1)
      content: Cropped section of input from row 1 to 5 and column 2 to 4.
  train_2:
    input:
      grid_size: [10, 12]
      objects:
        - color: 2 # red
          pixels: [[2, 4], [2, 5], [2, 6], [3, 5], [4, 3], [4, 4], [4, 5], [5, 3], [5, 5]]
          bounding_box:
            rows: [2, 5]
            cols: [3, 6]
      background_color: 0 # white
    output:
      grid_size: [4, 4]
      content: Cropped section of input from row 2 to 5 and column 3 to 6.
  train_3:
    input:
      grid_size: [12, 12]
      objects:
        - color: 8 # azure
          pixels: [[3, 4], [3, 6], [4, 3], [4, 4], [4, 5], [4, 6], [5, 6], [5, 7]]
          bounding_box:
            rows: [3, 5]
            cols: [3, 7]
      background_color: 0 # white
    output:
      grid_size: [3, 5]
      content: Cropped section of input from row 3 to 5 and column 3 to 7.

common_properties:
  - Input contains a single non-white object.
  - Background is always white (0).
  - Output is a subgrid of the input.
  - The output subgrid is the smallest rectangle containing all non-white pixels.

transformation:
  action: "crop"
  target: "non-white object"
  parameter: "minimal bounding box"
```


**Natural Language Program:**

1.  Scan the input grid to locate all pixels that are not white (color 0).
2.  Identify the coordinates (row and column indices) of all these non-white pixels.
3.  Determine the minimum and maximum row indices among these coordinates.
4.  Determine the minimum and maximum column indices among these coordinates.
5.  Define a rectangular region using these minimum and maximum row and column indices (inclusive).
6.  Extract (crop) this rectangular region from the input grid.
7.  The extracted region forms the output grid.
