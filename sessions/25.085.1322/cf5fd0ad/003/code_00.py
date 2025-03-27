import numpy as np

"""
Transforms a 3x3 input grid into a 12x12 output grid.
The transformation involves creating four distinct 3x3 tiles derived from the input:
1. Tile A: Input grid rotated 180 degrees.
2. Tile B: A specific rearrangement of input pixels where the first row is the reverse of the input's first row, the second row uses pixels (2,1), (1,1), (1,0), and the third row uses pixels (2,2), (1,2), (2,0).
3. Tile C: Another specific rearrangement where the first row uses pixels (2,0), (1,2), (2,2), the second row uses pixels (1,0), (1,1), (2,1), and the third row is a copy of the input's first row.
4. Tile D: The input grid itself (identity transformation).

These four tiles are then arranged in a 2x2 meta-pattern to fill the 12x12 output grid.
Each quadrant of the output grid (6x6) is composed of a 2x2 arrangement of one type of tile.
- Top-left 6x6 quadrant: Tiled with Tile A.
- Top-right 6x6 quadrant: Tiled with Tile B.
- Bottom-left 6x6 quadrant: Tiled with Tile C.
- Bottom-right 6x6 quadrant: Tiled with Tile D.

Input Grid Indices (I):
[[I(0,0), I(0,1), I(0,2)],
 [I(1,0), I(1,1), I(1,2)],
 [I(2,0), I(2,1), I(2,2)]]

Tile A (Rotate 180):
[[I(2,2), I(2,1), I(2,0)],
 [I(1,2), I(1,1), I(1,0)],
 [I(0,2), I(0,1), I(0,0)]]

Tile B (Custom 1 - Corrected):
[[I(0,2), I(0,1), I(0,0)],  # Reversed input row 0
 [I(2,1), I(1,1), I(1,0)],  # Pixels H, E, D
 [I(2,2), I(1,2), I(2,0)]]   # Pixels I, F, G

Tile C (Custom 2):
[[I(2,0), I(1,2), I(2,2)],  # Pixels G, F, I
 [I(1,0), I(1,1), I(2,1)],  # Pixels D, E, H
 [I(0,0), I(0,1), I(0,2)]]   # Input row 0

Tile D (Identity):
[[I(0,0), I(0,1), I(0,2)],
 [I(1,0), I(1,1), I(1,2)],
 [I(2,0), I(2,1), I(2,2)]]
"""

# Helper function for 180 rotation
def _rotate_180(grid):
    """Rotates a 3x3 numpy array by 180 degrees."""
    return np.rot90(grid, 2)

# Helper function for Transform B (Corrected)
def _transform_b(grid):
    """Applies the specific pixel rearrangement for Tile B."""
    new_grid = np.zeros_like(grid)
    # Row 0: Reversed input row 0
    new_grid[0, :] = grid[0, ::-1]
    # Row 1: Pixels from input H, E, D -> (2,1), (1,1), (1,0)
    new_grid[1, :] = [grid[2, 1], grid[1, 1], grid[1, 0]]
    # Row 2: Pixels from input I, F, G -> (2,2), (1,2), (2,0)
    new_grid[2, :] = [grid[2, 2], grid[1, 2], grid[2, 0]]
    return new_grid

# Helper function for Transform C
def _transform_c(grid):
    """Applies the specific pixel rearrangement for Tile C."""
    new_grid = np.zeros_like(grid)
    # Row 0: Pixels from input G, F, I -> (2,0), (1,2), (2,2)
    new_grid[0, :] = [grid[2, 0], grid[1, 2], grid[2, 2]]
    # Row 1: Pixels from input D, E, H -> (1,0), (1,1), (2,1)
    new_grid[1, :] = [grid[1, 0], grid[1, 1], grid[2, 1]]
    # Row 2: Copy input row 0
    new_grid[2, :] = grid[0, :]
    return new_grid

# Helper function for Identity (Transform D)
def _identity(grid):
    """Returns a copy of the input grid."""
    # Return a copy to avoid modifying the original if passed by reference elsewhere
    return grid.copy() 

def transform(input_grid):
    """
    Transforms the input 3x3 grid into a 12x12 grid based on tiling rules.

    Args:
        input_grid: A list of lists representing the 3x3 input grid.

    Returns:
        A list of lists representing the 12x12 output grid.
    """
    # Convert input list of lists to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    
    # Ensure input is 3x3 (optional check, based on task constraints)
    if input_np.shape != (3, 3):
        # Handle error or assume valid input based on ARC context
        # For ARC, inputs usually match expectations from training
        pass # Or raise ValueError("Input grid must be 3x3")

    # Generate the four transformed 3x3 tiles using helper functions
    tile_a = _rotate_180(input_np)
    tile_b = _transform_b(input_np) # Uses the corrected logic
    tile_c = _transform_c(input_np)
    tile_d = _identity(input_np) # Tile D is the original input
    
    # Define the dimensions
    tile_height, tile_width = 3, 3
    output_height, output_width = 12, 12
    quadrant_size = 6
    
    # Initialize the 12x12 output grid
    output_grid = np.zeros((output_height, output_width), dtype=int)
    
    # Tile the output grid quadrant by quadrant
    # Each quadrant is 6x6, containing a 2x2 arrangement of the corresponding tile
    
    # Iterate through the 2x2 arrangement within each quadrant
    for r_idx in range(2): # Tile row index within the 2x2 grid
        for c_idx in range(2): # Tile column index within the 2x2 grid
            # Calculate the top-left corner of the current tile placement
            r_start_tile = r_idx * tile_height
            c_start_tile = c_idx * tile_width

            # Place Tile A in Top-Left Quadrant
            output_grid[r_start_tile : r_start_tile + tile_height, 
                        c_start_tile : c_start_tile + tile_width] = tile_a
            
            # Place Tile B in Top-Right Quadrant (offset columns by quadrant_size)
            output_grid[r_start_tile : r_start_tile + tile_height, 
                        quadrant_size + c_start_tile : quadrant_size + c_start_tile + tile_width] = tile_b

            # Place Tile C in Bottom-Left Quadrant (offset rows by quadrant_size)
            output_grid[quadrant_size + r_start_tile : quadrant_size + r_start_tile + tile_height, 
                        c_start_tile : c_start_tile + tile_width] = tile_c
            
            # Place Tile D in Bottom-Right Quadrant (offset rows and columns by quadrant_size)
            output_grid[quadrant_size + r_start_tile : quadrant_size + r_start_tile + tile_height, 
                        quadrant_size + c_start_tile : quadrant_size + c_start_tile + tile_width] = tile_d
            
    # Convert the final numpy array back to a list of lists for the required output format
    return output_grid.tolist()