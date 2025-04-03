
## train_1

**input:**
```
0 0 0 3 0 0 3 3 3 0 0 0 3 3 0 0 0 3 3 3 0 0 3 3 0 0 0
```


**output:**
```
0 0 0 1 0 0 5 5 5 0 0 0 2 2 0 0 0 5 5 5 0 0 2 2 0 0 0
```


## train_2

**input:**
```
0 0 3 0 3 3 0 3 3 3 0 3 0 0 0 3 3 3 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 1 0 2 2 0 5 5 5 0 1 0 0 0 5 5 5 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 3 0 0 0 3 3 0 3 3 3 0 3 3 0 0 0 3 3 3 0 0 0 0 0 0
```


**output:**
```
0 0 1 0 0 0 2 2 0 5 5 5 0 2 2 0 0 0 5 5 5 0 0 0 0 0 0
```

*   **Perception:**
    *   The input and output grids have the same dimensions (1x27 in this example).
    *   The input grids contain only white (0) and green (3) pixels.
    *   The output grids contain white (0), blue (1), red (2), and gray (5) pixels.
    *   The transformation preserves the positions of white pixels.
    *   The green pixels in the input appear in contiguous horizontal blocks of varying lengths (1, 2, or 3 pixels).
    *   In the output, these blocks of green pixels are replaced by blocks of a single color, maintaining the original position and size.
    *   The replacement color depends on the length of the original green block:
        *   A block of one green pixel (length 1) is replaced by blue (1).
        *   A block of two green pixels (length 2) is replaced by red (2).
        *   A block of three green pixels (length 3) is replaced by gray (5).

*   **YAML Facts:**
    
```yaml
    task_description: Recolor contiguous horizontal blocks of green pixels based on their length.
    grid_properties:
      - dimensions_preserved: True
      - background_color: white (0)
      - background_preserved: True
    objects:
      - object_type: contiguous_block
        input_color: green (3)
        properties:
          - property: horizontal_length
            values: [1, 2, 3]
        actions:
          - action: recolor
            based_on: horizontal_length
            mapping:
              1: blue (1)
              2: red (2)
              3: gray (5)
        output_colors: [blue (1), red (2), gray (5)]
    relationships:
      - relationship: input_output_mapping
        description: Each contiguous horizontal block of green pixels in the input corresponds to a block of the same size and position in the output, but with a color determined by the input block's length.
    ```


*   **Natural Language Program:**
    1.  Create an output grid with the same dimensions as the input grid, initially filled with white (0) pixels.
    2.  Iterate through the input grid horizontally, identifying contiguous sequences (blocks) of green (3) pixels.
    3.  For each identified green block:
        a.  Determine its length (number of pixels).
        b.  Determine the replacement color based on the length:
            *   If the length is 1, the replacement color is blue (1).
            *   If the length is 2, the replacement color is red (2).
            *   If the length is 3, the replacement color is gray (5).
        c.  Fill the corresponding positions in the output grid with the determined replacement color.
    4.  Ensure all pixels that were not part of a green block in the input remain white (0) in the output (this is handled by step 1 and overwriting in step 3c).
    5.  Return the completed output grid.
