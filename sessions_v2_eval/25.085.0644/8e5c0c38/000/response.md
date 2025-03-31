*   **Perception:** The input grids contain multiple distinct, non-background colored objects (shapes) against a uniform background color. The background color is the most frequent color in the grid (`azure` in the first example, `white` in the second). The transformation involves modifying these colored objects by removing specific pixels. The pixels removed appear to be those within an object that do not have any immediate (cardinal, i.e., up, down, left, right) neighbors of the same color. Pixels that only have diagonal neighbors of the same color, or no same-color neighbors at all, are changed to the background color. The overall shapes are preserved but appear slightly "eroded" or "cleaned up" by removing these less connected pixels.

*   **Facts:**
    
```yaml
    task_context:
      description: "Remove pixels from colored objects that lack cardinal neighbors of the same color."
      grid_properties:
        - size: Variable (e.g., 22x22 in examples)
        - background_color: The most frequent color in the input grid.
      objects:
        - definition: Contiguous areas of pixels with the same non-background color.
        - properties: Each object has a specific color.
      transformation:
        - type: Pixel modification
        - target: Pixels within non-background colored objects.
        - rule: Change a pixel's color to the background color if it has no cardinal (up, down, left, right) neighbors of the same color.
        - condition_details: Only consider neighbors within the grid boundaries. Diagonal neighbors do not prevent removal.
    ```


*   **Natural Language Program:**
    1.  Identify the background color by finding the most frequent pixel color in the input grid.
    2.  Create a copy of the input grid to serve as the output grid.
    3.  Iterate through each pixel (cell) of the input grid, examining its row and column index.
    4.  For the current pixel, check if its color is the same as the identified background color.
    5.  If the pixel's color is *not* the background color:
        a.  Check its four cardinal neighbors (up, down, left, right), staying within the grid boundaries.
        b.  Count how many of these cardinal neighbors have the *same* color as the current pixel.
        c.  If the count of same-colored cardinal neighbors is zero, change the color of the corresponding pixel in the *output* grid to the background color.
    6.  If the pixel's color *is* the background color, or if it has at least one same-colored cardinal neighbor, keep its original color in the output grid.
    7.  After iterating through all pixels, the modified grid is the final output.