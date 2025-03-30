"""
Identifies white pixels (color 0) enclosed by non-white pixels and fills them with green (color 3). 
Enclosed means the white pixels are not connected to the grid boundary via a path of other white pixels using 4-directional adjacency.
Uses a Breadth-First Search (BFS) algorithm starting from the boundary white pixels to mark all 'exterior' white pixels. 
Any remaining white pixels after the BFS are considered 'interior' and are filled with green.
"""

import numpy as np
from collections import deque

def transform(input_grid):
    """
    Fills interior white regions (color 0) of a grid with green (color 3).

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed grid.
    """
    # Convert input list of lists to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape
    
    # Create a copy of the grid to modify, this will become the output grid
    output_grid = grid.copy()

    # Define colors and a temporary marker
    background_color = 0 # white
    fill_color = 3       # green
    temp_marker = -1     # A temporary value not present in the original grid (0-9) to mark visited exterior white cells

    # Initialize a queue for the BFS
    queue = deque()
    
    # Initialize visited set/array (optional but can prevent adding duplicates to queue, though checking marker is sufficient)
    # Using the output_grid itself for marking avoids needing a separate visited array.

    # Step 1: Identify initial boundary white pixels and start the BFS
    # Iterate through all boundary cells
    for r in range(rows):
        # Left edge
        if output_grid[r, 0] == background_color:
            if output_grid[r, 0] != temp_marker: # Check if not already marked (e.g., corners)
                output_grid[r, 0] = temp_marker
                queue.append((r, 0))
        # Right edge
        if output_grid[r, cols - 1] == background_color:
            if output_grid[r, cols - 1] != temp_marker: # Check if not already marked
                 output_grid[r, cols - 1] = temp_marker
                 queue.append((r, cols - 1))
            
    for c in range(cols): # Iterate columns (corners handled above)
        # Top edge
        if output_grid[0, c] == background_color:
             if output_grid[0, c] != temp_marker: # Check if not already marked
                 output_grid[0, c] = temp_marker
                 queue.append((0, c))
        # Bottom edge
        if output_grid[rows - 1, c] == background_color:
             if output_grid[rows - 1, c] != temp_marker: # Check if not already marked
                 output_grid[rows - 1, c] = temp_marker
                 queue.append((rows - 1, c))

    # Step 2: Perform the BFS to mark all exterior white pixels reachable from the boundary
    while queue:
        r, c = queue.popleft()
        
        # Check 4-directional neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            
            # Check if neighbor is within bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if neighbor is white (background_color) AND hasn't been marked yet
                if output_grid[nr, nc] == background_color:
                    # Mark it as exterior (connected to boundary) using the temp marker
                    output_grid[nr, nc] = temp_marker
                    # Add it to the queue to process its neighbors
                    queue.append((nr, nc))
                    
    # Step 3: Final pass to fill interior white pixels and reset exterior ones
    # Iterate through the entire grid
    for r in range(rows):
        for c in range(cols):
            # If a pixel is still marked as background_color (0), it's interior because
            # it wasn't reached by the BFS from the boundary. Fill it with green.
            if output_grid[r, c] == background_color:
                output_grid[r, c] = fill_color
            # If a pixel was marked with the temporary marker (-1), it's an exterior white pixel.
            # Reset it back to the original background color (white).
            elif output_grid[r, c] == temp_marker:
                 output_grid[r, c] = background_color
            # Otherwise (non-white pixels originally), leave them as they were (already copied)

    # Convert the final numpy array back to a list of lists for the required output format
    return output_grid.tolist()