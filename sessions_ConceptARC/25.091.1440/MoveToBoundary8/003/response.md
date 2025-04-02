```python
import numpy as np

"""
Identifies a single static line object (horizontal or vertical) and multiple 
single-pixel point objects of a different color. 
Moves each point object by a fixed vector determined by the line's orientation.
If the line is horizontal, the movement vector is (-5, +5) (5 steps up, 5 steps right).
If the line is vertical, the movement vector is (0, +4) (0 steps vertically, 4 steps right).
The output grid contains the static line in its original position and the points 
in their new calculated positions, against a background of color 0. Points moved 
outside the grid boundaries are omitted.
"""

def find_objects(grid):
    """
    Finds connected components (objects) of non-background colors in the grid.
    Uses 4-way connectivity (up, down, left, right).

    Args:
        grid (np.array): The input grid.

    Returns:
        dict: A dictionary where keys are colors (int > 0) and values are lists 
              of lists of coordinates [(r, c), ...], representing each distinct 
              object of that color. 
              Example: {2: [[(1,1), (1,2)], [(3,3)]], 4: [[(5,5)]]}
    """
    objects = {}
    visited = np.zeros_like(grid, dtype=bool)
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # If it's a non-background pixel and not visited yet
            if color != 0 and not visited[r, c]:
                obj_coords = []
                q = [(r, c)] # Queue for BFS
                visited[r, c] = True
                
                # Breadth-First Search to find all connected pixels of the same color
                while q:
                    row, col = q.pop(0)
                    obj_coords.append((row, col))
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check if neighbor is within bounds, has the same color, and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                # Store the found object coordinates, grouped by color
                if color not in objects:
                    objects[color] = []
                objects[color].append(obj_coords)
    return objects

def analyze_line(coords):
    """
    Checks if a list of coordinates forms a continuous straight line (horizontal or vertical).

    Args:
        coords (list): A list of (row, col) tuples representing an object's pixels.

    Returns:
        dict or None: A dictionary with line properties {'orientation': 'horizontal'/'vertical', 
                      'position': row/col index, 'span': [min_col/row, max_col/row]} 
                      if it's a valid line, otherwise None.
    """
    if not coords:
        return None

    rows = [r for r, c in coords]
    cols = [c for r, c in coords]

    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)
    num_pixels = len(coords)

    # Check if all points share the same row (horizontal)
    if min_r == max_r:
        # Verify it's continuous (number of pixels matches width)
        if num_pixels == (max_c - min_c + 1):
             return {
                "orientation": "horizontal",
                "position": min_r, # The row index
                "span": [min_c, max_c] # The column range
            }
            
    # Check if all points share the same column (vertical)
    elif min_c == max_c:
        # Verify it's continuous (number of pixels matches height)
        if num_pixels == (max_r - min_r + 1):
            return {
                "orientation": "vertical",
                "position": min_c, # The column index
                "span": [min_r, max_r] # The row range
            }
            
    # If neither horizontal nor vertical and continuous
    return None 

def transform(input_grid):
    """
    Applies the transformation rule based on a static line and moving points.
    """
    input_grid_np = np.array(input_grid, dtype=int)
    rows, cols = input_grid_np.shape
    # Initialize output grid with background color 0
    output_grid = np.zeros_like(input_grid_np) 

    # 1. Find all colored objects
    objects_by_color = find_objects(input_grid_np)
    
    # Handle empty input grid
    if not objects_by_color:
        return output_grid.tolist() 

    static_line_coords = None
    static_line_color = -1
    line_props = None
    moving_points_coords = []
    moving_points_color = -1

    # 2. Identify the line object
    # Iterate through each color and its objects
    for color, components in objects_by_color.items():
        for component_coords in components:
            # Check if this component is a valid line
            props = analyze_line(component_coords)
            if props:
                # Found the line
                static_line_coords = component_coords
                static_line_color = color
                line_props = props
                break # Stop searching for lines within this color
        if line_props:
            break # Stop searching through other colors

    # Handle case where no line is found
    if static_line_coords is None:
        # If no line found, maybe return original grid or empty? 
        # Based on examples, transformation always happens if objects exist.
        # This case might indicate an unexpected input format. Let's return input.
        # print("Warning: Could not identify a static line object.")
        return input_grid # Or potentially raise an error or return empty grid

    # 3. Identify the moving points (all pixels of the *other* color)
    for color, components in objects_by_color.items():
        if color != static_line_color:
            moving_points_color = color
            # Collect all coordinates for this color
            for component_coords in components:
                 # Assume all components of the non-line color are individual points
                 moving_points_coords.extend(component_coords) 
            break # Assume only one color for moving points

    # 4. Determine movement vector based on line orientation
    delta_r, delta_c = 0, 0
    if line_props["orientation"] == "horizontal":
        delta_r = -5 # Move up
        delta_c = +5 # Move right
    elif line_props["orientation"] == "vertical":
        delta_r = 0  # No vertical move
        delta_c = +4 # Move right

    # 5. Construct the output grid
    # 5a. Draw the static line
    for r, c in static_line_coords:
        # Check bounds just in case, though line should be within original grid
        if 0 <= r < rows and 0 <= c < cols:
             output_grid[r, c] = static_line_color

    # 5b. Calculate new positions for moving points and draw them
    if moving_points_color != -1:
        for r_orig, c_orig in moving_points_coords:
            # Calculate new position
            new_r = r_orig + delta_r
            new_c = c_orig + delta_c

            # Draw the point at the new position ONLY if it's within grid bounds
            if 0 <= new_r < rows and 0 <= new_c < cols:
                output_grid[new_r, new_c] = moving_points_color
            # else: Point moved off-grid, it's omitted from the output.

    # 6. Return the final grid
    return output_grid.tolist()
```