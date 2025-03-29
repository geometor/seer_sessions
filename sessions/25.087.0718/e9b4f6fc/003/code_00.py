import numpy as np
from collections import Counter, deque

"""
Identifies the largest connected non-background object in the input grid. 
Determines a "characteristic color" based on the most frequent color among the 
object's border pixels (pixels adjacent to background/edge). Transforms the 
colors of all pixels within this largest object based on specific rules dictated 
by the characteristic color:
- If characteristic_color=Azure(8): Swap Red(2)<->Green(3), Swap Blue(1)<->Yellow(4).
- If characteristic_color=Green(3): Blue(1)->Red(2), Gray(5)->Yellow(4), Azure(8)->Magenta(6).
- If characteristic_color=Blue(1): Yellow(4)->Red(2), Azure(8)->Green(3).
Other colors within the object remain unchanged. The output grid contains only 
the transformed target object, cropped to its bounding box.
"""

# --- Helper Functions ---

def find_objects(grid_np):
    """
    Finds all connected components (objects) of non-background pixels (1-9) 
    in the grid using Breadth-First Search (BFS). Considers 8-way adjacency 
    (including diagonals).

    Args:
        grid_np (np.ndarray): The input grid as a NumPy array.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object 
              and contains:
              - 'pixels': set of (row, col) tuples for the object's pixels.
              - 'size': integer count of pixels in the object.
              - 'bb': tuple (min_row, min_col, max_row, max_col) bounding box.
    """
    height, width = grid_np.shape
    visited = np.zeros_like(grid_np, dtype=bool)
    objects = []
    for r in range(height):
        for c in range(width):
            # Start BFS if pixel is non-background and not visited
            if grid_np[r, c] != 0 and not visited[r, c]:
                current_object_pixels = set()
                q = deque([(r, c)])
                visited[r, c] = True
                current_object_pixels.add((r, c))
                min_r, min_c, max_r, max_c = r, c, r, c

                while q:
                    row, col = q.popleft()
                    # Update bounding box coordinates
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Explore 8 neighbors
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            # Check bounds and if neighbor is non-background and not visited
                            if 0 <= nr < height and 0 <= nc < width and \
                               grid_np[nr, nc] != 0 and not visited[nr, nc]:
                                visited[nr, nc] = True
                                current_object_pixels.add((nr, nc))
                                q.append((nr, nc))
                                
                # Store found object details
                if current_object_pixels:
                    objects.append({
                        'pixels': current_object_pixels,
                        'size': len(current_object_pixels),
                        'bb': (min_r, min_c, max_r, max_c)
                    })
    return objects

def get_border_pixels(grid_np, obj_pixels):
    """
    Identifies the border pixels of a given object. A border pixel is an object 
    pixel that is adjacent (8-way) to a background pixel (0) or the grid edge.

    Args:
        grid_np (np.ndarray): The input grid as a NumPy array.
        obj_pixels (set): A set of (row, col) tuples representing the object's pixels.

    Returns:
        set: A set of (row, col) tuples representing the border pixels.
    """
    height, width = grid_np.shape
    border_pixels = set()
    for r, c in obj_pixels:
        is_border = False
        # Check 8 neighbors
        for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                if dr == 0 and dc == 0:
                    continue
                nr, nc = r + dr, c + dc
                # Check if neighbor is outside grid bounds or is background (0)
                if not (0 <= nr < height and 0 <= nc < width) or \
                   grid_np[nr, nc] == 0:
                    is_border = True
                    break # Found a condition making it a border pixel
        if is_border:
             border_pixels.add((r, c))
             
    # Ensure even single-pixel objects touching background are counted
    if not border_pixels and len(obj_pixels) > 0:
         r,c = next(iter(obj_pixels)) # Get any pixel from the object
         for dr in [-1, 0, 1]:
            for dc in [-1, 0, 1]:
                 if dr == 0 and dc == 0: continue
                 nr, nc = r + dr, c + dc
                 if not (0 <= nr < height and 0 <= nc < width) or grid_np[nr, nc] == 0:
                     # If any neighbor is background/edge, the whole (small) object counts as border
                      return obj_pixels


    return border_pixels

