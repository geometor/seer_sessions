
Previous Code:
```python
import numpy as np
from collections import Counter

"""
Identify the background color (most frequent).
Identify a 'template' object located on the bottom row: determine its color (template_color) and shape (template_shape).
Identify the 'main' object color (most frequent non-background, non-template color).
Define a 'replacement' color based on the template color (yellow=4 maps to green=3).
Initialize the output grid as a copy of the input.
Iterate through all possible locations in the grid that could contain the template_shape:
1. If an area matches the template_shape and consists entirely of the main_color, replace that area in the output with the replacement_color.
2. If an area matches the template_shape and consists entirely of the template_color (i.e., it's the original template instance), replace that area in the output with the replacement_color.
3. If an area matches the template_shape, consists entirely of the background_color, AND is edge-adjacent to any pixel of the main_color in the input grid, fill that area in the output with the template_color.
Pixels not modified by these rules retain their original color from the input grid.
"""

def find_objects(grid, target_color):
    """Finds connected components of a specific color."""
    if grid.size == 0:
        return []
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            if grid[r, c] == target_color and not visited[r, c]:
                obj_pixels = []
                q = [(r, c)]
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c
                
                while q:
                    row, col = q.pop(0)
                    obj_pixels.append((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr, nc] == target_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                
                bounding_box = (min_r, min_c, max_r, max_c)
                objects.append({'pixels': obj_pixels, 'bbox': bounding_box, 'color': target_color})
    return objects

def get_shape_from_bbox(bbox):
    """Calculates height and width from bounding box."""
    min_r, min_c, max_r, max_c = bbox
    return (max_r - min_r + 1, max_c - min_c + 1)

def check_area_color(grid, r, c, shape_h, shape_w, color):
    """Checks if the specified area in the grid is uniformly of the given color."""
    height, width = grid.shape
    if r + shape_h > height or c + shape_w > width:
        return False # Shape out of bounds
    return np.all(grid[r:r+shape_h, c:c+shape_w] == color)

def check_adjacency(grid, r, c, shape_h, shape_w, adjacent_color):
    """Checks if any pixel within the r,c area is edge-adjacent to adjacent_color outside the area."""
    height, width = grid.shape
    for i in range(shape_h):
        for j in range(shape_w):
            row, col = r + i, c + j
            # Check neighbors (N, S, E, W)
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = row + dr, col + dc
                # Check if neighbor is within grid bounds
                if 0 <= nr < height and 0 <= nc < width:
                    # Check if neighbor is OUTSIDE the shape area
                    is_outside = not (0 <= nr - r < shape_h and 0 <= nc - c < shape_w)
                    if is_outside and grid[nr, nc] == adjacent_color:
                        return True
    return False

def fill_area(grid, r, c, shape_h, shape_w, color):
    """Fills the specified area in the grid with the given color."""
    grid[r:r+shape_h, c:c+shape_w] = color

def transform(input_grid):
    """
    Applies the transformation rules based on identifying a template object
    on the bottom row and replacing/filling based on its shape and color relationships.
    """
    input_array = np.array(input_grid, dtype=int)
    height, width = input_array.shape
    output_array = np.copy(input_array)

    # 1. Identify Background Color
    colors, counts = np.unique(input_array, return_counts=True)
    if not colors.size: return [] # Handle empty grid case
    background_color = colors[np.argmax(counts)]

    # 2. Identify Template Object
    template_object = None
    template_color = -1
    template_shape = None
    template_bbox = None
    
    # Find non-background objects touching the bottom row
    potential_template_colors = [c for c in colors if c != background_color]
    found_template = False
    for color in potential_template_colors:
        objects = find_objects(input_array, color)
        for obj in objects:
            min_r, min_c, max_r, max_c = obj['bbox']
            # Check if the object is entirely on the bottom row
            # Or more robustly, check if *any* part is on the bottom row and it's unique there
            # Let's assume the unique non-background object fully contained in the bottom row
            is_on_bottom_row = True
            for r_pix, c_pix in obj['pixels']:
                if r_pix != height - 1:
                    is_on_bottom_row = False
                    break
            
            if is_on_bottom_row:
                 # Simple check: find first object completely on bottom row
                 # More complex logic might be needed if multiple objects fit this
                 template_object = obj
                 template_color = color
                 template_bbox = obj['bbox']
                 template_shape = get_shape_from_bbox(template_bbox)
                 found_template = True
                 break # Assume first one found is the template
        if found_template:
            break

    if not found_template:
        # Fallback or error handling if no template found
        # Maybe look for the smallest non-background object? Or unique color?
        # For now, assume template is always found as per examples
        # A reasonable fallback might be to return input if structure isn't matched
        return input_grid 

    # 3. Identify Main Object Color
    main_color_candidates = {}
    for r in range(height):
        for c in range(width):
            color = input_array[r, c]
            if color != background_color and color != template_color:
                main_color_candidates[color] = main_color_candidates.get(color, 0) + 1
    
    if not main_color_candidates:
         # No main color found (maybe only background and template exist)
         # Or maybe the template IS the main color in some cases?
         # Let's assume a main color distinct from template exists based on examples.
         # Return input if no clear main color.
         return input_grid 

    main_color = max(main_color_candidates, key=main_color_candidates.get)


    # 4. Determine Replacement Color (Specific mapping: yellow -> green)
    replacement_color = -1
    if template_color == 4: # Yellow
        replacement_color = 3 # Green
    else:
        # Define behavior for other template colors if needed
        # Default to template color itself? Or an error?
        # Given examples, let's stick to the 4->3 mapping.
        # If template isn't yellow, maybe no replacement happens.
        # Let's assume the rule only applies if template is yellow.
        if template_color != 4:
             return input_grid # Or apply different logic

    # 5. Iterate and Apply Rules
    template_h, template_w = template_shape
    
    # Keep track of areas modified by rules 1, 2, 3 to avoid overwriting them later
    # when copying non-modified main object parts. However, the current logic
    # initializes output as a copy, so we only overwrite based on rules.

    for r in range(height - template_h + 1):
        for c in range(width - template_w + 1):
            # Rule 1: Main Object Match -> Replace with replacement_color
            if check_area_color(input_array, r, c, template_h, template_w, main_color):
                fill_area(output_array, r, c, template_h, template_w, replacement_color)

            # Rule 2: Template Object Match -> Replace with replacement_color
            # This specifically targets the original template instance(s)
            elif check_area_color(input_array, r, c, template_h, template_w, template_color):
                 fill_area(output_array, r, c, template_h, template_w, replacement_color)

            # Rule 3: Adjacent Background Match -> Fill with template_color
            elif check_area_color(input_array, r, c, template_h, template_w, background_color):
                if check_adjacency(input_array, r, c, template_h, template_w, main_color):
                    fill_area(output_array, r, c, template_h, template_w, template_color) # Fill with original template color

    # No explicit step 8 needed as we started with a copy and selectively overwrote.

    return output_array.tolist()
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 8 8 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 8 8 8 8 8 8 8 8 8 8 8 1 1 1 1
1 1 1 1 1 1 1 1 8 8 8 8 8 8 8 8 8 8 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 8 8 8 8 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 8 8 8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1 1 1 1
1 1 1 8 8 8 8 8 8 8 8 8 8 8 8 8 8 1 1 1 1 1
1 1 8 8 8 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1 1 1
1 1 1 8 8 8 8 8 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 8 8 1 1 1 1 1
1 1 1 1 1 1 1 1 1 8 8 8 8 8 8 8 8 8 1 1 1 1
1 1 1 1 1 1 1 1 1 8 8 8 8 8 8 8 8 8 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 8 8 8 8 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 8 8 8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 8 8 8 8 8 8 8 8 8 1 1 1 1 8 8 1 1 1 1 1
1 1 8 8 8 8 8 8 8 8 8 8 1 1 1 8 8 8 1 1 1 1
1 1 8 8 8 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 8 8 8 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 8 8 8 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 8 8 8 8 8 1 1 1 1 1 1 1 1 8 8 8 8 8 1 1 1
1 1 8 8 8 8 8 1 1 1 1 8 8 8 8 8 8 8 8 1 1 1
1 1 1 1 8 8 1 1 8 8 8 8 8 8 8 8 8 8 8 1 1 1
1 1 1 1 1 1 1 1 1 8 8 8 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 4 4 4 4 1 1 1 1 1 1 1
```
Expected Output:
```
1 1 1 1 1 1 1 1 1 1 1 3 3 3 3 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 8 8 8 8 4 4 4 4 8 8 8 1 1 1 1
1 1 1 1 1 1 1 1 8 8 8 1 1 1 1 8 8 8 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 4 4 4 4 8 8 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 3 3 3 1 1 1 1 3 3 3 3 1 1 1 1 1 1 1
1 1 1 1 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1 1 1 1
1 1 1 8 8 8 8 8 8 8 8 4 4 4 4 8 8 1 1 1 1 1
1 1 8 8 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1 1 1 1
1 1 1 8 8 8 8 8 1 1 1 4 4 4 4 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 8 8 1 1 1 1 1
1 1 1 1 1 1 1 1 1 3 3 3 3 3 3 3 3 3 1 1 1 1
1 1 1 1 1 1 1 1 1 8 8 1 1 1 1 8 8 8 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 4 4 4 4 8 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 8 8 8 1 1 1 1 4 4 4 4 1 1 1 1 1 1 1
1 1 8 8 8 8 8 8 8 8 8 1 1 1 1 8 8 1 1 1 1 1
1 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 3 1 1 1 1
1 1 8 8 8 8 8 8 8 8 8 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 8 8 8 1 4 4 4 4 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 8 8 8 1 1 1 1 1 1 4 4 4 4 1 1 1 1 1 1 1
1 8 8 8 8 8 1 1 1 1 1 1 1 1 1 8 8 8 8 1 1 1
1 1 3 3 3 3 3 1 1 1 1 3 3 3 3 3 3 3 3 1 1 1
1 1 1 1 8 8 1 1 8 8 8 1 1 1 1 8 8 8 8 1 1 1
1 1 1 1 1 1 1 1 1 8 8 4 4 4 4 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 4 4 4 4 1 1 1 1 1 1 1
```
Transformed Output:
```
1 1 1 1 1 1 1 1 4 4 4 4 4 4 4 4 1 1 1 1 1 1
1 1 1 1 4 4 4 4 4 4 4 8 8 4 4 4 4 4 4 4 4 1
1 1 1 4 4 4 4 3 3 3 3 3 3 3 3 3 3 3 4 4 4 4
1 1 1 1 4 4 4 4 3 3 3 3 3 3 3 3 3 3 4 4 4 4
1 1 1 1 1 4 4 4 4 4 4 4 4 3 3 3 3 4 4 4 4 1
1 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 1 1
4 4 4 4 8 8 8 4 4 4 4 4 4 4 1 1 1 1 1 1 1 1
4 4 4 4 3 3 3 3 3 3 3 4 4 4 4 4 4 4 4 4 1 1
1 1 1 3 3 3 3 3 3 3 3 3 3 3 3 3 3 4 4 4 4 1
1 1 3 3 3 3 3 3 3 3 3 3 4 4 4 4 4 4 4 4 1 1
1 1 1 3 3 3 3 3 4 4 4 4 4 4 4 4 4 4 4 4 1 1
4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 8 8 4 4 4 4 1
1 1 1 1 1 4 4 4 4 3 3 3 3 3 3 3 3 3 4 4 4 4
1 1 1 1 1 4 4 4 4 3 3 3 3 3 3 3 3 3 4 4 4 4
1 1 1 1 1 1 4 4 4 4 4 4 3 3 3 3 4 4 4 4 4 1
1 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 1 1 1
4 4 4 4 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4 4 1 1
1 1 3 3 3 3 3 3 3 3 3 4 4 4 4 8 8 4 4 4 4 1
1 1 3 3 3 3 3 3 3 3 3 3 1 1 1 8 8 8 4 4 4 4
1 1 3 3 3 3 3 3 3 3 3 3 4 4 4 4 4 4 4 4 4 1
4 4 4 4 4 4 4 8 8 8 4 4 4 4 4 1 1 1 1 1 1 1
4 4 4 4 4 4 4 4 4 4 4 4 4 1 1 1 1 1 1 1 1 1
1 1 8 8 8 4 4 4 4 1 1 4 4 4 4 4 4 4 4 4 4 4
1 3 3 3 3 3 4 4 4 4 4 4 4 4 3 3 3 3 3 1 1 1
1 1 3 3 3 3 3 4 4 4 4 3 3 3 3 3 3 3 3 1 1 1
4 4 4 4 8 8 1 1 3 3 3 3 3 3 3 3 3 3 3 1 1 1
1 4 4 4 4 4 4 4 4 8 8 8 4 4 4 4 4 4 4 4 4 4
1 1 1 1 1 1 4 4 4 4 4 4 4 4 4 1 1 1 1 1 1 1
1 1 1 1 1 1 1 1 1 1 1 3 3 3 3 1 1 1 1 1 1 1
```
Match: False
Pixels Off: 412
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 129.15360501567397

