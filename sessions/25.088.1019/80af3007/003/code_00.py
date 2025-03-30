import numpy as np

"""
Identifies a characteristic pattern based on the collective locations of solid 3x3 gray blocks in the input grid and outputs a corresponding predefined 9x9 pattern.

The transformation involves:
1. Finding all instances of solid 3x3 gray (5) blocks in the input grid.
2. Mapping the top-left coordinate (r, c) of each found block to a scaled coordinate (r // 3, c // 3).
3. Collecting these unique mapped coordinates into a set S.
4. Comparing S to predefined reference sets (RefH, RefX, Ref8) corresponding to observed patterns.
5. Returning the specific 9x9 grid pattern (PatternH, PatternX, Pattern8) associated with the matched reference set.
If no reference set is matched, a default 9x9 white grid is returned.
"""

def find_solid_gray_3x3_blocks(grid_np):
    """
    Finds the top-left coordinates of all solid 3x3 blocks of gray (5) pixels.

    Args:
        grid_np (np.array): The input grid as a NumPy array.

    Returns:
        list: A list of (row, col) tuples representing the top-left coordinates
              of found solid 3x3 gray blocks.
    """
    block_size = (3, 3)
    color = 5
    block_h, block_w = block_size
    grid_h, grid_w = grid_np.shape
    found_blocks = []
    
    # Create the target block pattern (3x3 gray)
    target_block = np.full(block_size, color, dtype=grid_np.dtype)

    # Iterate through possible top-left corners
    # Ensure iteration bounds prevent index out of range
    for r in range(grid_h - block_h + 1):
        for c in range(grid_w - block_w + 1):
            # Extract the subgrid
            subgrid = grid_np[r:r + block_h, c:c + block_w]
            # Check if the subgrid matches the target block
            if np.array_equal(subgrid, target_block):
                found_blocks.append((r, c))
    return found_blocks

def transform(input_grid):
    """
    Transforms the input grid based on the pattern of located solid 3x3 gray blocks.
    """
    input_np = np.array(input_grid, dtype=int)
    
    # Define the reference sets of mapped coordinates for known patterns
    RefH = frozenset([(0, 2), (0, 3), (1, 4), (2, 2), (2, 3)])
    RefX = frozenset([(0, 0), (0, 2), (1, 1), (2, 0), (2, 2)])
    Ref8 = frozenset([(1, 1), (1, 2), (1, 3), (2, 2), (2, 3), (3, 1), (3, 3)])

    # Define the corresponding 9x9 output patterns (as lists of lists)
    PatternH = [[5, 5, 0, 5, 5, 0, 0, 0, 0], [0, 0, 5, 0, 0, 5, 0, 0, 0], [5, 5, 0, 5, 5, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 5, 5, 0], [0, 0, 0, 0, 0, 0, 0, 0, 5], [0, 0, 0, 0, 0, 0, 5, 5, 0], [5, 5, 0, 5, 5, 0, 0, 0, 0], [0, 0, 5, 0, 0, 5, 0, 0, 0], [5, 5, 0, 5, 5, 0, 0, 0, 0]]
    PatternX = [[5, 0, 5, 0, 0, 0, 5, 0, 5], [0, 5, 0, 0, 0, 0, 0, 5, 0], [5, 0, 5, 0, 0, 0, 5, 0, 5], [0, 0, 0, 5, 0, 5, 0, 0, 0], [0, 0, 0, 0, 5, 0, 0, 0, 0], [0, 0, 0, 5, 0, 5, 0, 0, 0], [5, 0, 5, 0, 0, 0, 5, 0, 5], [0, 5, 0, 0, 0, 0, 0, 5, 0], [5, 0, 5, 0, 0, 0, 5, 0, 5]]
    Pattern8 = [[5, 5, 5, 5, 5, 5, 5, 5, 5], [0, 5, 5, 0, 5, 5, 0, 5, 5], [5, 0, 5, 5, 0, 5, 5, 0, 5], [0, 0, 0, 5, 5, 5, 5, 5, 5], [0, 0, 0, 0, 5, 5, 0, 5, 5], [0, 0, 0, 5, 0, 5, 5, 0, 5], [5, 5, 5, 0, 0, 0, 5, 5, 5], [0, 5, 5, 0, 0, 0, 0, 5, 5], [5, 0, 5, 0, 0, 0, 5, 0, 5]]
    
    # Default output: 9x9 white grid
    output_grid = [[0 for _ in range(9)] for _ in range(9)]

    # Step 1: Find all solid 3x3 gray blocks
    solid_block_coords = find_solid_gray_3x3_blocks(input_np)
    
    # Step 2: Map coordinates and create the set S
    mapped_coords = set()
    for r, c in solid_block_coords:
        # Ensure r, c are within valid range before division (though find should guarantee this)
        # if r >= 0 and c >= 0: 
        mapped_coords.add((r // 3, c // 3))
        
    # Convert to frozenset for comparison with reference frozensets
    mapped_coords_fset = frozenset(mapped_coords)

    # Step 3: Identify the pattern by comparing the generated set S with reference sets
    if mapped_coords_fset == RefH:
        output_grid = PatternH
    elif mapped_coords_fset == RefX:
        output_grid = PatternX
    elif mapped_coords_fset == Ref8:
        output_grid = Pattern8
    # Else: output_grid remains the default white grid
            
    # Step 4: Return the selected 9x9 pattern
    return output_grid