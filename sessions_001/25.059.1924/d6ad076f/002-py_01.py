"""
The transformation rule identifies existing colored blocks (non-white) and inserts an azure block (color 8) of a determined dimension, effectively separating groups of colored blocks if they exist in the same row or column. The size of the azure block matches the width or height of adjacent blocks.
"""

import numpy as np

def find_blocks(grid):
    """Finds rectangular blocks of non-zero colors in the grid."""
    blocks = []
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                block_coords = []
                stack = [(r, c)]
                visited[r, c] = True

                while stack:
                    row, col = stack.pop()
                    block_coords.append((row, col))

                    # Check adjacent cells
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and grid[nr, nc] == color and not visited[nr, nc]:
                            stack.append((nr, nc))
                            visited[nr, nc] = True

                # Determine block boundaries
                min_row = min(block_coords, key=lambda x: x[0])[0]
                max_row = max(block_coords, key=lambda x: x[0])[0]
                min_col = min(block_coords, key=lambda x: x[1])[1]
                max_col = max(block_coords, key=lambda x: x[1])[1]

                blocks.append({
                    "color": color,
                    "min_row": min_row,
                    "max_row": max_row,
                    "min_col": min_col,
                    "max_col": max_col,
                })

    return blocks

def transform(input_grid):
    """Transforms the input grid by inserting azure blocks."""
    output_grid = input_grid.copy()
    blocks = find_blocks(input_grid)

    # Iterate through pairs of blocks to find insertion points
    for i in range(len(blocks)):
        for j in range(i + 1, len(blocks)):
            block1 = blocks[i]
            block2 = blocks[j]

            # Check for vertical insertion
            if block1["min_col"] == block2["min_col"] and block1["max_col"] == block2["max_col"] :
                if block1["max_row"] + 1 < block2["min_row"] :  # block 1 above block 2
                    insert_row_start = block1["max_row"] + 1
                    insert_row_end = block2["min_row"] -1 # exclusive
                    insert_col_start = block1["min_col"]
                    insert_col_end = block1["max_col"]  #inclusive

                    for r in range(insert_row_start, insert_row_end+1):  #inclusive
                       for c in range(insert_col_start, insert_col_end + 1):
                           output_grid[r,c] = 8
                    return output_grid # insert only once

                elif block2["max_row"] + 1 < block1["min_row"] : #block 2 above block 1
                    insert_row_start = block2["max_row"] + 1
                    insert_row_end = block1["min_row"] - 1  # exclusive
                    insert_col_start = block1["min_col"]
                    insert_col_end = block1["max_col"] #inclusive

                    for r in range(insert_row_start, insert_row_end+1): # inclusive
                        for c in range(insert_col_start, insert_col_end+1):
                            output_grid[r,c] = 8
                    return output_grid # insert only once


            #check for horisontal insertion
            if block1["min_row"] == block2["min_row"] and block1["max_row"] == block2["max_row"]:
                if block1["max_col"] + 1 < block2["min_col"]:  #block 1 on the left
                    insert_col_start = block1["max_col"] + 1
                    insert_col_end = block2["min_col"] -1 # exclusive
                    insert_row_start = block1["min_row"]
                    insert_row_end = block1["max_row"] #inclusive

                    for r in range(insert_row_start, insert_row_end+1):  #inclusive
                        for c in range(insert_col_start, insert_col_end + 1):
                            output_grid[r,c] = 8
                    return output_grid # insert only once

                elif block2["max_col"] + 1 < block1["min_col"]:  # block 2 on the left

                    insert_col_start = block2["max_col"] + 1
                    insert_col_end = block1["min_col"] -1 #exclusive
                    insert_row_start = block1["min_row"]
                    insert_row_end = block1["max_row"]  #inclusive

                    for r in range(insert_row_start, insert_row_end + 1):
                        for c in range(insert_col_start, insert_col_end + 1): # inclusive
                            output_grid[r,c] = 8
                    return output_grid # insert only once


    return output_grid