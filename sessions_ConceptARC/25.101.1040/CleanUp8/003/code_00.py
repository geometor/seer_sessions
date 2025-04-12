import collections
from typing import List, Tuple, Set

"""
Transforms an input grid based on two criteria related to 2x2 squares:
1. Identifies contiguous objects of the same non-white color. If an object's bounding box is exactly 2x2, the corresponding 2x2 area in the output grid is filled with the object's color.
2. Scans the input grid for any 2x2 area composed entirely of the same non-white color. If found, the corresponding 2x2 area in the output grid is filled with that color.
The final output grid contains all such identified 2x2 squares, filled with their respective colors, on a white background. Duplicates identified by both criteria are handled implicitly by drawing onto the same output location.
"""

def find_objects(grid: list[list[int]]) -> list[tuple[int, set[tuple[int, int]]]]:
    """
    Identifies all distinct contiguous objects of non-white pixels in the grid
    using 4-way adjacency.

    Args:
        grid: The input 2D list representing the grid.

    Returns:
        A list of tuples, where each tuple contains:
        - The color (int) of the object.
        - A set of (row, col) tuples representing the pixels of the object.
    """
    if not grid or not grid[0]:
        return []
    
    height = len(grid)
    width = len(grid[0])
    visited = set()
    objects = []

    for r in range(height):
        for c in range(width):
            if grid[r][c] != 0 and (r, c) not in visited:
                color = grid[r][c]
                obj_pixels = set()
                q = collections.deque([(r, c)])
                visited.add((r, c))
                
                while q:
                    row, col = q.popleft()
                    obj_pixels.add((row, col))
                    
                    # Check neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        # Check bounds and if the neighbor is the same color and not visited
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid[nr][nc] == color and (nr, nc) not in visited:
                            visited.add((nr, nc))
                            q.append((nr, nc))
                            
                if obj_pixels:
                    objects.append((color, obj_pixels))
                    
    return objects

def calculate_bounding_box(pixels: set[tuple[int, int]]) -> tuple[int, int, int, int]:
    """
    Calculates the bounding box (top-left corner, height, width) of a set of pixels.

    Args:
        pixels: A set of (row, col) tuples.

    Returns:
        A tuple containing (min_row, min_col, height, width).
        Returns (0, 0, 0, 0) if pixels is empty.
    """
    if not pixels:
        return 0, 0, 0, 0
        
    min_row = min(r for r, c in pixels)
    max_row = max(r for r, c in pixels)
    min_col = min(c for r, c in pixels)
    max_col = max(c for r, c in pixels)
    
    height = max_row - min_row + 1
    width = max_col - min_col + 1
    
    return min_row, min_col, height, width

def find_solid_2x2_squares(grid: list[list[int]]) -> Set[Tuple[int, Tuple[int, int]]]:
    """
    Finds all 2x2 squares in the grid that are solidly filled with the same
    non-white color.

    Args:
        grid: The input 2D list representing the grid.

    Returns:
        A set of tuples, where each tuple contains:
        - The color (int) of the solid square.
        - A tuple (row, col) representing the top-left corner of the square.
    """
    solid_squares = set()
    if not grid or not grid[0]:
        return solid_squares

    height = len(grid)
    width = len(grid[0])

    # Iterate through possible top-left corners (r, c) for a 2x2 square
    for r in range(height - 1):
        for c in range(width - 1):
            # Get the color of the top-left pixel
            color = grid[r][c]
            
            # Check if it's a non-white color and if all four pixels match
            if color != 0 and \
               grid[r+1][c] == color and \
               grid[r][c+1] == color and \
               grid[r+1][c+1] == color:
                solid_squares.add((color, (r, c)))
                
    return solid_squares


def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    if not input_grid or not input_grid[0]:
        return []

    height = len(input_grid)
    width = len(input_grid[0])
    
    # initialize output_grid with background color (white, 0)
    output_grid = [[0 for _ in range(width)] for _ in range(height)]
    
    # Use a set to store the (color, top_left_coords) of squares to draw, avoiding duplicates
    squares_to_draw: Set[Tuple[int, Tuple[int, int]]] = set()

    # --- Step 1: Identify squares based on object bounding boxes ---
    # Find all contiguous non-white objects
    objects = find_objects(input_grid)
    
    # Iterate through each object
    for color, pixels in objects:
        # Calculate its bounding box
        min_row, min_col, bb_height, bb_width = calculate_bounding_box(pixels)
        
        # Check if the bounding box is exactly 2x2
        if bb_height == 2 and bb_width == 2:
            # Add its color and top-left corner to the set
            squares_to_draw.add((color, (min_row, min_col)))

    # --- Step 2: Identify squares based on solid 2x2 patterns ---
    # Find all solid 2x2 non-white squares directly in the grid
    solid_squares = find_solid_2x2_squares(input_grid)
    
    # Add these squares to the set (duplicates are handled automatically by the set)
    squares_to_draw.update(solid_squares)

    # --- Step 3: Generate the output grid ---
    # Iterate through the unique squares identified
    for color, (r, c) in squares_to_draw:
        # Fill the 2x2 area in the output grid
        # Ensure drawing stays within bounds (should generally be safe given how squares are found)
        if r + 1 < height and c + 1 < width:
             output_grid[r][c] = color
             output_grid[r+1][c] = color
             output_grid[r][c+1] = color
             output_grid[r+1][c+1] = color
             
    return output_grid