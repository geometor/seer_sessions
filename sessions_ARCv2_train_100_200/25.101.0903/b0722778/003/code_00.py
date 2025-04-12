"""
Transforms the input grid based on the following logic:
1. The input grid is viewed as a macro-grid of 2x2 blocks separated by single white (0) rows/columns.
2. For each row of 2x2 blocks in the input:
   a. Select one 2x2 block:
      - If it's the second block row (index 1), choose the block with the minimum sum of pixels.
      - Otherwise, choose the block with the maximum sum of pixels.
      - Ties are broken by choosing the rightmost block among those tied.
   b. Transform the selected 2x2 block `[[a, b], [c, d]]` based on its internal pattern/symmetry using a set of prioritized rules:
      i.   If `a == c and b == d`: Output `[[b, b], [a, a]]`.
      ii.  Else if `a == b and c == d`: Output `[[c, a], [c, a]]`.
      iii. Else if `a == c and c == d`: Output `[[b, a], [d, c]]`.
      iv.  Else if `a == c`: Output `[[c, c], [c, b]]`.
      v.   Else if `c == d`: Output `[[a, b], [a, b]]`.
      vi.  Else if `a == b`: Output `[[a, b], [b, c]]`.
      vii. Else (Fallback): Output `[[b, a], [d, c]]`.
   c. Place the transformed 2x2 block into the corresponding row of the output grid.
3. The output grid has the same height as the input but a fixed width of 2.
4. White separator rows from the input structure are preserved in the output.
5. Note: The transformation for the block selected in Example 1, Row 1 (br=1) does not produce the expected output based on these rules; this case represents an anomaly or requires a different interpretation not covered here.
"""

import math

# Helper functions
def get_2x2_block(grid: list[list[int]], r: int, c: int) -> list[list[int]] | None:
    """
    Extracts a 2x2 block from the grid starting at (r, c).
    Returns None if the block goes out of bounds.
    """
    H = len(grid)
    W = len(grid[0])
    if r + 1 >= H or c + 1 >= W:
        return None
    return [
        [grid[r][c], grid[r][c+1]],
        [grid[r+1][c], grid[r+1][c+1]]
    ]

def calculate_sum(block: list[list[int]]) -> int:
    """Calculates the sum of the 4 pixels in a 2x2 block."""
    # Assumes block is always 2x2
    return block[0][0] + block[0][1] + block[1][0] + block[1][1]

def transform_block(block: list[list[int]]) -> list[list[int]]:
    """
    Applies the specific prioritized transformation rule to a 2x2 block
    based on its internal pattern.
    """
    a, b = block[0]
    c, d = block[1]

    # Rule 1: Left col same, Right col same (a=c and b=d)
    if a == c and b == d:
        return [[b, b], [a, a]]
    # Rule 2: Top row same, Bottom row same (a=b and c=d)
    elif a == b and c == d:
        return [[c, a], [c, a]]
    # Rule 3: Three corners same (a=c and c=d -> a=c=d)
    elif a == c and c == d:
         # Horizontal Reflection -> [[b, a], [d, c]]
        return [[b, a], [d, c]]
    # Rule 4: Left col same (a=c)
    elif a == c:
         # Pattern T_ccb -> [[c, c], [c, b]]
        return [[c, c], [c, b]]
    # Rule 5: Bottom row same (c=d)
    elif c == d:
        # Pattern T_abab -> [[a, b], [a, b]]
        return [[a, b], [a, b]]
    # Rule 6: Top row same (a=b)
    elif a == b:
         # Pattern T_abbc -> [[a, b], [b, c]]
        return [[a, b], [b, c]]
    # Rule 7: Fallback (no specific pattern matched)
    else:
        # Horizontal Reflection -> [[b, a], [d, c]]
        return [[b, a], [d, c]]

def place_block(grid: list[list[int]], block: list[list[int]], r: int, c: int):
    """Places a 2x2 block into the grid at position (r, c). Assumes bounds are checked beforehand."""
    grid[r][c] = block[0][0]
    grid[r][c+1] = block[0][1]
    grid[r+1][c] = block[1][0]
    grid[r+1][c+1] = block[1][1]


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    H = len(input_grid)
    W = len(input_grid[0])
    H_out = H
    W_out = 2

    # Initialize output grid with white (0)
    output_grid = [[0] * W_out for _ in range(H_out)]

    # Calculate the number of block rows based on the input height
    # Each block row takes 2 rows + 1 separator row (except potentially the last)
    num_block_rows = (H + 1) // 3

    # Process each block row
    for br in range(num_block_rows):
        start_row = br * 3

        # Check if the block row fits entirely within the grid height
        if start_row + 1 >= H:
            continue # Skip incomplete block rows if they occur at the bottom

        # Extract the three potential 2x2 input blocks for this row
        # along with their original horizontal block index (0, 1, 2)
        blocks_data = [] # Stores (block, block_sum, original_col_index)
        for bc_idx in range(3):
             start_col = bc_idx * 3
             block = get_2x2_block(input_grid, start_row, start_col)
             if block: # Check if block is within bounds
                 block_sum = calculate_sum(block)
                 blocks_data.append({'block': block, 'sum': block_sum, 'index': bc_idx})

        if not blocks_data: # No valid blocks found in this row
            continue

        # Select block based on sum and row index (br)
        selected_block_info = None
        if br == 1: # Minimize for the second block row (index 1)
            min_s = min(item['sum'] for item in blocks_data)
            # Filter candidates with the minimum sum
            candidates = [item for item in blocks_data if item['sum'] == min_s]
        else: # Maximize for other rows
            max_s = max(item['sum'] for item in blocks_data)
            # Filter candidates with the maximum sum
            candidates = [item for item in blocks_data if item['sum'] == max_s]

        # Tie-break by selecting the candidate with the highest original column index
        selected_block_info = max(candidates, key=lambda item: item['index'])
        selected_block = selected_block_info['block']

        # Transform the selected block
        transformed_block = transform_block(selected_block)

        # Place the transformed block into the output grid at the corresponding row, column 0
        # Ensure placement is within output grid bounds (should be fine given H_out=H)
        if start_row + 1 < H_out:
             place_block(output_grid, transformed_block, start_row, 0)

    # Overwrite separator rows in the output grid with white (0)
    # Separator rows occur at indices 2, 5, 8, ...
    for r in range(2, H, 3):
        if r < H_out: # Ensure row index is within output grid bounds
             output_grid[r] = [0] * W_out # Set the separator row to white

    return output_grid