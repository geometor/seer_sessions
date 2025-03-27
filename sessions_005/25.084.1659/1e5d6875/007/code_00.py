import numpy as np

"""
Transforms the input grid pixel by pixel based on local neighborhood rules. 
Specifically, it changes the color of orange (7) pixels depending on whether they have adjacent red (2) or gray (5) neighbors (using 8-way adjacency).

1. Iterate through each pixel of the input grid.
2. If the pixel is orange (7):
    a. Check its 8 neighbors (up, down, left, right, and diagonals).
    b. If any neighbor is red (2), change the corresponding output pixel to green (3).
    c. Else if any neighbor is gray (5), change the corresponding output pixel to yellow (4).
    d. If the orange pixel has neither red nor gray neighbors, it remains orange (7) in the output.
3. If the pixel is not orange (7), its color remains unchanged in the output grid.
"""

def transform(input_grid):
    """
    Applies a pixel-by-pixel color transformation based on neighbor colors.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input to numpy array for efficient neighbor checking
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_np)

    # Iterate through each pixel in the grid
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is orange
            if input_np[r, c] == 7:
                found_red_neighbor = False
                found_gray_neighbor = False

                # Check all 8 neighbors (including diagonals)
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        # Skip the pixel itself
                        if dr == 0 and dc == 0:
                            continue
                        
                        # Calculate neighbor coordinates
                        nr, nc = r + dr, c + dc

                        # Check if the neighbor is within grid bounds
                        if 0 <= nr < height and 0 <= nc < width:
                            neighbor_color = input_np[nr, nc]
                            
                            # Check for red neighbor (priority)
                            if neighbor_color == 2: # red
                                found_red_neighbor = True
                                break # Red found, no need to check further neighbors for this pixel
                            # Check for gray neighbor (only if red not found yet)
                            elif neighbor_color == 5: # gray
                                found_gray_neighbor = True
                                # Continue checking other neighbors in case a red one exists
                                
                    # If red was found in the inner loop, break the outer loop too
                    if found_red_neighbor:
                        break

                # Apply the color change rule based on found neighbors
                if found_red_neighbor:
                    output_grid[r, c] = 3 # Change to green
                elif found_gray_neighbor:
                    output_grid[r, c] = 4 # Change to yellow
                # Else: it remains orange (7) as it was initially copied

    # Convert the result back to a list of lists before returning
    return output_grid.tolist()