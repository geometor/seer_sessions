
## train_1

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 2 1 5 2 0 0 0 0 0 0 0 7 7 7 7 0 0 0 0
0 2 8 9 0 0 0 0 0 0 0 0 7 7 7 7 0 0 0 0
0 2 2 0 0 0 0 0 0 0 0 0 7 7 7 7 0 0 0 0
0 2 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 4 4 4 4 4 4 0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 4 4 4 0 0 0 0 0 0 0 0 0 3 0 0 0
0 0 0 0 4 4 0 0 0 0 0 0 0 0 3 3 3 0 0 0
0 0 0 0 4 0 0 0 0 0 0 0 0 0 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 3 3 3 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
1 1 1 1 1 5 5 5
1 1 1 1 9 5 5 5
1 1 1 9 9 5 5 5
1 1 9 9 9 5 5 5
1 9 9 9 9 9 9 9
8 8 8 9 9 9 9 9
8 8 8 9 9 9 9 9
8 8 8 8 8 9 9 9
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 5 5 5 5 5 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 5 5 0 0 0
0 0 0 0 6 6 6 0 0 0 0 0 0 0 0 5 5 0 0 0
0 0 0 0 6 6 6 0 0 0 0 0 0 0 5 5 5 0 0 0
0 0 0 0 6 2 4 6 6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 8 3 6 6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 6 6 6 6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 6 6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 6 6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 6 6 6 6 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 1 1 0
0 9 9 9 9 9 9 0 0 0 0 0 0 0 0 1 1 1 1 0
0 9 9 9 9 9 9 0 0 0 0 0 0 0 0 1 1 1 1 0
0 9 9 9 9 9 9 0 0 0 0 0 0 0 0 1 1 1 1 0
0 9 9 9 9 9 9 0 0 0 0 0 0 0 0 1 1 1 1 0
0 9 9 0 0 9 9 0 0 0 0 0 0 0 0 1 1 1 1 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```


**output:**
```
2 2 2 4 4 4 4 4 4 4
2 2 2 4 4 4 4 4 4 4
2 2 2 2 2 4 4 4 4 4
2 2 2 2 2 4 4 4 4 4
2 2 2 2 2 3 3 3 3 3
8 8 8 2 2 3 3 3 3 3
8 8 2 2 2 2 3 3 3 3
8 8 2 2 2 2 3 3 3 3
8 8 8 8 8 3 3 3 3 3
8 8 8 8 8 3 3 3 3 3
```

## Perception

1.  **Input/Output Format:** The input is a 2D grid of integers (colors), typically 20x20. The output is also a 2D grid of integers, but smaller (e.g., 8x8, 10x10).
2.  **Input Content:** The input grid contains multiple contiguous areas (shapes) of non-zero integers (colors) on a background of 0. Usually, one of these shapes contains smaller regions of different non-zero integers within its boundary, which are distinct from its own primary color. I'll call these internal colors "noise".
3.  **Core Task:** The primary goal is to identify the shape containing this internal "noise", extract the pattern of the noise itself, and then render this pattern onto the output grid.
4.  **Transformation:**
    *   **Identification:** Locate the single shape whose constituent cells include values different from both the shape's main color and the background color (0).
    *   **Extraction:** Isolate the noise pattern. This involves finding the minimum bounding box containing only the noise pixels (excluding the main shape color and background 0). This forms a smaller `noise_grid`.
    *   **Scaling:** Determine the dimensions of the `noise_grid` (`H_n`, `W_n`) and the output grid (`H_out`, `W_out`). Calculate an integer scaling factor, `scale = H_out / H_n = W_out / W_n`.
    *   **Rendering:** Generate the output grid by mapping each output pixel `(r, c)` back to the `noise_grid` space and determining its color based on the noise values in its vicinity. The exact rendering rule appears complex, but seems strongly related to taking the *maximum* color value from a small neighborhood (potentially 4 specific neighbors) in the `noise_grid` corresponding to the output pixel's scaled location. Boundary conditions (when neighbors fall outside the `noise_grid`) likely default to a value of 0.

## Facts

```yaml
task_type: grid_transformation

