import numpy as np
import copy

"""
Transforms the input grid based on the following rules:
1. Identify cells with value '2' as the static boundary.
2. Identify cells with value '5' as the movable objects.
3. For each cell containing '5' at position (r, c):
    a. Find the nearest boundary cell ('2') in each of the four cardinal directions (left, right, up, down).
    b. Determine the minimum distance among these four directions.
    c. If the minimum distance corresponds to a horizontal direction (left or right), reflect the '5' horizontally across the nearest vertical boundary line.
    d. If the minimum distance corresponds to a vertical direction (up or down), reflect the '5' vertically across the nearest horizontal boundary line.
    e. If there's a tie in minimum distance between horizontal and vertical directions, prioritize horizontal reflection (across the vertical boundary).
4. In the output grid:
    a. Set the original position (r, c) of the '5' to '0'.
    b. Set the calculated reflected position (new_r, new_c) to '5', ensuring it's within the grid boundaries.
5. Cells with value '0' and '2' remain unchanged in their positions.
"""

def _find_movable_objects(grid: np.ndarray, value: int) -> list[tuple[int, int]]:
    """Finds all coordinates of cells with the specified value."""
    rows, cols = np.where(grid == value)
    return list(zip(rows, cols))

def _get_nearest_boundary_distances(grid: np.ndarray, r: int, c: int, boundary_value: int) -> dict:
    """
    Calculates the distance to the nearest boundary cell in each cardinal direction.
    Returns a dictionary with distances {'left', 'right', 'up', 'down'} 
    and boundary coordinates {'c_left', 'c_right', 'r_up', 'r_down'}.
    Distances are infinity if no boundary is found in that direction.
    """
    height, width = grid.shape
    distances = {
        'left': float('inf'), 'right': float('inf'),
        'up': float('inf'), 'down': float('inf'),
        'c_left': -1, 'c_right': -1, 'r_up': -1, 'r_down': -1
    }

    # Search Left
    for search_c in range(c - 1, -1, -1):
        if grid[r, search_c] == boundary_value:
            distances['left'] = c - search_c
            distances['c_left'] = search_c
            break
            
    # Search Right
    for search_c in range(c + 1, width):
        if grid[r, search_c] == boundary_value:
            distances['right'] = search_c - c
            distances['c_right'] = search_c
            break

    # Search Up
    for search_r in range(r - 1, -1, -1):
        if grid[search_r, c] == boundary_value:
            distances['up'] = r - search_r
            distances['r_up'] = search_r
            break
            
    # Search Down
    for search_r in range(r + 1, height):
        if grid[search_r, c] == boundary_value:
            distances['down'] = search_r - r
            distances['r_down'] = search_r
            break
            
    return distances

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Reflects points with value 5 across the nearest boundary segment 
    formed by points with value 2.
    """
    # Convert to numpy array for easier manipulation
    grid_np = np.array(input_grid, dtype=int)
    output_grid_np = copy.deepcopy(grid_np)
    height, width = grid_np.shape
    
    movable_value = 5
    boundary_value = 2
    background_value = 0

    # Find all initial positions of the movable objects
    movable_coords = _find_movable_objects(grid_np, movable_value)

    # Store reflection results before modifying the grid
    reflections = []

    # Calculate reflections for each movable object
    for r, c in movable_coords:
        # Find nearest boundary distances
        distances = _get_nearest_boundary_distances(grid_np, r, c, boundary_value)

        # Determine minimum distance and reflection type
        min_dist = float('inf')
        reflect_type = None # 'horizontal' or 'vertical'
        reflect_coord = -1

        # Check horizontal distances (priority given to horizontal reflection in case of tie)
        if distances['left'] <= distances['right'] and distances['left'] != float('inf'):
            min_dist = distances['left']
            reflect_type = 'horizontal'
            reflect_coord = distances['c_left']
        elif distances['right'] < distances['left'] and distances['right'] != float('inf'):
             min_dist = distances['right']
             reflect_type = 'horizontal'
             reflect_coord = distances['c_right']
             
        # Check vertical distances
        min_dist_vert = float('inf')
        reflect_type_vert = None
        reflect_coord_vert = -1
        if distances['up'] <= distances['down'] and distances['up'] != float('inf'):
             min_dist_vert = distances['up']
             reflect_type_vert = 'vertical'
             reflect_coord_vert = distances['r_up']
        elif distances['down'] < distances['up'] and distances['down'] != float('inf'):
             min_dist_vert = distances['down']
             reflect_type_vert = 'vertical'
             reflect_coord_vert = distances['r_down']

        # Compare min horizontal and min vertical distance
        if min_dist_vert < min_dist:
             min_dist = min_dist_vert
             reflect_type = reflect_type_vert
             reflect_coord = reflect_coord_vert
        
        # Calculate new coordinates if a reflection axis was found
        new_r, new_c = -1, -1
        if reflect_type == 'horizontal':
            # Reflect horizontally across vertical line at reflect_coord (c_b)
            c_b = reflect_coord
            new_r = r
            new_c = c_b + (c_b - c) 
        elif reflect_type == 'vertical':
            # Reflect vertically across horizontal line at reflect_coord (r_b)
            r_b = reflect_coord
            new_r = r_b + (r_b - r)
            new_c = c

        # Check if reflection occurred and store results
        if reflect_type is not None:
           reflections.append(((r, c), (new_r, new_c)))


    # Apply reflections to the output grid
    for original_pos, new_pos in reflections:
        r_orig, c_orig = original_pos
        new_r, new_c = new_pos
        
        # Set original position to background
        output_grid_np[r_orig, c_orig] = background_value
        
        # Set new position to movable value, checking boundaries
        if 0 <= new_r < height and 0 <= new_c < width:
            output_grid_np[new_r, new_c] = movable_value
        # Else: if reflection goes out of bounds, the object effectively disappears

    # Convert back to list of lists
    output_grid = output_grid_np.tolist()
    return output_grid