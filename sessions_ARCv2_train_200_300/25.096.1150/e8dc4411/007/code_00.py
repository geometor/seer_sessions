import numpy as np
from collections import Counter

"""
Transforms the input grid by identifying a source cell, a background color, and a reference zero cell. 
Two directions are determined: a primary diagonal direction (D1) away from the zero cell, and a secondary axis-aligned direction (D2') derived from D1. 
Two rays are drawn starting from the source cell, one in direction D1 and one in direction D2'. 
A ray colors cells with the source color only if the cell is within bounds and its color in the *original* input grid was the background color. 
The ray stops extending if it hits the grid boundary or a non-background cell. The original grid content (source, zeros, etc.) remains otherwise unchanged.
"""

# === Helper Functions ===

def find_background_color(grid: np.ndarray) -> int:
    """Identifies the most frequent color in the grid, assumed to be the background."""
    counts = Counter(grid.flatten())
    if not counts:
        raise ValueError("Grid is empty, cannot determine background color.")
    # Ensure the background color is returned as a standard Python int
    background_color = int(counts.most_common(1)[0][0])
    return background_color

def find_source_cell(grid: np.ndarray, background_color: int) -> tuple[int, int, int]:
    """Finds the unique cell that is not the background color and not zero."""
    source_candidates = []
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            color = grid[r, c]
            if color != background_color and color != 0:
                # Store row, col, and color as standard Python ints
                source_candidates.append((r, c, int(color)))
    
    if len(source_candidates) == 0:
         raise ValueError("No source cell found (non-background, non-zero).")
    if len(source_candidates) > 1:
         # Based on examples, uniqueness is expected. If not unique, use the first found.
         print(f"Warning: Expected 1 source cell, found {len(source_candidates)}. Using the first one: {source_candidates[0]}")

    return source_candidates[0] # (row, col, color)

def find_any_zero_cell(grid: np.ndarray) -> tuple[int, int]:
    """Finds the location of any cell containing zero."""
    zero_locations = np.where(grid == 0)
    if len(zero_locations[0]) == 0:
         raise ValueError("No zero cell found.")
    
    # Return the coordinates of the first zero cell found as standard Python ints
    return int(zero_locations[0][0]), int(zero_locations[1][0]) # (row, col)

def draw_ray(input_grid: np.ndarray, output_grid: np.ndarray, 
             start_r: int, start_c: int, dr: int, dc: int, 
             source_color: int, background_color: int):
    """Draws a ray from the start position in the given direction."""
    rows, cols = input_grid.shape
    current_r, current_c = start_r, start_c
    
    while True:
        # Calculate next position
        next_r = current_r + dr
        next_c = current_c + dc
        
        # Check boundaries
        if not (0 <= next_r < rows and 0 <= next_c < cols):
            break # Stop if out of bounds
            
        # Check color condition in the *original* grid
        if input_grid[next_r, next_c] != background_color:
            break # Stop if not background color
            
        # Draw on the output grid
        output_grid[next_r, next_c] = source_color
        
        # Update current position for the next step
        current_r, current_c = next_r, next_c


# === Main Transformation Function ===

def transform(input_grid_list: list[list[int]]) -> list[list[int]]:
    """
    Applies the two-ray drawing transformation based on source, zero, and background cells.
    """
    # Convert input list to numpy array for efficient operations
    input_grid = np.array(input_grid_list, dtype=int)
    
    # Handle empty grid edge case
    if input_grid.size == 0:
        return [] 
        
    rows, cols = input_grid.shape
    
    # Create a copy of the input grid to modify for the output
    output_grid = np.copy(input_grid)

    try:
        # 1. Identify key elements
        background_color = find_background_color(input_grid)
        source_row, source_col, source_color = find_source_cell(input_grid, background_color)
        zero_row, zero_col = find_any_zero_cell(input_grid)

        # 2. Determine primary diagonal direction (D1)
        # Vector points away from zero relative to source
        delta_r = source_row - zero_row
        delta_c = source_col - zero_col
        d1_dr = int(np.sign(delta_r)) # Primary row step
        d1_dc = int(np.sign(delta_c)) # Primary col step
        
        # Check if D1 is non-diagonal (not expected based on examples)
        if d1_dr == 0 or d1_dc == 0:
             print(f"Warning: Calculated D1 ({d1_dr},{d1_dc}) is not strictly diagonal. Source=({source_row},{source_col}), Zero=({zero_row},{zero_col}). Results might be unexpected.")
             # Proceeding anyway, ray drawing might just stop early or work correctly

        # 3. Determine secondary axis-aligned direction (D2') based on D1
        d2_dr, d2_dc = 0, 0 # Initialize secondary steps
        if d1_dr == 1:
            d2_dr = 1  # Secondary step is Down
            d2_dc = 0
        elif d1_dr == -1:
            d2_dr = 0  # Secondary step is horizontal
            d2_dc = d1_dc # Match horizontal direction of D1
        else: # d1_dr is 0 (vertical alignment of source and zero)
             # This case needs a defined rule. Examples don't cover it.
             # Let's assume if vertically aligned, D2' also goes horizontally like D1's horizontal component.
             print(f"Warning: Vertical alignment detected (D1=({d1_dr},{d1_dc})). D2' calculation might be incorrect.")
             d2_dr = 0
             d2_dc = d1_dc # Use D1's horizontal component (could be 0 if source == zero)
             if d2_dc == 0: # Source and zero at same location - error state
                 raise ValueError("Source and Zero cells are at the same location or D1 is (0,0). Cannot determine directions.")


        # 4. Draw the two rays starting from the source cell
        # Draw ray using D1
        draw_ray(input_grid, output_grid, source_row, source_col, d1_dr, d1_dc, source_color, background_color)
        
        # Draw ray using D2'
        draw_ray(input_grid, output_grid, source_row, source_col, d2_dr, d2_dc, source_color, background_color)

    except ValueError as e:
        # Handle errors during element identification or direction calculation
        print(f"Error during transformation: {e}. Returning original grid.")
        # Return the original grid (converted back to list) if setup fails
        return input_grid.tolist()

    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()