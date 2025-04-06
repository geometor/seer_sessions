import copy

"""
Transforms an input grid based on the presence of a 'trigger' color (1, 2, or 3) relative to blocks of color 5.

Rule Selection:
- If the trigger color is 3, apply the "Expansion Rule".
- If the trigger color is 1 or 2, apply the "Projection Rule".

Expansion Rule (Trigger 3):
- Cells with color 3 become 5 if they are orthogonally adjacent to a cell with color 5 in the input.
- Otherwise, cells with color 3 become 0.
- All other cells (0 or 5) remain unchanged.

Projection Rule (Triggers 1 or 2):
- Identify the top-most (min_row_5) and bottom-most (max_row_5) rows of the main horizontal block of color 5.
- Trigger cells (1 or 2) located above the block project color 5 onto the row directly above the block (min_row_5 - 1) in the same column.
- Trigger cells (1 or 2) located below the block project color 5 onto the row directly below the block (max_row_5 + 1) in the same column.
- The original trigger cells are changed to 0.
- All other cells (0 or 5) remain unchanged unless modified by the projection.
"""

def _find_trigger_color(grid: list[list[int]]) -> int | None:
    """Finds the first trigger color (1, 2, or 3) in the grid."""
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] in [1, 2, 3]:
                return grid[r][c]
    return None # Should not happen based on problem description

def _find_5_block_rows(grid: list[list[int]]) -> tuple[int | None, int | None]:
    """Finds the minimum and maximum row indices containing the color 5."""
    min_row_5 = None
    max_row_5 = None
    rows = len(grid)
    cols = len(grid[0]) if rows > 0 else 0

    for r in range(rows):
        for c in range(cols):
            if grid[r][c] == 5:
                if min_row_5 is None:
                    min_row_5 = r
                max_row_5 = r
                # Optimization: once a 5 is found in a row,
                # we know this row contributes to the block boundary
                # calculation, no need to check other cells in this row
                # for the purpose of finding min/max row.
                break 
                
    return min_row_5, max_row_5

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the transformation rule based on the trigger color found in the input grid.
    """
    if not input_grid or not input_grid[0]:
        return []

    rows = len(input_grid)
    cols = len(input_grid[0])

    # Create a deep copy of the input grid to modify
    output_grid = copy.deepcopy(input_grid)

    # 1. Analyze Input: Identify the trigger color
    trigger_color = _find_trigger_color(input_grid)

    # 2. Select and Apply Rule
    if trigger_color == 3:
        # Apply Expansion Rule
        for r in range(rows):
            for c in range(cols):
                if input_grid[r][c] == 3:
                    # Check orthogonal neighbors in the *input* grid
                    has_5_neighbor = False
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = r + dr, c + dc
                        if 0 <= nr < rows and 0 <= nc < cols and input_grid[nr][nc] == 5:
                            has_5_neighbor = True
                            break
                    
                    # Update the *output* grid
                    if has_5_neighbor:
                        output_grid[r][c] = 5
                    else:
                        output_grid[r][c] = 0
        # Cells originally 0 or 5 are already correct due to the initial deep copy

    elif trigger_color in [1, 2]:
        # Apply Projection Rule
        min_row_5, max_row_5 = _find_5_block_rows(input_grid)

        # Check if a block of 5s was actually found
        if min_row_5 is None or max_row_5 is None:
             # If no 5s, just remove triggers and return
             for r in range(rows):
                for c in range(cols):
                    if output_grid[r][c] == trigger_color:
                         output_grid[r][c] = 0
             return output_grid

        # First pass: Remove original trigger cells from the output grid
        trigger_locations = []
        for r in range(rows):
            for c in range(cols):
                if input_grid[r][c] == trigger_color:
                    output_grid[r][c] = 0 # Remove trigger from its original spot
                    trigger_locations.append((r, c)) # Keep track of where they were

        # Second pass: Apply projections based on original trigger locations
        for r, c in trigger_locations:
             # Project downwards onto row above the block
             if r < min_row_5:
                 target_r = min_row_5 - 1
                 if 0 <= target_r < rows: # Check bounds
                     output_grid[target_r][c] = 5
             
             # Project upwards onto row below the block
             elif r > max_row_5:
                 target_r = max_row_5 + 1
                 if 0 <= target_r < rows: # Check bounds
                     output_grid[target_r][c] = 5
        # Cells originally 0 or 5 are already correct unless projected upon

    # 5. Final Output
    return output_grid