**Perception**

The task involves processing an input grid containing various colors and producing an output grid of the same dimensions. Observing the input-output pairs reveals a consistent pattern: the output grid retains only the pixels that were 'azure' (color 8) in the input grid, keeping them in their original positions. All other pixels in the input grid, regardless of their original color (including 'white' or color 0), are replaced with 'white' (color 0) in the output grid. The transformation acts as a color filter, specifically isolating the 'azure' pixels against a 'white' background.

**Facts**


```yaml
Task: Color Filtering

Input:
  - Grid: 2D array of pixels with colors 0-9.
  - Contains various colored objects/pixels.
  - Contains 'azure' (8) colored pixels.

Output:
  - Grid: 2D array of pixels with the same dimensions as the input.
  - Contains only 'white' (0) and 'azure' (8) pixels.

Transformation:
  - Rule: Isolate 'azure' pixels.
  - Process: Iterate through each pixel of the input grid.
  - Condition: Check if the pixel color is 'azure' (8).
  - Action_True: If the pixel is 'azure', copy its color (8) to the corresponding position in the output grid.
  - Action_False: If the pixel is not 'azure', set the corresponding position in the output grid to 'white' (0).

Relationships:
  - The position of 'azure' pixels is preserved from input to output.
  - All non-'azure' pixels in the input map to 'white' pixels in the output.
  - The dimensions of the input and output grids are identical for each example pair.
```


**Natural Language Program**

1.  Initialize an output grid with the same height and width as the input grid, filling it entirely with 'white' pixels (color 0).
2.  Examine each pixel in the input grid, row by row, column by column.
3.  For each pixel, check if its color is 'azure' (color 8).
4.  If the input pixel's color is 'azure', update the pixel at the corresponding position (same row and column) in the output grid to 'azure' (color 8).
5.  If the input pixel's color is not 'azure', leave the corresponding pixel in the output grid as 'white' (color 0).
6.  After checking all pixels in the input grid, the resulting output grid is the final result.