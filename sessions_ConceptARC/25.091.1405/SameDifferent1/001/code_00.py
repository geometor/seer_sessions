import numpy as np

"""
Identifies all non-white objects in the input grid. Classifies each object as 'solid' 
(if its pixels perfectly fill its bounding box) or 'non-solid'. 
Counts the number of solid (N_solid) and non-solid (N_non_solid) objects.
If N_solid and N_non_solid are different, keeps only the non-solid objects in the output grid.
If N_solid equals N_non_solid, keeps only the solid objects in the output grid.
All pixels belonging to objects that are not kept become white (0) in the output.
"""

def find_objects(grid):
    """
    Finds all connected objects of the same non-background color in the grid.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A list of tuples, where each tuple represents an object and contains:
        (color, set of coordinates {(row, col), ...}).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # Check if the cell is part of the background or already visited
            if color == 0 or visited[r, c]:
                continue
                
            # Start BFS to find the connected object
            obj_coords = set()
            queue = [(r, c)]
            visited[r, c] = True
            
            while queue:
                row, col = queue.pop(0)
                obj_coords.add((row, col))
                
                # Explore neighbors (orthogonal)
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = row + dr, col + dc
                    
                    # Check bounds and if the neighbor has the same color and not visited
                    if 0 <= nr < rows and 0 <= nc < cols and \
                       grid[nr, nc] == color and not visited[nr, nc]:
                        visited[nr, nc] = True
                        queue.append((nr, nc))
                        
            objects.append((color, obj_coords))
            
    return objects

def get_bounding_box(obj_coords):
    """Calculates the bounding box for a set of coordinates."""
    if not obj_coords:
        return None
    rows = [r for r, c in obj_coords]
    cols = [c for r, c in obj_coords]
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)
    return min_r, min_c, max_r, max_c

def is_solid(obj_coords, bbox):
    """Checks if an object's pixels fill its bounding box."""
    if not obj_coords or bbox is None:
        return False
    min_r, min_c, max_r, max_c = bbox
    bbox_height = max_r - min_r + 1
    bbox_width = max_c - min_c + 1
    bbox_area = bbox_height * bbox_width
    return len(obj_coords) == bbox_area

def transform(input_grid):
    """
    Filters objects based on solidity and counts.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A numpy array representing the output grid.
    """
    # Convert input to numpy array
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape
    
    # Initialize output grid with background color
    output_grid = np.zeros_like(grid, dtype=int)
    
    # Find all objects in the input grid
    objects = find_objects(grid)
    
    # Classify objects and count
    solid_objects = []
    non_solid_objects = []
    for color, coords in objects:
        bbox = get_bounding_box(coords)
        if is_solid(coords, bbox):
            solid_objects.append((color, coords))
        else:
            non_solid_objects.append((color, coords))
            
    N_solid = len(solid_objects)
    N_non_solid = len(non_solid_objects)
    
    # Determine which objects to keep
    objects_to_keep = []
    if N_solid > N_non_solid or N_non_solid > N_solid:
        # Keep non-solid if counts are different
        objects_to_keep = non_solid_objects
    elif N_solid == N_non_solid:
        # Keep solid if counts are equal
        objects_to_keep = solid_objects
        
    # Draw the kept objects onto the output grid
    for color, coords in objects_to_keep:
        for r, c in coords:
            if 0 <= r < rows and 0 <= c < cols: # Redundant check, but safe
                output_grid[r, c] = color
                
    return output_grid.tolist() # Return as list of lists if required by testing framework