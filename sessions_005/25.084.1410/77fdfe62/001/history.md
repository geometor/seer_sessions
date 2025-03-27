
## train_1

**input:**
```
9 1 0 0 1 4
1 1 1 1 1 1
0 1 8 8 1 0
0 1 8 0 1 0
1 1 1 1 1 1
2 1 0 0 1 3
```


**output:**
```
9 4
2 0
```


## train_2

**input:**
```
2 1 0 0 0 0 1 3
1 1 1 1 1 1 1 1
0 1 0 8 0 0 1 0
0 1 8 8 0 8 1 0
0 1 0 0 8 0 1 0
0 1 8 0 8 8 1 0
1 1 1 1 1 1 1 1
4 1 0 0 0 0 1 6
```


**output:**
```
0 2 0 0
2 2 0 3
0 0 6 0
4 0 6 6
```


## train_3

**input:**
```
6 1 0 0 0 0 1 2
1 1 1 1 1 1 1 1
0 1 0 8 0 8 1 0
0 1 8 8 8 0 1 0
0 1 8 0 8 8 1 0
0 1 8 8 8 0 1 0
1 1 1 1 1 1 1 1
7 1 0 0 0 0 1 4
```


**output:**
```
0 6 0 2
6 6 2 0
7 0 4 4
7 7 4 0
```

Okay, let's analyze the task examples.

## Perception

1.  **Input Grid Structure:** Each input grid has a distinct structure:
    *   A central rectangular area containing white (0) and azure (8) pixels.
    *   This central area is enclosed by a single-pixel-thick frame of blue (1) pixels.
    *   The blue frame is separated from the grid's outer boundary by one layer of pixels (which are mostly white (0), except at the corners).
    *   The four corner pixels of the input grid have distinct colors (maroon, yellow, red, green, magenta, orange, etc.).

2.  **Output Grid Structure:** The output grid is smaller than the input grid. Its dimensions match the dimensions of the central area *inside* the blue frame of the input grid.

3.  **Transformation Logic:**
    *   The output grid seems to be derived directly from the central area (inside the blue frame) of the input grid.
    *   The white (0) pixels within the input's central area appear to remain white (0) in the corresponding positions in the output grid.
    *   The azure (8) pixels within the input's central area are replaced in the output grid. The replacement color depends on the position of the azure pixel within the central area.
    *   Specifically, the central area can be divided into four equal quadrants (Top-Left, Top-Right, Bottom-Left, Bottom-Right).
    *   If an azure (8) pixel is in the Top-Left quadrant of the central area, it's replaced by the color of the Top-Left corner pixel of the *original input grid*.
    *   Similarly, azure (8) pixels in the Top-Right, Bottom-Left, and Bottom-Right quadrants of the central area are replaced by the colors of the Top-Right, Bottom-Left, and Bottom-Right corner pixels of the *original input grid*, respectively.

4.  **Consistency:** This pattern holds across all three training examples. The size of the central area determines the output size, and the mapping rule based on azure pixels, quadrants, and input corner colors consistently produces the correct output.

## Facts


```yaml
Task: Map pixels within a framed area based on position and input corner colors.

Input_Grid:
  - Properties:
      - Contains a blue (1) frame.
      - Frame is 1 pixel thick.
      - Frame is offset by 1 pixel from the grid edges.
      - Has distinct colors at the four corner pixels (C_TL, C_TR, C_BL, C_BR).
      - Contains a central rectangular area ('Inner_Grid') enclosed by the blue frame.
  - Objects:
      - Blue_Frame: A rectangle of blue (1) pixels.
      - Inner_Grid: The rectangular subgrid enclosed by Blue_Frame.
        - Properties: Contains white (0) and azure (8) pixels. Dimensions determine Output_Grid size. Can be divided into four equal quadrants (Q_TL, Q_TR, Q_BL, Q_BR).
      - Corner_Pixels: The four pixels at the absolute corners of Input_Grid.
        - Properties: C_TL (Top-Left), C_TR (Top-Right), C_BL (Bottom-Left), C_BR (Bottom-Right). Values are used for mapping.

Output_Grid:
  - Properties:
      - Dimensions match Inner_Grid dimensions.
      - Content is derived from Inner_Grid.

Transformation:
  - Action: Identify Blue_Frame and extract Inner_Grid.
  - Action: Identify the four Corner_Pixels (C_TL, C_TR, C_BL, C_BR) of Input_Grid.
  - Action: Create Output_Grid with the same dimensions as Inner_Grid.
  - Rule: For each pixel `P` at `(r, c)` in Inner_Grid:
      - If `P` is white (0), set Output_Grid pixel at `(r, c)` to white (0).
      - If `P` is azure (8):
          - Determine the quadrant of `(r, c)` within Inner_Grid.
          - If `(r, c)` is in Q_TL, set Output_Grid pixel at `(r, c)` to C_TL.
          - If `(r, c)` is in Q_TR, set Output_Grid pixel at `(r, c)` to C_TR.
          - If `(r, c)` is in Q_BL, set Output_Grid pixel at `(r, c)` to C_BL.
          - If `(r, c)` is in Q_BR, set Output_Grid pixel at `(r, c)` to C_BR.

Relationships:
  - Output_Grid size is determined by Inner_Grid size.
  - Output_Grid content depends on Inner_Grid pixel values and their positions relative to Inner_Grid quadrants.
  - The colors used for replacement in Output_Grid are sourced from the Corner_Pixels of Input_Grid.
```


## Natural Language Program

1.  **Identify the Inner Grid:** Locate the rectangular frame composed entirely of blue (1) pixels within the input grid. Extract the subgrid enclosed by this blue frame; this is the "inner grid". Note its height (H) and width (W).
2.  **Identify Corner Colors:** Record the colors of the four corner pixels of the original input grid: Top-Left (C_TL), Top-Right (C_TR), Bottom-Left (C_BL), and Bottom-Right (C_BR).
3.  **Initialize Output Grid:** Create a new grid (the "output grid") with the same dimensions (H x W) as the inner grid.
4.  **Process Inner Grid Pixels:** Iterate through each pixel `P` at row `r` and column `c` of the inner grid (where `0 <= r < H` and `0 <= c < W`):
    *   **If `P` is white (0):** Set the corresponding pixel in the output grid at `(r, c)` to white (0).
    *   **If `P` is azure (8):**
        *   Determine the quadrant for the pixel `(r, c)` based on the midpoint of the inner grid (H/2, W/2):
            *   If `r < H/2` and `c < W/2` (Top-Left quadrant), set the output grid pixel at `(r, c)` to `C_TL`.
            *   If `r < H/2` and `c >= W/2` (Top-Right quadrant), set the output grid pixel at `(r, c)` to `C_TR`.
            *   If `r >= H/2` and `c < W/2` (Bottom-Left quadrant), set the output grid pixel at `(r, c)` to `C_BL`.
            *   If `r >= H/2` and `c >= W/2` (Bottom-Right quadrant), set the output grid pixel at `(r, c)` to `C_BR`.
5.  **Return Output:** The completed output grid is the result.
