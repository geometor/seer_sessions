
## train_1

**input:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 2 0 0 0 0
0 0 2 2 2 0 0 0
0 0 2 2 0 0 0 0
```


**output:**
```
0 2 0 0 2 0
2 2 2 2 2 2
2 2 0 2 2 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0
0 8 8 0 0 0 0 0
0 0 8 0 0 0 0 0
0 8 8 8 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
8 8 0 8 8 0
0 8 0 0 8 0
8 8 8 8 8 8
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0
0 0 0 0 0 1 1 0
0 0 0 0 1 0 0 0
0 0 0 0 0 1 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0
```


**output:**
```
0 1 1 0 1 1
1 0 0 1 0 0
0 1 0 0 1 0
```

*   **Perception**:
    *   Each input grid contains a white background (color 0) and a single contiguous object composed of a non-white color (red, azure, or blue).
    *   The non-white object's shape varies across examples but seems confined within a relatively small area.
    *   The output grid is smaller than the input grid and contains only the non-white color from the input object and white pixels.
    *   The output grid dimensions appear consistent across examples (3x6).
    *   The pattern in the output grid seems directly related to the shape of the non-white object in the input.

*   **Facts**:
    
```yaml
    task_type: object transformation
    components:
      - role: background
        color: white
        properties: fills most of the input grid
      - role: primary_object
        count: 1
        color: non-white (varies: red, azure, blue)
        properties:
          - contiguous
          - shape varies
          - enclosed within a 3x3 bounding box in all examples
    transformation:
      - action: find_object
        target: primary_object
        criteria: color is not white
      - action: get_bounding_box
        target: primary_object
        result: bounding_box_subgrid (3x3 in examples)
      - action: construct_output
        source: bounding_box_subgrid
        output_dimensions: height of bounding_box_subgrid, 2 * width of bounding_box_subgrid (3x6 in examples)
        method: horizontal duplication (concatenate bounding_box_subgrid with itself side-by-side)
        color_preservation: True (non-white color remains the same)
    relationships:
      - The output grid's content is derived solely from the minimal bounding box of the input object.
      - The output grid's width is twice the width of the input object's bounding box.
      - The output grid's height is the same as the height of the input object's bounding box.
    ```


*   **Natural Language Program**:
    1.  Identify the single contiguous block of non-white pixels (the object) in the input grid.
    2.  Determine the minimal bounding box that encloses this object.
    3.  Extract the subgrid corresponding to this bounding box.
    4.  Construct the output grid by horizontally concatenating the extracted subgrid with a copy of itself. The resulting output grid will have the same height as the bounding box subgrid and twice its width.
