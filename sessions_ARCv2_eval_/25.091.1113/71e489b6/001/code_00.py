import numpy as np

def transform(input_grid):
    """
    Transforms the input grid based on the following rule:
    1. Identify black pixels (0) that are completely surrounded by blue pixels (1), 
       considering all 8 neighbors (including diagonals).
    2. For each such identified black pixel, change the color of its surrounding blue neighbors 
       within the 3x3 area centered on the black pixel to orange (7) in the output grid.
    3. The central black pixel itself remains black.
    4. All other pixels retain their original color.
    """
    
    # Convert input to numpy array for easier manipulation and copying
    input_np = np.array(input_grid, dtype=int)
    # Initialize output_grid as a copy of the input grid
    output_grid = input_np.copy()
    
    rows, cols = input_np.shape

    # Iterate through each pixel of the input grid
    for r in range(rows):
        for c in range(cols):
            # Check if the current pixel is black (0)
            if input_np[r, c] == 0:
                is_isolated_defect = True
                neighbor_count = 0 # Count how many valid neighbors exist

                # Check all 8 neighbors (including diagonals)
                for dr in range(-1, 2):
                    for dc in range(-1, 2):
                        # Skip the center pixel itself
                        if dr == 0 and dc == 0:
                            continue

                        nr, nc = r + dr, c + dc

                        # Check if the neighbor is within grid boundaries
                        if 0 <= nr < rows and 0 <= nc < cols:
                            neighbor_count += 1
                            # If any neighbor is NOT blue (1), this black pixel is not isolated
                            if input_np[nr, nc] != 1:
                                is_isolated_defect = False
                                break # No need to check further neighbors for this pixel
                    if not is_isolated_defect:
                        break # Exit outer loop as well
                
                # Also ensure there was at least one neighbor (handles 1x1 grids or edge cases if needed, although problem constraints likely prevent 1x1 black pixels surrounded by blue)
                if neighbor_count == 0:
                     is_isolated_defect = False
                     
                # If the black pixel is an isolated defect (all existing neighbors are blue)
                if is_isolated_defect:
                    # Apply the color change to the blue neighbors in the output grid
                    for dr in range(-1, 2):
                        for dc in range(-1, 2):
                            # Skip the center pixel itself
                            if dr == 0 and dc == 0:
                                continue

                            nr, nc = r + dr, c + dc

                            # Check if the neighbor is within bounds AND was originally blue
                            if 0 <= nr < rows and 0 <= nc < cols and input_np[nr, nc] == 1:
                                # Change the color in the output grid to orange (7)
                                output_grid[nr, nc] = 7

    # Return the modified grid as a list of lists if needed, otherwise numpy array is fine for ARC
    # return output_grid.tolist() 
    return output_grid