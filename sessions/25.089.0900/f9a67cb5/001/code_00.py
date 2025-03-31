import collections
import copy

"""
Perform a flood fill operation starting from the single red (2) pixel.
The fill spreads cardinally (up, down, left, right) into adjacent white (0) pixels.
The spread is blocked by azure (8) pixels and the grid boundaries.
Azure pixels and the original red pixel remain unchanged.
"""

def transform(input_grid):
    """
    Applies a flood fill transformation starting from the red pixel.

    Args:
        input_grid (list[list[int]]): The input 2D grid.

    Returns:
        list[list[int]]: The transformed 2D grid.
    """

    # Get grid dimensions
    height = len(input_grid)
    if height == 0:
        return []
    width = len(input_grid[0])
    if width == 0:
        return [[] for _ in range(height)]

    # Initialize output_grid as a deep copy of the input_grid
    output_grid = copy.deepcopy(input_grid)

    # Find the starting red pixel (color 2)
    start_pos = None
    for r in range(height):
        for c in range(width):
            if input_grid[r][c] == 2:
                start_pos = (r, c)
                break
        if start_pos:
            break

    # If no starting red pixel is found, return the original grid copy
    if not start_pos:
        return output_grid

    # Initialize the queue for Breadth-First Search (BFS) flood fill
    queue = collections.deque([start_pos])
    # Initialize a set to keep track of visited coordinates to avoid cycles and redundant checks
    visited = {start_pos}

    # Define cardinal directions (up, down, left, right)
    directions = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # Perform the flood fill
    while queue:
        # Get the current pixel coordinates from the queue
        current_r, current_c = queue.popleft()

        # Explore neighbors in cardinal directions
        for dr, dc in directions:
            neighbor_r, neighbor_c = current_r + dr, current_c + dc

            # Check if the neighbor is within the grid boundaries
            if 0 <= neighbor_r < height and 0 <= neighbor_c < width:
                # Check if the neighbor has already been visited
                if (neighbor_r, neighbor_c) not in visited:
                    # Mark the neighbor as visited
                    visited.add((neighbor_r, neighbor_c))
                    
                    # Check if the neighbor pixel is white (0) - the fill target
                    if output_grid[neighbor_r][neighbor_c] == 0:
                        # Change the neighbor's color to red (2) in the output grid
                        output_grid[neighbor_r][neighbor_c] = 2
                        # Add the neighbor to the queue to process its neighbors later
                        queue.append((neighbor_r, neighbor_c))

    # Return the modified grid
    return output_grid