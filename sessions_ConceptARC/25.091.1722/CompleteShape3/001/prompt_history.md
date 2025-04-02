
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 0 0 4 4 0 0 0 0
0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 4 0 0
0 4 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 4 0 0
0 4 4 0 0 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 4 4 0 0
0 4 0 0 0 0 0 4 0 0
0 4 0 0 0 0 0 4 0 0
0 4 0 0 0 0 0 4 0 0
0 4 0 0 0 0 0 4 0 0
0 4 4 4 4 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 6 6 0 6 0
0 0 0 0 0 0 0 0 6 0
0 6 0 0 0 0 0 0 6 0
0 0 0 0 0 0 0 0 0 0
0 6 0 0 0 0 0 0 6 0
0 6 6 0 6 6 6 0 6 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 6 6 6 6 6 6 6 6 0
0 6 0 0 0 0 0 0 6 0
0 6 0 0 0 0 0 0 6 0
0 6 0 0 0 0 0 0 6 0
0 6 0 0 0 0 0 0 6 0
0 6 6 6 6 6 6 6 6 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
```

Okay, let's analyze the provided examples.

**Perception of the Elements:**

1.  **Grid Structure:** Both input and output grids are 10x10.
2.  **Colors:** The primary colors involved are white (0) as the background and a single non-background color (yellow-4 in the first example, magenta-6 in the second).
3.  **Input Pattern:** The non-background pixels in the input grids appear scattered, seemingly without a clear geometric shape initially. They act like markers or points.
4.  **Output Pattern:** The non-background pixels in the output grids form a hollow rectangle.
5.  **Relationship:** The rectangle in the output appears to be defined by the extent of the non-background pixels in the input. Specifically, the rectangle's edges align with the minimum and maximum row and column indices of the input's non-background pixels.
6.  **Transformation:** The transformation identifies the spatial bounds (minimum and maximum rows and columns) defined by the non-background pixels in the input and then draws the perimeter of the resulting bounding box using that same non-background color in the output grid. The interior of the rectangle and the area outside remain the background color.

**Facts (YAML):**


```yaml
task_description: "Identify the bounding box defined by non-background pixels in the input grid and draw the perimeter of this box in the output grid using the same non-background color."
elements:
  - element: background_pixel
    color_name: white
    color_value: 0
    role: Fills the grid where no other objects are present. Remains unchanged in the output unless overwritten by the output shape.
  - element: marker_pixels
    color_name: Varies (yellow in ex1, magenta in ex2)
    color_value: Non-zero value (4 in ex1, 6 in ex2)
    role: A set of pixels in the input grid defining spatial coordinates.
    properties:
      - scattered locations
      - determine the extent (min/max row/col) of the output shape
  - element: output_rectangle
    color_name: Same as marker_pixels
    color_value: Same as marker_pixels
    role: The primary object generated in the output grid.
    properties:
      - shape: hollow rectangle (perimeter only)
      - location: Defined by the minimum and maximum row and column indices of the input marker_pixels.
      - thickness: 1 pixel
grid_properties:
  - size: Remains constant between input and output (10x10 in examples).
relationships:
  - type: bounding_box
    input_element: marker_pixels
    output_element: output_rectangle
    description: The output_rectangle represents the perimeter of the minimum bounding box enclosing all marker_pixels from the input.
  - type: color_persistence
    input_element: marker_pixels
    output_element: output_rectangle
    description: The color of the output_rectangle is the same as the color of the input marker_pixels.
  - type: background_preservation
    input_element: background_pixel
    output_element: background_pixel
    description: The background color remains the same and fills areas not occupied by the output_rectangle.
actions:
  - action: find_extents
    input: marker_pixels locations
    output: min_row, max_row, min_col, max_col
    description: Determine the minimum bounding box coordinates containing all marker_pixels.
  - action: draw_perimeter
    input: min_row, max_row, min_col, max_col, marker_color
    output: output_grid with hollow rectangle
    description: Create an output grid of the same size as the input, initialized with the background color. Draw the top, bottom, left, and right edges of the bounding box using the marker_color.
```


**Natural Language Program:**

1.  Identify the single non-background color (let's call it `marker_color`) present in the input grid and find the coordinates (row, column) of all pixels with this `marker_color`.
2.  Determine the minimum row index (`min_row`), maximum row index (`max_row`), minimum column index (`min_col`), and maximum column index (`max_col`) among these coordinates.
3.  Create a new output grid with the same dimensions as the input grid, filled entirely with the background color (white, 0).
4.  Draw the perimeter of the rectangle defined by the calculated extents onto the output grid using the `marker_color`:
    a.  Fill the pixels from (`min_row`, `min_col`) to (`min_row`, `max_col`) with `marker_color`.
    b.  Fill the pixels from (`max_row`, `min_col`) to (`max_row`, `max_col`) with `marker_color`.
    c.  Fill the pixels from (`min_row + 1`, `min_col`) to (`max_row - 1`, `min_col`) with `marker_color`.
    d.  Fill the pixels from (`min_row + 1`, `max_col`) to (`max_row - 1`, `max_col`) with `marker_color`.
5.  Return the modified output grid.