## Example 2:
Input:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 2 2 2 8 2 2 2 8 8 8 8 8 2 2 2 2 8 8
8 8 8 8 2 2 2 2 2 2 2 8 8 8 8 2 2 2 2 2 8 8
8 8 8 8 8 8 2 2 2 2 8 8 8 8 8 8 2 2 2 2 8 8
8 8 8 8 8 2 2 2 2 2 8 8 8 8 8 8 8 8 2 8 8 8
8 8 2 2 2 2 2 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 2 2 2 2 2 2 2 2 8 8 8 8 8 8 8 8
8 8 8 8 8 8 2 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 2 2 2 8 8 8 2 2 8 8 8 8 8 8 8 8
8 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 2 2 8 8 8 8 8 8 8 8 2 2 2 2 2 2 2 2 8 8
8 8 8 8 8 8 8 8 8 8 8 2 2 2 2 2 2 2 2 2 8 8
8 8 8 8 8 8 8 8 8 8 8 2 2 2 2 2 2 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
2 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
2 8 2 2 2 2 2 2 8 8 8 8 8 8 8 2 2 2 2 2 2 2
8 8 8 2 2 2 2 2 2 8 8 8 8 2 2 2 2 2 2 2 8 8
8 8 8 8 2 2 2 2 2 2 2 8 8 8 8 2 2 2 2 8 2 2
8 8 8 8 8 8 8 8 8 2 2 8 8 8 8 8 2 2 2 2 2 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 2 2 2 2 8
8 8 8 8 8 8 2 2 2 2 2 8 8 8 8 8 8 2 2 2 8 8
8 8 8 8 8 8 2 2 2 2 2 2 2 2 2 2 2 2 2 8 8 8
8 8 8 8 8 8 8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 2 2 2 2 2 8 8 8 8 8 8 8 8
8 8 4 4 4 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Expected Output:
```
8 8 3 3 3 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 4 4 4 2 2 8 2 2 2 8 8 8 8 8 2 2 2 2 8 8
8 8 8 8 8 2 2 2 2 2 2 8 8 8 8 2 2 2 2 2 8 8
8 8 4 4 4 8 2 2 2 2 8 8 8 8 8 8 2 2 2 2 8 8
8 8 8 8 8 2 2 2 2 2 8 8 8 8 8 8 8 8 2 8 8 8
8 8 3 3 3 3 3 3 3 3 3 3 3 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 2 2 2 2 2 2 2 2 8 8 8 8 8 8 8 8
8 8 4 4 4 8 2 2 2 2 2 2 2 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 2 2 2 8 8 8 2 2 8 8 8 8 8 8 8 8
8 2 4 4 4 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 2 8 8 8 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 3 3 3 3 3 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 8 8 8 2 2 2 2 2 2 2 2 8 8
8 8 4 4 4 8 8 8 8 8 8 2 2 2 2 2 2 2 2 2 8 8
8 8 8 8 8 8 8 8 8 8 8 2 2 2 2 2 2 8 8 8 8 8
8 8 4 4 4 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 8 8 8 2 2 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
3 3 3 3 3 3 3 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
2 8 8 8 8 2 2 2 8 8 8 8 8 8 8 2 2 2 2 2 2 2
8 8 4 4 4 2 2 2 2 8 8 8 8 2 2 2 2 2 2 2 8 8
8 8 8 8 8 2 2 2 2 2 2 8 8 8 8 2 2 2 2 8 2 2
8 8 4 4 4 8 8 8 8 2 2 8 8 8 8 8 2 2 2 2 2 8
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 2 2 2 2 2 8
8 8 3 3 3 8 3 3 3 3 3 8 8 8 8 8 8 3 3 3 8 8
8 8 8 8 8 8 2 2 2 2 2 2 2 2 2 2 2 2 2 8 8 8
8 8 4 4 4 8 8 8 2 2 2 2 2 2 8 8 8 8 8 8 8 8
8 8 8 8 8 8 8 8 8 2 2 2 2 2 8 8 8 8 8 8 8 8
8 8 4 4 4 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
```
Transformed Output:
```
8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8 8
8 8 4 4 4 4 4 4 4 4 4 4 4 8 4 4 4 4 4 4 4 4
8 4 4 4 3 3 3 8 3 3 3 4 4 4 4 4 3 3 3 3 8 8
8 4 4 4 3 3 3 3 3 3 3 4 4 4 4 3 3 3 3 3 8 8
8 8 4 4 4 4 3 3 3 3 4 4 4 4 4 4 3 3 3 3 8 8
4 4 4 4 4 3 3 3 3 3 4 4 4 4 4 4 4 4 2 4 4 4
8 8 3 3 3 3 3 3 3 3 3 3 3 4 4 4 4 4 4 4 4 8
4 4 4 4 4 4 3 3 3 3 3 3 3 3 4 4 4 8 8 8 8 8
8 8 8 4 4 4 3 3 3 3 3 3 3 4 4 4 8 8 8 8 8 8
4 4 4 4 4 4 3 3 3 4 4 4 2 2 4 4 4 8 8 8 8 8
8 2 2 4 4 4 4 4 4 4 4 4 4 4 4 4 8 8 8 8 8 8
8 3 3 3 3 3 4 4 4 8 8 8 8 8 8 8 8 8 8 8 8 8
8 3 3 3 3 3 4 4 4 8 4 4 4 4 4 4 4 4 4 4 4 4
8 8 2 2 4 4 4 4 8 4 4 4 3 3 3 3 3 3 3 3 8 8
4 4 4 4 4 4 8 8 4 4 4 3 3 3 3 3 3 3 3 3 8 8
8 8 8 8 8 8 8 8 4 4 4 3 3 3 3 3 3 4 4 4 4 4
8 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 4 8 8 8
4 4 4 3 3 3 3 4 4 4 8 8 8 8 8 8 8 8 8 8 8 8
3 3 3 3 3 3 3 4 4 4 8 8 8 4 4 4 4 4 4 4 4 4
2 8 3 3 3 3 3 3 4 4 4 4 4 4 4 3 3 3 3 3 3 3
4 4 4 3 3 3 3 3 3 4 4 4 4 3 3 3 3 3 3 3 8 8
8 4 4 4 3 3 3 3 3 3 3 4 4 4 4 3 3 3 3 8 2 2
8 8 4 4 4 4 4 4 4 2 2 4 4 4 4 4 3 3 3 3 3 8
8 8 8 8 4 4 4 4 4 4 4 4 4 4 4 4 3 3 3 3 3 8
8 8 8 4 4 4 3 3 3 3 3 4 4 4 4 4 4 3 3 3 8 8
8 8 8 4 4 4 3 3 3 3 3 3 3 3 3 3 3 3 3 4 4 4
8 8 8 8 4 4 4 4 3 3 3 3 3 3 4 4 4 4 4 4 4 8
8 8 8 8 8 8 4 4 4 3 3 3 3 3 4 4 4 8 8 8 8 8
8 8 3 3 3 8 8 4 4 4 4 4 4 4 4 4 8 8 8 8 8 8
```
Match: False
Pixels Off: 421
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 131.97492163009406
