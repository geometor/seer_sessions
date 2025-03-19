"""
Identifies a 2x2 arrangement of color regions within the input grid and represents their colors in a 2x2 output grid, preserving the spatial arrangement.
"""

import numpy as np

def find_blocks(grid):
    # Find distinct colored regions in the grid.
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    blocks = []

    def dfs(r, c, color):
        if (r < 0 or r >= rows or c < 0 or c >= cols or
                visited[r, c] or grid[r, c] != color):
            return []
        visited[r, c] = True
        region = [(r, c)]
        region.extend(dfs(r + 1, c, color))
        region.extend(dfs(r - 1, c, color))
        region.extend(dfs(r, c + 1, color))
        region.extend(dfs(r, c - 1, color))
        return region

    for r in range(rows):
        for c in range(cols):
            if not visited[r, c] and grid[r, c] != 0:
                region = dfs(r, c, grid[r, c])
                if region:
                    # Calculate bounding box
                    min_row = min(p[0] for p in region)
                    max_row = max(p[0] for p in region)
                    min_col = min(p[1] for p in region)
                    max_col = max(p[1] for p in region)
                    
                    blocks.append({
                        "color": grid[r, c],
                        "min_row": min_row,
                        "max_row": max_row,
                        "min_col": min_col,
                        "max_col": max_col
                    })
    return blocks

def get_block_order(blocks):
     # Sort blocks based on their top-left corner coordinates.
    sorted_blocks = sorted(blocks, key=lambda block: (block["min_row"], block["min_col"]))
    
    #Assuming a 2x2 arrangement
    if len(sorted_blocks) == 4:
        return [sorted_blocks[0], sorted_blocks[1], sorted_blocks[2], sorted_blocks[3]]
    else:
        return [] # or raise Exception("Not exact four blocks for a 2x2 arrangement")

def transform(input_grid):
    """
    Transforms the input grid by extracting the colors of the 2x2 blocks and creating a corresponding 2x2 output.
    """
    # Find distinct blocks in the input grid
    blocks = find_blocks(np.array(input_grid))
    
    # Order the blocks based on their top-left coordinates, expecting a 2x2 arrangement
    ordered_blocks = get_block_order(blocks)

    # Initialize the output grid
    output_grid = np.zeros((2, 2), dtype=int)
    
    if len(ordered_blocks)==4:

        # Populate output grid with colors of ordered blocks
        output_grid[0, 0] = ordered_blocks[0]["color"]  # Top-left
        output_grid[0, 1] = ordered_blocks[1]["color"]  # Top-right
        output_grid[1, 0] = ordered_blocks[2]["color"]  # Bottom-left
        output_grid[1, 1] = ordered_blocks[3]["color"]  # Bottom-right

    return output_grid