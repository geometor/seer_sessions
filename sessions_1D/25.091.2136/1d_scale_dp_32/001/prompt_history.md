
## train_1

**input:**
```
0 0 0 0 6 6 6 0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 6 6 6 6 6 6 6 6 6 6 6 6 3 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 3
```


**output:**
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 3
```


## train_3

**input:**
```
0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 0 0 0 0 0 0 0 3 0
```


**output:**
```
0 0 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 2 3 0
```

*   **Perception:** The task involves processing single-row grids. Each input grid contains a contiguous block of a single color (other than white or green) and a single green pixel located somewhere to the right of the block. There are typically white pixels separating the block and the green pixel. The transformation extends the colored block to the right, filling the gap of white pixels between the original end of the block and the position just before the green pixel. The green pixel acts as a boundary marker, stopping the extension. The color of the block being extended varies between examples.

*   **Facts:**
    
```yaml
    task_type: grid_transformation
    grid_dimensionality: 1D (single row)
    input_features:
      - object_type: contiguous_block
        color: non-white (0), non-green (3)
        quantity: 1
        properties: [variable_color, variable_start_index, variable_end_index]
      - object_type: single_pixel
        color: green (3)
        quantity: 1
        properties: [fixed_color, variable_index]
      - object_type: background_pixels
        color: white (0)
        quantity: variable
        properties: [fixed_color]
    relationships:
      - type: spatial
        description: The contiguous block is always located to the left of the green pixel.
      - type: separation
        description: White pixels exist between the right edge of the block and the green pixel.
    actions:
      - action: identify
        target: contiguous block (non-white, non-green)
        details: Determine its color and end index.
      - action: identify
        target: green pixel (3)
        details: Determine its index.
      - action: modify_pixels
        target: white pixels (0)
        condition: Located between the end index of the block + 1 and the index of the green pixel - 1.
        effect: Change their color to the color of the contiguous block.
    output_features:
      - object_type: contiguous_block
        description: The original block is extended rightward.
        properties: [original_color, original_start_index, new_end_index]
        new_end_index: index of the green pixel - 1
      - object_type: single_pixel
        color: green (3)
        description: Remains unchanged in position and color.
      - object_type: background_pixels
        color: white (0)
        description: Pixels to the left of the original block start and to the right of the green pixel remain unchanged.
    ```


*   **Natural Language Program:**
    1.  Identify the single contiguous horizontal block of a color that is not white (0) or green (3). Note its color and the index of its rightmost pixel (end index).
    2.  Identify the index of the single green (3) pixel.
    3.  Iterate through the grid from the position immediately to the right of the block's end index up to, but not including, the index of the green pixel.
    4.  For each pixel in this range, change its color to the color identified in step 1.
    5.  Leave all other pixels in the grid unchanged.
    6.  The output is the modified grid.
