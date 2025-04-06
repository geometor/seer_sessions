import copy

"""
The transformation identifies the single non-zero color (C_in) in the 3x3 input grid. 
It then determines a corresponding output color (C_out) based on a fixed mapping: 3 maps to 1, 5 maps to 4, and 8 maps to 2. 
Finally, it constructs a 3x3 output grid where the positions that were 0 in the input grid are filled with C_out, 
and the positions that held C_in in the input grid are set to 0. Essentially, it creates a spatial complement pattern with a mapped color.
"""

def find_non_zero_color(grid: list[list[int]]) -> int:
    """Finds the unique non-zero color value in the grid."""
    non_zero_val = 0
    for r in range(len(grid)):
        for c in range(len(grid[0])):
            if grid[r][c] != 0:
                # Check if we already found a different non-zero value
                if non_zero_val != 0 and grid[r][c] != non_zero_val:
                    # Handle case of multiple non-zero colors if needed, 
                    # but based on examples, assume only one.
                    print(f"Warning: Multiple non-zero colors found. Using {grid[r][c]}")
                    return grid[r][c] # Or raise error
                non_zero_val = grid[r][c]
    if non_zero_val == 0:
         print(f"Warning: No non-zero colors found.") # handle case where grid is all zeros
         # Decide default behavior - maybe return 0 or raise error
    return non_zero_val

def map_color(input_color: int) -> int:
    """Maps the input non-zero color to the corresponding output color."""
    mapping = {
        3: 1,
        5: 4,
        8: 2,
        # Add mapping for 0 if input can be all zeros, perhaps maps to 0?
        # Based on examples, 0 in input becomes C_out, C_in becomes 0.
        # If input grid is all 0s, what should C_in/C_out be?
        # Assuming input always has one non-zero color based on examples.
    }
    if input_color not in mapping:
        # Handle unexpected input colors if necessary
        print(f"Warning: Unmapped input color {input_color}. Returning 0.")
        return 0 # Default or raise error
    return mapping[input_color]

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies the described transformation to the input grid.
    """
    # Ensure grid dimensions are as expected (optional check)
    rows = len(input_grid)
    if rows == 0:
        return []
    cols = len(input_grid[0])
    if rows != 3 or cols != 3:
         print(f"Warning: Expected 3x3 grid, got {rows}x{cols}. Attempting transformation anyway.")
         # Or raise ValueError("Input grid must be 3x3")

    # 1. Identify Input Pattern: Find the unique non-zero color (C_in)
    c_in = find_non_zero_color(input_grid)

    # Handle the case where the input grid might be all zeros
    if c_in == 0:
         # According to the pattern (0 maps to C_out, C_in maps to 0),
         # if C_in is 0, maybe the output should be all 0s?
         # Or maybe there's a default C_out? Let's assume all 0s output for now.
         return [[0 for _ in range(cols)] for _ in range(rows)]


    # 2. Determine Output Color (C_out)
    c_out = map_color(c_in)

    # 3. Construct Output Grid
    # Initialize an output grid of the same size, perhaps with zeros
    output_grid = [[0 for _ in range(cols)] for _ in range(rows)]

    # 4. Populate Output Grid
    for r in range(rows):
        for c in range(cols):
            # If the input cell is 0, set the output cell to C_out
            if input_grid[r][c] == 0:
                output_grid[r][c] = c_out
            # If the input cell is C_in, set the output cell to 0
            elif input_grid[r][c] == c_in:
                output_grid[r][c] = 0
            # Handle unexpected values if necessary (though examples don't show this)
            else:
                 print(f"Warning: Unexpected value {input_grid[r][c]} at ({r},{c}). Setting output to 0.")
                 output_grid[r][c] = 0 # Or handle differently

    return output_grid