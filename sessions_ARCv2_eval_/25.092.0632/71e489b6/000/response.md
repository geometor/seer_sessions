*   **Perception:**
    *   The input grids consist primarily of white (1) and black (0) pixels.
    *   The output grids are largely identical to the input grids, but some white (1) pixels are changed to orange (7).
    *   The changes occur around specific black (0) pixels in the input.
    *   The black pixels triggering the change appear to be "isolated", meaning they are not adjacent (up, down, left, right) to any other black pixels. Black pixels that are part of lines or larger black areas do not trigger changes.
    *   For each isolated black pixel in the input, its adjacent white neighbors (up, down, left, right) are changed to orange (7) in the output grid.
    *   The isolated black pixel itself remains black (0) in the output grid.
    *   All other pixels (non-isolated black pixels, white pixels not adjacent to isolated black pixels, and pixels of other colors if they existed) retain their original color.
    *   The orange pixels form shapes resembling 'T's or '+'s centered *around* the position of the original isolated black pixel, depending on how many white neighbors it had.

*   **Facts:**
    
```yaml
    task_elements:
      - element: grid
        description: A 2D array of pixels with colors represented by integers 0-9.
      - element: pixel
        properties:
          - color: (black: 0, white: 1, orange: 7)
          - position: (row, column)
          - neighborhood: Cardinal adjacent pixels (up, down, left, right).
      - element: isolated_black_pixel
        definition: A black (0) pixel whose cardinal neighbors are all non-black.
        relationship: Triggers a change in its white neighbors.
    transformation:
      - action: identify_isolated_black_pixels
        input: input_grid
        criteria: Pixel color is black (0) AND all cardinal neighbors are not black (0).
      - action: modify_neighbors
        input: input_grid, identified_isolated_black_pixels
        process: For each isolated black pixel, iterate through its cardinal neighbors in the input grid.
        condition: If a neighbor is white (1).
        output_effect: Change the color of that neighbor pixel to orange (7) in the output grid.
      - action: copy_unmodified_pixels
        input: input_grid
        process: All pixels not identified as white neighbors of isolated black pixels retain their original color in the output grid. This includes the isolated black pixels themselves.
    ```


*   **Natural Language Program:**
    1.  Initialize the output grid as a copy of the input grid.
    2.  Iterate through each pixel of the input grid using its row and column index.
    3.  For the current pixel, check if its color is black (0).
    4.  If the pixel is black, examine its four cardinal neighbors (up, down, left, right), considering grid boundaries.
    5.  Count how many of these neighbors are also black (0).
    6.  If the count of black neighbors is zero, then the current black pixel is "isolated".
    7.  For this isolated black pixel, re-examine its four cardinal neighbors in the *input* grid.
    8.  For each cardinal neighbor that exists (is within grid bounds) and has the color white (1) in the input grid, change the color of the corresponding pixel in the *output* grid to orange (7).
    9.  Leave the isolated black pixel itself as black (0) in the output grid (it was copied initially).
    10. After checking all pixels in the input grid, the final output grid contains the required transformation.