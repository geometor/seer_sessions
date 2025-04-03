import numpy as np
from collections import deque

"""
Identify contiguous green (3) objects using 4-connectivity (pixels sharing an edge).
Calculate the size (pixel count) of each identified green object.
If the object's size is even, change the color of all pixels belonging to that object to magenta (6).
If the object's size is odd, change the color of all pixels belonging to that object to gray (5).
Leave all other pixels (specifically white background, 0) unchanged.
"""

def find_objects(grid, target_color):
    """
    Finds all distinct connected components (objects) of a specific color in a grid.

    Args:
        grid (np.array): The input 2D grid.
        target_color (int): The color of the pixels forming the objects to find.

    Returns:
        list: A list of objects. Each object is represented as a list of
              coordinate tuples (row, col).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    # Iterate through each cell of the grid
    for r in range(rows):
        for c in range(cols):
            # If we find a pixel of the target color that hasn't been visited yet,
            # start a Breadth-First Search (BFS) to find the connected component.
            if grid[r, c] == target_color and not visited[r, c]:
                current_object_coords = []
                q = deque([(r, c)])
                visited[r, c] = True # Mark the starting cell as visited

                while q:
                    row, col = q.popleft()
                    current_object_coords.append((row, col)) # Add current cell to the object

                    # Define the 4 neighbors (up, down, left, right)
                    neighbors = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                    for dr, dc in neighbors:
                        nr, nc = row + dr, col + dc

                        # Check if the neighbor is within grid bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # Check if the neighbor has the target color and hasn't been visited
                            if grid[nr, nc] == target_color and not visited[nr, nc]:
                                visited[nr, nc] = True # Mark neighbor as visited
                                q.append((nr, nc)) # Add neighbor to the queue for processing

                # After the BFS completes for one object, add its coordinates to the list
                if current_object_coords:
                    objects.append(current_object_coords)
    return objects

def transform(input_grid):
    """
    Transforms the input grid by changing the color of green objects based on their size parity.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_grid)
    
    # Define the colors involved
    target_color = 3 # green
    odd_color = 5    # gray
    even_color = 6   # magenta

    # Find all green objects in the input grid
    green_objects = find_objects(input_grid, target_color)

    # Process each found green object
    for obj_coords in green_objects:
        # Calculate the size of the object
        obj_size = len(obj_coords)

        # Determine the output color based on size parity
        if obj_size % 2 == 0:
            output_color = even_color # Magenta for even size
        else:
            output_color = odd_color  # Gray for odd size

        # Update the output grid by changing the color of all pixels in the current object
        for r, c in obj_coords:
            output_grid[r, c] = output_color

    # Return the modified grid
    return output_grid