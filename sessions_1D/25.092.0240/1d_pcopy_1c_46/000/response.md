*   **Perception**: The task operates on input grids that are always a single row (1xN). The transformation involves modifying these rows based on the arrangement of non-white pixels. Specifically, it identifies non-white pixels that are "isolated" horizontally, meaning their immediate left and right neighbors are white (color 0) or are grid boundaries. When an isolated pixel of a certain color is found, it is expanded into a horizontal block of three pixels of that same color, centered at the original pixel's position. Pixels that are already part of a horizontal sequence of two or more pixels of the same color are not changed. The output grid has the same dimensions as the input grid.

*   **Facts YAML**:
    
```yaml
    task_type: grid_transformation
    grid_dimensionality: 1D # Input grids are effectively 1xN
    transformation_scope: local # Changes depend on immediate neighbors
    objects:
      - type: pixel
        properties:
          - color: integer (0-9)
          - position: integer index within the row
      - type: horizontal_block
        properties:
          - color: integer (non-zero)
          - length: integer >= 1
          - pixels: list of adjacent pixels of the same color
    relationships:
      - type: adjacency
        description: Pixels immediately to the left or right of a given pixel.
      - type: isolation
        description: A non-white pixel is isolated if its left and right adjacent positions contain white pixels (0) or are outside the grid boundaries.
    actions:
      - name: identify_isolated_pixels
        input: input grid
        output: list of positions of isolated non-white pixels
        condition: Pixel color is non-zero AND (left neighbor is white OR boundary) AND (right neighbor is white OR boundary).
      - name: expand_to_3_block
        input: position of an isolated pixel, its color
        output: modifies the output grid
        effect: Colors the pixel at the input position, the position to its left (if exists), and the position to its right (if exists) with the input color. Centered on the original isolated pixel.
    state_changes:
      - description: Pixels that were white might become non-white if they are adjacent to an isolated pixel being expanded.
      - description: Isolated non-white pixels become part of a 3-pixel block.
      - description: Non-white pixels already part of blocks of length >= 2 remain unchanged.
    invariance:
      - Grid dimensions remain the same.
      - The relative order of existing blocks (length >= 2) is preserved.
      - White pixels not adjacent to an isolated pixel remain white.
    ```


*   **Natural Language Program**:
    1.  Initialize an output grid as a copy of the input grid.
    2.  Iterate through each pixel in the input grid row from left to right using its index `i`.
    3.  Get the color `C` of the pixel at index `i` in the input grid.
    4.  If the color `C` is not white (0):
        a.  Check if this pixel is isolated:
            i.  Determine the color of the left neighbor (use white if `i` is 0).
            ii. Determine the color of the right neighbor (use white if `i` is the last index).
            iii. The pixel is isolated if both the left and right neighbors are white (0).
        b.  If the pixel at index `i` is isolated:
            i.  Change the color of the pixel at index `i` in the *output* grid to `C`.
            ii. If index `i-1` is within the grid bounds, change the color of the pixel at `i-1` in the *output* grid to `C`.
            iii. If index `i+1` is within the grid bounds, change the color of the pixel at `i+1` in the *output* grid to `C`.
    5.  After checking all pixels in the input grid, return the modified output grid.