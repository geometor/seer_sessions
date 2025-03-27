
## train_1

**input:**
```
2 7 7 1 0 3 0 0 0 3
0 0 0 9 0 0 0 0 3 7
0 0 0 1 0 0 0 6 0 9
0 0 0 0 0 0 0 1 0 0
9 0 0 0 0 0 0 0 0 0
0 0 0 0 2 0 0 0 3 0
0 5 0 7 3 0 0 0 1 0
4 4 0 0 0 1 0 0 0 5
0 0 0 0 0 0 0 5 3 0
0 0 0 0 4 5 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 2 6 2 0
0 0 0 0 0 0 2 2 2 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 1 0 0 0 5 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 2 0 0 0 1
0 0 1 0 0 0 0 0 0 5
0 0 8 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0
0 5 1 0 1 0 0 0 0 0
0 8 1 0 0 0 1 0 3 0
0 0 0 0 0 0 0 3 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0 0 0
2 4 2 0 0 0 0 0 0 0
2 2 2 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_3

**input:**
```
6 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 0 0 2 8
0 7 0 0 2 0 5 0 2 0
0 9 0 1 0 0 0 0 0 0
0 9 0 0 0 0 0 0 0 1
0 0 0 0 0 6 0 0 0 0
0 1 0 7 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 3 0 0 0
0 0 5 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 2 2 2 0 0
0 0 0 0 0 2 3 2 0 0
0 0 0 0 0 2 2 2 0 0
```

*   **Perception**: The task involves identifying a specific, unique pixel in the input grid and then creating a 3x3 pattern centered on that pixel's location in the output grid. The input grids contain scattered pixels of various colors, while the output grids are mostly white, featuring only the 3x3 pattern. The central pixel of the output pattern retains the color of the unique pixel identified in the input, and the eight surrounding pixels of the pattern are colored red (2). All other pixels in the output grid are white (0). The key seems to be finding the pixel whose color value appears only once in the entire input grid.

*   **Facts YAML**:
    
```yaml
    task_description: Identify the pixel with a unique color in the input grid and draw a 3x3 square centered at its location in the output grid.
    
    elements:
      - element: grid
        description: A 2D array of pixels with colors represented by integers 0-9.
      - element: pixel
        description: An individual cell in the grid with a specific color value and location (row, column).
      - element: unique_color_pixel
        description: The single pixel in the input grid whose color value occurs exactly once.
        properties:
          - color: The color value (integer 1-9) that is unique across the input grid.
          - location: The (row, column) coordinates of this pixel.
      - element: output_pattern
        description: A 3x3 square pattern in the output grid.
        properties:
          - center_pixel: Located at the same coordinates as the input unique_color_pixel, retaining its color.
          - surrounding_pixels: The 8 pixels adjacent (including diagonals) to the center_pixel.
          - surrounding_color: Always red (2).
      - element: background_pixel
        description: All pixels in the output grid not part of the output_pattern.
        properties:
          - color: Always white (0).
    
    transformation:
      - action: identify_unique_color
        input: input_grid
        output: unique_color_value
        description: Count the occurrences of each non-white color in the input grid. Identify the color value that appears exactly once.
      - action: find_pixel_location
        input: input_grid, unique_color_value
        output: unique_pixel_location (row, column)
        description: Find the coordinates of the pixel having the unique_color_value.
      - action: create_output_grid
        input: input_grid_dimensions
        output: output_grid
        description: Initialize an output grid of the same dimensions as the input, filled entirely with white (0).
      - action: place_center_pixel
        input: output_grid, unique_pixel_location, unique_color_value
        output: modified_output_grid
        description: Set the pixel at unique_pixel_location in the output grid to unique_color_value.
      - action: draw_frame
        input: output_grid, unique_pixel_location
        output: final_output_grid
        description: Set the 8 neighboring pixels (adjacent and diagonal) around the unique_pixel_location to red (2), handling boundary conditions (neighbors outside the grid are ignored).
    
    relationships:
      - type: centering
        description: The output_pattern is centered on the location of the unique_color_pixel from the input grid.
      - type: color_mapping
        description: The center of the output_pattern uses the unique_color_value from the input. The frame of the output_pattern always uses red (2). The background uses white (0).
    ```


*   **Natural Language Program**:
    1.  Determine the dimensions (height H, width W) of the input grid.
    2.  Count the frequency of each color (1-9) present in the input grid.
    3.  Identify the color (`unique_color`) that appears exactly once.
    4.  Find the row and column index (`center_row`, `center_col`) of the pixel with the `unique_color`.
    5.  Create a new HxW output grid and initialize all its pixels to white (0).
    6.  Set the pixel at (`center_row`, `center_col`) in the output grid to `unique_color`.
    7.  For each of the 8 neighboring positions around (`center_row`, `center_col`) (i.e., `center_row-1` to `center_row+1`, `center_col-1` to `center_col+1`, excluding the center itself):
        a.  Check if the neighbor position is within the grid boundaries (0 <= row < H and 0 <= col < W).
        b.  If the neighbor position is within bounds, set the pixel at that position in the output grid to red (2).
    8.  Return the completed output grid.
