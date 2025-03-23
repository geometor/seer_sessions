```python
"""
1.  **Identify Seed Columns:** Find columns that have vertical stacks of the same non-zero color, where the colors are vertically stacked adjacent to each other. These stacks define the "seed columns".
2.  **Group by Color:** Group the seed column pixels by their color.
3.  **Row-Specific Insertion:** For each color:
    *   Identify the rows where this color appears in the seed columns.
    *   For each identified row, copy the pixel from the original seed column. Insert additional copies of the same color from seed column to the right of the original pixel.
    *   The number of inserted columns will be equal to difference between row indices of the colored pixels of same color.
4.  **Other Rows:** Rows that do *not* contain any of the seed colors are copied directly from the input to the output without modification.
5. Prevent expansion: if inserted columns would exceed bounds of input grid, trim them
"""

import numpy as np

def find_seed_columns(grid):
    """
    Identifies seed columns based on vertically stacked, adjacent colors.
    """
    rows, cols = grid.shape
    seed_columns = set()
    for c in range(cols):
        for r in range(rows - 1):  # Check for adjacent pairs
            if grid[r, c] != 0 and grid[r, c] == grid[r + 1, c]:
                seed_columns.add(c)
                break  # Move to the next column
    return list(seed_columns)

def get_seed_data(grid, seed_columns):
    """
    Groups seed column pixels by color and stores their locations.
    """
    seed_data = {}  # {color: [(row, col), ...]}
    for c in seed_columns:
        for r in range(grid.shape[0]):
            color = grid[r, c]
            if color != 0:
                if color not in seed_data:
                    seed_data[color] = []
                seed_data[color].append((r, c))
    return seed_data

def transform(input_grid):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    output_grid = np.copy(input_grid)

    seed_columns = find_seed_columns(input_grid)
    seed_data = get_seed_data(input_grid, seed_columns)

    for color, locations in seed_data.items():
        # Get unique rows for this color
        rows_to_transform = sorted(list(set([r for r, _ in locations])))

        for row_index in rows_to_transform:
            # Build new row with insertions
            new_row = []
            for col_index in range(cols):
                new_row.append(input_grid[row_index, col_index]) # always copy original

                if (row_index, col_index) in locations:

                    # calculate number of insertions based on distance between row indices
                    seed_row_indices = []
                    for r,c in locations:
                        if c == col_index:
                           seed_row_indices.append(r)

                    insertions = 1
                    if len(seed_row_indices) > 0:
                        idx = seed_row_indices.index(row_index)
                        if idx < len(seed_row_indices) -1:
                            insertions = seed_row_indices[idx+1] - seed_row_indices[idx]
                    
                    for _ in range(insertions):
                        new_row.append(input_grid[row_index, col_index]) # insert copies

            output_grid[row_index] = np.array(new_row[:cols]) # Trim to fit

    return output_grid.tolist()
```