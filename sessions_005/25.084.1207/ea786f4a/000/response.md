**Perception**

The input grid in each example consists primarily of a single solid color (red, blue, or green) with one distinct pixel of 'white' (color 0) located somewhere within the grid. The output grid maintains the same dimensions as the input grid. The transformation modifies the grid based on the position of the initial 'white' pixel. Specifically, the output grid displays a pattern where pixels alternate between 'white' and the original background color. This alternating pattern resembles a checkerboard or a distance-based coloring scheme originating from the initial 'white' pixel's location. The pixels that become 'white' in the output are those whose Manhattan distance (sum of absolute differences in row and column coordinates) from the original 'white' pixel is an even number (0, 2, 4, ...). Pixels with an odd Manhattan distance retain the original background color.

**Facts**


```yaml
task_context:
  - description: Each input grid has a uniform background color with a single 'white' (0) pixel embedded within it.
  - grid_dimensions: Input and output grids have the same height and width.
  - colors_involved: White (0) and one other color (Red=2, Blue=1, Green=3) per example.

transformation_details:
  - name: Pattern generation based on distance from a central point.
  - input_objects:
      - type: background
        color: The dominant color in the input grid (e.g., Red, Blue, Green).
      - type: marker
        color: White (0)
        location: The coordinates (row, column) of the single white pixel.
        count: 1
  - output_objects:
      - type: grid pattern
        description: Pixels are colored based on their Manhattan distance from the input marker's location.
        colors:
          - White (0): Assigned to pixels where the Manhattan distance from the input marker is even.
          - Background color: Assigned to pixels where the Manhattan distance from the input marker is odd.
  - relationship: The color of each pixel in the output grid is determined by its Manhattan distance to the location of the single 'white' pixel in the input grid.

distance_metric:
  - name: Manhattan distance (L1 norm)
  - formula: |row1 - row2| + |col1 - col2|
  - application: Used to calculate the distance between each grid cell and the location of the input 'white' pixel.
```


**Natural Language Program**

1.  Identify the primary background color (non-white color) present in the input grid.
2.  Locate the coordinates (row `r0`, column `c0`) of the single 'white' pixel in the input grid.
3.  Create a new output grid with the same dimensions as the input grid.
4.  For each pixel at coordinates (row `r`, column `c`) in the new grid:
    a.  Calculate the Manhattan distance `d` between (`r`, `c`) and (`r0`, `c0`): `d = abs(r - r0) + abs(c - c0)`.
    b.  Check if the distance `d` is an even number (i.e., `d % 2 == 0`).
    c.  If `d` is even, set the color of the pixel at (`r`, `c`) in the output grid to 'white' (0).
    d.  If `d` is odd, set the color of the pixel at (`r`, `c`) in the output grid to the primary background color identified in step 1.
5.  Return the completed output grid.