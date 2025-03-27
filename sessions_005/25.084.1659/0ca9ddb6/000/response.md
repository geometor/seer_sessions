**Perception:**

The input grids contain scattered single pixels of various colors (azure, red, blue, magenta) on a white background. The output grids retain all the original colored pixels in their original positions. Additionally, new pixels appear in the output grid: yellow (4) and orange (7).

The appearance of the new pixels seems related to the positions of the red (2) and blue (1) pixels in the input grid.

*   **Yellow (4) pixels:** Appear diagonally adjacent to the red (2) pixels. Specifically, they form the corners of a 3x3 square centered on each red pixel, provided those corner positions are within the grid bounds and were originally white.
*   **Orange (7) pixels:** Appear orthogonally adjacent (up, down, left, right) to the blue (1) pixels. Specifically, they form a plus shape centered on each blue pixel, provided those adjacent positions are within the grid bounds and were originally white.

Pixels of other colors (azure - 8, magenta - 6) do not seem to influence the output or change themselves. The white (0) background pixels are only changed if they become yellow or orange according to the rules above.

**Facts:**


```yaml
elements:
  - type: grid
    description: Input and output are 2D grids of pixels with integer values 0-9 representing colors.
  - type: pixel
    color: red (2)
    role: source
    action: Creates yellow (4) pixels at diagonal adjacent positions.
  - type: pixel
    color: blue (1)
    role: source
    action: Creates orange (7) pixels at orthogonal adjacent positions.
  - type: pixel
    color: yellow (4)
    role: generated
    relationship: Diagonally adjacent to red (2) pixels.
  - type: pixel
    color: orange (7)
    role: generated
    relationship: Orthogonally adjacent to blue (1) pixels.
  - type: pixel
    colors: [azure (8), magenta (6)]
    role: static
    description: These pixels remain unchanged in the output.
  - type: pixel
    color: white (0)
    role: background
    action: Can be overwritten by generated yellow (4) or orange (7) pixels. Otherwise remains white.

constraints:
  - Generated pixels (yellow and orange) only appear if the target position is within the grid boundaries.
  - Generated pixels only overwrite white (0) pixels. Original non-white pixels are preserved.

transformation:
  - Identify all red (2) pixels in the input grid.
  - For each red pixel, find its diagonal neighbors (top-left, top-right, bottom-left, bottom-right).
  - If a diagonal neighbor is within the grid bounds and is currently white (0), change its color to yellow (4).
  - Identify all blue (1) pixels in the input grid.
  - For each blue pixel, find its orthogonal neighbors (up, down, left, right).
  - If an orthogonal neighbor is within the grid bounds and is currently white (0), change its color to orange (7).
  - Preserve all original non-white pixels from the input grid.
```


**Natural Language Program:**

1.  Initialize the output grid as a copy of the input grid.
2.  Iterate through each cell (pixel) of the input grid.
3.  If a cell contains a red (2) pixel:
    *   Check its four diagonal neighbors (relative coordinates: (-1,-1), (-1,+1), (+1,-1), (+1,+1)).
    *   For each diagonal neighbor:
        *   If the neighbor's coordinates are within the grid boundaries AND the corresponding cell in the *output* grid is currently white (0), change the color of that cell in the output grid to yellow (4).
4.  If a cell contains a blue (1) pixel:
    *   Check its four orthogonal neighbors (relative coordinates: (-1,0), (+1,0), (0,-1), (0,+1)).
    *   For each orthogonal neighbor:
        *   If the neighbor's coordinates are within the grid boundaries AND the corresponding cell in the *output* grid is currently white (0), change the color of that cell in the output grid to orange (7).
5.  Return the modified output grid. (Note: This description implies iteration order might matter if a red and blue pixel could influence the same white cell. However, based on the examples, orthogonal neighbors of blue and diagonal neighbors of red don't seem to overlap in a way that causes conflict. The initial copy ensures original pixels aren't overwritten incorrectly). A safer approach is to first identify all target cells to change and their new colors based on the input, then update the output grid. Revised program:

**Revised Natural Language Program:**

1.  Create a list to store modifications (target coordinates and new color).
2.  Iterate through each cell `(r, c)` of the input grid.
3.  If the input cell `(r, c)` is red (2):
    *   For each diagonal offset `(dr, dc)` in `[(-1,-1), (-1,+1), (+1,-1), (+1,+1)]`:
        *   Calculate target coordinates `(nr, nc) = (r + dr, c + dc)`.
        *   If `(nr, nc)` is within grid bounds AND the input cell `(nr, nc)` is white (0), add `((nr, nc), yellow(4))` to the modifications list.
4.  If the input cell `(r, c)` is blue (1):
    *   For each orthogonal offset `(dr, dc)` in `[(-1,0), (+1,0), (0,-1), (0,+1)]`:
        *   Calculate target coordinates `(nr, nc) = (r + dr, c + dc)`.
        *   If `(nr, nc)` is within grid bounds AND the input cell `(nr, nc)` is white (0), add `((nr, nc), orange(7))` to the modifications list.
5.  Initialize the output grid as a copy of the input grid.
6.  Iterate through the modifications list. For each `((r, c), color)`:
    *   Set the output grid cell `(r, c)` to `color`.
7.  Return the output grid.