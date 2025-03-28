```python
"""
Simulate a gravity-like effect where non-red, non-white objects 'fall' towards 
a static red object until they hit the red object, another object, or the 
grid boundary. The direction of 'gravity' is determined by the relative 
position of the red object(s) compared to the other colored objects. If the red 
object is predominantly below the others, gravity is downwards. If it's to the 
left, gravity is leftwards. If it's to the right, gravity is rightwards. 
Objects move one step at a time iteratively until no object can move further.
"""

import numpy as np

def determine_direction(grid):
    """
    Determines the direction of movement based on the relative positions of
    red (2) pixels and other non-white (0) pixels.
    Returns: tuple (delta_row, delta_col) representing the direction vector.
             (1, 0) for down, (0, -1) for left, (0, 1) for right.
             Returns (0, 0) if direction cannot be determined or no movement needed.
    """
    height, width = grid.shape
    red_pixels = np.argwhere(grid == 2)
    other_pixels = np.argwhere((grid != 0) & (grid != 2))

    if red_pixels.size == 0 or other_pixels.size == 0:
        return (0, 0) # No barrier or nothing to move

    # Calculate average positions
    red_r_avg = np.mean(red_pixels[:, 0])
    red_c_avg = np.mean(red_pixels[:, 1])
    other_r_avg = np.mean(other_pixels[:, 0])
    other_c_avg = np.mean(other_pixels[:, 1])

    # Compare average positions to determine dominant direction
    # Check vertical difference primarily first, then horizontal
    if red_r_avg > other_r_avg + 0.5: # Red is significantly below others
         # Check if red spans horizontally more than vertically, reinforcing 'down'
         red_height = np.max(red_pixels[:, 0]) - np.min(red_pixels[:, 0]) + 1
         red_width = np.max(red_pixels[:, 1]) - np.min(red_pixels[:, 1]) + 1
         if red_width >= red_height or red_r_avg > height * 0.6 : # Bias towards down if low
             return (1, 0) # Down
             
    # Check horizontal only if vertical wasn't conclusive or red isn't clearly below
    if red_c_avg < other_c_avg - 0.5: # Red is significantly left of others
        # Check if red spans vertically more than horizontally, reinforcing 'left'
        red_height = np.max(red_pixels[:, 0]) - np.min(red_pixels[:, 0]) + 1
        red_width = np.max(red_pixels[:, 1]) - np.min(red_pixels[:, 1]) + 1
        if red_height >= red_width or red_c_avg < width * 0.4: # Bias towards left if far left
            return (0, -1) # Left
            
    if red_c_avg > other_c_avg + 0.5: # Red is significantly right of others
         # Check if red spans vertically more than horizontally, reinforcing 'right'
         red_height = np.max(red_pixels[:, 0]) - np.min(red_pixels[:, 0]) + 1
         red_width = np.max(red_pixels[:, 1]) - np.min(red_pixels[:, 1]) + 1
         if red_height >= red_width or red_c_avg > width * 0.6: # Bias towards right if far right
             return (0, 1) # Right

    # Fallback / edge cases - e.g., objects surrounding barrier
    # Use boundary proximity if averages are close
    if np.any(red_pixels[:,0] == height - 1) and not np.any(red_pixels[:,0] == 0): return (1, 0) # Down if red touches bottom
    if np.any(red_pixels[:,1] == 0) and not np.any(red_pixels[:,1] == width - 1): return (0, -1) # Left if red touches left
    if np.any(red_pixels[:,1] == width - 1) and not np.any(red_pixels[:,0] == 0): return (0, 1) # Right if red touches right
        
    return (0, 0) # Default to no movement if unclear


def transform(input_grid):
    """
    Applies a gravity-like transformation to the input grid. Non-red, non-white
    pixels move towards the static red pixels until blocked.
    Args:
        input_grid (list[list[int]]): The input grid.
    Returns:
        list[list[int]]: The transformed grid.
    """
    # Convert to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    height, width = grid.shape
    
    # Determine the direction of movement
    delta_r, delta_c = determine_direction(grid)

    # If no direction determined, return the original grid
    if delta_r == 0 and delta_c == 0:
        return grid.tolist()

    # Simulation loop: continue as long as any pixel moves
    while True:
        moved_in_iteration = False
        pixels_to_move = [] # Store (old_r, old_c, new_r, new_c)

        # Determine iteration order based on direction to handle dependencies correctly
        # Process pixels that are "further away" from the barrier first in the direction of movement
        if delta_r == 1: # Down
            row_indices = range(height - 2, -1, -1) # Bottom-up (excluding last row)
            col_indices = range(width)
        elif delta_c == -1: # Left
            row_indices = range(height)
            col_indices = range(1, width) # Right-to-left (excluding first column)
        elif delta_c == 1: # Right
            row_indices = range(height)
            col_indices = range(width - 2, -1, -1) # Left-to-right (excluding last column)
        else: # Should not happen if direction is determined, but handle defensively
             row_indices = range(height)
             col_indices = range(width)

        # Iterate through potentially moving pixels
        for r in row_indices:
            for c in col_indices:
                pixel_color = grid[r, c]
                
                # Check if the pixel is a movable object (non-white, non-red)
                if pixel_color != 0 and pixel_color != 2:
                    # Calculate potential next position
                    next_r, next_c = r + delta_r, c + delta_c

                    # Check if the next position is valid
                    # 1. Within grid boundaries
                    if 0 <= next_r < height and 0 <= next_c < width:
                        # 2. The target cell is currently empty (white)
                        if grid[next_r, next_c] == 0:
                            # Mark this pixel for movement
                            pixels_to_move.append((r, c, next_r, next_c))
                            moved_in_iteration = True
                        # Else: Blocked by boundary, red barrier, or another object
                    # Else: Blocked by grid boundary

        # If no pixels moved in this iteration, the simulation is stable
        if not moved_in_iteration:
            break

        # Apply the movements for this iteration
        # Important: Clear old positions first, then fill new ones to avoid conflicts within the same step
        
        # Store colors before clearing
        move_details = []
        for r, c, nr, nc in pixels_to_move:
             move_details.append({'color': grid[r,c], 'nr': nr, 'nc': nc})
        
        # Clear old positions
        for r, c, _, _ in pixels_to_move:
            grid[r, c] = 0
            
        # Fill new positions
        for move in move_details:
             grid[move['nr'], move['nc']] = move['color']


    # Convert the final numpy array back to a list of lists
    output_grid = grid.tolist()
    return output_grid

```