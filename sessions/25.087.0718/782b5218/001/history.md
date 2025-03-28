
## train_1

**input:**
```
5 5 5 0 5 0 0 0 5 5
5 0 0 5 5 0 5 0 5 5
0 5 5 0 5 5 0 5 0 0
2 0 5 5 2 0 5 0 2 5
5 2 0 2 0 2 0 2 0 2
0 0 2 5 5 5 2 0 5 0
5 5 0 0 0 5 5 5 5 5
0 5 0 5 5 0 5 0 5 5
0 5 5 0 5 0 5 0 5 5
5 5 0 0 5 5 5 5 5 5
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 0 0 0 2 0 0 0 2 0
5 2 0 2 5 2 0 2 5 2
5 5 2 5 5 5 2 5 5 5
5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5
5 5 5 5 5 5 5 5 5 5
```


## train_2

**input:**
```
1 0 1 1 1 1 1 1 1 0
0 0 1 0 1 1 0 1 0 1
1 1 0 0 1 1 1 1 1 0
2 2 2 2 2 2 2 2 2 2
0 0 1 1 0 0 0 0 0 0
1 1 0 1 0 0 0 0 1 0
0 1 1 1 0 1 1 0 1 0
1 1 0 0 0 1 0 0 1 0
0 0 1 0 0 0 1 1 0 0
0 1 1 1 0 1 1 0 0 1
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0
2 2 2 2 2 2 2 2 2 2
1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1
```


## train_3

**input:**
```
0 8 8 0 8 0 8 8 0 0
2 0 8 8 0 8 0 0 0 8
2 2 8 0 0 0 0 0 0 0
0 2 2 0 8 0 0 0 0 0
8 8 2 2 0 0 0 8 8 0
8 8 8 2 2 8 0 0 0 0
0 0 0 0 2 2 8 8 8 0
8 0 8 0 0 2 2 8 8 8
8 8 0 0 0 0 2 2 8 0
0 8 0 8 0 8 8 2 2 8
```


**output:**
```
0 0 0 0 0 0 0 0 0 0
2 0 0 0 0 0 0 0 0 0
2 2 0 0 0 0 0 0 0 0
8 2 2 0 0 0 0 0 0 0
8 8 2 2 0 0 0 0 0 0
8 8 8 2 2 0 0 0 0 0
8 8 8 8 2 2 0 0 0 0
8 8 8 8 8 2 2 0 0 0
8 8 8 8 8 8 2 2 0 0
8 8 8 8 8 8 8 2 2 0
```

Okay, let's analyze the provided examples to understand the transformation logic.

**Perception**

1.  **Example 1 Analysis:** The input contains white (0), red (2), and gray (5) pixels. The output preserves the red (2) pixels and the gray (5) pixels located at or below the highest red pixel in each column. All pixels *above* the highest red pixel in any given column (including white and gray pixels) are changed to white (0). This suggests a column-specific filtering process based on the vertical position of the red pixels.

2.  **Example 2 Analysis:** The input contains white (0), blue (1), and red (2) pixels. A distinct feature is row 3, composed entirely of red (2) pixels. In the output, this red row is preserved. All rows above it (0-2) are changed to white (0). All rows below it (4-9) are changed to blue (1). This indicates a global transformation based on a horizontal separator line. The colors above and below the separator are determined by the background color (white) and the third color present (blue).

3.  **Example 3 Analysis:** The input contains white (0), red (2), and azure (8) pixels. The output displays a fixed diagonal pattern. A band, two pixels thick diagonally, is colored red (2). The area below this band is filled with azure (8), and the area above is filled with white (0). The specific locations of the input red and azure pixels do not seem to directly map to the output positions, but rather the *presence* of red (2) and azure (8) alongside the background white (0) determines the colors used in the fixed output pattern.

4.  **Synthesis:** The task appears to involve identifying a key color (red=2 in all examples) and potentially a third color. Based on the *configuration* of the key color (scattered, solid row) or the *number* of distinct colors, a specific transformation rule is applied:
    *   **Rule 1 (Solid Row):** If a solid horizontal row of the key color exists, it acts as a separator. Above becomes background, below becomes the third color, the separator row is preserved. (Example 2)
    *   **Rule 2 (Three Colors, Fixed Pattern):** If no solid row exists, but exactly three colors are present (background, key color, third color), a fixed diagonal pattern is generated using these three colors. (Example 3)
    *   **Rule 3 (Column Filter):** If neither of the above applies (e.g., three colors present but not matching Rule 2 pattern, or only two colors present), apply a column-wise filter: find the highest occurrence of the key color in each column and change everything above it to the background color. (Example 1)

