
## train_1

**input:**
```
1 1 0 0 0 0 0 0 0 1 0 0 1 0 0 1 0 1 0 1
0 1 0 0 0 0 0 1 1 1 1 0 0 1 1 0 0 0 0 0
```


**output:**
```
1 1 6 6 6 6 6 0 0 1 0 0 1 0 0 1 0 1 0 1
0 1 6 6 6 6 6 1 1 1 1 0 0 1 1 0 0 0 0 0
```


## train_2

**input:**
```
1 1 1 0 0 1 1 0 1 1 1 1 0 0 0 0 0 1 0 1
1 1 1 0 1 1 0 0 1 0 1 0 1 1 0 0 0 1 1 1
0 0 1 1 1 0 0 1 0 1 0 1 1 0 1 0 1 1 1 0
0 1 0 1 0 0 0 1 1 0 1 1 1 0 0 0 1 1 1 1
```


**output:**
```
1 1 1 0 0 1 1 0 1 1 1 1 0 0 6 6 6 1 0 1
1 1 1 0 1 1 0 0 1 0 1 0 1 1 6 6 6 1 1 1
0 0 1 1 1 0 0 1 0 1 0 1 1 0 1 0 1 1 1 0
0 1 0 1 0 0 0 1 1 0 1 1 1 0 0 0 1 1 1 1
```


## train_3

**input:**
```
0 0 1 0 0 1 0 0 0 1 1 1 1 1 0 0 0 0 0 0
1 0 0 0 0 1 1 0 0 1 0 0 0 0 0 1 0 0 0 0
1 0 1 1 0 0 1 0 1 0 1 0 1 0 0 0 1 0 0 0
0 0 1 0 0 0 1 1 0 0 1 1 1 1 1 1 1 0 0 1
```


**output:**
```
0 0 1 0 0 1 0 0 0 1 1 1 1 1 0 0 0 6 6 6
1 0 0 0 0 1 1 0 0 1 0 0 0 0 0 1 0 6 6 6
1 0 1 1 0 0 1 0 1 0 1 0 1 0 0 0 1 6 6 6
0 0 1 0 0 0 1 1 0 0 1 1 1 1 1 1 1 0 0 1
```


## train_4

**input:**
```
5 1 1 1 1 1 5 0 0 0 0 0 0 0 0 0 0 1 1 0 1 0 0 1 0 0 0 0 1 0
0 1 0 1 0 0 0 1 1 1 1 0 1 1 1 0 0 0 0 1 1 1 0 1 0 1 1 1 1 1
1 1 0 0 0 1 0 1 0 1 1 1 0 1 1 0 0 0 0 1 0 0 1 1 0 0 1 0 0 0
```


**output:**
```
5 1 1 1 1 1 5 0 0 0 0 0 0 0 0 0 0 1 1 0 1 0 0 1 0 0 0 0 1 0
0 1 0 1 0 0 0 1 1 1 1 0 1 1 1 6 6 6 6 1 1 1 0 1 0 1 1 1 1 1
1 1 0 0 0 1 0 1 0 1 1 1 0 1 1 6 6 6 6 1 0 0 1 1 0 0 1 0 0 0
```

*   **Perception**:
    *   The task involves transforming input grids containing primarily white (0) and blue (1) pixels, although other colors like gray (5) can appear but seem incidental to the core logic.
    *   The output grids are identical to the input grids, except that a specific rectangular region composed entirely of white pixels in the input has been recolored to magenta (6) in the output.
    *   The key challenge is to identify the criteria used to select *which* white rectangular block is filled.
    *   By analyzing the dimensions and positions of the filled blocks across examples, a pattern emerges: the selected block is the one with the greatest height among all possible rectangular blocks consisting solely of white pixels.
    *   If multiple white blocks share the maximum height, the one with the largest area (width * height) is chosen.
    *   Further tie-breaking (e.g., top-most, then left-most) might be necessary in general, although not explicitly required by these specific examples.

*   **Facts**:
    
```yaml
    task_type: transformation
    grid_properties:
      - dimensions: variable height and width (up to 30x30)
      - involved_colors: white (0), blue (1), magenta (6), gray (5)
    objects:
      - type: rectangular_block
        properties:
          - color: white (0)
          - contiguous: yes
          - dimensions: height, width
          - area: height * width
          - position: top-left corner (row, column)
    transformation:
      - action: find_all
        target: rectangular_blocks
        condition: color is white (0)
      - action: identify_criteria
        criteria:
          - primary: maximum height
          - secondary: maximum area (if tie in height)
          - tertiary (tie-breaking): top-most (min row index), then left-most (min column index)
      - action: select_one
        target: rectangular_block (matching criteria)
      - action: fill_color
        target: selected rectangular_block
        new_color: magenta (6)
      - action: keep_unchanged
        target: all other pixels
    ```


*   **Natural Language Program**:
    1.  Identify all possible rectangular blocks within the input grid that are composed entirely of white (0) pixels. Record their height, width, area (height * width), and the coordinates (row, column) of their top-left corner.
    2.  Find the maximum height among all identified white rectangular blocks.
    3.  Filter the list of white blocks to keep only those that have this maximum height.
    4.  From this filtered list, find the maximum area.
    5.  Filter the list again to keep only those blocks that have both the maximum height and the maximum area.
    6.  If more than one block remains, select the one whose top-left corner has the smallest row index (top-most).
    7.  If more than one block still remains (i.e., they are in the same top row), select the one whose top-left corner has the smallest column index (left-most). There should now be only one uniquely selected block.
    8.  Create the output grid by copying the input grid.
    9.  Recolor all the pixels within the bounds of the selected rectangular block to magenta (6) in the output grid.
