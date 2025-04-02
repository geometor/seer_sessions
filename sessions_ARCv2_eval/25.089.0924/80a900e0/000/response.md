*   **Perception of Task Elements:**
    *   The input and output grids share a common checkerboard background pattern of blue (1) and white (0) pixels.
    *   The input grids contain sparsely distributed "source" pixels of other colors (azure-8, green-3 in train\_1; red-2, green-3, yellow-4 in train\_2).
    *   The transformation involves modifying the blue (1) pixels based on the locations of specific source pixels.
    *   In the output grids, the source pixels seem to 'radiate' or 'propagate' their color along diagonal lines.
    *   This propagation replaces the blue (1) pixels along these diagonal lines, while white (0) pixels and green (3) pixels remain unchanged.
    *   The propagation extends outwards from the source pixel location to the boundaries of the grid.
    *   Only certain source colors (azure-8, red-2, yellow-4) participate in this propagation; green (3) pixels do not.

*   **YAML Facts:**
    
```yaml
    task_context:
      grid_properties:
        - background: Checkerboard pattern of blue (1) and white (0).
        - dimensions: Variable height and width.
      objects:
        - type: background_pixel
          colors: [blue (1), white (0)]
          role: Forms the base pattern, blue pixels are targets for modification.
        - type: source_pixel
          colors: [azure (8), red (2), yellow (4)] # Propagating colors
          role: Initiate diagonal propagation.
        - type: inert_pixel
          colors: [green (3)] # Non-propagating color
          role: Present in the grid but does not affect the transformation.
    transformation:
      action: diagonal_propagation
      actor: source_pixel (azure, red, yellow)
      target: background_pixel (blue)
      rule:
        - Identify all source pixels (azure, red, yellow) in the input grid.
        - For each source pixel:
          - Trace four diagonal lines (up-left, up-right, down-left, down-right) starting from the source pixel's location.
          - Along each traced diagonal line:
            - If a pixel location contains a blue (1) pixel in the input grid:
              - Change the color of that pixel in the output grid to the color of the source pixel that initiated the trace.
      constraints:
        - Propagation only affects blue (1) pixels.
        - White (0) pixels and inert pixels (green-3) are unaffected by propagation.
        - Propagation stops at the grid boundaries.
        - The state of the grid for determining propagation targets is the original input grid state.
      output_composition:
        - Start with a copy of the input grid.
        - Apply all modifications caused by propagation from all source pixels.
        - Inert pixels (green-3) and the original source pixels remain in their input locations.
        - White pixels remain unchanged unless a source pixel was located there (which doesn't seem to happen in examples).
    ```


*   **Natural Language Program:**
    1.  Create a copy of the input grid to serve as the initial output grid.
    2.  Identify all pixels in the input grid that have a "propagating color": azure (8), red (2), or yellow (4). Record their locations and colors.
    3.  For each identified propagating pixel (let its location be `(row, col)` and its color be `prop_color`):
        a.  Trace the **up-left** diagonal: Iterate `i` from 1 upwards. Calculate the position `(row - i, col - i)`. If this position is within the grid boundaries and the pixel at `(row - i, col - i)` in the *original input grid* is blue (1), change the pixel at `(row - i, col - i)` in the *output grid* to `prop_color`. Stop this trace when the position goes out of bounds.
        b.  Trace the **up-right** diagonal: Iterate `i` from 1 upwards. Calculate the position `(row - i, col + i)`. If this position is within the grid boundaries and the pixel at `(row - i, col + i)` in the *original input grid* is blue (1), change the pixel at `(row - i, col + i)` in the *output grid* to `prop_color`. Stop this trace when the position goes out of bounds.
        c.  Trace the **down-left** diagonal: Iterate `i` from 1 upwards. Calculate the position `(row + i, col - i)`. If this position is within the grid boundaries and the pixel at `(row + i, col - i)` in the *original input grid* is blue (1), change the pixel at `(row + i, col - i)` in the *output grid* to `prop_color`. Stop this trace when the position goes out of bounds.
        d.  Trace the **down-right** diagonal: Iterate `i` from 1 upwards. Calculate the position `(row + i, col + i)`. If this position is within the grid boundaries and the pixel at `(row + i, col + i)` in the *original input grid* is blue (1), change the pixel at `(row + i, col + i)` in the *output grid* to `prop_color`. Stop this trace when the position goes out of bounds.
    4.  Return the modified output grid.