
## train_1

**input:**
```
0 2 2 0 0
2 2 2 2 0
0 0 2 2 0
0 0 2 2 0
4 4 4 4 4
1 0 0 1 0
1 1 1 0 1
0 0 1 1 1
1 1 1 0 0
```


**output:**
```
3 3 3 3 0
3 3 3 3 3
0 0 3 3 3
3 3 3 3 0
```


## train_2

**input:**
```
2 2 2 2 2
0 0 0 2 0
0 2 0 2 2
2 2 2 2 2
4 4 4 4 4
0 1 1 0 0
1 1 0 1 0
1 1 0 0 0
0 0 1 1 1
```


**output:**
```
3 3 3 3 3
3 3 0 3 0
3 3 0 3 3
3 3 3 3 3
```


## train_3

**input:**
```
0 0 0 0 0
0 2 2 2 0
0 2 0 0 0
2 2 2 0 2
4 4 4 4 4
1 1 0 0 1
1 1 0 1 1
1 0 1 0 1
0 1 0 1 1
```


**output:**
```
3 3 0 0 3
3 3 3 3 3
3 3 3 0 3
3 3 3 3 3
```


## train_4

**input:**
```
0 2 0 0 2
0 2 2 0 2
0 0 0 2 2
0 0 2 2 0
4 4 4 4 4
1 0 1 0 0
1 0 0 1 0
0 0 0 0 1
0 1 1 1 0
```


**output:**
```
3 3 3 0 3
3 3 3 3 3
0 0 0 3 3
0 3 3 3 0
```

Okay, let's analyze the provided examples.

## Perception

1.  **Input Structure:** The input grids consistently feature a horizontal line composed entirely of yellow pixels (color 4). This line divides the input grid into two distinct sections: a top section and a bottom section.
2.  **Color Distribution (Input):**
    *   The top section contains only red (2) and white (0) pixels.
    *   The bottom section contains only blue (1) and white (0) pixels.
    *   The yellow line (4) acts solely as a separator.
3.  **Output Structure:** The output grid's dimensions match the dimensions of either the top or bottom section of the input grid (excluding the separator line).
4.  **Color Distribution (Output):** The output grids contain only green (3) and white (0) pixels.
5.  **Transformation Pattern:** The transformation appears to involve comparing the pixels in the top section with the pixels in the corresponding positions in the bottom section.
    *   Observing the examples, a green pixel (3) appears in the output grid if *either* the corresponding pixel in the top section is red (2) *or* the corresponding pixel in the bottom section is blue (1).
    *   If both the corresponding top pixel and bottom pixel are white (0), the output pixel is also white (0).
6.  **Object Identification:** We can consider the top section, bottom section, and separator line as distinct components of the input. The transformation operates by combining information from the top and bottom sections based on specific color conditions.

## Facts


```yaml
task_elements:
  - item: input_grid
    properties:
      - contains a horizontal separator line of yellow (4) pixels
      - divided into a top_section and a bottom_section by the separator
  - item: separator
    type: horizontal_line
    color: yellow (4)
    function: divides input_grid
  - item: top_section
    location: above separator
    pixels: contains red (2) and white (0)
    dimensions: H x W
  - item: bottom_section
    location: below separator
    pixels: contains blue (1) and white (0)
    dimensions: H x W (same as top_section)
  - item: output_grid
    pixels: contains green (3) and white (0)
    dimensions: H x W (same as top_section and bottom_section)
    derivation: result of combining top_section and bottom_section pixel-wise

transformation_rule:
  - step: locate the horizontal separator line (yellow, 4)
  - step: extract the grid section above the separator (top_grid)
  - step: extract the grid section below the separator (bottom_grid)
  - step: initialize an output_grid with the same dimensions as top_grid/bottom_grid
  - step: iterate through each pixel position (row, col) within the dimensions
  - step: get the pixel value top_pixel from top_grid at (row, col)
  - step: get the pixel value bottom_pixel from bottom_grid at (row, col)
  - step: apply conditional logic:
      - if top_pixel is red (2) OR bottom_pixel is blue (1):
          set output_grid[row][col] to green (3)
      - else (if top_pixel is white (0) AND bottom_pixel is white (0)):
          set output_grid[row][col] to white (0)
  - step: return the completed output_grid
```


## Natural Language Program

1.  Identify the horizontal row composed entirely of yellow (4) pixels in the input grid. This is the separator line.
2.  Define the region above the separator line as the "top grid".
3.  Define the region below the separator line as the "bottom grid". (The top and bottom grids will have identical dimensions).
4.  Create a new, empty output grid with the same height and width as the top grid (or bottom grid).
5.  For each corresponding pixel position `(row, col)` in the top grid and bottom grid:
    a.  Check the color of the pixel at `(row, col)` in the top grid.
    b.  Check the color of the pixel at `(row, col)` in the bottom grid.
    c.  If the top grid pixel is red (2) OR the bottom grid pixel is blue (1), set the pixel at `(row, col)` in the output grid to green (3).
    d.  Otherwise (meaning the top grid pixel is white (0) AND the bottom grid pixel is white (0)), set the pixel at `(row, col)` in the output grid to white (0).
6.  The resulting grid is the final output.
