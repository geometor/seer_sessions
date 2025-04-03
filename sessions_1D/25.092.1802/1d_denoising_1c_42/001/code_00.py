import numpy as np

"""
Identifies the primary non-background color in the input grid.
Finds all contiguous objects composed of this primary color (using horizontal/vertical adjacency).
Determines the object with the largest number of pixels.
Creates an output grid containing only the pixels of this largest object, with all other pixels set to the background color (0).
"""

def find_objects(grid, target_color):
    """
    Finds all contiguous objects of a specific color in the grid.

    Args:
        grid (np.array): The input grid.
        target_color (int): The color of the objects to find.

    Returns:
        list: A list of sets, where each set contains the (row, col) coordinates
              of the pixels belonging to a single contiguous object.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            # If we find a pixel of the target color that hasn't been visited yet,
            # start a search (BFS) to find its connected component (object).
            if grid[r, c] == target_color and not visited[r, c]:
                obj_coords = set()
                q = [(r, c)] # Queue for BFS
                visited[r, c] = True

                while q:
                    row, col = q.pop(0)
                    obj_coords.add((row, col))

                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc

                        # Check if neighbor is within bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # Check if neighbor is the target color and not visited
                            if grid[nr, nc] == target_color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                
                if obj_coords: # Should always be true here, but good practice
                    objects.append(obj_coords)
                    
    return objects

def transform(input_grid):
    """
    Filters the input grid to keep only the largest contiguous object of the
    primary non-background color.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 2D numpy array representing the output grid.
    """
    
    # 1. Identify the primary non-background color
    # Find unique non-zero colors and assume the most frequent one is primary
    # Or simpler: find *any* non-zero color if examples guarantee only one.
    unique_colors, counts = np.unique(input_grid, return_counts=True)
    primary_color = 0 
    for color in unique_colors:
        if color != 0:
            primary_color = color
            break # Assume only one non-background color based on examples
            
    if primary_color == 0: # Handle case of all background pixels
        return np.copy(input_grid)

    # 2. Find all distinct contiguous objects of the primary color
    objects = find_objects(input_grid, primary_color)

    # 3. Calculate sizes and find the largest object
    largest_object_coords = set()
    max_size = 0
    if objects: # Check if any objects were found
        for obj in objects:
            if len(obj) > max_size:
                max_size = len(obj)
                largest_object_coords = obj
        
    # 4. Create the output grid (initialized with background color)
    output_grid = np.zeros_like(input_grid) # Fills with 0 (background)

    # 5. Populate the output grid with the largest object
    for r, c in largest_object_coords:
        output_grid[r, c] = primary_color

    return output_grid
