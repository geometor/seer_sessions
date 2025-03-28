import numpy as np

def find_wall_location(grid):
    """
    Determines the location of the 'wall' (block of red pixels) 
    based on which edge has the most red pixels.
    """
    H, W = grid.shape
    
    # Count red pixels (value 2) on each edge
    sum_bottom = np.sum(grid[H-1, :] == 2)
    sum_top = np.sum(grid[0, :] == 2)
    sum_left = np.sum(grid[:, 0] == 2)
    sum_right = np.sum(grid[:, W-1] == 2)
    
    sums = {
        'bottom': sum_bottom,
        'top': sum_top,
        'left': sum_left,
        'right': sum_right
    }
    
    # Find the edge with the maximum count
    # If all counts are 0, return None or a default
    if all(v == 0 for v in sums.values()):
        return None 
        
    wall_location = max(sums, key=sums.get)
    return wall_location

def transform(input_grid):
    """
    Identifies Azure (8) pixels and a Red (2) wall in the input grid.
    For each Azure pixel, it draws a diagonal Green (3) line starting 
    from the adjacent cell, moving away from the Red wall, until it 
    hits the grid boundary or a non-White (0) pixel.
    The original Azure and Red pixels remain unchanged.
    """
    
    # Convert input list of lists to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    H, W = input_np.shape
    
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_np)
    
    # Find coordinates of all Azure (8) pixels
    azure_pixels = np.argwhere(input_np == 8)
    
    # If there are no azure pixels, return the original grid
    if azure_pixels.size == 0:
        return output_grid.tolist()
        
    # Determine the location of the red wall
    wall_loc = find_wall_location(input_np)
    
    # If no wall is found, return the original grid (or handle as error/default)
    if wall_loc is None:
        # Based on examples, a wall seems required. If none, maybe no change?
        return output_grid.tolist() 
        
    # Determine the diagonal direction (dr, dc) based on the wall location
    # dr = change in row, dc = change in column
    if wall_loc == 'bottom':
        dr, dc = -1, 1  # Up-Right
    elif wall_loc == 'right':
        dr, dc = -1, -1 # Up-Left
    elif wall_loc == 'left':
        dr, dc = -1, 1  # Up-Right
    elif wall_loc == 'top':
        # Assumption based on symmetry, not seen in examples
        dr, dc = 1, 1   # Down-Right (Needs verification if top wall occurs) 
    else: 
        # Should not happen if wall_loc is one of the four or None
        return output_grid.tolist()

    # Iterate through each found Azure pixel
    for r, c in azure_pixels:
        # Calculate the starting position for the green line
        current_r, current_c = r + dr, c + dc
        
        # Draw the green line diagonally
        while 0 <= current_r < H and 0 <= current_c < W:
            # Check the corresponding cell in the *output* grid
            if output_grid[current_r, current_c] == 0: # If it's white
                output_grid[current_r, current_c] = 3 # Change it to green
                # Move to the next diagonal position
                current_r += dr
                current_c += dc
            else:
                # Stop if we hit a non-white pixel or the boundary (checked by while)
                break
                
    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()