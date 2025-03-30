import numpy as np
from typing import List

"""
Transformation Description:
The input grid consists of a background (white, 0), grid lines of a single color (e.g., red, blue, azure), and a unique 3x3 pattern located within one of the cells defined by the grid lines. The grid lines are 1 pixel thick and define 3x3 content cells, making a repeating 4x4 unit (3x3 content + 1 row/col of grid line).

The transformation identifies the 3x3 pattern and the row/column index of the cell it occupies in the input. It then determines the parity (even/odd) of this source cell's row and column index. 

The output grid maintains the same grid line structure as the input. The identified 3x3 pattern is replicated into all 3x3 content cells whose row and column indices have the *same parity* as the source cell's row and column indices, respectively. Cells not meeting this parity requirement retain the background color.
"""

def find_grid_and_pattern_params(grid_np):
    """
    Identifies grid line color, cell size, grid spacing, 
    and locates the unique pattern and its cell coordinates.
    Assumes a regular grid structure with 3x3 content cells and 1px lines.
    """
    height, width = grid_np.shape
    
    # Assume grid lines are at indices 3, 7, 11...
    # Grid line color can be inferred from these positions (assuming not background)
    grid_line_color = -1
    if height > 3 and grid_np[3, 0] != 0:
        grid_line_color = grid_np[3, 0]
    elif width > 3 and grid_np[0, 3] != 0:
        grid_line_color = grid_np[0, 3]
    else:
        # Fallback or error handling if grid is too small or unusual
        # For this problem, we can likely assume a valid grid structure
        # Let's check a few more points if the first ones were background (unlikely given examples)
         if height > 3 and width > 3:
            if grid_np[3,3] != 0: # Check a grid intersection point, might be the grid color
                 # Need to be careful this isn't the pattern color.
                 # Let's stick to checking the lines themselves first.
                 # A more robust way might be to find the most frequent non-background color on rows/cols 3, 7,...
                 pass # Simple assumption might be okay for ARC

    # Assuming background is 0
    background_color = 0
    
    # Cell dimensions based on problem description
    cell_content_size = (3, 3)
    grid_unit_size = (4, 4) # 3x3 content + 1px border

    num_cell_rows = height // grid_unit_size[0]
    num_cell_cols = width // grid_unit_size[1]

    pattern = None
    pattern_cell_row = -1
    pattern_cell_col = -1

    # Find the unique pattern and its location
    for r_cell in range(num_cell_rows):
        for c_cell in range(num_cell_cols):
            r_start = r_cell * grid_unit_size[0]
            c_start = c_cell * grid_unit_size[1]
            
            cell_content = grid_np[r_start:r_start + cell_content_size[0], 
                                   c_start:c_start + cell_content_size[1]]
            
            # Check if the cell contains anything other than the background
            if np.any(cell_content != background_color):
                pattern = cell_content
                pattern_cell_row = r_cell
                pattern_cell_col = c_cell
                break # Found the pattern
        if pattern is not None:
            break
            
    if pattern is None:
        raise ValueError("Pattern not found in input grid.")

    return pattern, pattern_cell_row, pattern_cell_col, grid_unit_size, cell_content_size, num_cell_rows, num_cell_cols


def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the pattern replication based on cell index parity.
    
    1. Identifies the grid structure (assuming 4x4 repeating units with 3x3 content cells).
    2. Locates the unique 3x3 pattern and its source cell's row/column index.
    3. Determines the parity (even/odd) of the source cell's indices.
    4. Creates an output grid by copying the input grid structure.
    5. Replicates the pattern into all cells whose row/column indices match the source parity.
    """
    input_np = np.array(input_grid, dtype=np.int8)
    output_np = np.copy(input_np) # Start with a copy to preserve grid lines

    # Get pattern, its location, and grid parameters
    try:
        pattern, pattern_cell_row, pattern_cell_col, grid_unit_size, cell_content_size, num_cell_rows, num_cell_cols = find_grid_and_pattern_params(input_np)
    except ValueError as e:
        print(f"Error processing grid: {e}")
        # Return input or empty grid? Returning input seems safer if pattern not found.
        return input_grid 

    # Determine the parity of the source cell
    source_row_parity = pattern_cell_row % 2
    source_col_parity = pattern_cell_col % 2

    # Iterate through all cells and place the pattern based on parity matching
    for r_cell in range(num_cell_rows):
        for c_cell in range(num_cell_cols):
            # Determine the parity of the current target cell
            target_row_parity = r_cell % 2
            target_col_parity = c_cell % 2

            # Calculate the top-left corner of the 3x3 content area for this cell
            r_start = r_cell * grid_unit_size[0]
            c_start = c_cell * grid_unit_size[1]
            
            # Check if the target cell's parity matches the source cell's parity
            if target_row_parity == source_row_parity and target_col_parity == source_col_parity:
                # Place the pattern in the output grid
                output_np[r_start:r_start + cell_content_size[0], 
                          c_start:c_start + cell_content_size[1]] = pattern
            else:
                 # Ensure non-target cells are background (already handled by copy if input was clean,
                 # but this makes it explicit and handles cases where input might have noise)
                 # Check if this cell IS NOT the original pattern cell before clearing
                 # (otherwise we might clear the pattern before copying it everywhere)
                 # Actually, starting with a copy of input is better. We only need to *place* the pattern.
                 # Grid lines and original background cells are preserved by the copy.
                 pass # No action needed for non-target cells if we started with a copy.


    return output_np.tolist()