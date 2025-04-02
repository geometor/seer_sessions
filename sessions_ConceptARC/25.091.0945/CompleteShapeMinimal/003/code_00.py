import numpy as np
from collections import deque

"""
Transforms the input grid by identifying regions of white pixels (color 0) that are completely enclosed by a single non-white color. 
These enclosed white regions ("holes") are then filled with the color of the surrounding non-white object. 
White pixels connected to the grid border are considered external and remain unchanged.
"""

def transform(input_grid):
    """
    Fills enclosed white regions (holes) within non-white objects.

    Args:
        input_grid (list): A list of lists representing the input grid.

    Returns:
        list: A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    grid = np.array(input_grid, dtype=int)
    output_grid = np.copy(grid)
    height, width = grid.shape

    # Initialize a boolean grid to keep track of visited pixels during searches.
    visited = np.zeros((height, width), dtype=bool)
    
    # --- Step 1: Identify all white pixels connected to the border (external) ---
    q = deque()

    # Add all border white pixels to the queue and mark them as visited.
    for r in range(height):
        for c in [0, width - 1]: # Left and right columns
            if grid[r, c] == 0 and not visited[r, c]:
                visited[r, c] = True
                q.append((r, c))
    for c in range(1, width - 1): # Top and bottom rows (excluding corners already checked)
        for r in [0, height - 1]: 
            if grid[r, c] == 0 and not visited[r, c]:
                visited[r, c] = True
                q.append((r, c))

    # Perform BFS starting from border white pixels to find all connected white pixels.
    while q:
        r, c = q.popleft()

        # Check four adjacent neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if neighbor is within grid bounds
            if 0 <= nr < height and 0 <= nc < width:
                # If the neighbor is white and hasn't been visited, mark and add to queue
                if grid[nr, nc] == 0 and not visited[nr, nc]:
                    visited[nr, nc] = True
                    q.append((nr, nc))

    # --- Step 2: Identify and fill internal holes ---
    # Iterate through all pixels in the grid.
    for r in range(height):
        for c in range(width):
            # If a pixel is white (0) and was *not* visited during the external white pixel search,
            # it must be part of an internal hole.
            if grid[r, c] == 0 and not visited[r, c]:
                
                # Start a new BFS to find all pixels of this specific hole and determine the fill color.
                hole_q = deque()
                hole_pixels = [] 
                fill_color = -1 # Initialize fill color (use -1 to indicate not found yet)
                
                # Add starting pixel to queue and mark visited
                hole_q.append((r, c))
                visited[r, c] = True # Mark as visited to avoid reprocessing

                while hole_q:
                    hr, hc = hole_q.popleft()
                    hole_pixels.append((hr, hc)) # Add to the list of pixels in this hole
                    
                    # Check neighbors to find the fill color and continue BFS within the hole
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nhr, nhc = hr + dr, hc + dc

                        if 0 <= nhr < height and 0 <= nhc < width:
                            neighbor_val = grid[nhr, nhc]
                            
                            # If neighbor is non-white, it defines the fill color
                            if neighbor_val != 0:
                                # Assumption: Holes are enclosed by a single color.
                                if fill_color == -1:
                                    fill_color = neighbor_val
                                # Optional: Add check if fill_color != -1 and neighbor_val != fill_color 
                                # This would indicate an unexpected input structure.
                                    
                            # If neighbor is white and hasn't been visited yet (part of the same hole)
                            elif not visited[nhr, nhc]:
                                visited[nhr, nhc] = True # Mark visited
                                hole_q.append((nhr, nhc)) # Add to hole BFS queue

                # After exploring the entire hole, fill the pixels in the output grid
                if fill_color != -1: # Ensure a fill color was found
                    for hr, hc in hole_pixels:
                        output_grid[hr, hc] = fill_color
                # If fill_color remains -1, it means a white region wasn't enclosed (shouldn't happen based on logic)
                # or the hole finding logic has an issue. Leave it white in the output.

    # Convert the final NumPy array back to a list of lists
    return output_grid.tolist()