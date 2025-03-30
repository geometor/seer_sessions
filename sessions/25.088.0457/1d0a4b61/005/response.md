```python
import numpy as np

"""
Reconstructs a complete, repeating pattern within a bordered area, using noisy 
observations from the input grid.

1.  Input Analysis: Verifies grid dimensions (>= 3x3) and the presence of a 
    solid blue (1) 1-pixel border.
2.  Isolate Interior: Extracts the subgrid excluding the border.
3.  Determine Pattern Period: Analyzes the non-white pixels within the interior 
    to find the smallest repeating rectangular unit (pattern tile) of height `p_h` 
    and width `p_w`. A period (ph, pw) is valid if all non-white pixels 
    `input[r, c]` corresponding to the same relative position `(r % ph, c % pw)` 
    within the tile have the same color. The smallest valid period is chosen.
4.  Reconstruct Pattern Tile: Creates a `p_h` x `p_w` tile initialized to white (0). 
    Populates it by iterating through the input interior: if `input[r, c]` is 
    non-white, its color is placed at `pattern_tile[r % p_h, c % p_w]`.
5.  Construct Output Grid: Creates a new grid of the same size as the input.
6.  Draw Border: Fills the 1-pixel border with blue (1).
7.  Tile Interior: Fills the output grid's interior by tiling the reconstructed 
    `pattern_tile`. The color for `output[r, c]` (where `1 <= r < H-1`, 
    `1 <= c < W-1`) is taken from `pattern_tile[(r-1) % p_h, (c-1) % p_w]`.
8.  Return: Returns the completed output grid.
"""

def determine_pattern_period(interior_grid):
    """
    Determines the smallest valid pattern period (height, width) for the interior.

    Args:
        interior_grid: A numpy array representing the grid inside the border.

    Returns:
        A tuple (p_h, p_w) representing the period height and width, 
        or None if no valid period is found.
    """
    interior_h, interior_w = interior_grid.shape
    if interior_h == 0 or interior_w == 0:
        return None # No interior to find a pattern in

    # Iterate through all possible period dimensions (ph, pw)
    for ph in range(1, interior_h + 1):
        for pw in range(1, interior_w + 1):
            # Check if this period (ph, pw) is valid
            pattern_check = {}  # Stores {(pr, pc): color}
            valid_period = True
            for r in range(interior_h):
                for c in range(interior_w):
                    color = interior_grid[r, c]
                    if color != 0:  # Only check non-white pixels
                        pr, pc = r % ph, c % pw
                        if (pr, pc) in pattern_check:
                            # Check for color conflict at this pattern position
                            if pattern_check[(pr, pc)] != color:
                                valid_period = False
                                break # Conflict found, try next period width
                        else:
                            # First time seeing a color for this pattern position
                            pattern_check[(pr, pc)] = color
                if not valid_period:
                    break # Conflict found, try next period width
            
            # If no conflicts were found for this (ph, pw)
            if valid_period:
                # This is the smallest valid period found so far
                return ph, pw
                
    # Should ideally always find a period (at worst, the full interior size)
    # If the loop completes without returning, it implies an issue or 
    # an empty interior which was handled earlier.
    # However, to be safe, return None if no period is explicitly found.
    return None 

def reconstruct_pattern_tile(interior_grid, p_h, p_w):
    """
    Reconstructs the clean pattern tile based on the determined period.

    Args:
        interior_grid: A numpy array representing the grid inside the border.
        p_h: The determined pattern height.
        p_w: The determined pattern width.

    Returns:
        A numpy array representing the p_h x p_w clean pattern tile.
    """
    # Initialize tile with white (0)
    pattern_tile = np.zeros((p_h, p_w), dtype=int)
    interior_h, interior_w = interior_grid.shape

    # Iterate through the interior grid
    for r in range(interior_h):
        for c in range(interior_w):
            color = interior_grid[r, c]
            # If the pixel is not white, place it onto the pattern tile
            if color != 0:
                pr = r % p_h
                pc = c % p_w
                # Overwrite is fine because determine_pattern_period ensured consistency
                pattern_tile[pr, pc] = color
                
    return pattern_tile

def transform(input_grid_list):
    """
    Transforms the input grid according to the reconstruction logic.

    Args:
        input_grid_list: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
        
    Raises:
        ValueError: If grid dimensions are too small, border is incorrect, 
                    or pattern period cannot be determined.
    """
    # Convert to numpy array for easier manipulation
    input_grid = np.array(input_grid_list, dtype=int)
    H, W = input_grid.shape

    # --- Step 1: Input Analysis ---
    if H < 3 or W < 3:
        raise ValueError(f"Grid dimensions ({H}x{W}) too small. Must be at least 3x3.")

    # Check border (assuming it must be solid blue color 1)
    border_pixels = np.concatenate([
        input_grid[0, :], input_grid[-1, :], 
        input_grid[1:-1, 0], input_grid[1:-1, -1]
    ])
    if not np.all(border_pixels == 1):
        raise ValueError("Input grid border is not uniformly blue (1).")

    # --- Step 2: Isolate Interior ---
    interior_grid = input_grid[1:-1, 1:-1]
    interior_h, interior_w = interior_grid.shape

    # --- Step 3: Determine Pattern Period ---
    period = determine_pattern_period(interior_grid)
    if period is None:
        # This case might occur if the interior is empty or if logic failed
        raise ValueError(f"Could not determine pattern period for interior size {interior_h}x{interior_w}.")
    p_h, p_w = period
    
    # --- Step 4: Reconstruct Pattern Tile ---
    clean_pattern_tile = reconstruct_pattern_tile(interior_grid, p_h, p_w)

    # --- Step 5: Construct Output Grid ---
    output_grid = np.zeros_like(input_grid)

    # --- Step 6: Draw Border ---
    output_grid[0, :] = 1
    output_grid[H-1, :] = 1
    output_grid[:, 0] = 1
    output_grid[:, W-1] = 1

    # --- Step 7: Tile Interior ---
    # Iterate through the output grid's interior positions
    for r in range(1, H - 1):
        for c in range(1, W - 1):
            # Calculate corresponding position in the pattern tile
            # Use (r-1) and (c-1) because tile coordinates relate to the interior top-left (1,1)
            pr = (r - 1) % p_h
            pc = (c - 1) % p_w
            # Assign color from the clean pattern tile
            output_grid[r, c] = clean_pattern_tile[pr, pc]

    # --- Step 8: Return ---
    # Convert back to list of lists for the required output format
    return output_grid.tolist()
```