
## train_1

**input:**
```
4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4
4 4 9 4 4 4 4 4
4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4
4 4 4 4 4 4 4 4
```


**output:**
```
1 1 1 4 4 4 4 4
4 4 1 4 4 4 4 4
4 4 1 4 4 4 4 4
4 4 9 4 4 4 4 4
4 4 1 4 4 4 4 4
4 4 1 4 4 4 4 4
4 4 1 4 4 4 4 4
4 4 1 1 1 1 1 1
```


## train_2

**input:**
```
7 7 7 7 7
7 7 7 7 7
7 7 8 7 7
7 7 7 7 7
7 7 7 7 7
```


**output:**
```
7 7 1 1 1
7 7 1 7 7
7 7 8 7 7
7 7 1 7 7
1 1 1 7 7
```


## train_3

**input:**
```
2 2 2 2 2 2 2
2 2 2 2 2 2 2
2 2 2 2 2 2 2
2 2 2 2 4 2 2
2 2 2 2 2 2 2
2 2 2 2 2 2 2
2 2 2 2 2 2 2
```


**output:**
```
1 1 1 1 1 2 2
2 2 2 2 1 2 2
2 2 2 2 1 2 2
2 2 2 2 4 2 2
2 2 2 2 1 2 2
2 2 2 2 1 2 2
2 2 2 2 1 1 1
```

**Perception**

The input is a grid containing primarily one color (the background color) and a single, unique pixel of a different color (the 'marker' pixel). The output grid retains the original marker pixel and the background color in most positions. However, a path-like structure of blue pixels (color 1) is introduced. This path seems to originate from the top-left corner, follow the top edge to the marker's column, descend along that column (skipping the marker pixel itself), reach the bottom edge, and then proceed along the bottom edge either leftwards to the first column or rightwards to the last column. The direction taken along the bottom edge appears dependent on the marker's horizontal position relative to the grid's center.

**Facts**


```yaml
task_elements:
  - item: input_grid
    description: A 2D grid of pixels with dimensions between 1x1 and 30x30.
    properties:
      - dominant_color: The color appearing in most cells (background_color).
      - unique_pixel: One cell contains a color different from the dominant_color (marker_pixel).
        properties:
          - color: marker_color
          - position: (marker_row, marker_col)
      - dimensions: (height, width)

  - item: output_grid
    description: A 2D grid, same dimensions as the input_grid.
    properties:
      - background_color: Same as the input_grid's dominant_color.
      - marker_pixel: Unchanged from the input_grid (same color and position).
      - blue_path: A set of pixels changed to blue (color 1). These pixels were originally background_color pixels in the input_grid.

relationships:
  - type: transformation
    description: Pixels along a specific path defined by the marker_pixel's position are changed from background_color to blue.
    details:
      - step_1: Identify background_color (most frequent color in input).
      - step_2: Identify marker_pixel (the unique non-background pixel) and its position (marker_row, marker_col).
      - step_3: Determine the path segments:
          - Segment 1 (Top Row): From (0, 0) to (0, marker_col).
          - Segment 2 (Marker Column): From (0, marker_col) to (height - 1, marker_col), excluding (marker_row, marker_col).
          - Segment 3 (Bottom Row): Direction depends on marker_col relative to grid width.
            - If marker_col < width / 2: Path runs from (height - 1, marker_col) to (height - 1, width - 1).
            - If marker_col >= width / 2: Path runs from (height - 1, 0) to (height - 1, marker_col).
      - step_4: Change the color of all background_color pixels located on these path segments to blue (1). Keep the marker_pixel and other background_color pixels unchanged.

```


**Natural Language Program**

1.  Determine the background color by finding the most frequent pixel color in the input grid.
2.  Locate the single 'marker' pixel, which has a color different from the background color. Record its row (`marker_row`) and column (`marker_col`).
3.  Get the dimensions of the grid: height and width.
4.  Initialize the output grid as a copy of the input grid.
5.  Draw the blue path by changing background-colored pixels to blue (color 1) along the following segments:
    a.  **Top Row Segment:** For each column `c` from 0 up to and including `marker_col`, if the pixel at `(0, c)` has the background color, change it to blue.
    b.  **Marker Column Segment:** For each row `r` from 0 up to `height - 1`, if `r` is not equal to `marker_row` and the pixel at `(r, marker_col)` has the background color, change it to blue.
    c.  **Bottom Row Segment:**
        i.  Check if the marker column `marker_col` is strictly less than half the grid width (`width / 2`).
        ii. If it is (marker is in the left half), then for each column `c` from `marker_col` up to `width - 1`, if the pixel at `(height - 1, c)` has the background color, change it to blue.
        iii. If it is not (marker is in the right half or exact center), then for each column `c` from 0 up to and including `marker_col`, if the pixel at `(height - 1, c)` has the background color, change it to blue.
6.  The resulting grid is the output.