**Facts**


```yaml
task_elements:
  - name: grid
    type: 2D array of integers (pixels)
    properties:
      - height: variable (1-30)
      - width: variable (1-30)
      - pixels: integer values 0-9 representing colors
  - name: colors
    type: set of integers present in the grid
    properties:
      - background_color: typically 0 (white)
      - key_color: a specific non-background color triggering transformations (e.g., 2 (red))
      - third_color: another non-background color used in some rules (e.g., 1 (blue), 5 (gray), 8 (azure))
  - name: structures
    type: patterns or arrangements of pixels
    properties:
      - solid_horizontal_row: a row composed entirely of the key_color
      - column_highest_key_pixel: the uppermost pixel of the key_color within a column
      - fixed_diagonal_band: a specific geometric pattern used in Rule 2

relationships:
  - description: The transformation rule depends on the configuration of the key_color and the number/identity of colors present.
  - condition: Presence of a solid_horizontal_row of the key_color.
    action: Apply Rule 1 (Row Separation).
  - condition: Absence of solid_horizontal_row AND presence of exactly three distinct colors (background, key, third).
    action: Apply Rule 2 (Fixed Diagonal Pattern Construction).
  - condition: Absence of conditions for Rule 1 and Rule 2.
    action: Apply Rule 3 (Column Filtering based on key_color).

actions:
  - name: identify_colors
    description: Find unique colors, identify background, key, and third colors.
  - name: detect_solid_row
    description: Check if any row consists solely of the key_color.
  - name: apply_row_separation
    description: Modify grid based on the solid row separator (Rule 1). Fill above with background, below with third color, keep separator.
  - name: apply_fixed_pattern
    description: Construct output grid using the fixed diagonal band pattern (Rule 2) with key_color, third_color, and background_color.
  - name: apply_column_filter
    description: Modify grid column by column (Rule 3). Find highest key_color pixel, set pixels above to background.
```


**Natural Language Program**

1.  **Analyze Input:** Identify all unique colors present in the input grid. Assume white (0) is the background color. Identify red (2) as the potential `key_color`. If a third distinct color exists, identify it as the `third_color`.
2.  **Check for Solid Key Color Row:** Iterate through each row of the input grid. If a row is found consisting entirely of the `key_color` (red=2):
    a.  Create a new output grid of the same dimensions.
    b.  Copy the solid `key_color` row to the corresponding row in the output grid.
    c.  Fill all rows in the output grid *above* the solid row with the background color (white=0).
    d.  Fill all rows in the output grid *below* the solid row with the `third_color` identified in step 1.
    e.  Return the output grid.
3.  **Check for Three Colors & Fixed Pattern Rule:** If no solid `key_color` row was found, check if exactly three distinct colors were identified in step 1 (background, `key_color`, `third_color`).
    a.  If yes: Create a new output grid of the same dimensions.
    b.  For each cell `(row, col)` in the output grid:
        i.  If `row == col + 1` or `row == col + 2` (within grid bounds), set the cell value to the `key_color` (red=2).
        ii. Else if `row > col + 2` (within grid bounds), set the cell value to the `third_color`.
        iii. Else (`row < col + 1`), set the cell value to the background color (white=0).
    c.  Return the output grid.
4.  **Apply Column Filter Rule:** If neither of the above conditions was met:
    a.  Create a new output grid, initially as a copy of the input grid.
    b.  For each column `col` from 0 to width-1:
        i.  Find the smallest row index `min_row` such that the input grid cell `(min_row, col)` contains the `key_color` (red=2).
        ii. If such a `min_row` exists (i.e., the `key_color` is present in the column):
            *   Iterate through rows `r` from 0 to `min_row - 1`.
            *   Set the output grid cell `(r, col)` to the background color (white=0).
        iii. If no `key_color` exists in the column, the column in the output grid remains unchanged from the input.
    c.  Return the output grid.
