
## train_1

**input:**
```
0 0 0 0 0 7 0 7 0 0
0 0 0 0 0 7 0 7 0 0
0 0 0 7 7 7 0 7 0 0
0 0 0 7 0 0 0 7 0 0
0 0 0 7 0 7 7 7 0 0
0 0 0 7 0 7 0 0 0 0
0 0 0 7 0 7 0 0 0 0
0 0 0 7 9 7 0 0 0 0
0 0 0 7 0 7 0 0 0 0
0 0 0 7 0 7 0 0 0 0
```


**output:**
```
0 0 0 0 0 7 8 7 0 0
0 0 0 0 0 7 8 7 0 0
0 0 0 7 7 7 8 7 0 0
0 0 0 7 8 8 8 7 0 0
0 0 0 7 8 7 7 7 0 0
0 0 0 7 8 7 0 0 0 0
0 0 0 7 8 7 0 0 0 0
0 0 0 7 8 7 0 0 0 0
0 0 0 7 8 7 0 0 0 0
0 0 0 7 8 7 0 0 0 0
```


## train_2

**input:**
```
7 0 7 0 0 0 0 0 0 0
7 0 7 0 0 0 0 0 0 0
7 0 7 7 7 7 0 0 0 0
7 0 0 0 0 7 0 0 0 0
7 7 7 7 0 7 0 0 0 0
0 0 0 7 0 7 7 7 7 0
0 0 0 7 9 0 0 0 7 0
0 0 0 7 7 7 7 0 7 0
0 0 0 0 0 0 7 0 7 0
0 0 0 0 0 0 7 0 7 0
```


**output:**
```
7 8 7 0 0 0 0 0 0 0
7 8 7 0 0 0 0 0 0 0
7 8 7 7 7 7 0 0 0 0
7 8 8 8 8 7 0 0 0 0
7 7 7 7 8 7 0 0 0 0
0 0 0 7 8 7 7 7 7 0
0 0 0 7 9 0 0 0 7 0
0 0 0 7 7 7 7 0 7 0
0 0 0 0 0 0 7 0 7 0
0 0 0 0 0 0 7 0 7 0
```


## train_3

**input:**
```
0 0 7 0 7 0 0 0 0 0
0 0 7 0 7 0 0 0 0 0
0 0 7 0 7 7 7 0 0 0
0 0 7 0 0 0 7 0 0 0
0 0 7 7 7 9 7 0 0 0
0 0 0 0 7 0 7 0 0 0
0 0 0 0 7 0 7 7 7 0
0 0 0 0 7 0 0 0 7 0
0 0 0 0 7 7 7 0 7 0
0 0 0 0 0 0 7 0 7 0
```


**output:**
```
0 0 7 8 7 0 0 0 0 0
0 0 7 8 7 0 0 0 0 0
0 0 7 8 7 7 7 0 0 0
0 0 7 8 8 8 7 0 0 0
0 0 7 7 7 8 7 0 0 0
0 0 0 0 7 8 7 0 0 0
0 0 0 0 7 8 7 7 7 0
0 0 0 0 7 8 8 8 7 0
0 0 0 0 7 7 7 8 7 0
0 0 0 0 0 0 7 8 7 0
```


## train_4

**input:**
```
0 0 0 7 0 7 0 0 0 0
0 0 0 7 0 7 0 0 0 0
0 0 0 7 0 7 7 7 0 0
0 0 0 7 0 0 0 7 0 0
0 0 0 7 7 7 0 7 0 0
0 0 0 0 0 7 0 7 0 0
0 0 0 0 0 7 0 7 0 0
0 0 0 0 0 7 0 7 7 7
0 0 0 0 0 7 0 0 0 0
0 0 0 0 0 7 7 7 7 7
```


**output:**
```
0 0 0 7 8 7 0 0 0 0
0 0 0 7 8 7 0 0 0 0
0 0 0 7 8 7 7 7 0 0
0 0 0 7 8 8 8 7 0 0
0 0 0 7 7 7 8 7 0 0
0 0 0 0 0 7 8 7 0 0
0 0 0 0 0 7 8 7 0 0
0 0 0 0 0 7 8 7 7 7
0 0 0 0 0 7 8 8 8 8
0 0 0 0 0 7 7 7 7 7
```

*   **Perception:**
    *   The input grids consist primarily of white (0) and orange (7) pixels. Some inputs contain a single maroon (9) pixel.
    *   The orange pixels form connected shapes that act as boundaries or walls.
    *   The output grids are identical to the input grids, except that some white (0) pixels are replaced with azure (8) pixels.
    *   In examples train\_1 and train\_3, the maroon (9) pixel is also replaced with azure (8). In train\_2, the maroon pixel remains unchanged.
    *   The azure (8) pixels appear in regions enclosed by the orange (7) boundaries.
    *   The transformation seems to involve identifying areas completely surrounded by orange pixels and filling these areas with azure pixels.
    *   Pixels that are not orange and are not enclosed by orange pixels remain unchanged.
    *   The maroon pixel (9) is treated like a white pixel (0) for the purpose of filling: if it's inside an enclosed region, it becomes azure (8); otherwise (like in train\_2, where it touches the 'outside'), it remains unchanged.

*   **Facts YAML:**
    
```yaml
    elements:
      - object: grid
        pixels:
          - color: white (0)
            role: background / fillable
          - color: orange (7)
            role: boundary / wall
          - color: maroon (9)
            role: fillable (sometimes present)
          - color: azure (8)
            role: fill_color (output only)
    relationships:
      - type: spatial
        description: Orange pixels form contiguous boundaries.
      - type: topological
        description: Regions of non-orange pixels can be enclosed by orange boundaries.
    actions:
      - action: identify_boundaries
        input: grid
        using: orange (7) pixels
        output: boundary_map
      - action: identify_enclosed_regions
        input: grid, boundary_map
        description: Find connected components of non-orange pixels that do not touch the grid edges.
        output: enclosed_pixel_coordinates
      - action: fill_regions
        input: grid, enclosed_pixel_coordinates
        color: azure (8)
        target_pixels: Pixels at enclosed_pixel_coordinates (originally white or maroon)
        output: modified_grid
    transformation:
      - step: Copy the input grid to create the output grid.
      - step: Identify all pixels that are not orange (7).
      - step: Determine which of these non-orange pixels belong to regions completely enclosed by orange (7) pixels (i.e., they cannot reach the border of the grid without crossing an orange pixel).
      - step: Change the color of all identified enclosed pixels (whether originally white or maroon) to azure (8) in the output grid.
      - step: Leave all orange pixels and all non-orange pixels not part of an enclosed region unchanged.
    ```


*   **Natural Language Program:**
    1.  Identify all pixels with the color orange (7) as boundary pixels.
    2.  Identify all regions of connected pixels that are *not* orange.
    3.  Determine which of these non-orange regions are completely enclosed by the orange boundaries (meaning they do not touch any edge of the grid). This can be done using a flood fill algorithm starting from all non-orange pixels on the grid's border; any non-orange pixel not reached by this flood fill is considered enclosed.
    4.  For every pixel identified as being within an enclosed region, change its color to azure (8) in the output grid.
    5.  All other pixels (the orange boundary pixels and the non-orange pixels not in an enclosed region) retain their original color in the output grid.
