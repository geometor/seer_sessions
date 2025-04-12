
## train_1

**input:**
```
0 3 3 0 3 3 0 3 3 0 4 4 0
0 3 4 0 3 3 0 3 3 0 3 3 0
0 3 3 0 4 3 0 3 4 0 4 3 0
0 3 3 0 3 4 0 3 3 0 3 4 0
0 4 3 0 3 4 0 3 3 0 3 3 0
0 3 3 0 3 3 0 3 3 0 3 3 0
```


**output:**
```
0 3 3 0 3 3 0 3 3 0 4 4 0
0 3 3 0 3 4 0 3 3 0 3 3 0
0 3 4 0 3 3 0 4 3 0 4 3 0
0 3 3 0 3 3 0 3 4 0 3 4 0
0 3 3 0 4 3 0 3 4 0 3 3 0
0 3 3 0 3 3 0 3 3 0 3 3 0
```


## train_2

**input:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 0 7 7 7 0 7 7 7 0
0 6 6 6 0 7 7 7 0 7 7 7 0
0 7 7 7 0 6 6 7 0 7 7 7 0
0 7 7 7 0 7 7 7 0 7 6 7 0
0 7 7 7 0 7 7 7 0 7 7 7 0
```


**output:**
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 0 7 7 7 0 7 7 7 0
0 7 7 7 0 7 7 7 0 6 6 6 0
0 7 7 7 0 6 6 7 0 7 7 7 0
0 7 6 7 0 7 7 7 0 7 7 7 0
0 7 7 7 0 7 7 7 0 7 7 7 0
```

## Perception

1.  **Grid Structure:** Both input and output grids are the same size (6x13 for train_1, 6x13 for train_2).
2.  **Colors:** Each grid uses three colors: a background color (white/0), a 'majority' color (green/3 in train_1, orange/7 in train_2), and a 'minority' color (yellow/4 in train_1, magenta/6 in train_2).
3.  **Separators:** Vertical columns of the background color (white/0) divide the grid into distinct blocks or segments. In train_1, these are columns 0, 3, 6, 9, 12, defining 4 blocks of width 2. In train_2, these are columns 0, 4, 8, 12, defining 3 blocks of width 3.
4.  **Transformation:** The transformation modifies the colors within the blocks, keeping the background and separators unchanged. The core change involves the locations of the minority color pixels.
5.  **Train_2 Logic:** In train_2, the pattern of minority pixels (magenta/6) found in the first block (cols 1-3) is moved to the last block (cols 9-11) in the output. Conversely, the pattern of minority pixels from the last block in the input is moved to the first block in the output. The middle block (cols 5-7) remains unchanged. Pixels change color accordingly: where a minority pixel moves from, it becomes the majority color; where it moves to, the existing majority color becomes the minority color. The number and shape of minority pixel groups are conserved between the swapped blocks.
6.  **Train_1 Discrepancy:** Applying the same "swap first and last block patterns" logic to train_1 does *not* produce the provided output for train_1. The changes in train_1 are more complex and don't fit this simple swapping pattern. However, the block structure and presence of majority/minority colors are consistent features. Given the clarity of the pattern in train_2, the "swap first/last block patterns" rule seems the most likely intended logic, potentially with conditions or variations not captured by train_1 alone, or train_1 might represent a different task variation.
7.  **Core Idea:** The task likely involves identifying structural blocks separated by background color and manipulating the patterns of a specific ('minority') color within these blocks, particularly focusing on the first and last blocks.

## Facts


```yaml
task_type: object_transformation # Modifying pixels based on block structure and color patterns

grid_properties:
  size: constant across input/output for each example
  background_color: white (0) acts as a separator
  separators: vertical columns of background_color divide the grid into blocks

block_properties:
  definition: contiguous columns between separator columns
  colors: contain two non-background colors per block
    - majority_color (M): the more frequent non-background color (e.g., green/3, orange/7)
    - minority_color (m): the less frequent non-background color (e.g., yellow/4, magenta/6)
  minority_pattern: the set of relative coordinates of minority_color pixels within a block

transformation_rule (derived primarily from train_2):
  scope: affects only non-background pixels within blocks
  action: swaps the minority_pattern between the first and the last block
  target: first and last vertical blocks
  unchanged: middle blocks remain identical to input
  color_changes:
    - in_first_block:
        - original minority pixels change m -> M
        - pixels corresponding to last_block's pattern change M -> m
    - in_last_block:
        - original minority pixels change m -> M
        - pixels corresponding to first_block's pattern change M -> m
  conservation:
    - number of minority pixels is conserved globally (observed in train_2)
    - relative shape/arrangement of minority pixels is conserved during the swap (observed in train_2)

discrepancy:
  train_1_output: does not match the output predicted by the first/last block swap rule derived from train_2. The transformation in train_1 appears different or more complex.
```


## Natural Language Program

