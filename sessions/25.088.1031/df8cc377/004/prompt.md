
Previous Code:
```python
import numpy as np
from collections import deque, defaultdict

"""
Fill the interior of two hollow rectangles with checkerboard patterns derived 
from swapped colors of scattered pixels found outside the rectangles.

1. Identify two hollow rectangles based on their single-pixel-thick borders.
2. Identify two distinct colors of single, scattered pixels located outside 
   the rectangles.
3. Remove the scattered pixels from the grid (set to white).
4. Fill the interior of the first rectangle found with a checkerboard pattern 
   using the color of the second scattered pixel type found.
5. Fill the interior of the second rectangle found with a checkerboard pattern 
   using the color of the first scattered pixel type found.
6. The checkerboard pattern starts with the fill color at the top-left interior cell, 
   alternating with white based on relative position (row_delta + col_delta).
"""

def find_objects(grid, ignore_colors={0}):
    """
    Finds connected components (objects) of the same color in the grid using BFS.

    Args:
        grid (np.ndarray): The input grid.
        ignore_colors (set): Set of colors to ignore (typically background).

    Returns:
        list: A list of objects, where each object is a tuple:
              (color, set of (row, col) coordinates).
              The list is implicitly ordered by the top-left coordinate of each object.
    """
    rows, cols = grid.shape
    visited = set()
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited:
                color = grid[r, c]
                if color in ignore_colors:
                    visited.add((r, c))
                    continue
                
                obj_coords = set()
                q = deque([(r, c)])
                visited.add((r, c))
                obj_coords.add((r, c))
                
                while q:
                    row, col = q.popleft()
                    
                    # Check 4-directional neighbors
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           (nr, nc) not in visited and grid[nr, nc] == color:
                            visited.add((nr, nc))
                            obj_coords.add((nr, nc))
                            q.append((nr, nc))
                            
                if obj_coords:
                    objects.append((color, obj_coords))
                    
    return objects

def get_bounding_box(coords):
    """Calculates the bounding box for a set of coordinates."""
    if not coords:
        return None
    min_r = min(r for r, c in coords)
    max_r = max(r for r, c in coords)
    min_c = min(c for r, c in coords)
    max_c = max(c for r, c in coords)
    return (min_r, min_c, max_r, max_c)

def is_hollow_rectangle(grid, coords):
    """
    Checks if a set of coordinates forms a hollow rectangle with a 1-pixel border.
    Returns True, bbox, interior_coords if it is, otherwise False, None, None.
    """
    if not coords:
        return False, None, None

    bbox = get_bounding_box(coords)
    if bbox is None:
        return False, None, None
    min_r, min_c, max_r, max_c = bbox

    # Check minimal size for a hollow rectangle (at least 3x3)
    if max_r - min_r < 2 or max_c - min_c < 2:
        return False, None, None

    border_color = grid[min(coords)] # Get color from any coord
    interior_coords = set()
    expected_border_coords = set()

    for r in range(min_r, max_r + 1):
        for c in range(min_c, max_c + 1):
            is_perimeter = (r == min_r or r == max_r or c == min_c or c == max_c)
            
            if is_perimeter:
                # Perimeter pixels must match the border color and be in coords
                if grid[r, c] != border_color or (r, c) not in coords:
                    return False, None, None
                expected_border_coords.add((r,c))
            else:
                # Interior pixels must be white (0)
                if grid[r, c] != 0:
                    return False, None, None
                interior_coords.add((r, c))

    # Verify the found coordinates exactly match the expected perimeter
    if coords != expected_border_coords:
         # This can happen if a pixel *inside* the bounding box has the border color
         return False, None, None

    # Must have an interior
    if not interior_coords:
        return False, None, None # Solid rectangle

    return True, bbox, interior_coords


def find_hollow_rectangles(objects, grid):
    """Identifies hollow rectangles from a list of objects."""
    rectangles = []
    all_rect_coords = set() # Store border and interior coords

    for color, coords in objects:
        is_rect, bbox, interior_coords = is_hollow_rectangle(grid, coords)
        if is_rect:
            # Calculate top-left interior coordinate
            min_interior_r = min(r for r, c in interior_coords)
            min_interior_c = min(c for r, c in interior_coords if r == min_interior_r)
            top_left_interior = (min_interior_r, min_interior_c)

            rect_info = {
                'border_color': color,
                'border_coords': coords,
                'bbox': bbox,
                'interior_coords': interior_coords,
                'top_left_interior': top_left_interior
            }
            rectangles.append(rect_info)
            all_rect_coords.update(coords)
            all_rect_coords.update(interior_coords) # Include interior for exclusion check

    return rectangles, all_rect_coords


def find_scattered_pixels(objects, excluded_coords):
    """Identifies single pixels outside the excluded coordinates."""
    scattered_pixels_map = defaultdict(list)
    scattered_colors_ordered = []
    pixels_to_remove = set()

    for color, coords in objects:
        if len(coords) == 1:
            coord = list(coords)[0]
            if coord not in excluded_coords:
                if color not in scattered_colors_ordered:
                    scattered_colors_ordered.append(color)
                scattered_pixels_map[color].append(coord)
                pixels_to_remove.add(coord)

    return scattered_pixels_map, scattered_colors_ordered, pixels_to_remove


def fill_checkerboard(grid, interior_coords, top_left_interior, fill_color):
    """Fills the specified interior coordinates with a checkerboard pattern."""
    if not interior_coords:
        return # No interior to fill

    r_start, c_start = top_left_interior
    for r, c in interior_coords:
        # Calculate checkerboard index relative to the top-left interior cell
        checker_index = (r - r_start) + (c - c_start)
        
        if checker_index % 2 == 0:
            # Even index gets the fill color
            grid[r, c] = fill_color
        else:
            # Odd index gets the background color (white)
            grid[r, c] = 0


def transform(input_grid):
    """
    Transforms the input grid by finding two hollow rectangles, identifying two
    types of scattered pixels outside them, removing the scattered pixels, and
    filling the rectangles' interiors with checkerboard patterns using the
    swapped scattered pixel colors.
    """
    output_grid = np.copy(input_grid)
    
    # 1. Find all colored objects (implicitly ordered by scan)
    objects = find_objects(output_grid, ignore_colors={0})

    # 2. Identify the two hollow rectangles and their properties
    # The order in `rectangles` list depends on the order from `find_objects`
    rectangles, rect_covered_coords = find_hollow_rectangles(objects, output_grid)

    # Check if exactly two rectangles were found
    if len(rectangles) != 2:
        # print(f"Error: Found {len(rectangles)} rectangles, expected 2.")
        return input_grid # Return original grid if condition not met

    # 3. Identify scattered pixels and their colors (outside rectangle areas)
    # The order in `scattered_colors_ordered` depends on scan order of first pixel of each color
    scattered_map, scattered_colors_ordered, pixels_to_remove = find_scattered_pixels(
        objects, rect_covered_coords
    )

    # Check if exactly two scattered colors were found
    if len(scattered_colors_ordered) != 2:
        # print(f"Error: Found {len(scattered_colors_ordered)} scattered colors, expected 2.")
        return input_grid # Return original grid if condition not met

    # 4. Remove scattered pixels from the output grid
    for r, c in pixels_to_remove:
        if 0 <= r < output_grid.shape[0] and 0 <= c < output_grid.shape[1]:
             output_grid[r, c] = 0 # Set to white

    # 5. Assign fill colors (swap the scattered colors based on order found)
    # Fill first rectangle found with second scattered color found
    fill_color_rect1 = scattered_colors_ordered[1]
    # Fill second rectangle found with first scattered color found
    fill_color_rect2 = scattered_colors_ordered[0]

    # 6. Fill interiors with checkerboard pattern
    # Fill the first rectangle identified
    fill_checkerboard(
        output_grid, 
        rectangles[0]['interior_coords'], 
        rectangles[0]['top_left_interior'], 
        fill_color_rect1
    )
    # Fill the second rectangle identified
    fill_checkerboard(
        output_grid, 
        rectangles[1]['interior_coords'], 
        rectangles[1]['top_left_interior'], 
        fill_color_rect2
    )

    return output_grid
```
Results for code_00.py:

