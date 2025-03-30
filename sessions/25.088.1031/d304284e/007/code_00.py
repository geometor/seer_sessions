import numpy as np
from typing import List, Tuple, Set, Dict

"""
Transforms the input grid by tiling the single non-background object
across the output grid. The process involves identifying the object, determining its properties (color, shape, location), and then repeatedly drawing its shape onto an initially white output grid. Tiles are separated by a 1-pixel white border. The color of each drawn tile depends on its position in the tiling grid (tile row index 'j', tile column index 'i'): magenta (6) if (i+1) is a multiple of 3, the object's original color if j=0 and (i+1) is not a multiple of 3, and white (0) otherwise (j>0 and (i+1) not a multiple of 3). Tiling continues until the starting position of a tile would be outside the grid boundaries, and individual pixels are only drawn if they fall within the grid boundaries (clipping).
"""

# === Helper Functions ===

def find_objects(grid: np.ndarray, ignore_color: int = 0) -> List[Dict]:
    """
    Finds connected components (objects) of the same color in a grid.
    Uses 4-way connectivity (von Neumann neighborhood).

    Args:
        grid: The input grid as a NumPy array.
        ignore_color: The color to ignore (typically the background).

    Returns:
        A list of dictionaries, where each dictionary represents an object
        and contains 'color' and 'coords' (a set of (row, col) tuples).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            if color != ignore_color and not visited[r, c]:
                obj_coords = set()
                q = [(r, c)]
                visited[r, c] = True
                
                while q:
                    row, col = q.pop(0)
                    obj_coords.add((row, col))
                    
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           not visited[nr, nc] and grid[nr, nc] == color:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
                if obj_coords:
                     objects.append({'color': color, 'coords': obj_coords})
    return objects

def get_bounding_box(coords: Set[Tuple[int, int]]) -> Tuple[int, int, int, int]:
    """
    Calculates the bounding box of a set of coordinates.

    Args:
        coords: A set of (row, col) tuples.

    Returns:
        A tuple (min_row, min_col, max_row, max_col). Returns (-1,-1,-1,-1) if coords is empty.
    """
    if not coords:
        return -1, -1, -1, -1
    min_row = min(r for r, c in coords)
    min_col = min(c for r, c in coords)
    max_row = max(r for r, c in coords)
    max_col = max(c for r, c in coords)
    return min_row, min_col, max_row, max_col

def get_relative_shape(coords: Set[Tuple[int, int]], min_row: int, min_col: int) -> Set[Tuple[int, int]]:
    """
    Gets the shape of an object relative to its top-left corner.

    Args:
        coords: The absolute coordinates of the object's pixels.
        min_row: The minimum row index of the object.
        min_col: The minimum column index of the object.

    Returns:
        A set of relative (dr, dc) coordinates.
    """
    return set((r - min_row, c - min_col) for r, c in coords)

# === Main Transformation Function ===

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the tiling and coloring transformation.
    """
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    background_color = 0
    magenta_color = 6

    # 1. Identify the single contiguous non-white object
    objects = find_objects(input_np, ignore_color=background_color)
    if not objects:
        # Return original if no object found (should not happen based on examples)
        return input_grid 
    # Assuming only one object based on the problem description and examples
    target_object = objects[0]
    original_color = target_object['color']
    object_coords = target_object['coords']

    # 2. Determine its properties: bounding box, shape, size
    min_r, min_c, max_r, max_c = get_bounding_box(object_coords)
    if min_r == -1: # Should not happen if an object was found
         return input_grid
        
    obj_height = max_r - min_r + 1
    obj_width = max_c - min_c + 1
    relative_shape = get_relative_shape(object_coords, min_r, min_c)

    # 3. Initialize the output grid with the background color
    output_np = np.full_like(input_np, background_color)

    # 4. Iterate through potential tile placements (row-major)
    j = 0 # Tile row index (0-based)
    while True:
        # Calculate the starting row for the current row of tiles (includes 1px border)
        current_start_r = min_r + j * (obj_height + 1) 
        
        # Check if the current tile row would START outside the grid vertically
        if current_start_r >= rows:
            break # Finished tiling vertically

        i = 0 # Tile column index (0-based)
        while True:
            # Calculate the starting column for the current tile (includes 1px border)
            current_start_c = min_c + i * (obj_width + 1) 

            # Check if the current tile would START outside the grid horizontally
            if current_start_c >= cols:
                break # Move to the next row (j++)
                
            # Determine the tile color based on row index 'j' and column index 'i'
            # Rule: Magenta if (i+1) is multiple of 3.
            # Otherwise: original color if j==0, background color if j>0.
            if (i + 1) % 3 == 0:
                tile_color = magenta_color
            else:
                if j == 0: # First row of tiles
                    tile_color = original_color
                else: # Subsequent rows of tiles (j > 0)
                    tile_color = background_color # Use white/background
            
            # Only draw non-background tiles
            if tile_color != background_color:
                # Place the object's shape onto the output grid, clipping at boundaries
                for dr, dc in relative_shape:
                    target_r = current_start_r + dr
                    target_c = current_start_c + dc
                    
                    # Check if the individual pixel is within grid bounds
                    if 0 <= target_r < rows and 0 <= target_c < cols:
                        output_np[target_r, target_c] = tile_color

            i += 1 # Move to the next potential tile column
        
        j += 1 # Move to the next potential tile row

    # 5. Return the completed output grid as a list of lists
    return output_np.tolist()