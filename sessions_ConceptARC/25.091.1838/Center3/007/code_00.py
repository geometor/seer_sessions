import numpy as np
from collections import deque
import math

"""
Identifies all 'perfect rectangle' objects (both solid and hollow with a background interior) 
within the input grid. Selects one specific rectangle based on a two-stage median filtering process: 
first by bounding box area, then by color. Finally, crops the input grid to the bounding box 
of the selected rectangle to produce the output.

Selection Logic:
1. Find all perfect rectangle objects (solid or hollow) within the input grid, ignoring the background color (assumed 0).
2. Calculate the bounding box area for each perfect rectangle.
3. Determine the median area among all found perfect rectangles. Use the lower middle value if the count is even.
4. Filter the rectangles, keeping only those whose area equals the median area.
5. If only one rectangle remains, select it.
6. If multiple rectangles remain (i.e., they share the median area):
    a. Get the color index of each of these remaining rectangles.
    b. Determine the median color index among them. Use the lower middle value if the count is even.
    c. Select the first rectangle encountered in the filtered list that has the median color index.
7. Crop the input grid to the bounding box of the finally selected rectangle.
"""

# === Helper Functions ===

def find_objects(grid, ignore_color=0):
    """
    Finds contiguous objects of colors other than ignore_color.

    Args:
        grid (np.array): The input grid.
        ignore_color (int): The color to ignore (usually background).

    Returns:
        list: A list of dictionaries, each representing an object with
              'color', 'coords' (set of (r, c) tuples), and 'bbox'
              (min_r, min_c, max_r, max_c). Returns empty list if grid is empty.
    """
    if grid.size == 0:
        return []
    rows, cols = grid.shape
    visited = set()
    objects = []
    
    # Iterate through each cell to find starting points of objects
    for r in range(rows):
        for c in range(cols):
            # If cell is not visited and not the ignored color, start BFS
            if (r, c) not in visited and grid[r, c] != ignore_color:
                color = grid[r, c]
                obj_coords = set()
                q = deque([(r, c)])
                visited.add((r, c))
                min_r, min_c = r, c
                max_r, max_c = r, c

                # Breadth-First Search to find all connected pixels of the same color
                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))
                    # Update bounding box coordinates
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check 4 cardinal neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Ensure neighbor is within grid bounds, not visited, and matches object color
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           (nr, nc) not in visited and grid[nr, nc] == color:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                            
                # Store found object properties if it has pixels
                if obj_coords: 
                    objects.append({
                        'color': color,
                        'coords': obj_coords,
                        'bbox': (min_r, min_c, max_r, max_c)
                    })
    return objects

def is_perfect_rectangle(obj, grid, background_color=0):
    """
    Checks if an object forms a perfect solid or hollow rectangle.

    Args:
        obj (dict): The object dictionary from find_objects.
        grid (np.array): The input grid.
        background_color (int): The background color.

    Returns:
        tuple: (bool, str or None) indicating (is_perfect, type), where type
               is 'solid', 'hollow', or None.
    """
    color = obj['color']
    coords = obj['coords']
    min_r, min_c, max_r, max_c = obj['bbox']
    height = max_r - min_r + 1
    width = max_c - min_c + 1

    # --- Solid Check ---
    is_solid = True
    # Quick check: number of pixels must match bounding box area
    if len(coords) != height * width: 
        is_solid = False
    else:
        # Check every cell within the bounding box matches the object color
        for r in range(min_r, max_r + 1):
            for c in range(min_c, max_c + 1):
                if grid[r, c] != color:
                    is_solid = False
                    break
            if not is_solid:
                break      
    if is_solid:
        return (True, 'solid') # Found a solid rectangle

    # --- Hollow Check (only if not solid) ---
    # A hollow rectangle must have space for an interior (min 3x3 bbox)
    if width <= 2 or height <= 2:
        return (False, None) # Too small to be hollow

    is_hollow = True
    all_coords_on_border = True
    # Check every cell within the bounding box
    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            is_border_cell = (r == min_r or r == max_r or c == min_c or c == max_c)
            
            if is_border_cell:
                # Border cells must:
                # 1. Have the object's color
                # 2. Be part of the object's coordinates (found by find_objects)
                if grid[r, c] != color or (r,c) not in coords:
                    is_hollow = False
                    break
            else: # Interior cells
                # Interior cells must:
                # 1. Have the background color
                # 2. NOT be part of the object's coordinates
                if grid[r, c] != background_color or (r,c) in coords:
                    is_hollow = False
                    break
        if not is_hollow:
            break # Exit outer loop if any check failed

    # Final verification for hollow: ensure all pixels originally found for the object
    # actually lie on the calculated border of the bounding box.
    if is_hollow:
        for r_obj, c_obj in coords:
             if not (r_obj == min_r or r_obj == max_r or c_obj == min_c or c_obj == max_c):
                 all_coords_on_border = False
                 is_hollow = False # Downgrade if any object pixel is inside the border
                 break
                 
    if is_hollow and all_coords_on_border:
        return (True, 'hollow') # Found a perfect hollow rectangle

    # If neither solid nor perfectly hollow criteria were met
    return (False, None)