1.  **Identify Background and Separators:** Determine the background color (typically white/0). Locate all columns composed entirely of this background color; these are the vertical separators.
2.  **Define Blocks:** Identify the contiguous vertical segments of the grid located between the separator columns. These are the blocks. Record the column indices defining each block.
3.  **Handle Edge Cases:** If the number of identified blocks is less than 2, return the input grid unchanged.
4.  **Identify Colors and Patterns:**
    a.  Within each block, determine the two non-background colors present: the majority color (M) and the minority color (m). (Assume consistency across blocks for M and m within a single task example).
    b.  Determine the relative coordinates (row, column_within_block) of all pixels with the minority color (m) within the first block (B1). Store this as `Pattern_First`.
    c.  Determine the relative coordinates of all pixels with the minority color (m) within the last block (Bn). Store this as `Pattern_Last`.
5.  **Perform Swap:**
    a.  Create a copy of the input grid to serve as the output grid.
    b.  Update the first block (B1) in the output grid:
        i.  For each original minority pixel location in B1 (defined by `Pattern_First`), change its color to the majority color (M).
        ii. For each relative coordinate in `Pattern_Last`, find the corresponding absolute coordinate within B1 and change the pixel at that location to the minority color (m).
    c.  Update the last block (Bn) in the output grid:
        i.  For each original minority pixel location in Bn (defined by `Pattern_Last`), change its color to the majority color (M).
        ii. For each relative coordinate in `Pattern_First`, find the corresponding absolute coordinate within Bn and change the pixel at that location to the minority color (m).
