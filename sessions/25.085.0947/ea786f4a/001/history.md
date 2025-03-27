
## train_1

**input:**
```
2 2 2 2 2
2 2 2 2 2
2 2 0 2 2
2 2 2 2 2
2 2 2 2 2
```


**output:**
```
0 2 2 2 0
2 0 2 0 2
2 2 0 2 2
2 0 2 0 2
0 2 2 2 0
```


## train_2

**input:**
```
1 1 1
1 0 1
1 1 1
```


**output:**
```
0 1 0
1 0 1
0 1 0
```


## train_3

**input:**
```
3 3 3 3 3 3 3
3 3 3 3 3 3 3
3 3 3 3 3 3 3
3 3 3 0 3 3 3
3 3 3 3 3 3 3
3 3 3 3 3 3 3
3 3 3 3 3 3 3
```


**output:**
```
0 3 3 3 3 3 0
3 0 3 3 3 0 3
3 3 0 3 0 3 3
3 3 3 0 3 3 3
3 3 0 3 0 3 3
3 0 3 3 3 0 3
0 3 3 3 3 3 0
```

**Perception**

1.  **Input Grids**: Each input grid consists of a solid background color (red, blue, or green in the examples) with a single pixel of a different color, white (0), located somewhere within the grid. The grids vary in size (5x5, 3x3, 7x7).
2.  **Output Grids**: The output grids have the same dimensions as their corresponding input grids. The single white pixel from the input remains white in the output. Many of the background pixels in the input are changed to white in the output, while others retain the original background color.
3.  **Pattern**: The pixels that change to white in the output, along with the original white pixel, form a pattern resembling a checkerboard or diamond shape centered on the original white pixel's location. Specifically, the color of a pixel in the output depends on its Manhattan distance (sum of absolute differences in row and column coordinates) from the original white pixel. Pixels at an even Manhattan distance become white, and pixels at an odd Manhattan distance retain the original background color.

**Facts**


```yaml
task_description: Change pixel colors based on their Manhattan distance from a single unique pixel.

elements:
  - element: grid
    description: A 2D array of pixels with colors represented by integers 0-9.
  - element: background_pixel
    description: Pixels making up the majority color of the input grid.
  - element: central_pixel
    description: A single pixel with a unique color (white, 0) in the input grid, serving as a reference point.
    properties:
      - color: white (0)
      - unique: True

properties:
  - property: grid_dimensions
    description: Height and width of the grid. Remains constant between input and output.
  - property: pixel_color
    description: The integer value (0-9) representing the color of a pixel.
  - property: pixel_coordinates
    description: The (row, column) position of a pixel within the grid.
  - property: manhattan_distance
    description: The distance between two pixels (r1, c1) and (r2, c2), calculated as |r1 - r2| + |c1 - c2|.

actions:
  - action: identify_central_pixel
    description: Find the coordinates (r0, c0) of the unique white (0) pixel in the input grid.
  - action: identify_background_color
    description: Determine the color of the pixels that are not the central_pixel.
  - action: calculate_distance
    description: For each pixel (r, c) in the grid, calculate its Manhattan distance to the central_pixel (r0, c0).
  - action: determine_output_color
    description: Based on the calculated Manhattan distance for a pixel (r, c).
    logic:
      - if distance is even: output color is white (0).
      - if distance is odd: output color is the original background color.
  - action: construct_output_grid
    description: Create a new grid of the same dimensions as the input, populating it with the determined output colors for each pixel.

relationships:
  - relationship: centrality
    description: The central_pixel acts as the origin for distance calculations.
  - relationship: distance_parity_determines_color
    description: The even or odd nature (parity) of the Manhattan distance from the central_pixel determines the output color of each pixel. Pixels equidistant from the center form patterns (like squares rotated by 45 degrees).
```


**Natural Language Program**

1.  Receive the input grid.
2.  Identify the coordinates (row `r0`, column `c0`) of the single white pixel (color 0).
3.  Identify the background color (`bg_color`) by finding the color of any pixel that is not white (0).
4.  Create a new output grid with the same dimensions as the input grid.
5.  Iterate through each pixel in the input grid at coordinates (row `r`, column `c`).
6.  For each pixel, calculate its Manhattan distance `d` from the white pixel: `d = absolute(r - r0) + absolute(c - c0)`.
7.  Check if the distance `d` is even or odd.
8.  If `d` is even, set the color of the corresponding pixel (r, c) in the output grid to white (0).
9.  If `d` is odd, set the color of the corresponding pixel (r, c) in the output grid to the identified background color (`bg_color`).
10. Return the completed output grid.
