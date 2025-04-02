
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 0 0 0 0 2
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 0 0 0 0 0 2 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 7 2 0 0
```


## train_3

**input:**
```
0 1 1 1 1 1 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 2 0
```


**output:**
```
0 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 2 0
```

*   **Perception of Task Elements:**
    *   The task operates on single-row grids (1D arrays).
    *   Each input grid contains a contiguous horizontal block of a single color (e.g., azure, orange, blue), which I'll call the "main color block".
    *   Each input grid also contains a single red pixel (color 2).
    *   The red pixel always appears somewhere to the right of the main color block.
    *   The space between the main color block and the red pixel is filled with white pixels (color 0).
    *   The transformation involves extending the main color block to the right.
    *   The extension stops just before the red pixel. The red pixel acts as a boundary.
    *   Pixels to the left of the main color block and pixels at or to the right of the red pixel remain unchanged.

*   **YAML Facts:**
    
```yaml
    task_type: extension
    grid_dimensionality: 1D (represented as 1xN grid)
    objects:
      - type: main_color_block
        description: A contiguous horizontal segment of a single non-white, non-red color.
        properties:
          color: variable (azure, orange, blue in examples)
          position: variable, starts somewhere from the left.
          length: variable.
      - type: boundary_pixel
        description: A single pixel acting as a stop marker.
        properties:
          color: red (2)
          position: variable, always to the right of the main_color_block.
      - type: background_pixels
        description: Pixels filling the space.
        properties:
          color: white (0)
          position: surrounding main_color_block and boundary_pixel, notably filling the gap between them.
    actions:
      - name: extend_block
        target: main_color_block
        direction: right
        termination_condition: Stop extension at the position immediately preceding the boundary_pixel.
        effect: Overwrites background_pixels between the original end of the main_color_block and the boundary_pixel with the color of the main_color_block.
    relationships:
      - type: spatial
        description: The main_color_block is located to the left of the boundary_pixel.
      - type: functional
        description: The boundary_pixel determines the extent of the extend_block action.
    invariants:
      - Pixels to the left of the original main_color_block remain unchanged.
      - The boundary_pixel (red pixel) remains unchanged.
      - Pixels to the right of the boundary_pixel remain unchanged.
    ```


*   **Natural Language Program:**
    1.  Identify the contiguous horizontal block of non-white, non-red color (the main color block). Record its color and the column index of its rightmost pixel.
    2.  Identify the column index of the single red pixel (color 2).
    3.  Starting from the column immediately to the right of the main color block's rightmost pixel, change all pixels to the color of the main color block, up to (but not including) the column containing the red pixel.
    4.  Leave all other pixels in the grid unchanged.
