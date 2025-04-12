import numpy as np
from collections import deque

"""
Identifies all contiguous non-white objects in the input grid. Filters these 
objects to find those whose pixels exactly form the perimeter of their square 
bounding box. Selects the square perimeter object with the largest bounding box 
size (side length). Creates a new output grid of the same size as the selected 
object's bounding box. The output grid contains a hollow square frame: the 
perimeter is filled with the color of the selected object, and the interior 
is filled with white (0).
"""

def find_objects(grid: np.ndarray) -> list[dict]:
    """
    Finds all contiguous objects of the same color in the grid.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A list of dictionaries, where each dictionary represents an object
        and contains its color, set of pixel coordinates, and bounding box.
    """
    rows, cols = grid.shape
    visited = set()
    objects = []
    
    for r in range(rows):
        for c in range(cols):
            if (r, c) not in visited and grid[r, c] != 0: # Non-white and not visited
                color = grid[r, c]
                obj_pixels = set()
                q = deque([(r, c)])
                visited.add((r, c))
                min_r, max_r = r, r
                min_c, max_c = c, c

                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)

                    # Explore neighbors (4-directional)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           (nr, nc) not in visited and grid[nr, nc] == color:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                            
                objects.append({
                    'color': color,
                    'pixels': obj_pixels,
                    'bbox': (min_r, min_c, max_r, max_c)
                })
    return objects

def is_square_perimeter(obj: dict) -> tuple[bool, int]:
    """
    Checks if an object's pixels form the exact perimeter of its square bounding box.

    Args:
        obj: A dictionary representing an object with 'color', 'pixels', and 'bbox'.

    Returns:
        A tuple: (True, side_length) if it's a square perimeter, 
                 (False, 0) otherwise.
    """
    min_r, min_c, max_r, max_c = obj['bbox']
    height = max_r - min_r + 1
    width = max_c - min_c + 1

    # Check if the bounding box is a square
    if width != height:
        return False, 0
        
    side_length = width # or height
    
    # Check if it's just a single point (1x1 square) - technically a perimeter, but trivial
    if side_length == 1:
        return len(obj['pixels']) == 1, 1

    # Calculate expected perimeter pixels
    expected_perimeter_pixels = set()
    # Top and bottom rows
    for c in range(min_c, max_c + 1):
        expected_perimeter_pixels.add((min_r, c))
        expected_perimeter_pixels.add((max_r, c))
    # Left and right columns (excluding corners already added)
    for r in range(min_r + 1, max_r):
        expected_perimeter_pixels.add((r, min_c))
        expected_perimeter_pixels.add((r, max_c))

    # Check if the object's pixels exactly match the calculated perimeter pixels
    if obj['pixels'] == expected_perimeter_pixels:
        return True, side_length
    else:
        return False, 0


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by finding the largest square perimeter object and 
    outputting it as a hollow square frame.
    """
    
    # Convert input list of lists to numpy array for easier processing
    grid_np = np.array(input_grid, dtype=int)
    
    # 1. Scan the input grid to identify all distinct contiguous blocks of non-white pixels.
    objects = find_objects(grid_np)
    
    # 2. & 3. Filter objects to find those that are square perimeters.
    square_perimeters = []
    for obj in objects:
        is_sq_perimeter, side_length = is_square_perimeter(obj)
        if is_sq_perimeter:
            obj['side_length'] = side_length
            square_perimeters.append(obj)

    # Handle cases where no square perimeter is found
    if not square_perimeters:
        # Based on examples, we expect at least one. 
        # Returning an empty grid or handling as an error might be appropriate.
        # Let's return an empty grid for now if this unexpected case occurs.
        return [] 

    # 4. Identify the square perimeter object with the maximum side length.
    largest_perimeter_obj = max(square_perimeters, key=lambda obj: obj['side_length'])

    # 5. Get the properties of the largest perimeter object.
    color = largest_perimeter_obj['color']
    side = largest_perimeter_obj['side_length']
    
    # 6. Create a new output grid of the determined size, initialized to white (0).
    output_grid_np = np.zeros((side, side), dtype=int)

    # 7. Fill the perimeter cells of the output grid with the object's color.
    if side > 0:
        output_grid_np[0, :] = color    # Top row
        output_grid_np[-1, :] = color   # Bottom row
        output_grid_np[:, 0] = color    # Left column
        output_grid_np[:, -1] = color   # Right column
        
    # 8. Interior is already filled with white (0) due to np.zeros initialization.

    # 9. Convert numpy array back to list of lists for the final output.
    output_grid = output_grid_np.tolist()

    return output_grid