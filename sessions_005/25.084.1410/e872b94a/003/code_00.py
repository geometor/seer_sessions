"""
Identify all distinct groups (connected components) of gray (5) pixels within the input grid. 
Consider pixels connected only if they are adjacent horizontally or vertically (cardinal connectivity). 
Count the total number of these separate gray components found (N). 
Construct a new output grid that has N rows and 1 column, filled entirely with the white (0) color.
"""

import numpy as np
from collections import deque # Using deque for efficient BFS queue

def _find_and_count_components_cardinal(grid, target_color):
    """
    Finds and counts connected components of a specific color using cardinal adjacency.

    Args:
        grid (np.array): The input grid.
        target_color (int): The color value of the pixels to form components.

    Returns:
        int: The total number of components found.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    count = 0

    # Iterate through each cell in the grid
    for r in range(rows):
        for c in range(cols):
            # If we find a pixel of the target color that hasn't been visited yet,
            # it's the start of a new component.
            if grid[r, c] == target_color and not visited[r, c]:
                count += 1  # Increment component count
                # Start a Breadth-First Search (BFS) to find all connected pixels
                # in this component and mark them as visited.
                queue = deque([(r, c)])
                visited[r, c] = True

                while queue:
                    row, col = queue.popleft()

                    # Check cardinal neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc

                        # Check if the neighbor is within grid bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # Check if the neighbor is the target color and hasn't been visited
                            if grid[nr, nc] == target_color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                queue.append((nr, nc))
    return count

def transform(input_grid):
    """
    Transforms the input grid by counting cardinally connected gray components
    and creating a white column output grid with height equal to the count.

    Args:
        input_grid (list of lists): The 2D input grid with pixel values 0-9.

    Returns:
        np.array: A 2D numpy array representing the output grid (N x 1, all zeros).
    """
    # Convert input list of lists to a numpy array for easier processing
    input_array = np.array(input_grid, dtype=int)

    # Define the target color for objects we need to count
    target_color = 5 # gray

    # Find and count the connected components of the target color using cardinal adjacency
    num_components = _find_and_count_components_cardinal(input_array, target_color)

    # The height of the output grid is the number of components found
    output_height = num_components
    # The width of the output grid is always 1 as per the task description
    output_width = 1

    # Create the output grid filled with white (0) pixels
    # Use np.zeros for efficiency and specify dtype=int
    output_grid = np.zeros((output_height, output_width), dtype=int)

    return output_grid