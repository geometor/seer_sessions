import numpy as np
import collections

"""
1. Identify the background color (assumed to be 0, white).
2. Create the output grid as an identical copy of the input grid.
3. Find all columns composed entirely of the background color ('separator columns').
4. Find all contiguous blocks of columns that contain at least one non-background pixel ('content blocks').
5. If there are no content blocks, return the unmodified output grid (which is a copy of the input).
6. Identify the first content block (leftmost). Let its columns range from `start_col` to `end_col`, and its width be `w = end_col - start_col + 1`.
7. Check if this first block is immediately preceded by a separator column (i.e., if `start_col > 0` and column `start_col - 1` is a separator column). Let the index of this preceding separator be `sep_idx = start_col - 1`.
8. If YES (preceded by separator):
   a. Calculate the target start column for placement: `target_start = start_col - (sep_idx + 1)`.
   b. Calculate the target end column: `target_end = target_start + w - 1`.
   c. Extract the pixel data of the first content block from the **input** grid (columns `start_col` to `end_col`).
   d. Reflect this extracted block data vertically (rows are reversed).
   e. Clear the region in the **output** grid corresponding to the target columns (`target_start` to `target_end`) by setting all pixels in these columns to the background color.
   f. Place the vertically reflected block data into the cleared target columns (`target_start` to `target_end`) of the **output** grid.
9. If NO (starts at column 0 or the preceding column is not a separator):
   a. The target columns are the original columns: `target_start = start_col`, `target_end = end_col`.
   b. Extract the pixel data of the first content block from the **input** grid (columns `start_col` to `end_col`).
   c. Reflect this extracted block data vertically.
   d. Clear the region in the **output** grid corresponding to the target columns (`target_start` to `target_end`) by setting all pixels in these columns to the background color.
   e. Place the vertically reflected block data into the cleared target columns (`target_start` to `target_end`) of the **output** grid.
10. Return the modified output grid. (No explicit copying of subsequent blocks is needed because the output started as a copy of the input, and only the placement area of the transformed first block is modified).
"""

def find_separator_columns(grid, background_color=0):
    """Finds indices of columns composed entirely of the background color."""
    separator_cols = set() # Use set for faster lookup
    height, width = grid.shape
    for c in range(width):
        if np.all(grid[:, c] == background_color):
            separator_cols.add(c)
    return separator_cols

def find_content_column_blocks(grid, separator_cols):
    """Finds contiguous blocks of columns that are not separator columns."""
    blocks = []
    height, width = grid.shape
    in_block = False
    start_col = -1
    for c in range(width):
        is_separator = c in separator_cols
        if not is_separator and not in_block:
            # Start of a new block
            in_block = True
            start_col = c
        elif is_separator and in_block:
            # End of a block
            in_block = False
            blocks.append((start_col, c - 1))
        # Check if the last column is part of a block
        elif c == width - 1 and in_block:
             blocks.append((start_col, c))
    return blocks

def transform(input_grid):
    """
    Transforms the input grid by copying it, then modifying the placement
    and orientation of the first content block based on whether it is
    preceded by a separator column. Other content remains unchanged from the initial copy.
    """
    # Convert input to numpy array for efficient operations
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    # Assume background color is 0 (white)
    background_color = 0

    # 1. Initialize output grid as a copy of the input grid
    output_np = np.copy(input_np)

    # 2. Find separator columns
    separator_cols = find_separator_columns(input_np, background_color)

    # 3. Find content blocks
    content_blocks = find_content_column_blocks(input_np, separator_cols)

    # 4. If no content blocks, return the initial copy
    if not content_blocks:
        return output_np.tolist()

    # 5. Identify the first content block
    first_block_start, first_block_end = content_blocks[0]
    first_block_width = first_block_end - first_block_start + 1

    # 6. Check if the first block is preceded by a separator
    preceded_by_separator = first_block_start > 0 and (first_block_start - 1) in separator_cols

    # 7. Determine target columns for placement
    if preceded_by_separator:
        # 7.a. Calculate target columns based on preceding separator index
        sep_idx = first_block_start - 1
        target_start = first_block_start - (sep_idx + 1)
        target_end = target_start + first_block_width - 1
    else:
        # 7.b. Target columns are the original columns
        target_start = first_block_start
        target_end = first_block_end

    # 8. Extract the first block data from the *input* grid
    block_data = input_np[:, first_block_start : first_block_end + 1]

    # 9. Reflect the extracted block data vertically
    reflected_block_data = np.flipud(block_data)

    # 10. Ensure target columns are within grid bounds (safety check)
    if 0 <= target_start < width and 0 <= target_end < width and target_end >= target_start :
        # 11. Clear the target area in the *output* grid
        output_np[:, target_start : target_end + 1] = background_color

        # 12. Place the reflected block data into the cleared target area
        output_np[:, target_start : target_end + 1] = reflected_block_data
    else:
        # This case should ideally not happen if logic is correct and inputs are valid ARC grids.
        # If it does, it might indicate an edge case or misunderstanding.
        # For robustness, we could leave the output unchanged in this unexpected scenario
        # or log a warning. Here, we'll proceed assuming valid targets based on examples.
        # If bounds are invalid, the original content in output_np remains.
        # However, if only clearing worked, then placing failed, we might have an issue.
        # The current logic places the reflected data only if bounds are valid.
        pass


    # 13. Return the modified output grid as a list of lists
    return output_np.tolist()