import numpy as np
from collections import deque

"""
Identifies the background color (assumed to be the color of the top-left pixel).
Finds all connected components (objects) of non-background colors, noting their 
shape, color, and original bounding box.
Creates a new grid of the same dimensions, filled with the background color.
For each identified object, determines a target vertical edge (Top or Bottom) based 
on the background color and the object's color according to specific rules:
 - If the background is White (0):
    - Green (3) and Blue (1) objects move to the Top edge.
    - Yellow (4) and Red (2) objects move to the Bottom edge.
 - If the background is Gray (5):
    - Green (3), Orange (7), Maroon (9), and Red (2) objects move to the Top edge.
    - Blue (1) and Yellow (4) objects move to the Bottom edge.
The object is then drawn onto the output grid, preserving its original horizontal 
position (column) and shape, but aligning either its top row with row 0 (for Top edge) 
or its bottom row with the last row of the grid (for Bottom edge).
"""

def find_objects(grid, background_color):
    """
    Finds all connected components (objects) of non-background colors using 8-way connectivity.

    Args:
        grid (np.array): The input grid.
        background_color (int): The color to ignore.

    Returns:
        list: A list of dictionaries, each representing an object with its
              properties: color, pixels_relative (relative to min_r, min_c), 
              height, width, min_r, min_c.
    """
    rows, cols = grid.shape
    visited = set()
    objects = []
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != background_color and (r, c) not in visited:
                color = grid[r, c]
                q = deque([(r, c)])
                visited.add((r, c))
                component_pixels_absolute = []
                min_r, min_c = r, c
                max_r, max_c = r, c

                # Breadth-First Search to find all connected pixels of the same color
                while q:
                    curr_r, curr_c = q.popleft()
                    component_pixels_absolute.append((curr_r, curr_c))
                    min_r = min(min_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_r = max(max_r, curr_r)
                    max_c = max(max_c, curr_c)

                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = curr_r + dr, curr_c + dc
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               grid[nr, nc] == color and (nr, nc) not in visited:
                                visited.add((nr, nc))
                                q.append((nr, nc))
                
                # Calculate object properties
                height = max_r - min_r + 1
                width = max_c - min_c + 1
                # Store pixel coordinates relative to the object's top-left corner (min_r, min_c)
                pixels_relative = [(pr - min_r, pc - min_c) for pr, pc in component_pixels_absolute]
                
                objects.append({
                    'color': color,
                    'pixels_relative': pixels_relative, # Coordinates relative to object's top-left
                    'height': height,
                    'width': width,
                    'min_r': min_r, # Original top row
                    'min_c': min_c, # Original left column
                })
    return objects

def transform(input_grid):
    """
    Transforms the input grid by moving objects vertically to the top or bottom edge
    based on background and object color, preserving horizontal position.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape

    # Determine background color (assuming top-left pixel)
    background_color = input_np[0, 0] 

    # Find all non-background objects
    objects = find_objects(input_np, background_color)

    # Create the output grid filled with the background color
    output_grid = np.full((rows, cols), background_color, dtype=int)

    # Define color mappings to target edge based on background
    top_edge_colors = {}
    bottom_edge_colors = {}

    if background_color == 0: # White background
        top_edge_colors = {3, 1}    # Green, Blue
        bottom_edge_colors = {4, 2} # Yellow, Red
    elif background_color == 5: # Gray background
        top_edge_colors = {3, 7, 9, 2} # Green, Orange, Maroon, Red
        bottom_edge_colors = {1, 4}    # Blue, Yellow
    else:
        # Default behavior for unhandled background colors: perhaps no movement?
        # For now, let's just copy input to output if background is unknown.
        print(f"Warning: Unhandled background color {background_color}. Returning original grid.")
        return input_grid # Or return output_grid which is just background

    # Place each object in the output grid at its new position
    for obj in objects:
        obj_color = obj['color']
        obj_height = obj['height']
        obj_min_c = obj['min_c'] # Target column is the original column
        
        target_row = -1 # Initialize target row

        # Determine target edge and calculate target_row
        if obj_color in top_edge_colors:
            target_row = 0 # Align top of object with row 0
        elif obj_color in bottom_edge_colors:
            target_row = rows - obj_height # Align bottom of object with last row
        else:
            # Handle unexpected colors within a known background case
            # Option: place at original position, place at top, or skip? Let's skip for now.
            print(f"Warning: Color {obj_color} rule undefined for background {background_color}. Skipping object.")
            continue 
            
        # Draw the object onto the output grid at the calculated position
        for dr, dc in obj['pixels_relative']:
            # Calculate absolute coordinates in the output grid
            place_r = target_row + dr
            place_c = obj_min_c + dc # Use original min_c for horizontal position
            
            # Check bounds before writing (should be safe if logic is correct)
            if 0 <= place_r < rows and 0 <= place_c < cols:
                output_grid[place_r, place_c] = obj_color
            else:
                # This indicates an error in calculation or unexpected input
                print(f"Error: Calculated pixel ({place_r}, {place_c}) out of bounds.")

    return output_grid.tolist()