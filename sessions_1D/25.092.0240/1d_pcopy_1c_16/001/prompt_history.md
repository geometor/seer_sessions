
## train_1

**input:**
```
0 0 9 9 9 0 0 0 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 9 9 9 0 0 9 9 9 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 2 2 2 0 0 0 2 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 2 2 2 0 0 2 2 2 0 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
0 0 8 8 8 0 0 0 0 8 0 0 0 0 0 8 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 8 8 8 0 0 0 8 8 8 0 0 0 8 8 8 0 8 8 8 0 0 0 0 0 0 0 0 0 0 0
```

*   **Perception:**
    *   The task involves modifying input grids containing various colored shapes on a white background.
    *   The primary colors observed are maroon (9), red (2), and azure (8), always on a white (0) background.
    *   Shapes appear as contiguous blocks of non-white pixels.
    *   The transformation specifically targets isolated, single non-white pixels.
    *   Larger shapes (composed of more than one pixel) remain unchanged in the output.
    *   Isolated single pixels are expanded horizontally to the right, forming a 1x3 line of the original pixel's color. The original pixel becomes the leftmost pixel of this new line.
    *   The background remains white, except where overwritten by the expanded pixels.

*   **YAML Facts:**
    
```yaml
    task_description: Modify grid based on the size of colored objects.
    background_color: white (0)
    objects:
      - type: shape
        properties:
          - color: non-white (e.g., maroon, red, azure)
          - connectivity: contiguous pixels (including diagonals)
          - size: number of pixels in the shape
    actions:
      - name: identify_objects
        description: Find all connected components of non-white pixels.
      - name: filter_objects
        criteria: Identify objects composed of exactly one pixel.
      - name: transform_single_pixel_objects
        description: Replace the single pixel with a 1x3 horizontal line of the same color, starting at the original pixel's location and extending rightwards.
        constraints: Respect grid boundaries; do not extend beyond the right edge.
      - name: preserve_larger_objects
        description: Copy objects composed of more than one pixel directly from input to output without change.
      - name: preserve_background
        description: Maintain white background pixels unless overwritten by the transformation.
    relationships:
      - The transformation rule depends solely on the size (pixel count) of each distinct colored object.
      - Single-pixel objects trigger expansion.
      - Multi-pixel objects are preserved.
    ```


*   **Natural Language Program:**
    1.  Initialize an output grid identical in size and background color (white) to the input grid.
    2.  Identify all distinct objects in the input grid. An object is a group of one or more contiguous pixels (sharing a side or corner) of the same non-white color.
    3.  For each identified object:
        a.  Count the number of pixels that make up the object.
        b.  If the object consists of exactly one pixel:
            i.  Determine the row `r`, column `c`, and color `clr` of this pixel.
            ii. In the output grid, color the pixel at `(r, c)` with `clr`.
            iii. If column `c+1` is within the grid bounds, color the pixel at `(r, c+1)` with `clr`.
            iv. If column `c+2` is within the grid bounds, color the pixel at `(r, c+2)` with `clr`.
        c.  If the object consists of more than one pixel:
            i.  Copy all pixels belonging to this object from their original positions in the input grid to the corresponding positions in the output grid.
    4.  Return the final output grid.