6.  **Return Output:** Return the modified grid.
```python
import copy
import numpy as np
from collections import Counter

"""
Transformation Rule:

1. Identify vertical separator columns composed entirely of the background color (0).
2. Define blocks as the vertical segments between these separators.
3. If there are fewer than two blocks, return the input unchanged.
4. Within the first and last blocks, identify the majority (M) and minority (m) non-background colors.
5. Extract the relative coordinates (row, col_within_block) of the minority color pixels within the first block (Pattern_First).
6. Extract the relative coordinates of the minority color pixels within the last block (Pattern_Last).
7. Create a copy of the input grid.
8. Modify the first block in the copy:
    - Change pixels at original minority locations (Pattern_First) to the majority color (M).
    - Change pixels at locations corresponding to Pattern_Last to the minority color (m).
9. Modify the last block in the copy:
    - Change pixels at original minority locations (Pattern_Last) to the majority color (M).
    - Change pixels at locations corresponding to Pattern_First to the minority color (m).
10. Return the modified grid.

This rule is derived primarily from train_2 and might not perfectly match train_1.
"""

def find_separator_columns(grid: list[list[int]], background_color: int = 0) -> list[int]:
    """Finds columns composed entirely of the background color."""
    if not grid:
        return []
    height = len(grid)
    width = len(grid[0])
    separator_cols = []
    for c in range(width):
        is_separator = True
        for r in range(height):
            if grid[r][c] != background_color:
                is_separator = False
                break
        if is_separator:
            separator_cols.append(c)
    return separator_cols

def define_blocks(separator_cols: list[int], width: int) -> list[tuple[int, int]]:
    """Defines block boundaries (start_col, end_col_exclusive) based on separators."""
    blocks = []
    start_col = 0
    for sep_col in separator_cols:
        # If there's content before the separator
        if sep_col > start_col:
            blocks.append((start_col, sep_col))
        start_col = sep_col + 1
    # Check for content after the last separator
    if start_col < width:
        blocks.append((start_col, width))

    # Adjust for grids starting/ending with separators
    filtered_blocks = []
    if blocks:
        # Remove block definition starting at col 0 if col 0 is a separator
        if separator_cols and separator_cols[0] == 0 and blocks[0][0] == 0:
             pass # block implicitly starts after separator
        else:
             # Check if first block actually starts *at* col 0 if col 0 isn't separator
             first_block_start = 0
             if separator_cols and separator_cols[0] > 0:
                 first_block_start = 0 # Content before first separator
             elif not separator_cols and width > 0:
                 first_block_start = 0 # No separators, one block

        current_start = first_block_start
        for sep_col in separator_cols:
            if sep_col > current_start:
                 filtered_blocks.append((current_start, sep_col))
            current_start = sep_col + 1

        if current_start < width:
             filtered_blocks.append((current_start, width))


    return filtered_blocks


def get_block_colors(grid: list[list[int]], block_bounds: tuple[int, int], background_color: int = 0) -> tuple[int | None, int | None]:
    """Identifies the majority and minority non-background colors in a block."""
    start_col, end_col = block_bounds
    height = len(grid)
    colors = []
    for r in range(height):
        for c in range(start_col, end_col):
            if grid[r][c] != background_color:
                colors.append(grid[r][c])

    if not colors:
        return None, None # No non-background colors

    counts = Counter(colors)
    if len(counts) == 1:
        # Only one non-background color, consider it the majority
        majority_color = list(counts.keys())[0]
        minority_color = None # Or potentially the same? Task examples suggest 2 distinct colors.
                              # Let's stick to None if only one is present.
    elif len(counts) >= 2:
        # Find the two most common (or only two if exactly two)
        sorted_colors = counts.most_common()
        majority_color = sorted_colors[0][0]
        minority_color = sorted_colors[1][0]
        # Handle potential ties for minority if more than 2 colors exist - assumes minority is the second most frequent
    else: # Should not happen if colors list is not empty
         majority_color = None
         minority_color = None

    return majority_color, minority_color


def extract_minority_pattern(grid: list[list[int]], block_bounds: tuple[int, int], minority_color: int) -> list[tuple[int, int]]:
    """Extracts relative coordinates (row, col_in_block) of the minority color."""
    start_col, end_col = block_bounds
    height = len(grid)
    pattern = []
    if minority_color is None: # Handle cases where a block might not have a defined minority color
        return []
    for r in range(height):
        for c in range(start_col, end_col):
            if grid[r][c] == minority_color:
                pattern.append((r, c - start_col))
    return pattern

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Identifies blocks separated by background color columns, then swaps the
    pattern of 'minority' color pixels between the first and last blocks.
    """
    # Make a deep copy to avoid modifying the original input
    output_grid = copy.deepcopy(input_grid)
    if not input_grid or not input_grid[0]:
        return output_grid # Handle empty grid case

    height = len(input_grid)
    width = len(input_grid[0])
    background_color = 0 # Assuming white is always background

    # 1. Identify Background and Separators
    separator_cols = find_separator_columns(input_grid, background_color)

    # 2. Define Blocks
    blocks = define_blocks(separator_cols, width)

    # 3. Handle Edge Cases (fewer than 2 blocks)
    if len(blocks) < 2:
        return output_grid # Return original grid if less than 2 blocks

    # 4. Identify Colors and Patterns for first and last blocks
    first_block_bounds = blocks[0]
    last_block_bounds = blocks[-1]

    # Determine colors based on the first block (assuming consistency)
    # Need robust way if first block has only one color or is empty
    majority_color, minority_color = get_block_colors(input_grid, first_block_bounds, background_color)

    # If colors couldn't be determined (e.g., empty block), try last block
    if majority_color is None or minority_color is None:
         maj_last, min_last = get_block_colors(input_grid, last_block_bounds, background_color)
         # Prioritize using colors if found in either block
         if majority_color is None: majority_color = maj_last
         if minority_color is None: minority_color = min_last

    # If still no minority color identified (e.g., both blocks have only one color type), cannot perform swap
    if minority_color is None or majority_color is None:
         # print("Warning: Could not definitively identify majority/minority colors for swapping.")
         return output_grid # Or return original? Returning original seems safer.


    pattern_first = extract_minority_pattern(input_grid, first_block_bounds, minority_color)
    pattern_last = extract_minority_pattern(input_grid, last_block_bounds, minority_color)

    # 5. Perform Swap
    first_block_start_col = first_block_bounds[0]
    last_block_start_col = last_block_bounds[0]

    # 5.b Update the first block (B1)
    # 5.b.i Change original minority pixels to majority
    for r, c_rel in pattern_first:
        abs_c = first_block_start_col + c_rel
        if 0 <= r < height and first_block_bounds[0] <= abs_c < first_block_bounds[1]:
             # Check if the pixel was indeed minority before changing
             if output_grid[r][abs_c] == minority_color:
                 output_grid[r][abs_c] = majority_color

    # 5.b.ii Change pixels according to last block's pattern to minority
    for r, c_rel in pattern_last:
        abs_c = first_block_start_col + c_rel
        # Ensure the target pixel is within grid bounds and the first block's column range
        # Also ensure we are not overwriting background/separator pixels
        if 0 <= r < height and first_block_bounds[0] <= abs_c < first_block_bounds[1]:
            if input_grid[r][abs_c] != background_color: # Check original input grid color
                 output_grid[r][abs_c] = minority_color

    # 5.c Update the last block (Bn)
    # 5.c.i Change original minority pixels to majority
    for r, c_rel in pattern_last:
        abs_c = last_block_start_col + c_rel
        if 0 <= r < height and last_block_bounds[0] <= abs_c < last_block_bounds[1]:
            if output_grid[r][abs_c] == minority_color:
                 output_grid[r][abs_c] = majority_color

    # 5.c.ii Change pixels according to first block's pattern to minority
    for r, c_rel in pattern_first:
        abs_c = last_block_start_col + c_rel
        if 0 <= r < height and last_block_bounds[0] <= abs_c < last_block_bounds[1]:
             if input_grid[r][abs_c] != background_color: # Check original input grid color
                output_grid[r][abs_c] = minority_color

    # 6. Return Output
    return output_grid
```
