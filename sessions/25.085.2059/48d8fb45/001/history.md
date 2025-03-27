
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 5 0 0
0 0 0 0 0 0 4 4 0 0
0 0 4 0 0 0 0 0 4 0
0 4 0 4 0 0 0 4 0 0
0 0 4 4 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
4 4 0
0 0 4
0 4 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 1 1
0 0 0 5 0 0 0 1 1 0
0 0 0 1 0 0 0 0 1 0
0 0 1 1 1 0 0 0 0 0
0 0 0 1 1 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 1 1 0 0
0 0 0 0 0 1 1 1 0 0
0 0 0 0 0 0 1 1 0 0
```


**output:**
```
0 1 0
1 1 1
0 1 1
```


## train_3

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 2 2 0 0 0 0 0 0
0 2 0 2 0 0 0 0 0 0
0 0 2 0 0 0 0 5 0 0
0 0 0 0 0 0 0 2 2 0
0 0 0 0 0 0 2 2 0 0
0 0 0 0 0 0 0 2 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 2 2
2 2 0
0 2 0
```

*   **Perception:**
    *   The input grids are 10x10 and contain mostly white pixels (0).
    *   Each input grid features several distinct objects composed of colored pixels (1-blue, 2-red, 4-yellow in the examples).
    *   Crucially, each input grid contains exactly one gray pixel (5).
    *   The output grids are smaller (3x3).
    *   Each output grid contains only white pixels (0) and pixels of a single color, which corresponds to one of the colors present in the input grid (excluding gray).
    *   The gray pixel in the input appears to act as a reference point.
    *   The specific color and pattern of the output grid seem determined by the colored object in the input grid that is closest to the gray pixel.
    *   The output pattern appears to be a fixed 3x3 template associated with the color of the closest object, rather than a direct transformation (like cropping or scaling) of that object.

*   **Facts:**
    
```yaml
    task_elements:
      - element: input_grid
        properties:
          - size: 10x10
          - background_color: white (0)
          - contains: colored_objects, gray_marker
      - element: output_grid
        properties:
          - size: 3x3
          - background_color: white (0)
          - contains: single_color_pattern
      - element: colored_objects
        properties:
          - color: varies (blue, red, yellow observed)
          - shape: contiguous blocks of same-colored pixels
          - location: scattered within input_grid
      - element: gray_marker
        properties:
          - color: gray (5)
          - count: exactly one per input_grid
          - role: reference point
      - element: single_color_pattern
        properties:
          - color: determined by closest colored_object to gray_marker
          - shape: fixed 3x3 pattern based on color
    relationships:
      - type: proximity
        from: gray_marker
        to: colored_objects
        metric: Euclidean distance (minimum distance between gray pixel and any pixel of an object)
      - type: selection
        based_on: proximity
        selects: the colored_object closest to the gray_marker
      - type: mapping
        input: color of the selected closest colored_object
        output: a specific 3x3 single_color_pattern
    actions:
      - action: locate
        target: gray_marker in input_grid
      - action: identify
        target: all colored_objects (non-white, non-gray contiguous pixels) in input_grid
      - action: calculate_distance
        from: gray_marker location
        to: all pixels of each colored_object
        find: minimum distance for each object
      - action: determine_closest_object
        using: minimum distances calculated
      - action: retrieve_color
        from: closest_object
      - action: generate_output
        using: fixed 3x3 pattern corresponding to the retrieved color
    ```


*   **Natural Language Program:**
    1.  Identify the coordinates of the single gray pixel (color 5) in the input grid.
    2.  Identify all distinct contiguous objects composed of pixels with colors other than white (0) or gray (5).
    3.  For each identified colored object, calculate the minimum Euclidean distance between the gray pixel's coordinates and the coordinates of any pixel belonging to that object.
    4.  Determine which colored object has the smallest minimum distance to the gray pixel. This is the "closest object".
    5.  Identify the color of this closest object.
    6.  Based on the color identified in step 5, generate a specific, predefined 3x3 output grid:
        *   If the color is blue (1), the output is `[[0, 1, 0], [1, 1, 1], [0, 1, 1]]`.
        *   If the color is red (2), the output is `[[0, 2, 2], [2, 2, 0], [0, 2, 0]]`.
        *   If the color is yellow (4), the output is `[[4, 4, 0], [0, 0, 4], [0, 4, 0]]`.
        *   (Assume similar fixed patterns exist for other potential colors encountered in test cases).
    7.  Return the generated 3x3 grid as the output.
