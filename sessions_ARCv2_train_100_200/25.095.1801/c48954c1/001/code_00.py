import copy

# Helper function to rotate a 3x3 grid 180 degrees
def rotate_180(grid: list[list[int]]) -> list[list[int]]:
    """Rotates a 3x3 grid 180 degrees."""
    rotated = [row[:] for row in grid] # Create a copy
    rotated.reverse() # Reverse row order
    for row in rotated:
        row.reverse() # Reverse elements in each row
    return rotated

# Helper function to reflect a 3x3 grid vertically (across horizontal midline)
def reflect_vertical(grid: list[list[int]]) -> list[list[int]]:
    """Reflects a 3x3 grid vertically."""
    reflected = [row[:] for row in grid] # Create a copy
    reflected.reverse() # Reverse row order
    return reflected

# Helper function to reflect a 3x3 grid horizontally (across vertical midline)
def reflect_horizontal(grid: list[list[int]]) -> list[list[int]]:
    """Reflects a 3x3 grid horizontally."""
    reflected = []
    for row in grid:
        new_row = row[:] # Create a copy of the row
        new_row.reverse() # Reverse elements in the row
        reflected.append(new_row)
    return reflected

# Helper function to place a 3x3 block into a larger grid
def place_block(target_grid: list[list[int]], block: list[list[int]], start_row: int, start_col: int):
    """Places a 3x3 block into the target_grid at the specified offset."""
    for r in range(3):
        for c in range(3):
            if start_row + r < len(target_grid) and start_col + c < len(target_grid[0]):
                 target_grid[start_row + r][start_col + c] = block[r][c]


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms a 3x3 input grid into a 9x9 output grid by arranging nine 3x3 blocks.
    Each block is a specific transformation (identity, 180-degree rotation, 
    vertical reflection, or horizontal reflection) of the input grid, arranged 
    in the pattern:
        R180 | RefV | R180
        -----+------+-----
        RefH | Id   | RefH
        -----+------+-----
        R180 | RefV | R180
    """
    
    # 1. Create the four transformed versions of the input grid
    identity_grid = input_grid # No transformation needed, can use directly
    rotated_grid = rotate_180(input_grid)
    reflected_v_grid = reflect_vertical(input_grid)
    reflected_h_grid = reflect_horizontal(input_grid)

    # 2. Initialize the 9x9 output grid (e.g., with zeros or None)
    output_grid = [[0 for _ in range(9)] for _ in range(9)] 
    
    # 3. Construct the output grid by placing the transformed blocks
    # Top row of blocks
    place_block(output_grid, rotated_grid, 0, 0)      # Block [0,0]
    place_block(output_grid, reflected_v_grid, 0, 3)   # Block [0,1]
    place_block(output_grid, rotated_grid, 0, 6)      # Block [0,2]

    # Middle row of blocks
    place_block(output_grid, reflected_h_grid, 3, 0)   # Block [1,0]
    place_block(output_grid, identity_grid, 3, 3)     # Block [1,1]
    place_block(output_grid, reflected_h_grid, 3, 6)   # Block [1,2]

    # Bottom row of blocks
    place_block(output_grid, rotated_grid, 6, 0)      # Block [2,0]
    place_block(output_grid, reflected_v_grid, 6, 3)   # Block [2,1]
    place_block(output_grid, rotated_grid, 6, 6)      # Block [2,2]

    # 4. Return the resulting 9x9 grid
    return output_grid
