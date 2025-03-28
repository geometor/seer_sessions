
## train_1

**input:**
```
2 2 2 2 2 0 0 0 0 0 2 2
2 2 2 2 2 0 0 0 0 0 2 2
2 2 2 2 2 0 0 0 0 0 2 2
2 2 2 2 2 0 0 0 0 0 2 2
2 2 2 2 2 0 0 0 0 0 2 2
2 2 2 2 2 2 2 2 2 2 2 2
2 4 4 4 1 4 2 2 2 2 2 2
2 4 4 1 4 4 2 2 2 2 2 2
2 4 1 4 1 1 2 2 2 2 2 2
2 4 4 1 4 1 2 2 2 2 2 2
2 4 4 4 4 4 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2
```


**output:**
```
2 2 2 2 2 4 1 4 4 4 2 2
2 2 2 2 2 4 4 1 4 4 2 2
2 2 2 2 2 1 1 4 1 4 2 2
2 2 2 2 2 1 4 1 4 4 2 2
2 2 2 2 2 4 4 4 4 4 2 2
2 2 2 2 2 2 2 2 2 2 2 2
2 4 4 4 1 4 2 2 2 2 2 2
2 4 4 1 4 4 2 2 2 2 2 2
2 4 1 4 1 1 2 2 2 2 2 2
2 4 4 1 4 1 2 2 2 2 2 2
2 4 4 4 4 4 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2
```


## train_2

**input:**
```
2 2 2 2 2 2 2 2 2 2 2 2
2 1 3 3 1 2 2 2 2 2 2 2
2 1 1 3 1 2 2 2 2 2 2 2
2 1 3 3 3 2 2 2 2 2 2 2
2 1 1 1 1 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 0 0 0 0 2 2 2 2
2 2 2 2 0 0 0 0 2 2 2 2
2 2 2 2 0 0 0 0 2 2 2 2
2 2 2 2 0 0 0 0 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2
```


**output:**
```
2 2 2 2 2 2 2 2 2 2 2 2
2 1 3 3 1 2 2 2 2 2 2 2
2 1 1 3 1 2 2 2 2 2 2 2
2 1 3 3 3 2 2 2 2 2 2 2
2 1 1 1 1 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2
2 2 2 2 1 3 3 1 2 2 2 2
2 2 2 2 1 3 1 1 2 2 2 2
2 2 2 2 3 3 3 1 2 2 2 2
2 2 2 2 1 1 1 1 2 2 2 2
2 2 2 2 2 2 2 2 2 2 2 2
```


## train_3

**input:**
```
1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
1 3 3 3 3 3 3 1 1 1 1 1
1 3 3 3 2 3 3 1 1 1 1 1
1 2 2 2 3 2 3 1 1 1 1 1
1 3 3 3 2 3 3 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 0 0 0 0 0 0 1 1 1
1 1 1 0 0 0 0 0 0 1 1 1
1 1 1 0 0 0 0 0 0 1 1 1
1 1 1 0 0 0 0 0 0 1 1 1
```


**output:**
```
1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
1 3 3 3 3 3 3 1 1 1 1 1
1 3 3 3 2 3 3 1 1 1 1 1
1 2 2 2 3 2 3 1 1 1 1 1
1 3 3 3 2 3 3 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 3 3 3 3 3 3 1 1 1
1 1 1 3 3 2 3 3 3 1 1 1
1 1 1 3 2 3 2 2 2 1 1 1
1 1 1 3 3 2 3 3 3 1 1 1
```

Okay, let's analyze the task examples.

**Perception**

1.  **Grid Structure:** Each input grid contains distinct regions. There's a large background area filled with a single color (Red in train_1 and train_2, Blue in train_3).
2.  **Key Objects:**
    *   **White Block (Color 0):** A rectangular block composed entirely of white pixels. Its size and position vary between examples.
    *   **Pattern Block:** Another rectangular block of the *same dimensions* as the White Block, located elsewhere in the grid. This block contains a pattern made of colors other than white and the main background color.
3.  **Transformation:** The core operation appears to be a "copy-paste". The pixel pattern within the Pattern Block is copied directly onto the location of the White Block in the output grid.
4.  **Invariance:** The rest of the grid, including the background and the original Pattern Block, remains unchanged in the output.
5.  **Relationship:** The White Block acts as a target or destination area, and the Pattern Block acts as the source of the pixel data to fill that area. The dimensions of these two blocks must match for the operation to be defined as observed.

**Facts**


```yaml
- task: Identify and replace a block of white pixels.
- objects:
    - name: background
      property: Most frequent color in the grid, excluding white (0). Remains unchanged.
    - name: white_block
      property: A contiguous rectangular block of white (0) pixels.
      property: Acts as the destination area for the transformation.
      property: Its dimensions (height, width) are important.
    - name: pattern_block
      property: A contiguous rectangular block containing pixels that are not white (0) and not the background color.
      property: Has the exact same dimensions (height, width) as the white_block.
      property: Acts as the source of the pattern to be copied.
      property: Its original location remains unchanged in the output.
- transformation:
    - action: find_bounding_box
      input: input_grid
      target: white_block
      output: white_bbox (top_row, left_col, height, width)
    - action: find_matching_block
      input: input_grid
      criteria:
        - dimensions must match white_bbox (height, width)
        - must not contain white (0) pixels
        - must not contain only background pixels
        - must be distinct from the white_block's location
      output: pattern_bbox (top_row, left_col, height, width)
    - action: copy_paste
      source_grid: input_grid
      source_bbox: pattern_bbox
      destination_grid: output_grid (initially a copy of input_grid)
      destination_bbox: white_bbox
      details: For each relative offset (dr, dc) from 0 to height-1 and 0 to width-1, the pixel at (white_bbox.top_row + dr, white_bbox.left_col + dc) in the output_grid is set to the value of the pixel at (pattern_bbox.top_row + dr, pattern_bbox.left_col + dc) in the input_grid.
```


**Natural Language Program**

1.  Identify the rectangular block composed entirely of white pixels (color 0). Record its top-left corner coordinates, height, and width.
2.  Scan the input grid to find another rectangular block that has the *exact same height and width* as the white block identified in step 1. This second block (the pattern block) must contain colors other than white (0) and potentially different from the grid's main background color. Record its top-left corner coordinates.
3.  Create a copy of the input grid to serve as the basis for the output grid.
4.  For each position within the bounds of the white block (using its recorded height and width):
    a.  Calculate the corresponding position within the pattern block using the same relative offset from their respective top-left corners.
    b.  Read the color value from the calculated position within the pattern block in the *original input grid*.
    c.  Write this color value to the corresponding position within the white block's area in the *copied grid*.
5.  The modified copied grid is the final output.
