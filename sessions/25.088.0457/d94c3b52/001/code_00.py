import copy
import collections

def find_objects(grid, color):
    """
    Finds all contiguous objects of a specified color in the grid.

    Args:
        grid (list of list of int): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list: A list of objects. Each object is represented as a dictionary
              with 'coords' (a set of (row, col) tuples) and 
              'shape' (a frozenset of relative (row, col) tuples from the top-left corner).
    """
    height = len(grid)
    width = len(grid[0])
    visited = set()
    objects = []
    
    for r in range(height):
        for c in range(width):
            if grid[r][c] == color and (r, c) not in visited:
                # Found the start of a potential new object
                object_coords = set()
                q = collections.deque([(r, c)])
                visited.add((r, c))
                min_r, min_c = r, c

                while q:
                    curr_r, curr_c = q.popleft()
                    object_coords.add((curr_r, curr_c))
                    min_r = min(min_r, curr_r)
                    min_c = min(min_c, curr_c)

                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            
                            nr, nc = curr_r + dr, curr_c + dc

                            # Check bounds and color and visited status
                            if 0 <= nr < height and 0 <= nc < width and \
                               grid[nr][nc] == color and (nr, nc) not in visited:
                                visited.add((nr, nc))
                                q.append((nr, nc))

                if object_coords:
                    # Calculate relative coordinates for the shape representation
                    relative_coords = frozenset((coord_r - min_r, coord_c - min_c) for coord_r, coord_c in object_coords)
                    objects.append({'coords': object_coords, 'shape': relative_coords})
                    
    return objects

def transform(input_grid):
    """
    Identifies blue shapes (color 1) in the input grid. If an identical shape exists
    in azure (color 8) anywhere in the input grid, the blue shape is recolored to 
    orange (color 7) in the output grid. Otherwise, the blue shape remains blue. 
    Azure shapes remain azure.

    Args:
        input_grid (list of list of int): The input grid represented as a 2D list.

    Returns:
        list of list of int: The transformed grid.
    """
    
    # Create a deep copy of the input grid to modify
    output_grid = copy.deepcopy(input_grid)
    
    # Find all blue objects (color 1)
    blue_objects = find_objects(input_grid, 1)
    
    # Find all azure objects (color 8)
    azure_objects = find_objects(input_grid, 8)
    
    # Create a set of unique shapes found among the azure objects for quick lookup
    # The shape is represented by a frozenset of relative coordinates
    azure_shapes = {obj['shape'] for obj in azure_objects}
    
    # Iterate through each blue object found
    for blue_obj in blue_objects:
        # Check if the shape of the current blue object exists in the set of azure shapes
        if blue_obj['shape'] in azure_shapes:
            # If a match is found, recolor the pixels of this blue object to orange (7)
            for r, c in blue_obj['coords']:
                output_grid[r][c] = 7
                
    # Return the modified grid
    return output_grid