```python
"""
Transforms a 6x6 input grid based on the parity of the position of a central 2x2 non-zero block.

1. Find the Source Block: Locates the 2x2 block of non-zero digits in the 6x6 input grid. Extracts its top-left corner coordinates (r, c) and its four digit values A (top-left), B (top-right), C (bottom-left), D (bottom-right).
2. Initialize Output Grid: Creates a deep copy of the input grid.
3. Check Position Parity: Determines if both r and c are odd, or if both r and c are even.
4. Generate and Place Corner Blocks based on Parity:
    - If r and c are both odd:
        - Places [[D, 0], [0, A]] at (r-1, c-1).
        - Places [[C, C], [0, 0]] at (r-1, c+2).
        - Places [[B, 0], [B, 0]] at (r+2, c-1).
        - Places [[A, A], [A, A]] at (r+2, c+2).
    - If r and c are both even:
        - Places [[D, D], [D, D]] at (r-2, c-2).
        - Places [[C, C], [C, C]] at (r-2, c+2).
        - Places [[B, B], [B, B]] at (r+2, c-2).
        - Places [[A, A], [A, A]] at (r+2, c+2).
5. Return the modified grid.
"""

import copy

def find_source_block(grid: list[list[int]]) -> tuple[int, int, int, int, int, int] | None:
    """
    Finds the top-left corner (r, c) and values (A, B, C, D) of the 2x2 non-zero block.
    Assumes exactly one such block exists.
    """
    height = len(grid)
    width = len(grid[0]) if height > 0 else 0
    for r in range(height - 1):
        for c in range(width - 1):
            # Check if all four cells in the 2x2 block are non-zero
            if (grid[r][c] != 0 and
                    grid[r][c+1] != 0 and
                    grid[r+1][c] != 0 and
                    grid[r+1][c+1] != 0):
                A = grid[r][c]
                B = grid[r][c+1]
                C = grid[r+1][c]
                D = grid[r+1][c+1]
                return r, c, A, B, C, D
    return None # Should not happen based on problem description

def place_block(grid: list[list[int]], block: list[list[int]], top_r: int, top_c: int):
    """
    Places a 2x2 block into the grid at the specified top-left coordinates.
    Overwrites existing values. Assumes placement is within grid boundaries.
    """
    height = len(grid)
    width = len(grid[0])
    for r_offset in range(2):
        for c_offset in range(2):
            target_r = top_r + r_offset
            target_c = top_c + c_offset
            # Basic boundary check (though problem implies valid placements)
            if 0 <= target_r < height and 0 <= target_c < width:
                 grid[target_r][target_c] = block[r_offset][c_offset]


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule based on the source block's position parity.
    """
    # initialize output_grid as a deep copy
    output_grid = copy.deepcopy(input_grid)
    
    # Find the source block details
    find_result = find_source_block(input_grid)
    if find_result is None:
        # Handle error case or return original grid if no block found
        return output_grid 
        
    r, c, A, B, C, D = find_result

    # Check parity and perform transformations
    r_is_odd = r % 2 != 0
    c_is_odd = c % 2 != 0
    r_is_even = not r_is_odd
    c_is_even = not c_is_odd

    if r_is_odd and c_is_odd:
        # Define and place corner blocks for odd/odd case
        tl_block = [[D, 0], [0, A]]
        tr_block = [[C, C], [0, 0]]
        bl_block = [[B, 0], [B, 0]]
        br_block = [[A, A], [A, A]] # Corrected train_1 example suggests A, not D

        place_block(output_grid, tl_block, r - 1, c - 1)
        place_block(output_grid, tr_block, r - 1, c + 2)
        place_block(output_grid, bl_block, r + 2, c - 1)
        place_block(output_grid, br_block, r + 2, c + 2)

    elif r_is_even and c_is_even:
         # Define and place corner blocks for even/even case
        tl_block = [[D, D], [D, D]]
        tr_block = [[C, C], [C, C]]
        bl_block = [[B, B], [B, B]]
        br_block = [[A, A], [A, A]]

        place_block(output_grid, tl_block, r - 2, c - 2)
        place_block(output_grid, tr_block, r - 2, c + 2)
        place_block(output_grid, bl_block, r + 2, c - 2)
        place_block(output_grid, br_block, r + 2, c + 2)
        
    # If parity is mixed (e.g., r odd, c even), do nothing additional based on examples
    # (The problem description implies only odd/odd or even/even cases occur)

    return output_grid
```