def get_bounding_box_area(bbox):
    """Calculates the area (width * height) of a bounding box."""
    min_r, min_c, max_r, max_c = bbox
    height = max_r - min_r + 1
    width = max_c - min_c + 1
    return height * width

def crop_grid(grid, bbox):
    """Extracts a subgrid defined by a bounding box."""
    min_r, min_c, max_r, max_c = bbox
    # Slicing using NumPy array indexing
    return grid[min_r:max_r+1, min_c:max_c+1]

def calculate_median_value(values):
    """
    Calculates the median of a list of numbers. 
    For an even number of elements, returns the lower of the two middle elements.
    """
    if not values: # Handle empty list case
        return None
    sorted_values = sorted(values)
    n = len(sorted_values)
    if n % 2 == 1:
        # Odd number of elements: return the middle one
        return sorted_values[n // 2]
    else:
        # Even number of elements: return the lower of the two middle elements (index n//2 - 1)
        return sorted_values[n // 2 - 1]

# === Main Transformation Function ===

def transform(input_grid):
    """
    Applies the transformation logic to the input grid.
    """
    # Convert input list of lists to NumPy array for efficient processing
    grid = np.array(input_grid)
    if grid.size == 0:
        return [] # Handle empty input grid

    # Assume background color is 0 (white)
    background_color = 0 

    # Step 1: Find all contiguous non-background objects
    all_objects = find_objects(grid, ignore_color=background_color)
    
    # Step 2: Filter these objects to keep only 'perfect rectangles' (solid or hollow)
    perfect_rectangles = []
    for obj in all_objects:
        is_perfect, rect_type = is_perfect_rectangle(obj, grid, background_color)
        if is_perfect:
            # Store rectangle type and calculate/store bounding box area
            obj['type'] = rect_type 
            obj['area'] = get_bounding_box_area(obj['bbox']) 
            perfect_rectangles.append(obj)
            
    # Handle case where no perfect rectangles are found in the input
    if not perfect_rectangles:
        # Return an empty grid representation as per ARC format
        return [[]] if grid.ndim > 1 else [] 

    # Step 3: Selection Logic - Stage 1: Filter by Median Area
    
    # Calculate median area using areas of all found perfect rectangles
    areas = [rect['area'] for rect in perfect_rectangles]
    median_area = calculate_median_value(areas) 
    
    # Filter the list to keep only rectangles with the median area
    median_area_rectangles = [rect for rect in perfect_rectangles if rect['area'] == median_area]
        
    selected_rectangle = None # Initialize variable to hold the final selection
    
    # Step 4: Selection Logic - Stage 2: Handle Count and Filter by Median Color
    
    # If exactly one rectangle has the median area, it's the selected one
    if len(median_area_rectangles) == 1:
         selected_rectangle = median_area_rectangles[0]
    # If multiple rectangles share the median area, apply median color filter
    elif len(median_area_rectangles) > 1:
         # Get the colors of the rectangles remaining after the area filter
         colors = [rect['color'] for rect in median_area_rectangles]
         # Calculate the median color among them
         median_color = calculate_median_value(colors)
         
         # Select the first rectangle encountered in the list that matches both median area and median color
         for rect in median_area_rectangles:
             if rect['color'] == median_color:
                 selected_rectangle = rect
                 break # Stop after finding the first match
    
    # Fallback mechanism: If the selection logic somehow fails to pick one
    # (e.g., if median_area_rectangles becomes empty unexpectedly), 
    # default to the first perfect rectangle found as a safety measure.
    # This should not happen with correct logic and typical ARC inputs.
    if selected_rectangle is None and perfect_rectangles:
         # This might indicate an edge case or logic error if reached
         # print("Warning: Selection logic did not uniquely identify a rectangle, using first perfect rectangle found.") # Optional debug print
         selected_rectangle = perfect_rectangles[0]

    # Step 5: Crop the input grid to the bounding box of the selected rectangle
    if selected_rectangle:
        output_grid_np = crop_grid(grid, selected_rectangle['bbox'])
    else:
        # This path should only be reachable if perfect_rectangles was empty initially
         return [[]] if grid.ndim > 1 else []

    # Convert the resulting NumPy array back to a list of lists for the final output format
    return output_grid_np.tolist()