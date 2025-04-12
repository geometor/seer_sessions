**Perception**

1.  **Input/Output Structure:** Both input and output are grids of colored pixels (represented by integers 0-9). White (0) acts as the background.
2.  **Key Elements:** The grids contain distinct types of non-background elements:
    *   A single "agent" pixel: This pixel seems to initiate the transformation. In the examples, it's often identified by being the only pixel of its color (yellow in train_1, red in train_3) or being spatially isolated from other pixels of the same color (the single orange pixel in train_2, distinct from the orange pixels in the top row).
    *   A set of "obstacle" pixels: These are the other non-background pixels. They seem to define boundaries or stopping points for the action initiated by the agent. They can form structures like lines (gray vertical line in train_1, orange horizontal line in train_2) or be scattered points (green diagonal points in train_3).
3.  **Transformation:** The core transformation is drawing a line segment originating from the agent pixel, using the agent pixel's color.
4.  **Line Direction:** The direction of the line appears determined by the agent's position relative to the grid boundaries. Agents near an edge or corner seem to draw lines moving away from that edge/corner (e.g., right edge -> move left, bottom edge -> move up, bottom-left corner -> move up-right).
5.  **Stopping Condition:** The line segment stops based on interaction with the obstacle pixels. The specific rule seems to depend on the arrangement of the obstacles:
    *   If obstacles form a solid line (like train_1, train_2), the drawn line stops exactly one pixel *before* reaching the row or column occupied by the obstacle line.
    *   If obstacles are scattered points (like train_3), the drawn line stops *at* the first pixel whose row OR column contains any obstacle pixel.

**Facts (YAML)**


```yaml
task_description: Draw a line from a single 'agent' pixel, using its color, until the line reaches a boundary defined by 'obstacle' pixels. The stopping rule depends on the obstacle configuration.

definitions:
  - name: background_pixel
    value: 0 # white
  - name: agent_pixel
    description: A unique non-background pixel, identified either by its unique color or spatial isolation.
    properties:
      - color: C
      - position: (r0, c0)
  - name: obstacle_pixels
    description: All non-background pixels excluding the agent pixel.
    properties:
      - positions: Set of (r, c) coordinates.
      - occupied_rows: R_O (Set of row indices containing obstacles).
      - occupied_cols: C_O (Set of column indices containing obstacles).
      - structure: Derived property, either 'solid_line' (if obstacles form a contiguous horizontal or vertical line) or 'scattered'.

parameters:
  - name: line_direction
    description: Vector (dr, dc) determined by agent position relative to grid boundaries.
    values:
      - (-1, 0) # Up
      - (1, 0)  # Down
      - (0, -1) # Left
      - (0, 1)  # Right
      - (-1, -1) # Up-Left
      - (-1, 1)  # Up-Right
      - (1, -1)  # Down-Left
      - (1, 1)   # Down-Right
    determination: Move away from the nearest grid edge/corner.

transformations:
  - step: Identify agent (C, (r0, c0)) and obstacles (O, R_O, C_O).
  - step: Classify obstacle structure ('solid_line' or 'scattered').
  - step: Determine line_direction (dr, dc).
  - step: Initialize current position (r, c) = (r0, c0).
  - step: Draw line segment based on obstacle structure:
      - if structure == 'solid_line':
          - Loop:
              - Calculate next position (nr, nc) = (r + dr, c + dc).
              - Check grid bounds for (nr, nc). If out, stop loop.
              - Check if (nr, nc) hits the obstacle line boundary (e.g., nr is in R_O if obstacle is horizontal line, nc is in C_O if obstacle is vertical line). If yes, stop loop.
              - If not stopped: color pixel (nr, nc) with C, update (r, c) = (nr, nc).
      - if structure == 'scattered':
          - Loop:
              - Calculate next position (nr, nc) = (r + dr, c + dc).
              - Check grid bounds for (nr, nc). If out, stop loop.
              - Check stop condition: Is row `nr` in R_O OR column `nc` in C_O?
              - If stop condition is TRUE: color pixel (nr, nc) with C, then stop loop.
              - If stop condition is FALSE: color pixel (nr, nc) with C, update (r, c) = (nr, nc).

output_grid: The input grid modified by coloring the pixels along the drawn line segment.
```


**Natural Language Program**

1.  Identify the agent pixel, which is the unique non-background pixel (either by color or spatial isolation). Note its color (C) and position (r0, c0).
2.  Identify all other non-background pixels as obstacles. Record the set of rows (R_O) and columns (C_O) they occupy.
3.  Analyze the obstacle positions to determine if they form a 'solid\_line' (horizontal or vertical) or are 'scattered'.
4.  Determine the drawing direction (dr, dc) by finding the nearest grid edge or corner to the agent pixel and selecting the direction moving away from it (e.g., if nearest is bottom-left corner, direction is up-right (-1, 1)).
5.  Initialize the current drawing position (r, c) to the agent's position (r0, c0).
6.  If the obstacle structure is 'solid\_line':
    *   Repeatedly calculate the next position (nr, nc) = (r + dr, c + dc).
    *   If (nr, nc) is outside the grid, stop drawing.
    *   If the obstacles form a horizontal line, check if the row `nr` is in R_O. If yes, stop drawing.
    *   If the obstacles form a vertical line, check if the column `nc` is in C_O. If yes, stop drawing.
    *   If not stopped, color the pixel at (nr, nc) with C, update (r, c) = (nr, nc), and repeat.
7.  If the obstacle structure is 'scattered':
    *   Repeatedly calculate the next position (nr, nc) = (r + dr, c + dc).
    *   If (nr, nc) is outside the grid, stop drawing.
    *   Check if the row `nr` is in R_O OR the column `nc` is in C_O.
    *   If this condition is TRUE, color the pixel at (nr, nc) with C, and then stop drawing.
    *   If this condition is FALSE, color the pixel at (nr, nc) with C, update (r, c) = (nr, nc), and repeat.
8.  Output the resulting grid.