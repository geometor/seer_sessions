
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 2 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 2 0 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 0 0
```


**output:**
```
0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 0 0
```


## train_3

**input:**
```
0 0 0 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 1 0 0 0 0 0 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception:** The task involves processing a single row (1D grid) containing a contiguous block of a single non-white color against a white background. The transformation preserves the first and last pixels of this colored block, changing all intermediate pixels within the block to white. The overall dimensions and the background color remain unchanged.

*   **Facts:**
    
```yaml
    task_type: object_transformation
    grid_dimensionality: 1D # Represented as 1xN arrays
    background_color: white (0)

    objects:
      - type: contiguous_block
        description: A horizontal sequence of identical non-white pixels.
        properties:
          - color: The specific non-white color of the block (e.g., red, green, blue).
          - location: Defined by the start and end indices within the row.
          - length: The number of pixels in the block.

    actions:
      - action: identify_block
        input: input_grid
        output: identified block object (color, start_index, end_index)
        description: Locates the start and end indices of the contiguous non-white block.
      - action: create_output
        input: input_grid dimensions, identified block object
        output: output_grid
        description: Generates the output grid based on the input dimensions and the block's properties.

    transformation:
      - description: Keep endpoints of the block
        details: The output grid retains the color of the identified block only at its original start and end indices. All other positions, including those previously occupied by the middle part of the block, are set to the background color (white).
        input_elements:
          - input_grid
          - identified_block (color, start_index, end_index)
        output_elements:
          - output_grid (same dimensions as input, initialized to white)
          - output_grid[start_index] = block_color
          - output_grid[end_index] = block_color

    relationships:
      - The output grid has the same dimensions as the input grid.
      - The non-white pixels in the output grid correspond directly to the start and end positions of the non-white block in the input grid.
      - The color of the non-white pixels in the output is identical to the color of the block in the input.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid, filled entirely with white pixels (color 0).
    2.  Scan the input grid to find the first non-white pixel. Record its color and its index (start index).
    3.  Continue scanning from the start index to find the last consecutive pixel of the same color. Record its index (end index).
    4.  Set the pixel in the output grid at the recorded start index to the recorded color.
    5.  Set the pixel in the output grid at the recorded end index to the recorded color.
    6.  Return the modified output grid.
