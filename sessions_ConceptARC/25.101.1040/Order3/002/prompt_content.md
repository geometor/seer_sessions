
Previous Code:
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
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 3 3 0 3 3 0 3 3 0 4 4 0
0 3 4 0 3 3 0 3 3 0 3 3 0
0 3 3 0 4 3 0 3 4 0 4 3 0
0 3 3 0 3 4 0 3 3 0 3 4 0
0 4 3 0 3 4 0 3 3 0 3 3 0
0 3 3 0 3 3 0 3 3 0 3 3 0
```
Expected Output:
```
0 3 3 0 3 3 0 3 3 0 4 4 0
0 3 3 0 3 4 0 3 3 0 3 3 0
0 3 4 0 3 3 0 4 3 0 4 3 0
0 3 3 0 3 3 0 3 4 0 3 4 0
0 3 3 0 4 3 0 3 4 0 3 3 0
0 3 3 0 3 3 0 3 3 0 3 3 0
```
Transformed Output:
```
0 4 4 0 3 3 0 3 3 0 3 3 0
0 3 3 0 3 3 0 3 3 0 3 4 0
0 4 3 0 4 3 0 3 4 0 3 3 0
0 3 4 0 3 4 0 3 3 0 3 3 0
0 3 3 0 3 4 0 3 3 0 4 3 0
0 3 3 0 3 3 0 3 3 0 3 3 0
```
Match: False
Pixels Off: 20
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 25.641025641025635

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 0 7 7 7 0 7 7 7 0
0 6 6 6 0 7 7 7 0 7 7 7 0
0 7 7 7 0 6 6 7 0 7 7 7 0
0 7 7 7 0 7 7 7 0 7 6 7 0
0 7 7 7 0 7 7 7 0 7 7 7 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 0 7 7 7 0 7 7 7 0
0 7 7 7 0 7 7 7 0 6 6 6 0
0 7 7 7 0 6 6 7 0 7 7 7 0
0 7 6 7 0 7 7 7 0 7 7 7 0
0 7 7 7 0 7 7 7 0 7 7 7 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0
0 7 7 7 0 7 7 7 0 7 7 7 0
0 7 7 7 0 7 7 7 0 6 6 6 0
0 7 7 7 0 6 6 7 0 7 7 7 0
0 7 6 7 0 7 7 7 0 7 7 7 0
0 7 7 7 0 7 7 7 0 7 7 7 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0.0
