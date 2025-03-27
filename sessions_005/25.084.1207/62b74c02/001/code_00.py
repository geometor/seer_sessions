import numpy as np

"""
For each row in the input grid, identify the initial contiguous block of non-white pixels starting from the left edge. Let the width of this block be 'W'. The transformation fills the remaining part of the row (originally white pixels from column W onwards) based on the pattern found in the initial block. 
The filling pattern consists of repetitions of the first color (C0) of the initial block, followed by the rest of the colors (C1 to C(W-1)) from the initial block. The number of repetitions of C0 is calculated to fill the exact space available between the end of the initial block and the start of the appended suffix (C1 to C(W-1)). The initial block itself (columns 0 to W-1) remains unchanged in the output.
"""

def find_pattern_width(input_grid):
    """
    Determines the width 'W' of the initial non-white pattern block.
    W is the index of the first column consisting entirely of white pixels (0).
    If no such column exists, W is the grid width.
    """
    height, width = input_grid.shape
    for w in range(width):
        # Check if all pixels in the current column are white (0)
        if np.all(input_grid[:, w] == 0):
            return w
    # If no all-white column is found, the pattern spans the entire width
    return width

def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid by filling the white space to the right of 
    an initial pattern based on the colors within that pattern for each row.

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A numpy array representing the transformed output grid.
    """
    # Get grid dimensions
    height, width = input_grid.shape
    
    # Create a copy of the input grid to modify; this preserves the initial pattern
    output_grid = np.copy(input_grid)
    
    # Determine the width 'W' of the initial non-white pattern block
    # This assumes W is consistent across all rows based on the examples,
    # defined by the first column that is *entirely* white.
    W = find_pattern_width(input_grid)

    # If W is 0 (grid starts with white) or W equals width (no white space to fill),
    # return the original grid (or the copy)
    if W == 0 or W == width:
        return output_grid

    # Iterate through each row to apply the transformation
    for r in range(height):
        # Extract the initial pattern from the current row
        pattern = input_grid[r, :W].tolist() # Convert to list for easier manipulation
        
        # If the pattern is empty (shouldn't happen if W > 0), skip
        if not pattern:
            continue
            
        # Get the first color (C0) and the suffix pattern (C1 to C(W-1))
        C0 = pattern[0]
        suffix = pattern[1:] # This will be empty if W=1
        suffix_len = len(suffix)
        
        # Calculate the total length of the area to be filled
        fill_area_len = width - W
        
        # Calculate the number of times C0 needs to be repeated
        # Ensure it's not negative, though the logic implies it shouldn't be
        num_repeats = max(0, fill_area_len - suffix_len)
        
        # Construct the sequence to fill the white space
        fill_sequence = [C0] * num_repeats + suffix
        
        # Ensure the fill sequence has the correct length before assignment
        # This acts as a safeguard, though ideally fill_area_len == len(fill_sequence)
        if len(fill_sequence) == fill_area_len:
             # Place the fill sequence into the output grid starting at column W
            output_grid[r, W:] = fill_sequence
        else:
            # Handle potential length mismatch (e.g., truncate or pad if necessary, 
            # though based on the logic it should fit perfectly)
            # For now, let's assume perfect fit based on observed pattern.
            # If errors occur, this is where to debug length calculations.
            # print(f"Warning: Row {r} fill sequence length mismatch. Expected {fill_area_len}, got {len(fill_sequence)}")
            # Truncate or pad to fit:
            output_grid[r, W:] = fill_sequence[:fill_area_len]


    return output_grid