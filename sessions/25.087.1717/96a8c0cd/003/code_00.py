import copy
import collections

# Define color constants for clarity
WHITE = 0
BLUE = 1
RED = 2
GREEN = 3

def transform(input_grid):
    """
    Performs a constrained flood fill. Finds the region containing the initial 
    red pixel (2) that is enclosed by blue (1), green (3), or grid boundaries. 
    Fills all white (0) pixels within this enclosed region with red (2). 
    Other pixels (blue, green, original red) remain unchanged.

    The process involves:
    1. Identifying all white pixels reachable from the grid border (external region).
    2. Identifying all white pixels *not* reachable from the border (internal region).
    3. Changing the color of the internal white pixels to red in the output grid.
    """
    
    # Get grid dimensions
    height = len(input_grid)
    width = len(input_grid[0])
    
    # Initialize output_grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)
    
    # Set to keep track of visited coordinates during the external flood fill
    # These are the white pixels reachable from the outside border.
    external_visited = set()
    
    # Queue for Breadth-First Search (BFS) starting from border white pixels
    queue = collections.deque()
    
    # Initialize the queue with all white pixels on the border
    for r in range(height):
        for c in range(width):
            # Check if the pixel is on the border
            if r == 0 or r == height - 1 or c == 0 or c == width - 1:
                # Check if the border pixel is white and not already visited
                if input_grid[r][c] == WHITE and (r, c) not in external_visited:
                    external_visited.add((r, c))
                    queue.append((r, c))

    # Define orthogonal directions (right, left, down, up)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Perform BFS to find all white pixels reachable from the border
    while queue:
        current_row, current_col = queue.popleft()
        
        # Explore neighbors
        for dr, dc in directions:
            neighbor_row, neighbor_col = current_row + dr, current_col + dc
            neighbor_coord = (neighbor_row, neighbor_col)
            
            # Check if the neighbor is within the grid boundaries
            if 0 <= neighbor_row < height and 0 <= neighbor_col < width:
                # Check if the neighbor is white in the input grid and hasn't been visited yet
                if input_grid[neighbor_row][neighbor_col] == WHITE and neighbor_coord not in external_visited:
                    # Mark neighbor as visited (part of the external white region)
                    external_visited.add(neighbor_coord)
                    # Add neighbor to the queue to explore from it
                    queue.append(neighbor_coord)

    # Iterate through the grid to fill the internal white pixels
    for r in range(height):
        for c in range(width):
            # Check if the pixel in the input grid is white
            if input_grid[r][c] == WHITE:
                # Check if this white pixel was *not* reached by the external fill
                if (r, c) not in external_visited:
                    # This is an internal white pixel, change it to red in the output grid
                    output_grid[r][c] = RED
                    
    # The original red pixel, blue pixels, and green pixels are preserved 
    # because they were either not white (so skipped in the final loop) 
    # or part of the initial copy. The original red pixel will naturally be 
    # part of the "internal" area if enclosed, and since it's not white, 
    # the final loop won't attempt to change it.

    return output_grid