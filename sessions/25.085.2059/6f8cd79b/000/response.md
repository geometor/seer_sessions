Okay, let's break down this task.

**Perception:**

1.  **Input Analysis:** The input grids are uniform rectangles completely filled with the color white (0). They vary in size (rows and columns).
2.  **Output Analysis:** The output grids have the exact same dimensions as their corresponding input grids. They feature a border of azure (8) pixels encompassing an inner area. The inner area retains the original color from the input, which is white (0) in these examples.
3.  **Transformation:** The core transformation appears to be identifying the boundary pixels of the input grid and changing their color to azure (8) in the output grid. Pixels not on the boundary retain their original color.

**YAML Facts:**


```yaml
task_name: draw_border
description: Creates a border around the input grid using a specific color.
examples:
  - id: train_1
    input_grid_size: [5, 4]
    output_grid_size: [5, 4]
    input_pixels:
      - color: 0 # white
        count: 20
    output_pixels:
      - color: 8 # azure
        count: 14 # (5*2) + (4-2)*2 = 10 + 4 = 14
        location: border_pixels
      - color: 0 # white
        count: 6 # (5-2) * (4-2) = 3 * 2 = 6
        location: inner_pixels
  - id: train_2
    input_grid_size: [4, 3]
    output_grid_size: [4, 3]
    input_pixels:
      - color: 0 # white
        count: 12
    output_pixels:
      - color: 8 # azure
        count: 10 # (4*2) + (3-2)*2 = 8 + 2 = 10
        location: border_pixels
      - color: 0 # white
        count: 2 # (4-2) * (3-2) = 2 * 1 = 2
        location: inner_pixels
  - id: train_3
    input_grid_size: [5, 6]
    output_grid_size: [5, 6]
    input_pixels:
      - color: 0 # white
        count: 30
    output_pixels:
      - color: 8 # azure
        count: 18 # (5*2) + (6-2)*2 = 10 + 8 = 18
        location: border_pixels
      - color: 0 # white
        count: 12 # (5-2) * (6-2) = 3 * 4 = 12
        location: inner_pixels
  - id: train_4
    input_grid_size: [3, 3]
    output_grid_size: [3, 3]
    input_pixels:
      - color: 0 # white
        count: 9
    output_pixels:
      - color: 8 # azure
        count: 8 # (3*2) + (3-2)*2 = 6 + 2 = 8
        location: border_pixels
      - color: 0 # white
        count: 1 # (3-2) * (3-2) = 1 * 1 = 1
        location: inner_pixels
grid_properties:
  - property: dimensions
    relationship: input and output grids have identical dimensions.
transformation:
  - type: boundary_coloring
    input_elements: all pixels
    output_elements:
      - pixels_on_border: changed to azure (8)
      - pixels_not_on_border: retain original color
definitions:
  - term: border_pixels
    description: Pixels located in the first row, last row, first column, or last column of the grid.
  - term: inner_pixels
    description: Pixels not located on the border.
```


**Natural Language Program:**

1.  Receive the input grid.
2.  Create a new output grid with the same dimensions (height and width) as the input grid.
3.  Iterate through each pixel of the input grid using its row index (`r`) and column index (`c`).
4.  Check if the pixel is located on the border of the grid. A pixel is on the border if its row index `r` is 0 (the first row) OR `r` is the last row index (height - 1) OR its column index `c` is 0 (the first column) OR `c` is the last column index (width - 1).
5.  If the pixel is on the border, set the color of the corresponding pixel in the output grid to azure (8).
6.  If the pixel is *not* on the border, copy the color of the input pixel to the corresponding pixel in the output grid.
7.  Return the completed output grid.