input_features:
  grid_dimensions: [20, 20] # Example, can vary
  background_color: 0
  objects:
    - type: shape
      properties:
        - color: integer (1-9)
        - contiguity: cells of the same color are connected
        - contains_noise: boolean (typically only one shape is True)
    - type: noise_pixel
      properties:
        - color: integer (1-9)
        - location: (row, col)
        - container_shape_color: integer (color of the shape it's inside)
      constraints:
        - color != 0
        - color != container_shape_color

output_features:
  grid_dimensions: variable (e.g., [8, 8], [10, 10]) depends on input
  content: grid derived from the noise pattern of one input shape

relationships:
  - type: containment
    description: One shape contains noise pixels.
  - type: transformation
    description: The noise pattern within the identified shape is scaled and rendered to produce the output grid.
  - type: scaling
    description: |
      Output grid dimensions are an integer multiple ('scale')
      of the noise pattern's minimal bounding box dimensions.
  - type: rendering_rule # Tentative hypothesis
    description: |
      Each output pixel's color is determined by the maximum color value
      among the four noise grid cells surrounding the output pixel's
      mapped location in the noise grid space. Out-of-bounds noise cells
      are treated as having a value of 0.

actions:
  - identify_noisy_shape: Find the unique shape containing internal noise pixels.
  - extract_noise_grid: Determine the minimal bounding box of noise pixels and create the noise_grid.
  - calculate_scale: Compute the scaling factor based on output grid and noise_grid dimensions.
  - render_output: For each output pixel, map its location, identify relevant noise neighbors, apply max function (with boundary handling), and assign color.

```

## Natural Language Program

1.  **Identify Target Shape:** Scan the input grid to find connected components (shapes) of non-zero colors. Identify the unique shape that contains pixels whose colors are neither the shape's primary color nor the background color (0). Let the primary color of this shape be `border_color`.
2.  **Extract Noise Pattern:**
    a.  Determine the bounding box of the identified target shape.
    b.  Within this bounding box, find all pixels whose color is not `border_color` and not 0. These are the "noise pixels".
    c.  Determine the minimum and maximum row and column indices occupied by these noise pixels.
    d.  Create a new grid, `noise_grid`, containing only these noise pixels, relative to their minimum row/column indices. Let the dimensions of `noise_grid` be `H_noise` x `W_noise`.
3.  **Determine Scaling:** Get the dimensions of the output grid, `H_out` x `W_out`. Calculate the scaling factor `scale = H_out / H_noise`. (Verify that `W_out / W_noise` yields the same integer scale).
4.  **Render Output Grid:** Create an output grid of size `H_out` x `W_out`. For each pixel `(r, c)` in the output grid (from row 0 to `H_out-1`, col 0 to `W_out-1`):
    a.  Map the output pixel location `(r, c)` to fractional coordinates in the `noise_grid` space: `r_f = r / scale`, `c_f = c / scale`.
    b.  Identify the four integer grid points surrounding `(r_f, c_f)` in the `noise_grid`:
        i.  `P_tl = (floor(r_f), floor(c_f))`
        ii. `P_tr = (floor(r_f), ceil(c_f))`
        iii. `P_bl = (ceil(r_f), floor(c_f))`
        iv. `P_br = (ceil(r_f), ceil(c_f))`
    c.  Initialize a list of neighbor values.
    d.  For each point `P = (nr, nc)` identified in step 4b:
        i.  Check if the coordinates `(nr, nc)` are within the bounds of the `noise_grid` (i.e., `0 <= nr < H_noise` and `0 <= nc < W_noise`).
        ii. If within bounds, add the value `noise_grid[nr][nc]` to the list of neighbor values.
        iii. If out of bounds, add the value 0 to the list of neighbor values.
    e.  Assign the color to the output pixel `(r, c)` by finding the maximum value in the list of neighbor values collected in step 4d.
