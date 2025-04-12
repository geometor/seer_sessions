```python
import collections
import copy

"""
Transforms an input grid by performing a flood fill operation starting from cells containing the digit 3. 
The fill spreads to adjacent (horizontally and vertically) cells containing the digit 7. 
Cells containing the digit 8 act as barriers and block the spread. The spread continues until no 
more adjacent 7s can be reached from the spreading 3s.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies a flood fill transformation to the input grid.

    Args:
        input_grid: A 2D list of integers representing the input grid.

    Returns:
        A 2D list of integers representing the transformed grid.
    """
    # Make a deep copy to avoid modifying the original input and to store the result
    output_grid = [row[:] for row in input_grid]
    
    # Get grid dimensions
    rows = len(output_grid)
    if rows == 0:
        return [] # Handle empty grid case
    cols = len(output_grid[0])
    if cols == 0:
        return [[] for _ in range(rows)] # Handle grids with empty rows

    # Initialize a queue for the Breadth-First Search (BFS) flood fill
    queue = collections.deque()

    # Identify initial source cells (value 3) and add them to the queue
    for r in range(rows):
        for c in range(cols):
            if output_grid[r][c] == 3:
                # Add initial '3' positions to the queue.
                # Note: We add them even though they are already 3, 
                # because their neighbors need to be checked.
                queue.append((r, c))

    # Define the four cardinal directions for checking neighbors
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Right, Left, Down, Up

    # Perform the flood fill (spread loop) using BFS
    while queue:
        # Get the current cell coordinates from the front of the queue
        r, c = queue.popleft()

        # Check neighbors in all four directions
        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            # Check if the neighbor is within grid boundaries
            if 0 <= nr < rows and 0 <= nc < cols:
                # Check if the neighbor cell is fillable (contains 7)
                if output_grid[nr][nc] == 7:
                    # Fill the neighbor cell with 3
                    output_grid[nr][nc] = 3
                    # Add the newly filled cell to the queue to continue the spread from it
                    queue.append((nr, nc))

    # Return the modified grid after the spread is complete
    return output_grid
```