
## train_1

**input:**
```
4 0 4 0 4 0 4 0 4 0 4 0 4
4 4 4 4 4 4 4 4 4 4 4 4 4
0 4 0 4 0 4 0 4 0 4 0 4 0
```


**output:**
```
6 0 4 0 4 0 6 0 4 0 4 0 6
6 4 4 6 4 4 6 4 4 6 4 4 6
0 4 0 6 0 4 0 4 0 6 0 4 0
```


## train_2

**input:**
```
0 4 0 4 0 4 0 4 0 4 0
4 4 4 4 4 4 4 4 4 4 4
4 0 4 0 4 0 4 0 4 0 4
```


**output:**
```
0 4 0 6 0 4 0 4 0 6 0
6 4 4 6 4 4 6 4 4 6 4
6 0 4 0 4 0 6 0 4 0 4
```


## train_3

**input:**
```
4 0 4 0 4 0 4 0 4 0 4
4 4 4 4 4 4 4 4 4 4 4
0 4 0 4 0 4 0 4 0 4 0
```


**output:**
```
6 0 4 0 4 0 6 0 4 0 4
6 4 4 6 4 4 6 4 4 6 4
0 4 0 6 0 4 0 4 0 6 0
```


## train_4

**input:**
```
0 4 0 4 0 4 0 4 0 4 0 4 0 4
4 4 4 4 4 4 4 4 4 4 4 4 4 4
4 0 4 0 4 0 4 0 4 0 4 0 4 0
```


**output:**
```
0 4 0 6 0 4 0 4 0 6 0 4 0 4
6 4 4 6 4 4 6 4 4 6 4 4 6 4
6 0 4 0 4 0 6 0 4 0 4 0 6 0
```


## train_5

**input:**
```
4 0 4 0 4 0 4 0 4 0
4 4 4 4 4 4 4 4 4 4
0 4 0 4 0 4 0 4 0 4
```


**output:**
```
6 0 4 0 4 0 6 0 4 0
6 4 4 6 4 4 6 4 4 6
0 4 0 6 0 4 0 4 0 6
```

*   **Perception**: The input grids are always 3 rows high and vary in width. They consist primarily of yellow (4) and white (0) pixels. Row 1 is consistently all yellow. Rows 0 and 2 display an alternating pattern, starting either with yellow-white or white-yellow. The output grids maintain the same dimensions and the white pixels remain unchanged. The transformation involves changing specific yellow (4) pixels to magenta (6). The positions where these changes occur follow a distinct pattern based on the row index and the initial configuration of rows 0 and 2.

*   **Facts**:
    
```yaml
    task_type: color_change
    grid_properties:
      - height: 3 (constant)
      - width: variable
      - colors_present_input: [white (0), yellow (4)]
      - colors_present_output: [white (0), yellow (4), magenta (6)]
    objects:
      - type: grid_pixels
        properties:
          - color: white (0)
          - color: yellow (4)
      - type: structure
        description: A connected structure formed by yellow pixels, resembling a fence with posts and a rail. Row 1 is the rail, rows 0 and 2 have alternating pixels forming posts.
    relationships:
      - white (0) pixels are static; they do not change.
      - yellow (4) pixels are potentially dynamic; some change to magenta (6).
    actions:
      - identify_pattern: Determine if row 0 starts with yellow (4) and row 2 starts with white (0), OR if row 0 starts with white (0) and row 2 starts with yellow (4).
      - conditional_color_change: Based on the identified pattern, change specific yellow (4) pixels to magenta (6) according to rules based on row and column index.
    transformation_rules:
      - rule_for_row_1: Yellow (4) pixels at column `col` change to magenta (6) if `col` is a multiple of 3. This rule applies regardless of the starting pattern.
      - rule_for_row_0_and_2: The rule depends on the starting pattern:
          - Pattern A (Row 0 starts yellow, Row 2 starts white):
              - Row 0: Yellow (4) changes to magenta (6) if `col` is a multiple of 6.
              - Row 2: Yellow (4) changes to magenta (6) if `col - 3` is a non-negative multiple of 6.
          - Pattern B (Row 0 starts white, Row 2 starts yellow):
              - Row 0: Yellow (4) changes to magenta (6) if `col - 3` is a non-negative multiple of 6.
              - Row 2: Yellow (4) changes to magenta (6) if `col` is a multiple of 6.
    ```


*   **Natural Language Program**:
    1.  Initialize the output grid as a copy of the input grid.
    2.  Check the color of the pixel at `(0, 0)` in the input grid.
    3.  **If** the pixel at `(0, 0)` is yellow (4) (Pattern A):
        *   Iterate through each column `col` from 0 to width-1.
        *   If the pixel at `(0, col)` is yellow (4) AND `col` is divisible by 6, change the corresponding pixel in the output grid to magenta (6).
        *   If the pixel at `(1, col)` is yellow (4) AND `col` is divisible by 3, change the corresponding pixel in the output grid to magenta (6).
        *   If the pixel at `(2, col)` is yellow (4) AND `col >= 3` AND `(col - 3)` is divisible by 6, change the corresponding pixel in the output grid to magenta (6).
    4.  **Else** (the pixel at `(0, 0)` must be white (0), implying Pattern B):
        *   Iterate through each column `col` from 0 to width-1.
        *   If the pixel at `(0, col)` is yellow (4) AND `col >= 3` AND `(col - 3)` is divisible by 6, change the corresponding pixel in the output grid to magenta (6).
        *   If the pixel at `(1, col)` is yellow (4) AND `col` is divisible by 3, change the corresponding pixel in the output grid to magenta (6).
        *   If the pixel at `(2, col)` is yellow (4) AND `col` is divisible by 6, change the corresponding pixel in the output grid to magenta (6).
    5.  Return the modified output grid.
