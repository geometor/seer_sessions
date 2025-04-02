import numpy as np

"""
Identifies distinct, contiguous objects of the same non-white color in the input grid.
Counts the number of these objects.
Creates a 1x6 output grid.
Fills the first 'N' cells of the output grid with yellow (4), where 'N' is the object count.
Fills the remaining cells with white (0).
"""

def find_objects(grid):
    """
    Finds and counts distinct contiguous objects of the same non-white color.

    Args:
        grid (np.array): The input grid.

    Returns:
        int: The number of distinct objects found.
    """
    rows = grid.shape[0]
    cols = grid.shape[1]
    visited = np.zeros_like(grid, dtype=bool)
    object_count = 0
    q = [] # Queue for BFS

    for r in range(rows):
        for c in range(cols):
            # Check if the cell is non-white (not 0) and hasn't been visited yet
            if grid[r, c] != 0 and not visited[r, c]:
                # Found the start of a new object
                object_count += 1
                object_color = grid[r, c]  # Color of the current object
                
                # Start BFS from this cell
                q.append((r, c))
                visited[r, c] = True

                while q:
                    curr_r, curr_c = q.pop(0)

                    # Check 4 cardinal neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = curr_r + dr, curr_c + dc

                        # Check if the neighbor is within bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # Check if the neighbor has the same color and hasn't been visited
                            if not visited[nr, nc] and grid[nr, nc] == object_color:
                                visited[nr, nc] = True
                                q.append((nr, nc))
    return object_count

def transform(input_grid):
    """
    Transforms the input grid based on the count of distinct non-white objects.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 1x6 numpy array representing the output grid.
    """
    # Convert input list of lists to numpy array if necessary
    input_grid_np = np.array(input_grid)

    # Count the number of distinct non-white objects
    num_objects = find_objects(input_grid_np)

    # Define the output grid dimensions (fixed at 1x6)
    output_height = 1
    output_width = 6
    
    # Initialize the output grid with white (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # Determine how many yellow cells to draw (capped by output width)
    num_yellow = min(num_objects, output_width)

    # Fill the beginning of the output row with yellow (4)
    for i in range(num_yellow):
        output_grid[0, i] = 4

    # The rest are already white (0) due to initialization

    return output_grid.tolist() # Return as list of lists per ARC standard