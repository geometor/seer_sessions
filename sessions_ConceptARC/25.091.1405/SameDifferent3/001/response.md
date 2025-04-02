```python
import numpy as np
from collections import defaultdict, deque

def find_objects(grid):
    """
    Finds all contiguous objects of the same color in a grid.

    Args:
        grid (np.array): The input grid.

    Returns:
        dict: A dictionary where keys are colors (int > 0) and values are lists 
              of objects. Each object is represented as a set of (row, col) tuples.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects_by_color = defaultdict(list)

    for r in range(height):
        for c in range(width):
            # Skip background color and already visited pixels
            if grid[r, c] == 0 or visited[r, c]:
                continue

            current_color = grid[r, c]
            current_object_pixels = set()
            queue = deque([(r, c)])
            visited[r, c] = True

            # Breadth-First Search (BFS) to find connected pixels of the same color
            while queue:
                row, col = queue.popleft()
                current_object_pixels.add((row, col))

                # Check 4 neighbors (up, down, left, right)
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = row + dr, col + dc

                    # Check bounds
                    if 0 <= nr < height and 0 <= nc < width:
                        # Check color match and visited status
                        if grid[nr, nc] == current_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            queue.append((nr, nc))
            
            # Store the found object
            objects_by_color[current_color].append(current_object_pixels)

    return objects_by_color


def transform(input_grid):
    """
    Identifies colors that appear in only one contiguous object within the grid 
    and removes those objects (changes their color to white/0). Objects of colors 
    that appear in two or more distinct locations are kept.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the transformed output grid.
    """
    # Convert input list of lists to numpy array for easier handling
    input_grid_np = np.array(input_grid, dtype=int)
    
    # Find all objects, grouped by color
    objects_by_color = find_objects(input_grid_np)

    # Initialize the output grid as a copy of the input
    output_grid = input_grid_np.copy()

    # Iterate through each color found in the grid
    for color, objects_list in objects_by_color.items():
        # Check if there is only one object of this color
        if len(objects_list) == 1:
            # Get the pixels of the single object
            pixels_to_remove = objects_list[0]
            # Change the color of these pixels to white (0) in the output grid
            for r, c in pixels_to_remove:
                output_grid[r, c] = 0

    return output_grid.tolist() # Convert back to list of lists if needed by caller
```