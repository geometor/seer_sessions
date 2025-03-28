
## train_1

**input:**
```
0 0 0 0 0
0 0 0 0 0
0 0 0 0 0
8 8 0 8 8
0 8 0 8 0
```


**output:**
```
0 8 0 8 0
8 8 0 8 8
0 0 0 0 0
8 8 0 8 8
0 8 0 8 0
```


## train_2

**input:**
```
0 0 0 0 2 0 2 0 2 2 0
0 0 0 0 2 2 2 0 2 2 2
0 0 0 0 2 2 2 0 2 2 2
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 0 0 0 0
0 0 0 0 2 0 2 0 0 0 0
0 0 0 0 2 2 2 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 2 2 2 0 2 2 2
0 0 0 0 2 2 2 0 2 2 2
0 0 0 0 2 0 2 0 2 2 0
```


**output:**
```
0 2 2 0 2 0 2 0 2 2 0
2 2 2 0 2 2 2 0 2 2 2
2 2 2 0 2 2 2 0 2 2 2
0 0 0 0 0 0 0 0 0 0 0
2 2 2 0 2 2 2 0 2 2 2
0 2 2 0 2 0 2 0 2 2 0
2 2 2 0 2 2 2 0 2 2 2
0 0 0 0 0 0 0 0 0 0 0
2 2 2 0 2 2 2 0 2 2 2
2 2 2 0 2 2 2 0 2 2 2
0 2 2 0 2 0 2 0 2 2 0
```

Okay, analyzing the provided examples:

**Perception**

1.  **Grid Structure:** Both examples involve grids containing a background color (white/0) and one other color forming distinct shapes or patterns (azure/8 in the first, red/2 in the second).
2.  **Input Pattern Location:** In both inputs, the salient non-background patterns are concentrated towards the bottom rows of the grid.
3.  **Output Pattern Location:** In the outputs, a pattern similar to the one at the bottom of the input appears at the very top rows. The original pattern also remains at the bottom.
4.  **Transformation:** The core transformation seems to involve identifying a specific block of rows at the bottom of the input, modifying it, and copying it to the top of the output grid.
5.  **Modification Detail:** Comparing the bottom input pattern rows with the top output pattern rows reveals that the *order* of the rows within the pattern block is vertically reversed during the copy process.
6.  **Row Preservation:** Rows in the input grid that are *not* part of the identified bottom pattern block appear unchanged in the output grid, maintaining their original row indices relative to the bottom of the grid (or, more precisely, shifted down by the height of the inserted block if you think from the top). However, it's simpler to think of the output as the input grid with its top rows overwritten by the transformed pattern.
7.  **Block Identification:** The pattern block seems to be defined as the contiguous set of rows from the bottom-most row containing a non-background pixel upwards to the top-most row of that connected bottom group.

**Facts**


```yaml
task_context:
  grid_properties:
    - dimensions_preserved: True # Input and Output grids have the same height and width.
    - colors_preserved: True # The set of colors used remains the same.
  background_color:
    - typical_value: 0 # White is the background in examples.
    - identification: Assumed to be the most frequent color.
objects:
  - object: pattern_block
    description: A contiguous block of rows located at the bottom of the input grid.
    properties:
      - contains_non_background_pixels: True
      - vertical_extent: Defined by the lowest and highest row indices within this bottom group that contain non-background pixels.
      - content: The specific pixel values within these rows.
actions:
  - action: identify_pattern_block
    input: input_grid
    output: pattern_block (including its rows and height H)
    logic: Find the lowest row index (max_row) containing a non-background pixel. Find the highest row index (min_row_of_block) such that all rows from min_row_of_block to max_row contain at least one non-background pixel OR are part of the connected structure starting from the bottom. A simpler definition might be: Find the index of the bottom-most non-background row (`last_row`). Find the index of the top-most non-background row (`first_row`). The block potentially spans `first_row` to `last_row`. However, looking at example 2, rows 3 and 7 are all background, separating patterns. The relevant block is only the *lowest* group. Revised Logic: Iterate rows from bottom to top. Identify the first row with non-background pixels (this is the bottom of the block). Continue iterating upwards as long as rows contain non-background pixels. The last such row marks the top of the block. Or even better: Find all rows containing non-background pixels. Identify the maximum row index (`max_r`). Find the minimum row index (`min_r_block`) such that `min_r_block` contains non-background pixels, and all rows between `min_r_block` and `max_r` (inclusive) form the lowest connected vertical block containing non-background elements. Let's simplify: Find the lowest row `R_bottom` with non-background pixels. Find the highest row `R_top` such that all rows between `R_top` and `R_bottom` (inclusive) define the lowest contiguous block containing non-background pixels.
     refinement: Start from the last row. Find the index of the last row containing any non-background color (`bottom_row_idx`). Find the index of the first row, searching from `bottom_row_idx` upwards, such that this row contains any non-background color, and all rows below it down to `bottom_row_idx` also contained non-background colors (This definition is still tricky because of separating background rows like row 7 in train_2).
    final_refinement: Find the index of the bottom-most row containing any non-background pixel (`max_row_idx`). Identify all row indices `r <= max_row_idx` that contain non-background pixels. Find the minimum row index (`min_row_idx`) among these. The pattern block consists of all rows from `min_row_idx` to `max_row_idx`, inclusive. Let H be `max_row_idx - min_row_idx + 1`.
  - action: extract_rows
    input: input_grid, pattern_block definition (min_row_idx, max_row_idx)
    output: list_of_rows (representing the pattern)
  - action: reverse_rows
    input: list_of_rows
    output: reversed_list_of_rows
  - action: create_output_grid
    input: input_grid, reversed_list_of_rows, H
    output: output_grid
    logic: Initialize output_grid as a copy of input_grid. Overwrite the top H rows (index 0 to H-1) of the output_grid with the rows from reversed_list_of_rows.
relationships:
  - relation: vertical_reversal
    source: rows in identified pattern_block (from input)
    target: rows placed at the top of the output grid
  - relation: preservation
    source: rows in input_grid outside the identified pattern_block range [min_row_idx, max_row_idx]
    target: corresponding rows in output_grid (below row H-1)
```


**Natural Language Program**

1.  Create a copy of the input grid; this will become the output grid.
2.  Determine the background color, assuming it's the most frequent color in the input grid.
3.  Identify all rows in the input grid that contain at least one pixel of a non-background color.
4.  Find the maximum index (`max_row_idx`) among these rows. This defines the bottom of the source pattern block.
5.  Find the minimum index (`min_row_idx`) among these rows *that belong to the lowest vertically contiguous group containing non-background pixels*. (Simpler approach from YAML refinement): Find the index of the bottom-most row with non-background color (`max_row_idx`). Find the index of the top-most row with non-background color (`min_row_idx_overall`). The block consists of all rows from `min_row_idx_overall` to `max_row_idx`. Calculate the height `H = max_row_idx - min_row_idx_overall + 1`.
6.  Extract the sequence of rows from the input grid, starting from `min_row_idx_overall` up to and including `max_row_idx`.
7.  Reverse the order of this sequence of rows.
8.  Replace the top `H` rows (from index 0 to `H-1`) of the output grid with the reversed sequence of rows obtained in the previous step.
9.  The rows in the output grid from index `H` downwards remain unchanged from the input grid copy.
10. Return the modified output grid.
