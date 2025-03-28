import numpy as np
from collections import Counter

"""
Analyzes the input grid to identify a repeating grid line color.
It then segments the grid into cells based on these grid lines.
Within each cell, it searches for a 2x2 block of a single color (excluding white 0 and the grid line color).
It counts the occurrences of each unique color found in these 2x2 blocks across all cells.
Finally, it constructs an output grid where each row represents a unique color found.
The row is filled with that color, and the length of the colored segment corresponds to its count.
The rows in the output grid are sorted based on the counts in ascending order.
"""

def find_grid_color(grid):
    """
    Identifies the color used for grid lines.
    It prioritizes colors that form complete rows and columns.
    If that fails, it uses heuristics based on dominant colors in rows/columns.
    """
    H, W = grid.shape
    candidate_colors = set(np.unique(grid)) - {0} # Non-background colors

    # Check for colors forming full rows AND columns
    for color in candidate_colors:
        is_row_grid = any(np.all(grid[r, :] == color) for r in range(H))
        is_col_grid = any(np.all(grid[:, c] == color) for c in range(W))
        if is_row_grid and is_col_grid:
            return color

    # Check for colors forming just full rows or just full columns
    # Prioritize row-forming colors if found
    for r in range(H):
        first_color = grid[r, 0]
        if first_color != 0 and np.all(grid[r, :] == first_color):
            return first_color
    for c in range(W):
        first_color = grid[0, c]
        if first_color != 0 and np.all(grid[:, c] == first_color):
            return first_color
            
    # Fallback heuristic: Check periodic appearance in first row/col (common pattern)
    if W > 4 and grid[0, 4] != 0: return grid[0, 4]
    if H > 4 and grid[4, 0] != 0: return grid[4, 0]

    # More general fallback: Most frequent non-zero color, potentially?
    # This seems risky as it might pick up a block color.
    # If no grid color found, maybe the task doesn't have one?
    # Let's return a default or raise an error if critical. For now -1.
    return -1 

def find_cells(grid, grid_color):
    """
    Segments the grid into cells based on the grid lines.
    Returns a list of numpy arrays, each representing a cell.
    """
    H, W = grid.shape
    
    # Find indices of rows/columns that consist entirely of the grid_color
    grid_rows = [r for r in range(H) if np.all(grid[r, :] == grid_color)]
    grid_cols = [c for c in range(W) if np.all(grid[:, c] == grid_color)]

    cells = []
    # Define row boundaries: start from 0, add 1 after each grid row, end at H
    row_starts = [0] + [r + 1 for r in grid_rows]
    row_ends = grid_rows + [H]
    # Define column boundaries: start from 0, add 1 after each grid col, end at W
    col_starts = [0] + [c + 1 for c in grid_cols]
    col_ends = grid_cols + [W]

    # Create cell subgrids using the calculated boundaries
    for r_start, r_end in zip(row_starts, row_ends):
        for c_start, c_end in zip(col_starts, col_ends):
            # Ensure the slice indices define a valid, non-empty area
            if r_start < r_end and c_start < c_end:
                cells.append(grid[r_start:r_end, c_start:c_end])
    return cells

def find_2x2_blocks_in_cell(cell, grid_color):
    """
    Finds the color of the first 2x2 block within a cell.
    Ignores background (0) and grid_color.
    Returns the color if found, otherwise None.
    """
    cell_h, cell_w = cell.shape
    # Iterate through possible top-left corners of a 2x2 block
    for r in range(cell_h - 1):
        for c in range(cell_w - 1):
            color = cell[r, c]
            # Check if the color is valid (not background, not grid color)
            if color != 0 and color != grid_color:
                # Check if the 2x2 area starting at (r, c) is monochrome with this color
                if (cell[r+1, c] == color and
                    cell[r, c+1] == color and
                    cell[r+1, c+1] == color):
                    return color  # Return the color of the found block
    return None # No valid 2x2 block found in this cell

def transform(input_grid_list):
    """
    Transforms the input grid based on counting 2x2 blocks within cells
    defined by grid lines, and creating a histogram sorted by counts.
    """
    input_grid = np.array(input_grid_list, dtype=int)

    # 1. Identify the grid_line color.
    grid_color = find_grid_color(input_grid)
    # if grid_color == -1:
        # Basic assumption if detection fails: treat whole grid as one cell, no grid color constraint
        # grid_color = -1 # Use a value that won't match any valid color (0-9)
        # cells = [input_grid]
    # Based on examples, grid color seems essential. Revert to strict finding.
    if grid_color == -1:
         print("Error: Grid color not found. Cannot proceed.")
         # Returning minimal grid as per spec possibility
         return [[0]] 

    # 2. Determine the boundaries of the cells.
    cells = find_cells(input_grid, grid_color)

    # 3. Initialize a counter for colors found in 2x2 blocks.
    color_counts = Counter()

    # 4-6. Iterate through cells, find 2x2 blocks, and count their colors.
    for cell in cells:
        block_color = find_2x2_blocks_in_cell(cell, grid_color)
        if block_color is not None:
            # Increment the count for the found color
            color_counts[block_color] += 1

    # 7. If no blocks were found, return a minimal grid.
    if not color_counts:
        return [[0]] 

    # 8. Calculate output grid dimensions.
    num_rows = len(color_counts)
    # Max count determines the width (number of columns)
    num_cols = max(color_counts.values()) 

    # 9. Sort the found colors based on their counts (ascending).
    # Use color value as a secondary sort key for stable ordering.
    sorted_colors = sorted(color_counts.items(), key=lambda item: (item[1], item[0]))

    # 10. Create the output grid, initialized with background color (0).
    output_grid = np.zeros((num_rows, num_cols), dtype=int)

    # 11. Fill the output grid row by row based on sorted colors and counts.
    for i, (color, count) in enumerate(sorted_colors):
        # Fill the first 'count' columns of the i-th row with the color
        output_grid[i, :count] = color

    # Convert the numpy array back to a list of lists for the expected output format
    return output_grid.tolist()
