import numpy as np
from collections import deque

"""
The transformation rule identifies the largest contiguous block of 'azure' (8) pixels and scattered non-'white', non-'azure' pixels ('projectors'). 
Each projector pixel casts its color orthogonally (horizontally or vertically) through 'white' (0) pixels onto the first 'azure' pixel it encounters within the largest azure block. 
The output grid reflects these color changes on the azure block, while the original projectors and unaffected azure pixels remain unchanged.
"""

def find_largest_object(grid, color):
    """Finds the coordinates of the largest contiguous object of a given color."""
    rows, cols = grid.shape
    visited = set()
    max_size = 0
    largest_object_coords = set()

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                current_size = 0
                current_object_coords = set()
                q = deque([(r, c)])
                visited.add((r, c))
                
                while q:
                    curr_r, curr_c = q.popleft()
                    current_object_coords.add((curr_r, curr_c))
                    current_size += 1
                    
                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc
                        
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                            
                if current_size > max_size:
                    max_size = current_size
                    largest_object_coords = current_object_coords
                    
    return largest_object_coords

def transform(input_grid):
    """
    Applies the projection transformation to the input grid.
    """
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    azure_color = 8
    white_color = 0

    # 1. Identify the largest contiguous block of 'azure' (8) pixels
    azure_block_coords = find_largest_object(input_grid, azure_color)
    if not azure_block_coords: # Handle cases with no azure block
        return output_grid

    # 2. Find all "projector pixels" (non-white, non-azure, outside the main azure block)
    projector_pixels = []
    for r in range(rows):
        for c in range(cols):
            color = input_grid[r, c]
            if color != white_color and color != azure_color:
                 # Ensure it's not part of the identified azure block (this check is technically redundant 
                 # if the color is not azure, but good for clarity)
                 if (r, c) not in azure_block_coords:
                     projector_pixels.append(((r, c), color))
            # Also consider pixels that might *look* like projectors but are azure, just not part of the largest block
            elif color == azure_color and (r, c) not in azure_block_coords:
                 projector_pixels.append(((r, c), color))


    # 3. For each projector pixel, trace projection paths
    for (pr, pc), p_color in projector_pixels:
        # Check the four orthogonal directions
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            # Start tracing from the cell adjacent to the projector
            curr_r, curr_c = pr + dr, pc + dc
            path_clear = True
            hit_target = None

            while 0 <= curr_r < rows and 0 <= curr_c < cols:
                cell_color = input_grid[curr_r, curr_c]
                cell_coord = (curr_r, curr_c)

                # If we hit an azure pixel within the largest block
                if cell_color == azure_color and cell_coord in azure_block_coords:
                    if path_clear: # Ensure the path only contained white pixels
                        hit_target = cell_coord
                    break # Stop tracing in this direction once an azure pixel (or blocker) is hit

                # If we hit a non-white pixel before hitting the target azure block
                elif cell_color != white_color:
                    path_clear = False
                    break # Path is blocked

                # Move to the next cell in the same direction
                curr_r += dr
                curr_c += dc
            
            # If a valid target was hit along a clear path
            if hit_target:
                # Modify the output grid at the target location
                output_grid[hit_target[0], hit_target[1]] = p_color
                # Optional: break here if a projector only affects one target pixel, even if multiple paths hit.
                # Based on examples, it seems one projector hits one target. Let's assume the first valid hit is the one.
                break 

    # 4. Return the modified output grid
    return output_grid