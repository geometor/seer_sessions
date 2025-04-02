import numpy as np
from collections import deque

"""
Transforms the input grid by identifying regions of white pixels (color 0) that are completely enclosed by a single non-white color (internal holes). 
If an internal hole consists of exactly 1 or 2 white pixels, those pixels are filled with the color of the surrounding non-white object. 
White pixels connected to the grid border (external background) and internal holes larger than 2 pixels remain unchanged.
"""

def transform(input_grid):
    """
    Fills small (size 1 or 2) enclosed white regions (holes) within non-white objects.

    Args:
        input_grid (list): A list of lists representing the input grid.

    Returns:
        list: A list of lists representing the transformed output grid.
    """
    # Convert input list of lists to a NumPy array for efficient processing
    grid = np.array(input_grid, dtype=int)
    # Create a copy to modify and return as the output
    output_grid = np.copy(grid)
    height, width = grid.shape

    # Initialize a boolean grid to keep track of visited pixels during searches.
    # This prevents recounting pixels or getting into infinite loops in BFS.
    # It will first track external background, then internal holes as they are found.
    visited = np.zeros((height, width), dtype=bool)

    # --- Step 1: Identify all white pixels connected to the border (external background) ---
    # Use Breadth-First Search (BFS) starting from all border white pixels.
    q_external = deque()

    # Add all border white pixels to the queue and mark them as visited.
    for r in range(height):
        for c in [0, width - 1]: # Left and right columns
            if grid[r, c] == 0 and not visited[r, c]:
                visited[r, c] = True
                q_external.append((r, c))
    for c in range(1, width - 1): # Top and bottom rows (excluding corners already checked)
        for r in [0, height - 1]:
            if grid[r, c] == 0 and not visited[r, c]:
                visited[r, c] = True
                q_external.append((r, c))

    # Perform BFS to find all white pixels reachable from the border.
    while q_external:
        r, c = q_external.popleft()

        # Check four adjacent neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if neighbor is within grid bounds
            if 0 <= nr < height and 0 <= nc < width:
                # If the neighbor is white and hasn't been visited, mark it as visited (part of external space) and add to queue
                if grid[nr, nc] == 0 and not visited[nr, nc]:
                    visited[nr, nc] = True
                    q_external.append((nr, nc))

    # --- Step 2: Identify and process internal holes ---
    # Iterate through all pixels in the grid.
    for r in range(height):
        for c in range(width):
            # If a pixel is white (0) and was *not* visited during the external white pixel search,
            # it must be the start of an internal hole.
            if grid[r, c] == 0 and not visited[r, c]:

                # Start a new BFS to find all pixels of this specific hole.
                q_hole = deque()
                current_hole_pixels = [] # Store coordinates of pixels in this hole
                enclosure_color = -1 # Store the color surrounding the hole (-1 indicates not found yet)
                
                # Add starting pixel to queue and mark visited IMMEDIATELY
                # This prevents this pixel from being accidentally included in another hole's BFS
                # or starting a redundant BFS from this pixel later in the loop.
                q_hole.append((r, c))
                visited[r, c] = True 

                # --- Hole BFS ---
                while q_hole:
                    hr, hc = q_hole.popleft()
                    current_hole_pixels.append((hr, hc)) # Add to the list of pixels in this hole

                    # Check neighbors to find the fill color and continue BFS within the hole
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nhr, nhc = hr + dr, hc + dc

                        # Check bounds
                        if 0 <= nhr < height and 0 <= nhc < width:
                            neighbor_val = grid[nhr, nhc]

                            # If neighbor is non-white, it defines the potential enclosure color
                            if neighbor_val != 0:
                                # Assumption: Holes are enclosed by a single color based on examples.
                                # Record the first non-white neighbor color found.
                                if enclosure_color == -1:
                                    enclosure_color = neighbor_val
                                # Optional: Could add check here: if enclosure_color != -1 and neighbor_val != enclosure_color: raise error...
                                
                            # If neighbor is white and hasn't been visited yet (part of the same internal hole)
                            elif not visited[nhr, nhc]:
                                visited[nhr, nhc] = True # Mark visited globally
                                q_hole.append((nhr, nhc)) # Add to this hole's BFS queue

                # --- Post-Hole BFS Processing ---
                # Calculate the size of the found hole.
                hole_size = len(current_hole_pixels)

                # Check if the hole size meets the criteria (1 or 2 pixels) and an enclosure color was found.
                if (hole_size == 1 or hole_size == 2) and enclosure_color != -1:
                    # Fill the pixels belonging to this small hole in the output grid.
                    for fill_r, fill_c in current_hole_pixels:
                        output_grid[fill_r, fill_c] = enclosure_color
                # Otherwise (hole size > 2 or no enclosure color found), do nothing, leave the hole as it is in the output_grid copy.

    # Convert the final NumPy array back to a standard Python list of lists
    return output_grid.tolist()