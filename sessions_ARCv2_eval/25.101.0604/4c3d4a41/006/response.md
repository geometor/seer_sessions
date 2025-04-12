## General Assessment and Strategy

The previous code execution (`code_00.py`) failed on both training examples with 16 incorrect pixels each. Comparing the `Expected Output` and `Transformed Output` revealed systematic errors primarily in how **Non-Frame 5s** and **Content Colors** were handled, particularly within the region enclosed by the "Main Frame".

**Analysis of Errors:**

1.  **Non-Frame 5s:** The logic intended to propagate the color from the cell below (if content color) or set to background (0) otherwise. The `Transformed Output` showed incorrect values (often 5), suggesting these cells might have been wrongly included in the `main_frame_mask` or the rule execution was flawed. The `Expected Output` clearly shows propagation (`E1[1,15]=4`, `E1[1,17]=7`) or removal (`E1[2,1]=0`).
2.  **Content Colors:** The "look down for 0 before 5" rule was overly simplistic and often incorrect. The `Expected Output` suggests a more nuanced rule related to vertical stacks of identical content colors. A content color `C` seems to remain `C` if it's the top of a vertical stack of `C`s, but turns to `5` if it's *not* the top of the stack *and* that stack eventually terminates on a background (0) or frame (5) cell below it.

**Strategy:**

1.  **Refine Main Frame Identification:** Ensure `find_main_frame_mask` robustly identifies only the single largest edge-touching component of 5s, excluding any disconnected internal or external 5s.
2.  **Implement Stack-Based Content Rule:** Replace the previous content color logic with the new "stack" rule:
    *   Identify if a content cell `(r, c)` is the top of a vertical stack of identical colors.
    *   If it *is* the top, it retains its color.
    *   If it's *not* the top, check what terminates the stack below. If terminated by 0 or 5, the cell becomes 5; otherwise, it retains its color.
3.  **Apply Rules Consistently:** Apply the Non-Frame 5 rule and the refined Content Color rule to all cells *not* part of the identified Main Frame. Assume external cells will correctly become 0 through these rules.
4.  **Use Input Grid for Decisions:** Base all decisions for an output cell `(r, c)` purely on the state of the *input* grid to avoid cascading errors from in-place modifications.
5.  **Update Documentation:** Update YAML and NLP to reflect the refined stack-based logic.

## Metrics

Based on the provided `code_execution` results for the previous code (`code_00.py`):

**Example 1:**

*   **Match:** False
*   **Pixels Off:** 16
*   **Size Correct:** True
*   **Input Size:** 8x20 (160 pixels)
*   **Output Size:** 8x20 (160 pixels)
*   **Pixel Accuracy:** (160 - 16) / 160 = 144 / 160 = 90.0%
*   **Color Palette Correct:** True
*   **Color Count Correct:** False

**Example 2:**

*   **Match:** False
*   **Pixels Off:** 16
*   **Size Correct:** True
*   **Input Size:** 8x20 (160 pixels)
*   **Output Size:** 8x20 (160 pixels)
*   **Pixel Accuracy:** (160 - 16) / 160 = 144 / 160 = 90.0%
*   **Color Palette Correct:** True
*   **Color Count Correct:** False

**Analysis:**

*   The identical error count (16 pixels) across different inputs strongly points to flaws in the core transformation logic rather than edge cases.
*   The 90% accuracy suggests the Main Frame identification and handling of background/external cells were likely mostly correct, with errors concentrated on internal Non-Frame 5s and Content Colors.
*   Incorrect color counts confirm the misapplication of transformation rules for specific color types.

## YAML Facts

