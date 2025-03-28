
## train_1

**input:**
```
8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8
8 8 8 9 9 8 8 8 8 8 8
8 8 8 8 9 9 8 8 8 8 8
8 8 8 8 8 9 9 9 8 8 8
8 8 8 8 9 8 9 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8
```


**output:**
```
8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8
8 9 9 9 9 9 9 9 9 9 8
8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8
```


## train_2

**input:**
```
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 3 8 8 8
8 8 8 8 3 3 3 8 8 8
8 8 8 8 8 3 3 8 8 8
8 8 8 8 8 8 8 8 8 8
```


**output:**
```
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
8 8 3 3 3 3 3 3 8 8
8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8
```


## train_3

**input:**
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 2 2 2 8 8
8 8 8 8 8 2 8 8 2 2 8 8 2 8 8
8 8 8 8 8 8 2 8 2 2 2 8 2 8 8
8 8 8 8 8 8 8 2 8 8 8 2 2 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```


**output:**
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
2 2 2 2 2 2 2 2 2 2 2 2 2 2 2
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```

Okay, let's analyze the task based on the provided examples.

**Perception of Elements:**

1.  **Grid Structure:** The inputs and outputs are 2D grids of pixels represented by integer color codes.
2.  **Background Color:** In all examples, the predominant color is 'azure' (8), acting as a background.
3.  **Foreground Object(s):** Each input grid contains multiple pixels of a single non-background color ('maroon' (9) in Ex1, 'green' (3) in Ex2, 'red' (2) in Ex3). These foreground pixels are scattered across different locations in the input grid.
4.  **Transformation:** The core transformation involves collecting all the scattered foreground pixels from the input and arranging them into a single, solid, horizontal line in the output grid. The background color fills the rest of the output grid.
5.  **Line Properties:**
    *   **Color:** The color of the line in the output is the same as the color of the scattered foreground pixels in the input.
    *   **Length:** The length of the horizontal line corresponds exactly to the total number of foreground pixels found in the input grid.
    *   **Position (Row):** The horizontal line in the output grid is consistently placed in the vertical middle row of the grid. If the grid has an even number of rows, the middle row closer to the top is used (integer division or floor of the center index). Specifically, the row index appears to be `floor((grid_height - 1) / 2)`.
    *   **Position (Column):** The horizontal line is horizontally centered within the determined row. The starting column index seems to be calculated as `floor((grid_width - line_length) / 2)`.

**YAML Fact Document:**


```yaml
task_description: Consolidate scattered pixels of a single foreground color into a centered horizontal line.

elements:
  - element: grid
    description: A 2D array of pixels representing colors.
    properties:
      - height: Integer number of rows.
      - width: Integer number of columns.
  - element: background_pixel
    description: The most frequent pixel color in the input grid, typically 'azure' (8).
  - element: foreground_pixels
    description: A collection of pixels in the input grid that are not the background color. All foreground pixels share the same color within a single example.
    properties:
      - color: The color code of the foreground pixels (e.g., 9, 3, 2).
      - count: The total number of foreground pixels.
      - locations: List of (row, column) coordinates for each foreground pixel.
  - element: output_line
    description: A solid horizontal line in the output grid composed of the foreground color.
    properties:
      - color: Same as the input foreground pixel color.
      - length: Equal to the count of input foreground pixels.
      - row_index: The vertical middle row of the grid, calculated as floor((grid_height - 1) / 2).
      - start_column_index: The starting column for the line, ensuring horizontal centering, calculated as floor((grid_width - length) / 2).

relationships:
  - relationship: Input to Output Grid Dimensions
    description: The output grid has the same height and width as the input grid.
  - relationship: Foreground Color Persistence
    description: The color of the foreground pixels in the input determines the color of the horizontal line in the output.
  - relationship: Pixel Count Conservation
    description: The total number of foreground pixels in the input determines the length of the horizontal line in the output.
  - relationship: Line Placement Rule
    description: The horizontal line is always placed in the vertical center row and horizontally centered based on grid dimensions and line length.

actions:
  - action: Identify Background and Foreground
    description: Determine the background color and locate all pixels of the single foreground color.
  - action: Count Foreground Pixels
    description: Calculate the total number of foreground pixels.
  - action: Determine Output Grid Dimensions
    description: Use the dimensions of the input grid for the output grid.
  - action: Calculate Line Position
    description: Compute the target row index (vertical center) and starting column index (horizontal center).
  - action: Construct Output Grid
    description: Create a new grid filled with the background color.
  - action: Draw Line
    description: Place the calculated horizontal line onto the output grid at the determined position.
```


**Natural Language Program:**

1.  Receive the input grid.
2.  Identify the background color (which is the most frequent color, usually 'azure' - 8).
3.  Find all pixels that are *not* the background color. Note their color (let's call it `line_color`) and count how many there are (let's call this `line_length`). Assume there's only one non-background color present.
4.  Determine the height (`H`) and width (`W`) of the input grid.
5.  Calculate the row index for the output line: `row_index = floor((H - 1) / 2)`.
6.  Calculate the starting column index for the output line: `start_col = floor((W - line_length) / 2)`.
7.  Create a new output grid with the same dimensions (`H` x `W`) and fill it entirely with the background color identified in step 2.
8.  In the output grid, starting at the coordinates (`row_index`, `start_col`), change the color of `line_length` consecutive pixels in that row to `line_color`.
9.  Return the modified output grid.
