
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 0 0 0 0 0 0 0 0 0 0 8 0 0
0 0 2 0 0 0 0 0 0 0 0 0 0 8 8 8 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0
0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 3 3 3 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 2 0 0 3 0 0 8 0
2 2 2 3 3 3 8 8 8
0 2 0 0 3 0 0 8 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0
0 0 3 0 3 0 0 0 0 0
0 0 0 3 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 1 0 0 0 0 0
0 0 0 1 0 1 0 0 0 0
0 0 0 0 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 8 0 0 0 0
0 0 0 0 8 0 8 0 0 0
0 0 0 0 0 8 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 3 0
3 0 3
0 3 0
0 1 0
1 0 1
0 1 0
0 8 0
8 0 8
0 8 0
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 2 0 2 0 0 0 0
0 0 0 0 2 0 0 0 0 0
0 0 0 2 0 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 1 0 1 0 0 0 0 0 0
0 0 1 0 0 0 0 0 0 0
0 1 0 1 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
2 0 2
0 2 0
2 0 2
1 0 1
0 1 0
1 0 1
```

**Perception of Task Elements:**

1.  **Input Grids:** The input grids contain multiple distinct objects, each made of a single non-white color (red, green, azure, blue). These objects are scattered across a larger white background. The objects often resemble plus signs ('+'), 'X' shapes, or diamonds, but they are defined simply as contiguous blocks of the same color.
2.  **Output Grids:** The output grids are significantly smaller than the input grids. They contain the same objects found in the input, but extracted and arranged differently.
3.  **Transformation:** The core transformation involves identifying each distinct non-white object in the input grid. For each object, its minimal bounding box (the smallest rectangle enclosing the object) is determined. The content within this bounding box is extracted. These extracted object subgrids are then stacked vertically in the output grid, preserving their original colors and relative pixel positions within their bounding boxes. The order of stacking seems to correspond to the order the objects are encountered, likely scanning top-to-bottom, left-to-right based on the top-left corner of their bounding boxes. The final output grid's width is determined by the maximum width of any extracted object's bounding box. The height is the sum of the heights of all extracted bounding boxes.

**YAML Facts:**


```yaml
task_description: Extract non-white objects based on their minimal bounding boxes and stack them vertically in the output.

elements:
  - role: background
    properties:
      color: white (0)
  - role: object
    properties:
      color: non-white (1-9)
      shape: contiguous block of a single color
      count: multiple per input grid
      location: scattered within the input grid

relationships:
  - type: spatial
    description: Objects are separated by the white background in the input.
  - type: transformation
    description: Each non-white object from the input is individually processed and contributes to the output.

actions:
  - name: identify_objects
    inputs: input_grid
    outputs: list of non-white objects (represented by their pixels and locations)
    description: Find all connected components of non-white pixels.
  - name: calculate_bounding_box
    inputs: object
    outputs: bounding_box (top-left corner coordinates, height, width)
    description: Determine the minimum rectangle enclosing all pixels of the object.
  - name: extract_object_subgrid
    inputs: input_grid, bounding_box
    outputs: subgrid (containing the object cropped to its bounding box)
    description: Crop the portion of the input grid defined by the object's bounding box.
  - name: stack_subgrids
    inputs: list of extracted subgrids
    outputs: output_grid
    description: Arrange the extracted subgrids vertically, one below the other, aligning them to the left. The final width is the maximum width among all subgrids.

output_properties:
  - property: composition
    value: Concatenation of extracted object subgrids.
  - property: arrangement
    value: Vertical stacking.
  - property: order
    value: Determined by the order of objects found in the input (likely top-to-bottom, left-to-right based on bounding box top-left corner).
  - property: dimensions
    value: Width is the maximum width of any extracted subgrid; height is the sum of the heights of all extracted subgrids.
```


**Natural Language Program:**

1.  Scan the input grid to identify all distinct contiguous objects composed of non-white pixels (colors 1 through 9). Treat each connected group of same-colored pixels as a single object.
2.  For each identified object:
    a.  Determine its minimal bounding box (the smallest rectangle containing all its pixels).
    b.  Extract the subgrid corresponding to this bounding box from the input grid.
3.  Collect all the extracted subgrids.
4.  Determine the order of these subgrids, likely based on the top-to-bottom, then left-to-right position of the top-left corner of their respective bounding boxes in the original input grid.
5.  Construct the output grid by vertically stacking the extracted subgrids in the determined order.
6.  The width of the output grid should be equal to the maximum width among all the extracted subgrids. Pad narrower subgrids with the background color (white) on the right if necessary to match this maximum width (although padding isn't explicitly shown in the examples, it's implied for consistent stacking).
7.  The height of the output grid should be the sum of the heights of all the extracted subgrids.
