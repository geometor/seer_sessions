"""
Identify nested colored frames within an azure (8) background in the input grid.
List the frame colors in the output, ordered from the outermost frame to the innermost frame.
The output is presented as a column vector (Nx1 grid).

Algorithm:
1. Initialize an empty list `frame_colors` to store the result.
2. Define the background color `background_color = 8`.
3. Keep track of colors already identified as frames or background in `found_colors`, initialized with `{background_color}`.
4. Start a Breadth-First Search (BFS) from the background pixels located at the border of the grid.
5. Maintain a queue `q` for the BFS and a `visited` array to track visited cells.
6. Iteratively identify frame layers:
   a. In each iteration, perform BFS starting from the cells of the current boundary color (initially the background).
   b. While exploring neighbors during BFS:
      i. If a neighbor has the same color as the current boundary, continue the BFS from it.
      ii. If a neighbor has a color C that has not been found yet (C not in `found_colors`), add C to a set `next_boundary_candidates`. Store the coordinates of these neighbors to potentially start the next BFS wave.
   c. After exploring all reachable cells of the current boundary color, check `next_boundary_candidates`.
   d. If the set is empty, it means no new frames were found adjacent to the current layer; stop the process.
   e. If the set contains exactly one color, this is the color of the next frame. Add it to `frame_colors`, add it to `found_colors`, and set it as the `current_boundary_color` for the next iteration.
   f. Prepare the queue `q` for the next iteration by adding the coordinates (stored in step 6.b.ii) corresponding to the newly found frame color. Mark these starting cells as visited.
   g. If `next_boundary_candidates` contains more than one color, the frame structure is ambiguous based on the current logic; raise an error.
7. Once the loop terminates, convert the `frame_colors` list into an Nx1 numpy array (column vector).
"""

import numpy as np
import collections

def transform(input_grid):
    """
    Identifies nested frame colors in a grid and returns them as a column vector.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list of integers.

    Returns:
        list of lists: An Nx1 grid (column vector) containing the ordered frame colors.
                       Returns empty list `[]` if input is empty or has no frames.
                       Returns `[[color]]` if only one frame.
    """
    grid = np.array(input_grid, dtype=int)
    
    if grid.size == 0:
        return [] # Handle empty input

    rows, cols = grid.shape
    
    # Initialize data structures
    q = collections.deque()
    visited = np.zeros_like(grid, dtype=bool)
    frame_colors = []
    background_color = 8
    found_colors = {background_color} # Keep track of colors already identified

    # Initialize queue with all border background cells
    # These cells form the starting points for finding the first frame
    initial_boundary_color = background_color
    for r in range(rows):
        for c in [0, cols - 1]: # Check first and last columns
            if 0 <= r < rows and 0 <= c < cols: # Ensure indices are valid (for 1xN or Nx1 grids)
                if grid[r, c] == initial_boundary_color and not visited[r, c]:
                    q.append((r, c))
                    visited[r, c] = True
    for c in range(cols): # Check first and last rows (avoid double-adding corners)
         for r in [0, rows - 1]:
             if 0 <= r < rows and 0 <= c < cols:
                if grid[r, c] == initial_boundary_color and not visited[r, c]:
                    q.append((r, c))
                    visited[r, c] = True
    
    # Iteratively find frames layer by layer using BFS
    current_boundary_color = initial_boundary_color
    while True:
        next_boundary_candidates = set()
        # Keep track of coordinates adjacent to the current layer that belong to potential next frames
        coords_for_next_layer_start = [] 

        # Use a temporary queue for the current layer's BFS exploration
        # so 'q' can be repopulated for the *next* layer's start points
        current_layer_q = q.copy()
        q.clear() # Clear q to be ready for the next layer's starting points

        # Perform BFS for the current boundary color
        while current_layer_q:
            r, c = current_layer_q.popleft()

            # Explore neighbors (up, down, left, right)
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc

                # Check if neighbor is within grid bounds
                if 0 <= nr < rows and 0 <= nc < cols:
                    neighbor_color = grid[nr, nc]
                    
                    if not visited[nr, nc]:
                        if neighbor_color == current_boundary_color:
                            # Continue BFS within the same color region
                            visited[nr, nc] = True
                            current_layer_q.append((nr, nc))
                        elif neighbor_color not in found_colors:
                            # Found a potential next frame color adjacent to the current layer
                            next_boundary_candidates.add(neighbor_color)
                            # Store its location - we'll use these to start the *next* BFS
                            coords_for_next_layer_start.append((nr, nc)) 
                        # else: neighbor has a color that's already been found (part of a previous frame or background) - ignore
        
        # Check results of the layer's BFS
        if not next_boundary_candidates:
            # No new adjacent colors found, means we've found all frames
            break 

        # Based on examples, assume exactly one new frame color is found per layer
        if len(next_boundary_candidates) > 1:
            # This case is ambiguous or not handled by the current logic based on observed patterns
            # You might need a more sophisticated way to choose if multiple candidates appear
            print(f"Warning: Found multiple candidates {next_boundary_candidates} adjacent to color {current_boundary_color}. Check task rules.")
            # Arbitrarily break or raise error, let's raise an error for clarity
            raise ValueError(f"Ambiguous frame structure detected. Found {next_boundary_candidates} adjacent to color {current_boundary_color}.")
            
        # Identify the next frame color
        next_frame_color = list(next_boundary_candidates)[0]
        frame_colors.append(next_frame_color)
        found_colors.add(next_frame_color)
        
        # Prepare the queue for the next iteration's BFS
        # Start the next BFS only from the cells of the newly found frame color
        # that were adjacent to the layer just processed.
        processed_for_next_q = set() # Avoid adding duplicate start points
        for nr_next, nc_next in coords_for_next_layer_start:
             # Check if the coordinate actually holds the next_frame_color (it should, by definition)
             # and if it hasn't been visited yet (important!) and not already added to the queue start points.
             if grid[nr_next, nc_next] == next_frame_color and not visited[nr_next, nc_next] and (nr_next, nc_next) not in processed_for_next_q:
                 q.append((nr_next, nc_next))
                 visited[nr_next, nc_next] = True # Mark the starting cells of the next layer as visited
                 processed_for_next_q.add((nr_next, nc_next))

        # Update the boundary color for the next iteration
        current_boundary_color = next_frame_color
        
        # If the queue for the next layer is empty (e.g., all adjacent cells of the new color were somehow already visited), stop.
        if not q:
            break
            
    # Format the output as an Nx1 grid (list of lists)
    output_grid = [[color] for color in frame_colors]
    
    return output_grid