import numpy as np

"""
Identify the two distinct non-white colored objects in the input grid. 
Determine the primary object based on the largest bounding box area, 
using the lower color index as a tie-breaker. Determine the secondary object.
Create a 3x3 output grid filled with the secondary object's color.
Map the primary object's pixels onto the 3x3 grid, preserving their relative positions within the primary object's bounding box, using the primary object's color.
"""

def find_objects(grid):
    """
    Finds all contiguous objects of non-background colors in the grid.
    Returns a dictionary mapping color to a list of pixel coordinates.
    """
    objects = {}
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != 0 and not visited[r, c]:
                obj_pixels = []
                q = [(r, c)]
                visited[r, c] = True
                
                while q:
                    row, col = q.pop(0)
                    obj_pixels.append((row, col))
                    
                    # Check neighbors (4-directional)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                # Store the found object by its color
                # Assumes only one object per color based on examples
                if color not in objects:
                    objects[color] = obj_pixels
                else:
                    # If multiple objects of the same color exist, this needs revision
                    # But based on examples, we merge them for bounding box calculation
                    objects[color].extend(obj_pixels) 
                    
    return objects

def get_object_details(pixels):
    """
    Calculates the bounding box and area for a list of pixels.
    Returns: min_r, min_c, height, width, area
    """
    if not pixels:
        return None, None, 0, 0, 0
        
    rows = [p[0] for p in pixels]
    cols = [p[1] for p in pixels]
    
    min_r, max_r = min(rows), max(rows)
    min_c, max_c = min(cols), max(cols)
    
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    area = height * width
    
    return min_r, min_c, height, width, area


def transform(input_grid_list):
    """
    Transforms the input grid based on the identified rules.

    Args:
        input_grid_list: A list of lists representing the input grid.

    Returns:
        A list of lists representing the 3x3 output grid.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    
    # 1. Identify the two distinct non-white colored objects
    objects_by_color = find_objects(input_grid)
    
    if len(objects_by_color) != 2:
        # Handle error or unexpected input: Should have exactly two colors
        print(f"Warning: Expected 2 objects, found {len(objects_by_color)}")
        # Fallback or error based on exact requirements, maybe return input or empty?
        # For now, let's try to proceed if possible or return empty
        if len(objects_by_color) < 2:
             return [[0]*3]*3 # Return empty 3x3 if fewer than 2 objects

    colors = list(objects_by_color.keys())
    color_a = colors[0]
    color_b = colors[1]
    pixels_a = objects_by_color[color_a]
    pixels_b = objects_by_color[color_b]

    # 2. Calculate bounding box details for each object
    min_r_a, min_c_a, _, _, area_a = get_object_details(pixels_a)
    min_r_b, min_c_b, _, _, area_b = get_object_details(pixels_b)

    # 3. Determine primary and secondary objects
    primary_color, secondary_color = None, None
    primary_pixels, primary_min_r, primary_min_c = None, None, None
    
    if area_a > area_b:
        primary_color = color_a
        secondary_color = color_b
        primary_pixels = pixels_a
        primary_min_r, primary_min_c = min_r_a, min_c_a
    elif area_b > area_a:
        primary_color = color_b
        secondary_color = color_a
        primary_pixels = pixels_b
        primary_min_r, primary_min_c = min_r_b, min_c_b
    else: # Areas are equal, use color index as tie-breaker
        if color_a < color_b:
            primary_color = color_a
            secondary_color = color_b
            primary_pixels = pixels_a
            primary_min_r, primary_min_c = min_r_a, min_c_a
        else:
            primary_color = color_b
            secondary_color = color_a
            primary_pixels = pixels_b
            primary_min_r, primary_min_c = min_r_b, min_c_b

    # 4. Create the 3x3 output grid initialized with the secondary color
    # Assuming output is always 3x3 based on examples
    output_grid = np.full((3, 3), secondary_color, dtype=int)

    # 5. Map primary object pixels to the output grid based on relative coordinates
    for r, c in primary_pixels:
        rel_r = r - primary_min_r
        rel_c = c - primary_min_c
        # Ensure the relative coordinates are within the 3x3 bounds
        if 0 <= rel_r < 3 and 0 <= rel_c < 3:
            output_grid[rel_r, rel_c] = primary_color
        else:
            # This case suggests the primary object's bounding box might be > 3x3
            # Or the relative calculation is off. Based on examples, this shouldn't happen.
             print(f"Warning: Pixel ({r},{c}) maps outside 3x3 grid to ({rel_r},{rel_c}). Primary BB starts at ({primary_min_r},{primary_min_c})")


    return output_grid.tolist()