Okay, let's analyze the task.

**Perception:**

The input grids consistently feature a background of `white` pixels (0) with a single pixel of a different color somewhere within the grid. The output grids retain the same dimensions as their corresponding inputs. The transformation appears to involve using the color of the single non-white input pixel to create a frame or border around the perimeter of the output grid. The interior of the output grid is filled with `white` pixels (0), effectively erasing the original position of the colored pixel if it was not on the border.

**Facts:**


```yaml
task_name: frame_color
description: Create a frame around the grid using the color of the single non-white pixel found in the input.
examples:
  - example_index: 1
    input_grid_size: [3, 3]
    output_grid_size: [3, 3]
    objects:
      - type: background
        color: white
        count: 8
      - type: pixel
        color: red
        count: 1
        position: [1, 1] # row, col
    output_objects:
      - type: frame
        color: red
        pixels: [[0, 0], [0, 1], [0, 2], [1, 0], [1, 2], [2, 0], [2, 1], [2, 2]]
      - type: background
        color: white
        pixels: [[1, 1]]
  - example_index: 2
    input_grid_size: [5, 3]
    output_grid_size: [5, 3]
    objects:
      - type: background
        color: white
        count: 14
      - type: pixel
        color: green
        count: 1
        position: [2, 1]
    output_objects:
      - type: frame
        color: green
        pixels: [[0, 0], [0, 1], [0, 2], [1, 0], [1, 2], [2, 0], [2, 2], [3, 0], [3, 2], [4, 0], [4, 1], [4, 2]]
      - type: background
        color: white
        pixels: [[1, 1], [2, 1], [3, 1]]
  - example_index: 3
    input_grid_size: [5, 7]
    output_grid_size: [5, 7]
    objects:
      - type: background
        color: white
        count: 34
      - type: pixel
        color: blue
        count: 1
        position: [2, 3]
    output_objects:
      - type: frame
        color: blue
        pixels: [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [0, 5], [0, 6], [1, 0], [1, 6], [2, 0], [2, 6], [3, 0], [3, 6], [4, 0], [4, 1], [4, 2], [4, 3], [4, 4], [4, 5], [4, 6]]
      - type: background
        color: white
        pixels: [[1, 1], [1, 2], [1, 3], [1, 4], [1, 5], [2, 1], [2, 2], [2, 3], [2, 4], [2, 5], [3, 1], [3, 2], [3, 3], [3, 4], [3, 5]]
  - example_index: 4
    input_grid_size: [5, 5]
    output_grid_size: [5, 5]
    objects:
      - type: background
        color: white
        count: 24
      - type: pixel
        color: magenta
        count: 1
        position: [2, 2]
    output_objects:
      - type: frame
        color: magenta
        pixels: [[0, 0], [0, 1], [0, 2], [0, 3], [0, 4], [1, 0], [1, 4], [2, 0], [2, 4], [3, 0], [3, 4], [4, 0], [4, 1], [4, 2], [4, 3], [4, 4]]
      - type: background
        color: white
        pixels: [[1, 1], [1, 2], [1, 3], [2, 1], [2, 2], [2, 3], [3, 1], [3, 2], [3, 3]]
transformation:
  input_characteristics:
    - Contains exactly one non-white pixel.
    - Background is white (0).
  output_characteristics:
    - Same dimensions as input.
    - A frame (outermost row/column) is colored.
    - The color of the frame matches the color of the single non-white pixel from the input.
    - The interior of the frame is filled with white (0) pixels.
  relationships:
    - The output grid dimensions are identical to the input grid dimensions.
    - The color used for the output frame is determined by the single non-white pixel in the input.
    - The positions of pixels in the output frame correspond to the border positions (row 0, last row, column 0, last column) of the grid.
    - All non-border positions in the output grid are set to white (0).
```


**Natural Language Program:**

1.  Identify the dimensions (height H, width W) of the input grid.
2.  Scan the input grid to find the single pixel that is not `white` (0). Record its color (let's call it C).
3.  Create a new output grid with the same dimensions (H x W).
4.  Iterate through each cell (pixel) of the new grid at position (row r, column c):
    a.  If the cell is located on the border (i.e., if r is 0, or r is H-1, or c is 0, or c is W-1), set the color of this cell to C.
    b.  Otherwise (if the cell is not on the border), set the color of this cell to `white` (0).
5.  Return the newly created grid as the output.