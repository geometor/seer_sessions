```python
import numpy as np

def find_objects(grid, color):
    """
    Finds all connected objects of a specific color in the grid using 4-way connectivity.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list: A list of objects, where each object is a list of (row, col) tuples.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                # Start a new object search (BFS)
                current_object = []
                q = [(r, c)]
                visited[r, c] = True
                while q:
                    row, col = q.pop(0)
                    current_object.append((row, col))

                    # Check neighbors (4-way connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                objects.append(current_object)
    return objects

def transform(input_grid):
    """
    Transforms gray (5) objects in the input grid based on their size.
    Objects with size 6 become red (2).
    Objects with other sizes become blue (1).
    White (0) pixels remain unchanged.
    """
    input_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_np) # Initialize output grid as a copy

    # Find all gray (5) objects
    gray_objects = find_objects(input_np, 5)

    # Process each gray object
    for obj_pixels in gray_objects:
        # Calculate the size of the object
        obj_size = len(obj_pixels)

        # Determine the target color based on size
        if obj_size == 6:
            target_color = 2 # Red
        else:
            target_color = 1 # Blue

        # Recolor the object in the output grid
        for r, c in obj_pixels:
            output_grid[r, c] = target_color

    # Convert back to list of lists for consistency if needed, though numpy array is fine
    return output_grid.tolist()

```