def get_characteristic_color(grid_np, border_pixels):
    """
    Determines the characteristic color by finding the most frequent color 
    among the border pixels. Ties are broken by choosing the smallest color index.

    Args:
        grid_np (np.ndarray): The input grid as a NumPy array.
        border_pixels (set): The set of border pixels for the target object.

    Returns:
        int: The characteristic color index, or -1 if no border pixels exist.
    """
    if not border_pixels:
        return -1 
    
    # Get colors of the border pixels
    border_colors = [grid_np[r, c] for r, c in border_pixels]
    if not border_colors:
        return -1

    # Count frequencies of each color
    color_counts = Counter(border_colors)
    
    # Find the most common color(s)
    # Sort by frequency (descending) then by color index (ascending) for tie-breaking
    most_common = sorted(color_counts.items(), key=lambda item: (-item[1], item[0]))
    
    # Return the color index of the most frequent (and smallest in case of tie)
    return most_common[0][0]

def transform_pixel_color(original_color, characteristic_color):
    """
    Applies color transformation rules based on the characteristic color.

    Args:
        original_color (int): The original color index of the pixel.
        characteristic_color (int): The determined characteristic color for the object.

    Returns:
        int: The transformed color index.
    """
    if characteristic_color == 8: # Azure border -> Azure rules
        if original_color == 2: return 3 # Red -> Green
        if original_color == 3: return 2 # Green -> Red
        if original_color == 1: return 4 # Blue -> Yellow
        if original_color == 4: return 1 # Yellow -> Blue
    elif characteristic_color == 3: # Green border -> Green rules
        if original_color == 1: return 2 # Blue -> Red
        if original_color == 5: return 4 # Gray -> Yellow
        if original_color == 8: return 6 # Azure -> Magenta
    elif characteristic_color == 1: # Blue border -> Blue rules
        if original_color == 4: return 2 # Yellow -> Red
        if original_color == 8: return 3 # Azure -> Green
        
    # If no specific rule applies for the characteristic color / original color combo,
    # or if characteristic color isn't one of the special cases (1, 3, 8),
    # return the original color.
    return original_color

# --- Main Transformation Function ---

def transform(input_grid):
    """
    Transforms the input grid according to the described logic: find the largest 
    object, determine its characteristic border color, transform all its pixels 
    based on rules associated with that color, and return the cropped, 
    transformed object.

    Args:
        input_grid (list of list of int): The input grid.

    Returns:
        list of list of int: The transformed output grid.
    """
    # Convert input to NumPy array for easier manipulation
    input_grid_np = np.array(input_grid, dtype=int)
    
    # 1. Find all non-background objects
    objects = find_objects(input_grid_np)

    # Handle case with no objects found
    if not objects:
        return [[]] # Return empty grid as per ARC convention maybe?

    # 2. Select the largest object
    # If sizes are equal, find_objects order + max will pick one deterministically.
    target_object = max(objects, key=lambda obj: obj['size'])
    target_pixels = target_object['pixels']
    min_r, min_c, max_r, max_c = target_object['bb']

    # 3. Determine the border pixels of the target object
    border_pixels = get_border_pixels(input_grid_np, target_pixels)

    # 4. Find the characteristic color from the border pixels
    characteristic_color = get_characteristic_color(input_grid_np, border_pixels)

    # Handle edge case where characteristic color couldn't be determined (e.g., no border pixels found)
    if characteristic_color == -1:
         # This case seems unlikely based on examples for the largest object, 
         # but if it happens, maybe return the object untransformed? Or empty?
         # Let's return it untransformed for now as a fallback.
         output_height = max_r - min_r + 1
         output_width = max_c - min_c + 1
         output_grid = np.zeros((output_height, output_width), dtype=int)
         for r, c in target_pixels:
              out_r, out_c = r - min_r, c - min_c
              output_grid[out_r, out_c] = input_grid_np[r,c]
         return output_grid.tolist()


    # 5. Create the output grid based on the target object's bounding box
    output_height = max_r - min_r + 1
    output_width = max_c - min_c + 1
    # Initialize with background color (0)
    output_grid = np.zeros((output_height, output_width), dtype=int) 

    # 6. Iterate through *all* pixels of the target object and apply transformation
    for r, c in target_pixels:
        # Get original color
        original_color = input_grid_np[r, c]
        
        # 7. Apply transformation rule based on characteristic color
        transformed_color = transform_pixel_color(original_color, characteristic_color)
        
        # 8. Place transformed color in the output grid at relative coordinates
        out_r = r - min_r
        out_c = c - min_c
        output_grid[out_r, out_c] = transformed_color
            
    # 9. Return the final cropped and transformed grid as a list of lists
    return output_grid.tolist()