```yaml
definitions:
  - name: FRAME_COLOR
    value: 5
  - name: BACKGROUND_COLOR
    value: 0
  - name: CONTENT_COLOR
    value: any color that is not FRAME_COLOR and not BACKGROUND_COLOR

elements:
  - object: grid
    properties:
      - type: 2D array of integers (colors)
      - size: H x W (constant per task)
      - source: input | output
  - object: cell
    properties:
      - coordinates: (r, c) where 0 <= row < H, 0 <= column < W
      - color: integer (from grid)
      - role: determined by color and location relative to main_frame
  - object: main_frame
    properties:
      - color: FRAME_COLOR
      - connectivity: The largest connected component of FRAME_COLOR cells in the input grid that touches at least one edge of the grid.
      - scope: A boolean mask (H x W) indicating membership.

actions:
  - action: identify_main_frame
    inputs:
      - input_grid
      - FRAME_COLOR
    outputs:
      - main_frame_mask: H x W boolean grid
  - action: determine_output_color
    inputs:
      - cell_coordinates: (r, c)
      - input_grid: H x W array
      - main_frame_mask: H x W boolean grid
    process:
      - If main_frame_mask[r, c] is True: return FRAME_COLOR.
      - Get I_curr = input_grid[r, c].
      - If I_curr == BACKGROUND_COLOR: return BACKGROUND_COLOR.
      - If I_curr == FRAME_COLOR: # Non-Frame 5
          - Get I_bel1 = input_grid[r+1, c] (handle boundary -> BACKGROUND_COLOR).
          - If I_bel1 is CONTENT_COLOR: return I_bel1.
          - Else: return BACKGROUND_COLOR.
      - If I_curr is CONTENT_COLOR (C):
          - Check if cell above is same color: `is_top_of_stack = (r == 0 or input_grid[r-1, c] != C)`.
          - If is_top_of_stack: return C.
          - Else (not top of stack):
              - Find stack height h >= 1 downwards: input_grid[r+i, c] == C for 0 <= i < h.
              - Get terminating_color = input_grid[r+h, c] (handle boundary -> BACKGROUND_COLOR).
              - If terminating_color == BACKGROUND_COLOR or terminating_color == FRAME_COLOR: return FRAME_COLOR.
              - Else: return C.
    outputs:
      - output_color: integer for cell (r, c) in the output grid

algorithm:
  - step: Initialize output_grid with same dimensions as input_grid.
  - step: Identify main_frame_mask from input_grid using identify_main_frame.
  - step: For each cell (r, c) from (0, 0) to (H-1, W-1):
      - Execute determine_output_color(r, c, input_grid, main_frame_mask).
      - Assign the result to output_grid[r, c].
  - step: Return output_grid.
```

## Natural Language Program

1.  **Define Constants:** Define `FRAME_COLOR` as 5, `BACKGROUND_COLOR` as 0. Any other color is a `CONTENT_COLOR`.
2.  **Identify Main Frame:** Analyze the input grid. Find the largest connected component of `FRAME_COLOR` cells where at least one cell in the component touches any edge (top, bottom, left, or right) of the grid. Create a boolean mask `main_frame_mask` indicating which cells belong to this Main Frame.
3.  **Initialize Output:** Create a new grid (the output grid) with the same dimensions as the input grid.
4.  **Determine Output for Each Cell:** Iterate through each cell `(r, c)` of the *input* grid:
    a.  **Main Frame Cell:** If `main_frame_mask[r, c]` is true, set `output[r, c]` to `FRAME_COLOR`.
    b.  **Background Cell:** If `main_frame_mask[r, c]` is false and `input[r, c]` is `BACKGROUND_COLOR`, set `output[r, c]` to `BACKGROUND_COLOR`.
    c.  **Non-Frame 5 Cell:** If `main_frame_mask[r, c]` is false and `input[r, c]` is `FRAME_COLOR`:
        i.  Check the color directly below in the input grid: `I_bel1 = input[r+1, c]` (treat out-of-bounds as `BACKGROUND_COLOR`).
        ii. If `I_bel1` is a `CONTENT_COLOR`, set `output[r, c]` to `I_bel1`.
        iii.Otherwise (if `I_bel1` is `FRAME_COLOR` or `BACKGROUND_COLOR`), set `output[r, c]` to `BACKGROUND_COLOR`.
    d.  **Content Color Cell:** If `main_frame_mask[r, c]` is false and `input[r, c]` is a `CONTENT_COLOR` (let's call it `C`):
        i.  Check if this cell is the **top** of a vertical stack of identical colors `C`. It is the top if `r` is 0 or if `input[r-1, c]` is not equal to `C`.
        ii. If it *is* the top of the stack, set `output[r, c]` to `C`.
        iii.If it is *not* the top of the stack (meaning `input[r-1, c]` is also `C`):
            1.  Find the height `h` (where `h >= 1`) of the continuous stack of color `C` starting from `(r, c)` downwards. (i.e., `input[r+i, c] == C` for `0 <= i < h` and `input[r+h, c] != C`).
            2.  Determine the terminating color `T = input[r+h, c]` (treat out-of-bounds as `BACKGROUND_COLOR`).
            3.  If the `terminating_color` `T` is `BACKGROUND_COLOR` or `FRAME_COLOR`, set `output[r, c]` to `FRAME_COLOR`.
            4.  Otherwise (if `T` is a `CONTENT_COLOR`), set `output[r, c]` to `C`.
5.  **Return Output:** The fully populated output grid is the result.