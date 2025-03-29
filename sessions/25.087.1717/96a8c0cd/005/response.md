```python
import copy
import collections

# Define color constants for clarity
WHITE = 0
BLUE = 1
RED = 2
GREEN = 3

def transform(input_grid):
    """
    Performs a constrained flood fill starting from the Red (2) pixel(s).
    The fill spreads orthogonally (up, down, left, right) through adjacent
    White (0) pixels. The fill is blocked by Blue (1) pixels, Green (3) pixels,
    and the grid boundaries. All reachable White (0) pixels are changed to Red (2)
    in the output grid. Original Red, Blue, and Green pixels are preserved.
    """
    
    # Get grid dimensions
    height = len(input_grid)
    width = len(input_grid[0])
    
    # Initialize output_grid as a deep copy of the input
    output_grid = copy.deepcopy(input_grid)
    
    # Set to keep track of visited coordinates during the flood fill
    visited = set()
    
    # Queue for Breadth-First Search (BFS) starting from initial Red pixels
    queue = collections.deque()
    
    # Find initial Red (2) pixels and add them to the queue and visited set
    for r in range(height):
        for c in range(width):
            if input_grid[r][c] == RED:
                start_coord = (r, c)
                # Only add if not already visited (handles overlapping initial red areas if they existed)
                if start_coord not in visited:
                    visited.add(start_coord)
                    queue.append(start_coord)
                    # Note: The initial red pixel itself is NOT changed in the output grid,
                    # it's just the starting point for the fill spreading into white areas.
                    # The deep copy already preserves its color.

    # Define orthogonal directions (right, left, down, up)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Perform BFS flood fill
    while queue:
        current_row, current_col = queue.popleft()
        
        # Explore neighbors
        for dr, dc in directions:
            neighbor_row, neighbor_col = current_row + dr, current_col + dc
            neighbor_coord = (neighbor_row, neighbor_col)
            
            # Check 1: Is the neighbor within the grid boundaries?
            if 0 <= neighbor_row < height and 0 <= neighbor_col < width:
                # Check 2: Has the neighbor already been visited?
                if neighbor_coord not in visited:
                    # Check 3: Is the neighbor White (0) in the *input* grid (fillable)?
                    if input_grid[neighbor_row][neighbor_col] == WHITE:
                        # If all checks pass:
                        # 1. Change the color in the output grid
                        output_grid[neighbor_row][neighbor_col] = RED
                        # 2. Mark neighbor as visited
                        visited.add(neighbor_coord)
                        # 3. Add neighbor to the queue to explore from it
                        queue.append(neighbor_coord)
                    else:
                         # If the neighbour is not white, but within bounds and not visited,
                         # mark it as visited anyway. This prevents reconsidering barrier
                         # cells (Blue, Green, or other non-white/non-red) multiple times.
                         # The initial Red cell(s) were already added to visited.
                         visited.add(neighbor_coord)


    # Return the modified grid
    return output_grid
```