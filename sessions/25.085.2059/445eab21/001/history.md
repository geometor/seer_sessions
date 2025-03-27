
## train_1

**input:**
```
6 6 6 6 6 0 0 0 0 0
6 0 0 0 6 0 0 0 0 0
6 0 0 0 6 0 0 0 0 0
6 6 6 6 6 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 7 7 7 7 7 7 0 0
0 0 7 0 0 0 0 7 0 0
0 0 7 0 0 0 0 7 0 0
0 0 7 7 7 7 7 7 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
7 7
7 7
```


## train_2

**input:**
```
0 7 7 7 7 0 0 0 0 0
0 7 0 0 7 0 0 0 0 0
0 7 0 0 7 0 0 0 0 0
0 7 7 7 7 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 0 0
0 0 0 8 0 0 0 8 0 0
0 0 0 8 0 0 0 8 0 0
0 0 0 8 8 8 8 8 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
8 8
8 8
```


## train_3

**input:**
```
0 4 4 4 4 4 4 0 0 0
0 4 0 0 0 0 4 0 0 0
0 4 0 0 0 0 4 0 0 0
0 4 0 0 0 0 4 0 0 0
0 4 0 0 0 0 4 0 0 0
0 4 0 0 0 0 4 0 0 0
0 4 4 4 4 4 4 0 0 0
0 0 0 0 0 0 0 2 2 2
0 0 0 0 0 0 0 2 0 2
0 0 0 0 0 0 0 2 2 2
```


**output:**
```
4 4
4 4
```

*   **Perception:** The input grid contains two distinct objects, each being a hollow rectangle constructed from a single, non-white color. The background is white. The two rectangles always have different colors and sizes. The output grid is consistently a 2x2 square filled with a single color. This output color matches the color of one of the rectangles present in the input grid. By comparing the sizes of the two rectangles in each example, it appears the output color is determined by the color of the rectangle that occupies the larger area (calculated by its bounding box).

*   **Facts:**
    
```yaml
    input_grid:
      description: A grid containing pixels of various colors.
      objects:
        - type: background
          color: white (0)
        - type: rectangle
          count: 2
          properties:
            - hollow
            - single_color (non-white)
            - distinct_colors
            - distinct_sizes
    output_grid:
      description: A 2x2 grid.
      properties:
        - uniform_color
    transformation:
      description: Selects one of the input rectangles based on size and uses its color for the output.
      steps:
        - identify_objects: Find all contiguous non-white pixel groups (rectangles).
        - calculate_property: For each rectangle, determine its bounding_box_area (width * height).
        - compare_property: Compare the bounding_box_area of the two rectangles.
        - select_object: Choose the rectangle with the larger bounding_box_area.
        - construct_output: Create a 2x2 grid filled with the color of the selected rectangle.
    relationships:
      - output_color: The color of the output grid is the color of the input rectangle with the largest bounding box area.
      - output_size: The output grid dimensions are fixed at 2x2.
    ```


*   **Natural Language Program:**
    1.  Identify the two distinct, non-white, hollow rectangular objects within the input grid.
    2.  For each identified rectangle, calculate the area of its bounding box (width multiplied by height).
    3.  Determine which of the two rectangles has the larger bounding box area.
    4.  Create a new 2x2 grid.
    5.  Fill this 2x2 grid entirely with the color of the rectangle identified in step 3 (the one with the larger area).
