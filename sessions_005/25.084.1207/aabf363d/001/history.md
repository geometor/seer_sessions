
## train_1

**input:**
```
0 0 0 0 0 0 0
0 0 0 3 0 0 0
0 0 3 3 3 0 0
0 3 3 3 3 0 0
0 3 3 0 0 0 0
0 0 3 3 0 0 0
6 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0
0 0 0 6 0 0 0
0 0 6 6 6 0 0
0 6 6 6 6 0 0
0 6 6 0 0 0 0
0 0 6 6 0 0 0
0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0
0 2 2 2 0 0 0
0 0 2 0 0 0 0
0 2 2 2 2 0 0
0 0 2 2 2 0 0
0 0 0 2 0 0 0
4 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0
0 4 4 4 0 0 0
0 0 4 0 0 0 0
0 4 4 4 4 0 0
0 0 4 4 4 0 0
0 0 0 4 0 0 0
0 0 0 0 0 0 0
```

*   **Perception**:
    The task involves transforming an input grid into an output grid. Both input and output grids have the same dimensions. The input grid contains a background color (white/0), a larger contiguous object of one color (`source_color`), and a single pixel of another color (`target_color`). In the provided examples, this single pixel is located at the bottom-left corner. The output grid retains the shape and position of the larger object but changes its color from `source_color` to `target_color`. The single pixel that provided the `target_color` is removed (changed to the background color) in the output. The background pixels remain unchanged.

*   **Facts**:
    
```yaml
    task_context: Recolor a primary object based on the color of a secondary, single-pixel object, then remove the secondary object.
    elements:
      - type: grid
        properties:
          - dimensions: constant between input and output (e.g., 7x7)
          - background_color: white (0)
      - type: object
        description: The main object to be recolored.
        properties:
          - contiguity: contiguous block of pixels
          - color: variable (e.g., green(3), red(2)) - referred to as source_color
          - size: largest object by pixel count (> 1 pixel)
          - location: variable within the grid
      - type: object
        description: The color source and location marker.
        properties:
          - contiguity: single pixel
          - color: variable (e.g., magenta(6), yellow(4)) - referred to as target_color
          - size: 1 pixel
          - location: fixed position (bottom-left corner, (rows-1, 0)) - referred to as target_location
    actions:
      - action: identify
        target: background_color (white/0)
      - action: identify
        target: all non-background contiguous objects
      - action: select
        criteria: object with size = 1 pixel
        results:
          - target_color (color of the single pixel)
          - target_location (coordinates of the single pixel)
      - action: select
        criteria: object with largest size (> 1 pixel)
        results:
          - source_color (original color of the largest object)
          - source_pixels (coordinates of all pixels belonging to the largest object)
      - action: initialize
        target: output grid
        value: copy of input grid
      - action: recolor
        target: pixels in output grid corresponding to source_pixels
        using: target_color
      - action: erase
        target: pixel in output grid at target_location
        using: background_color
    relationship:
      - The color of the single-pixel object dictates the final color of the largest object.
      - The single-pixel object is removed after its color is used.
    output_grid_description:
      - The largest object from the input grid maintains its shape and position but adopts the target_color.
      - The pixel at the target_location is set to the background color.
      - All other background pixels remain unchanged.
    ```


*   **Natural Language Program**:
    1.  Define the background color as white (0).
    2.  Scan the input grid to find all contiguous objects composed of non-background colors.
    3.  Identify the object consisting of exactly one pixel. Record its color as `target_color` and its coordinates as `target_location`.
    4.  Identify the largest contiguous object (the one containing the most pixels). Record the set of coordinates occupied by this object as `source_locations` and its color as `source_color`.
    5.  Create the output grid with the same dimensions as the input grid, initially filling it with the background color.
    6.  For each coordinate in `source_locations`, set the color of the corresponding pixel in the output grid to `target_color`.
    7.  Ensure the pixel at `target_location` in the output grid is set to the background color (this step might be implicitly handled by step 5 and 6 if the `target_location` is not part of `source_locations`, but explicitly setting it ensures correctness).
