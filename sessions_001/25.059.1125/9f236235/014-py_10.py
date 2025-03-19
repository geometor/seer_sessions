"""
Transforms an input grid by identifying contiguous regions (blocks) of specific
target colors and placing a representative pixel from each block into an output
grid, preserving their relative positions. The target colors can be blue (1),
red (2), green (3), or orange (7). The output grid's dimensions are determined
by the number of identified blocks.
"""

import numpy as np

def find_colored_blocks(grid, target_colors):
    """Finds distinct colored blocks in the grid."""
    blocks = []
    visited = set()

    def is_valid(r, c):
        return 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1]

    def dfs(r, c, color, block):
        if (r, c) in visited or not is_valid(r, c) or grid[r, c] != color:
            return
        visited.add((r, c))
        block.append((r, c))
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            dfs(r + dr, c + dc, color, block)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            color = grid[r, c]
            if color in target_colors and (r, c) not in visited:
                block = []
                dfs(r, c, color, block)
                blocks.append({"color": color, "pixels": block})
    return blocks

def get_representative_pixel(block):
    """Selects a representative pixel from a block (top-left corner)."""
    return block["pixels"][0]

def transform(input_grid):
    # Convert input_grid to a NumPy array
    input_grid = np.array(input_grid)

    # Determine target colors present in this example
    target_colors = sorted(list(set([color for color in np.unique(input_grid) if color in [1, 2, 3, 7]])))

    # Find colored blocks
    colored_blocks = find_colored_blocks(input_grid, target_colors)
    num_blocks = len(colored_blocks)

    # Determine output grid size
    if num_blocks == 0:
        return np.array([[]])  # Return empty grid if no target blocks
    elif num_blocks == 1:
        output_grid = np.zeros((1, 1), dtype=int)
        output_grid[0, 0] = colored_blocks[0]["color"]
        return output_grid
    else:
        grid_size = num_blocks
        output_grid = np.zeros((grid_size, grid_size), dtype=int)

    # Create a mapping of representative pixels to their relative positions
    positions = []
    for block in colored_blocks:
        r, c = get_representative_pixel(block)
        positions.append(((r, c), block["color"]))

    # Sort positions based on row and then column to maintain relative positions
    positions.sort()

    # Place representative pixels in the output grid
    for i, (pos, color) in enumerate(positions):
        row = i // grid_size
        col = i % grid_size
        output_grid[row, col] = color

    return output_grid