Train Set Results:

## Example 1:
Input:
```
0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0
0 8 0 0 0 0 0 8 0 0 0 0 0 0 0 0 6 0 0 0 6 0 0
0 8 0 0 0 0 0 8 0 0 0 3 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 6 0 0 0 0 4 4 4 4 4 4 4 0 0
0 0 0 6 0 0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 3 0 0 0 0 0 0 4 0 0 0 0 0 4 0 0
0 6 0 0 0 0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 4 0 0
0 0 0 0 0 6 0 0 0 0 0 0 0 0 4 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 3 0 0 0 4 0 0 0 0 0 4 0 0
0 6 0 0 0 0 0 0 0 0 0 0 0 0 4 0 0 0 0 0 4 0 0
0 0 0 0 0 3 0 0 0 0 6 0 0 0 4 4 4 4 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 6 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 3 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0 6 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 6 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 3 0 3 0 3 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 3 0 3 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 6 0 6 0 6 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 0 6 0 6 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 6 0 6 0 6 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 0 6 0 6 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 6 0 6 0 6 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 0 6 0 6 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 3 0 3 0 3 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 0 3 0 3 0 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 8 8 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 6 0 6 0 6 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 0 6 0 6 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 6 0 6 0 6 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 0 6 0 6 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 6 0 6 0 6 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 0 6 0 6 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 4 4 4 4 4 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0

## Example 2:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 8 0
0 0 2 2 2 2 2 0 0 0 8 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 0 0 2 0 0 0 0 0 0 0 0 0 0 4 0 0
0 0 2 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0 0 4 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 4 0 0 0 0 0 0 0 0 0 0 0 0 8 0 0 0 0 0
0 0 0 0 0 0 4 0 0 0 0 0 0 0 0 0 0 0 0 4
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 3 0 0
0 0 0 0 0 0 0 0 0 3 0 0 0 0 0 0 0 3 0 0
0 0 0 0 8 0 0 0 0 3 3 3 3 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 4 0 0 0 0 0 0 0 0 8 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 8 0 8 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 8 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 8 0 8 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 3 4 0 4 0 4 0 4 3 0 0
0 0 0 0 0 0 0 0 0 3 0 4 0 4 0 4 0 3 0 0
0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 4 0 4 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 0 4 0 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 4 0 4 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 2 2 2 2 2 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 3 8 0 8 0 8 0 8 3 0 0
0 0 0 0 0 0 0 0 0 3 0 8 0 8 0 8 0 3 0 0
0 0 0 0 0 0 0 0 0 3 3 3 3 3 3 3 3 3 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: False
Pixels Off: 12
Size Correct: True
Color Palette Correct: True
Color Count Correct: False
Score: 6.0

## Example 3:
Input:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 2 0 0 0 0 0 0 0 0 0 0 0 0
0 1 0 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 4 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 0 0 0 0 2 0 0 0 0 0 0 0
0 0 0 8 0 0 0 8 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Expected Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 4 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 2 0 2 8 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Transformed Output:
```
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 4 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 1 1 1 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 2 0 2 8 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 8 8 8 8 8 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0 0
```
Match: True
Pixels Off: 0
Size Correct: True
Color Palette Correct: True
Color Count Correct: True
Score: 0
