
## train_1

**input:**
```
4 2 4 4 6 4 5 5
2 4 4 4 6 4 4 5
4 2 4 4 6 4 5 5
2 4 4 6 4 4 4 5
4 2 4 6 4 4 5 5
2 4 4 6 4 4 4 5
4 2 4 6 4 4 5 5
2 4 4 4 6 4 4 5
4 2 4 4 6 4 5 5
2 4 4 4 6 4 4 5
```


**output:**
```
6 2 4 5 6 4 5 5
2 6 4 5 6 4 2 5
6 2 4 5 6 4 5 5
2 6 4 6 5 4 2 5
6 2 4 6 5 4 5 5
2 6 4 6 5 4 2 5
6 2 4 6 5 4 5 5
2 6 4 5 6 4 2 5
6 2 4 5 6 4 5 5
2 6 4 5 6 4 2 5
```


## train_2

**input:**
```
0 0 0 0 0 0 0 9
4 0 0 0 3 0 9 0
0 4 0 0 0 0 0 9
0 0 4 0 3 0 0 9
0 4 0 0 0 0 9 0
4 0 0 0 3 0 0 9
0 4 0 0 0 0 0 9
0 0 4 0 3 0 9 0
0 4 0 0 0 0 0 9
4 0 0 0 3 0 0 9
```


**output:**
```
3 3 3 0 9 0 4 9
4 3 3 0 3 0 9 4
3 4 3 0 9 0 4 9
3 3 4 0 3 0 4 9
3 4 3 0 9 0 9 4
4 3 3 0 3 0 4 9
3 4 3 0 9 0 4 9
3 3 4 0 3 0 9 4
3 4 3 0 9 0 4 9
4 3 3 0 3 0 4 9
```

**Perception**

The task requires transforming an input grid of colored pixels into an output grid of the same dimensions. Analyzing the two examples provided (`train_1` and `train_2`) reveals a consistent transformation mechanism:
1.  **Local Transformation:** The color of each pixel in the output grid is determined solely by the color of the corresponding pixel in the input grid and the colors of its immediate orthogonal neighbors (up, down, left, right) in the input grid.
2.  **Conditional Rules:** The transformation follows a set of specific, prioritized rules. Each rule checks if the central input pixel has a certain color and if one of its neighbors (in a specific position or any position) has another specific color.
3.  **Pixel Replacement:** If a rule's conditions are met, the output pixel takes on a new color specified by that rule. If multiple rules could apply to a pixel, a specific precedence order is followed (the first matching rule in the order determines the output).
4.  **Default Identity:** If no specific rule applies to an input pixel, its color remains unchanged in the output grid.
5.  **Context-Specific Rules:** While the *mechanism* of transformation (neighbor-based conditional replacement) is consistent across examples, the *specific* rules (which colors interact, what the resulting colors are, and the precedence) differ between `train_1` and `train_2`. This suggests the exact rules might be inferred from the context or patterns within each specific input grid, although the examples provided don't make the inference method explicit.

    *   In `train_1`, only Yellow (4) pixels change, influenced by neighboring Gray (5), Red (2), or Magenta (6).
    *   In `train_2`, White (0) pixels change if near Yellow (4), and Maroon (9) pixels change if to the right of Green (3).

**Facts**


```yaml
Transformation Type: Local Pixel Replacement
Grid Properties:
  - Input and Output grids have identical dimensions.
  - The set of colors used might be preserved or slightly altered depending on replacement rules.
Pixel Operation:
  - Iterate through each pixel (cell) of the input grid.
  - For each pixel, examine its color and the colors of its orthogonal neighbors (Top, Bottom, Left, Right).
Rule Application:
  - A set of conditional rules determines the output color.
  - Rule Format: IF InputPixelColor == X AND NeighborColorAtPositionP == Y THEN OutputPixelColor = Z
  - Neighbor Positions (P): Can be specific (e.g., Left, Top) or general (e.g., Any orthogonal).
  - Precedence: Rules are applied in a specific order. The first rule that matches determines the output color.
Default Behavior:
  - If no rule matches a given input pixel and its neighbors, the output pixel retains the input pixel's color.
Context Dependence:
  - The specific set of rules (X, Y, P -> Z) varies between the provided examples (`train_1` and `train_2`), indicating the rules are likely dependent on the input context.
```


**Natural Language Program**

1.  Initialize an output grid with the same dimensions as the input grid.
2.  For each pixel at position (row, column) in the input grid:
    a.  Get the color of the input pixel `C_in = Input[row, col]`.
    b.  Get the colors of its orthogonal neighbors in the input grid (handling boundary conditions where neighbors might not exist): `N_top`, `N_bottom`, `N_left`, `N_right`.
    c.  Check `C_in` and neighbor colors against a prioritized list of transformation rules specific to the task context.
        *   **Rule Format Example (derived from observations):**
            *   `IF C_in == ColorA AND NeighborCondition(ColorB, Position) THEN OutputColor = ColorC`
    d.  Apply the *first* rule in the list whose conditions are met. Set the corresponding output pixel `Output[row, col]` to the color specified by that rule.
    e.  If no rule's conditions are met, set the output pixel `Output[row, col]` to the original input color `C_in`.
3.  Return the completed output grid.
