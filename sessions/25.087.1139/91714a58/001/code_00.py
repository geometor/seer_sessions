import numpy as np
from collections import deque

"""
Isolate the largest contiguous block of non-black pixels from the input grid.

1.  Identify all distinct contiguous blocks (objects) of non-black pixels in the input grid. Contiguity is defined by horizontal and vertical adjacency.
2.  Calculate the size (number of pixels) of each identified object.
3.  Find the object with the maximum size. If there's a tie, the examples suggest only one largest object exists, but the code should handle potential ties (e.g., by taking the first one found).
4.  Create an output grid of the same dimensions as the input, initialized with black (0).
5.  Copy the pixels belonging to the largest object found in step 3 onto the output grid at their original positions, preserving their color.
"""

def find_objects(grid):
    """
    Finds all contiguous objects of non-black pixels in the grid.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A list of objects, where each object is represented as a dictionary
        containing 'color', 'size', and 'pixels' (a list of (row, col) tuples).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            # If the pixel is non-black and hasn't been visited yet
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                current_object_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                
                # Perform Breadth-First Search (BFS) to find all connected pixels of the same color
                while q:
                    row, col = q.popleft()
                    current_object_pixels.append((row, col))
                    
                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        # Check bounds, color match, and visited status
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                # Store the found object
                objects.append({
                    'color': color,
                    'size': len(current_object_pixels),
                    'pixels': current_object_pixels
                })
                
    return objects

def transform(input_grid):
    """
    Transforms the input grid by isolating the largest contiguous non-black object.

    Args:
        input_grid: A numpy array representing the input grid.

    Returns:
        A numpy array representing the output grid with only the largest object.
    """
    # Convert input list of lists to numpy array if necessary
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    
    # Initialize output_grid with the background color (black, 0)
    output_grid = np.zeros_like(input_grid)
    
    # Step 1 & 2: Identify all non-black objects and their sizes
    objects = find_objects(input_grid)
    
    # If no non-black objects are found, return the empty grid
    if not objects:
        return output_grid.tolist() # Return as list of lists per spec
        
    # Step 3: Find the object with the maximum size
    # Use max function with a lambda key to find the object dict with the largest 'size'
    largest_object = max(objects, key=lambda obj: obj['size'])
    
    # Step 4 & 5: Create output grid and draw the largest object
    obj_color = largest_object['color']
    for r, c in largest_object['pixels']:
        output_grid[r, c] = obj_color
        
    # Return the final grid as a list of lists
    return output_grid.tolist()