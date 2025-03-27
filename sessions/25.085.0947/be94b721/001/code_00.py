import numpy as np
from collections import deque

def find_objects(grid):
    """
    Finds all connected components (objects) of non-background pixels in the grid.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        list: A list of objects, where each object is a dictionary containing:
              'color': The color of the object's pixels.
              'coords': A set of (row, col) tuples representing the object's pixels.
              'size': The number of pixels in the object.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            # Check if the pixel is not background (0) and not visited
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                current_object_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True

                # Start BFS to find all connected pixels of the same color
                while q:
                    row, col = q.popleft()
                    current_object_coords.add((row, col))

                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc

                        # Check bounds and if the neighbor is the same color and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                # Store the found object
                objects.append({
                    'color': color,
                    'coords': current_object_coords,
                    'size': len(current_object_coords)
                })

    return objects

def get_bounding_box(coords):
    """
    Calculates the minimum bounding box for a set of coordinates.

    Args:
        coords (set): A set of (row, col) tuples.

    Returns:
        tuple: (min_row, min_col, max_row, max_col)
    """
    if not coords:
        return 0, 0, 0, 0 # Should not happen if an object is found
    min_row = min(r for r, c in coords)
    min_col = min(c for r, c in coords)
    max_row = max(r for r, c in coords)
    max_col = max(c for r, c in coords)
    return min_row, min_col, max_row, max_col


def transform(input_grid):
    """
    Identifies the largest non-background object in the input grid by pixel count,
    and returns a new grid containing only that object, cropped to its bounding box.

    1. Convert input list of lists to a NumPy array.
    2. Find all connected components (objects) of non-background pixels.
    3. Identify the object with the maximum number of pixels (largest size).
    4. Determine the bounding box coordinates of the largest object.
    5. Create an output grid sized to the bounding box, filled with background color (0).
    6. Copy the pixels of the largest object into the output grid, adjusting coordinates relative to the bounding box.
    7. Convert the output NumPy array back to a list of lists.
    """
    
    input_np = np.array(input_grid, dtype=int)
    
    # Find all objects in the grid
    objects = find_objects(input_np)

    # Handle case where there are no non-background objects
    if not objects:
        return [[]] # Or potentially return an empty grid or input based on convention

    # Find the largest object based on size (pixel count)
    largest_object = max(objects, key=lambda obj: obj['size'])

    # Get the coordinates and color of the largest object
    largest_coords = largest_object['coords']
    largest_color = largest_object['color'] # Actually, color is needed for placement

    # Determine the bounding box of the largest object
    min_r, min_c, max_r, max_c = get_bounding_box(largest_coords)

    # Calculate the dimensions of the output grid
    output_height = max_r - min_r + 1
    output_width = max_c - min_c + 1

    # Initialize the output grid with background color (0)
    output_np = np.zeros((output_height, output_width), dtype=int)

    # Place the largest object's pixels into the output grid
    for r, c in largest_coords:
        # Adjust coordinates relative to the top-left corner of the bounding box
        output_r = r - min_r
        output_c = c - min_c
        output_np[output_r, output_c] = largest_color

    # Convert the output NumPy array back to a list of lists
    output_grid = output_np.tolist()

    return output_grid