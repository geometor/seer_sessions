"""
The program constructs an output grid by analyzing the color blocks in the first two rows of the input grid. It then creates new rows based on these blocks, repeating the colors to fill the width of the output grid.

1.  **Identify Color Blocks:** Examine the first two rows of the input grid. Within each row, identify contiguous blocks of pixels with the same color. Each block is defined by its color and length.
2.  **Output Height:** The output height is the same as input height.
3.  **Construct Output Rows 3 and 4:** For each color block in the *first* input row, create a new row in the output grid where all pixels have the color of that block, and length of input grid width. The number of rows is same as the number of elements in first row.
4.  **Construct Output Rows:** stack first two original rows on top of newly created rows
5. Repeat Step 3, using the order of appearance of blocks to preserve their order.
"""

import numpy as np

def get_color_blocks(row):
    """Identifies contiguous blocks of the same color within a row."""
    blocks = []
    current_block = []
    for i in range(len(row)):
        if not current_block:
            current_block.append(row[i])
        elif row[i] == current_block[-1]:
            current_block.append(row[i])
        else:
            blocks.append((current_block[0], len(current_block)))  # (color, length)
            current_block = [row[i]]
    if current_block:
        blocks.append((current_block[0], len(current_block)))
    return blocks

def transform(input_grid):
    """Transforms the input grid according to the observed rule."""

    input_grid = np.array(input_grid)
    input_height = input_grid.shape[0]
    input_width = input_grid.shape[1]

    # Output height is the same as the input height.
    output_height = input_height
    output_grid = np.zeros((output_height, input_width), dtype=int)

    # Copy the first two rows to output
    output_grid[0] = input_grid[0]
    output_grid[1] = input_grid[1]

    # Get color blocks from the first row.
    first_row_blocks = get_color_blocks(input_grid[0])

    # construct new rows based on the blocks of first row
    row_index = 2
    for color, _ in first_row_blocks:
        output_grid[row_index] = np.full(input_width, color)
        row_index += 1

    # repeat until the end of the output
    num_repeats = (output_height - 2) // len(first_row_blocks)

    for _ in range(num_repeats -1):
        for color, _ in first_row_blocks:
          output_grid[row_index] = np.full(input_width, color)
          row_index += 1


    return output_grid.tolist()