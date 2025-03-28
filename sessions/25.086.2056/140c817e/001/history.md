
## train_1

**input:**
```
9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9
9 9 9 1 9 9 9 9 9
9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 1 9 9
9 9 9 9 9 9 9 9 9
9 9 9 9 9 9 9 9 9
```


**output:**
```
9 9 9 1 9 9 1 9 9
9 9 9 1 9 9 1 9 9
9 9 3 1 3 9 1 9 9
1 1 1 2 1 1 1 1 1
9 9 3 1 3 9 1 9 9
9 9 9 1 9 3 1 3 9
1 1 1 1 1 1 2 1 1
9 9 9 1 9 3 1 3 9
9 9 9 1 9 9 1 9 9
```


## train_2

**input:**
```
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 1 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 1 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 1 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 1 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8
```


**output:**
```
8 8 1 8 8 1 8 8 8 1 3 1 3
1 1 1 1 1 1 1 1 1 1 1 2 1
8 3 1 3 8 1 8 8 8 1 3 1 3
1 1 2 1 1 1 1 1 1 1 1 1 1
8 3 1 3 8 1 8 8 8 1 8 1 8
8 8 1 8 8 1 8 8 3 1 3 1 8
1 1 1 1 1 1 1 1 1 2 1 1 1
8 8 1 8 8 1 8 8 3 1 3 1 8
8 8 1 8 3 1 3 8 8 1 8 1 8
1 1 1 1 1 2 1 1 1 1 1 1 1
8 8 1 8 3 1 3 8 8 1 8 1 8
8 8 1 8 8 1 8 8 8 1 8 1 8
8 8 1 8 8 1 8 8 8 1 8 1 8
```


## train_3

**input:**
```
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 1 7 7
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7
7 7 1 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7
7 7 7 7 7 7 1 7 7 7 7
7 7 7 7 7 7 7 7 7 7 7
```


**output:**
```
7 7 1 7 7 7 1 3 1 3 7
1 1 1 1 1 1 1 1 2 1 1
7 7 1 7 7 7 1 3 1 3 7
7 3 1 3 7 7 1 7 1 7 7
1 1 2 1 1 1 1 1 1 1 1
7 3 1 3 7 7 1 7 1 7 7
7 7 1 7 7 7 1 7 1 7 7
7 7 1 7 7 7 1 7 1 7 7
7 7 1 7 7 3 1 3 1 7 7
1 1 1 1 1 1 2 1 1 1 1
7 7 1 7 7 3 1 3 1 7 7
```

Okay, let's analyze the task based on the provided examples.

**Perception:**

1.  **Input Structure:** The input grids consist primarily of a single background color (maroon `9`, azure `8`, or orange `7`) with a few sparsely placed single pixels of blue (`1`).
2.  **Output Structure:** The output grids retain the same dimensions and background color as the input. The locations corresponding to the original blue (`1`) pixels in the input are transformed, and additional patterns are introduced, centered around these original locations.
3.  **Core Transformation:** The transformation identifies each blue (`1`) pixel in the input and draws a specific pattern centered on its location in the output grid.
4.  **Pattern Details:**
    *   The original blue (`1`) pixel at `(r, c)` is replaced by a red (`2`) pixel in the output.
    *   A horizontal line of blue (`1`) pixels is drawn across the entire row `r`, except at the center column `c` (which is red `2`).
    *   A vertical line of blue (`1`) pixels is drawn down the entire column `c`, except at the center row `r` (which is red `2`).
    *   Green (`3`) pixels are placed at the four diagonal neighbors of the center pixel `(r, c)`, i.e., at `(r-1, c-1)`, `(r-1, c+1)`, `(r+1, c-1)`, and `(r+1, c+1)`, provided these coordinates are within the grid bounds.
5.  **Interaction/Overlapping:** When patterns from multiple input blue pixels overlap, the colors overwrite each other. The examples suggest a specific precedence: red (`2`) at the center seems final, green (`3`) seems to overwrite blue (`1`) at the diagonal locations, and blue (`1`) lines overwrite the background color. A two-stage process appears necessary: first draw the centers (`2`) and lines (`1`), then draw the diagonals (`3`).

**YAML Facts:**


```yaml
task_context:
  grid_properties:
    - dimensions: Input and output grids have the same height and width.
    - background_color: The predominant color in the input grid serves as the background and is preserved in the output grid where no other pattern is drawn.
  objects:
    - object: source_pixel
      description: Isolated pixels of blue color (1) in the input grid.
      properties:
        - color: blue (1)
        - location: (row, column) coordinates
    - object: pattern
      description: A composite shape drawn in the output grid centered on the location of each source_pixel.
      properties:
        - center_color: red (2) at the source_pixel location.
        - line_color: blue (1) forming horizontal and vertical lines through the center, extending to grid boundaries.
        - diagonal_color: green (3) placed at the four diagonal neighbors of the center.
actions:
  - action: identify_source_pixels
    input: input_grid
    output: list of coordinates (r, c) for all blue (1) pixels.
  - action: initialize_output
    input: input_grid dimensions, background_color
    output: output_grid filled with background_color.
  - action: draw_center_and_lines
    input: output_grid, source_pixel coordinates (r, c)
    output: modified output_grid
    steps:
      - Set output_grid[r, c] to red (2).
      - Fill output_grid[r, :] with blue (1), skipping column c.
      - Fill output_grid[:, c] with blue (1), skipping row r.
  - action: draw_diagonals
    input: output_grid, source_pixel coordinates (r, c)
    output: modified output_grid
    steps:
      - For each diagonal neighbor (nr, nc) of (r, c):
        - If (nr, nc) is within grid bounds, set output_grid[nr, nc] to green (3).
relationships:
  - Each source_pixel in the input corresponds to one pattern in the output.
  - The pattern's center is located at the source_pixel's original coordinates.
  - The pattern's colors (red 2, blue 1, green 3) overwrite the background color and potentially each other based on drawing order.
order_of_operations:
  - Initialize the output grid with the background color.
  - Iterate through all identified source_pixel coordinates. For each coordinate, perform the draw_center_and_lines action.
  - After processing all source pixels for centers and lines, iterate through all identified source_pixel coordinates again. For each coordinate, perform the draw_diagonals action.
```


**Natural Language Program:**

1.  Determine the background color by finding the most frequent color in the input grid.
2.  Create a new output grid with the same dimensions as the input grid, initially filled entirely with the background color.
3.  Identify the row and column coordinates of every blue (`1`) pixel in the input grid. Store these coordinates.
4.  **First Pass (Centers and Lines):** Iterate through the stored coordinates `(r, c)` of the original blue (`1`) pixels:
    a.  For the current coordinate `(r, c)`, draw a horizontal line of blue (`1`) pixels across the entire `r`-th row of the output grid.
    b.  Draw a vertical line of blue (`1`) pixels down the entire `c`-th column of the output grid.
    c.  Set the pixel at `output[r, c]` to red (`2`).
5.  **Second Pass (Diagonals):** Iterate *again* through the stored coordinates `(r, c)` of the original blue (`1`) pixels:
    a.  For the current coordinate `(r, c)`, examine its four diagonal neighbors: `(r-1, c-1)`, `(r-1, c+1)`, `(r+1, c-1)`, `(r+1, c+1)`.
    b.  For each diagonal neighbor `(nr, nc)` that falls within the bounds of the grid, set the pixel at `output[nr, nc]` to green (`3`). This may overwrite existing blue (`1`) pixels from the first pass.
6.  Return the completed output grid.
