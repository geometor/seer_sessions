import numpy as np
from collections import deque

"""
Identify all contiguous blocks of gray pixels (color 5). 
Identify all non-white source pixels in the first row (row 0).
For each gray block, find the source pixel in the first row that is horizontally closest to it. 
The horizontal distance is the minimum absolute difference in column indices between any pixel in the block and the source pixel.
Replace the color of all pixels in the gray block with the color of its closest source pixel. 
All other pixels remain unchanged.
"""

def find_objects(grid, color):
    """
    Finds all contiguous objects of a specific color in the grid.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list: A list of sets, where each set contains the (row, col) coordinates 
              of the pixels belonging to one object.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and not visited[r, c]:
                obj = set()
                q = deque([(r, c)])
                visited[r, c] = True
                while q:
                    row, col = q.popleft()
                    obj.add((row, col))
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                if obj:
                    objects.append(obj)
    return objects

def get_block_columns(block):
    """
    Finds the minimum and maximum column indices covered by a block.

    Args:
        block (set): A set of (row, col) coordinates representing the block.

    Returns:
        tuple: (min_col, max_col)
    """
    if not block:
        return None, None
    cols = [c for r, c in block]
    return min(cols), max(cols)

def calculate_horizontal_distance(block_min_col, block_max_col, source_col):
    """
    Calculates the minimum horizontal distance between a block's column range 
    and a source pixel's column.

    Args:
        block_min_col (int): The minimum column index of the block.
        block_max_col (int): The maximum column index of the block.
        source_col (int): The column index of the source pixel.

    Returns:
        int: The minimum horizontal distance.
    """
    if block_min_col <= source_col <= block_max_col:
        return 0
    elif source_col < block_min_col:
        return block_min_col - source_col
    else: # source_col > block_max_col
        return source_col - block_max_col

def transform(input_grid):
    """
    Transforms the input grid by recoloring gray blocks based on the horizontally 
    closest source color in the top row.
    
    Args:
        input_grid (list or np.array): The input grid.
        
    Returns:
        np.array: The transformed output grid.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    rows, cols = grid.shape

    # 1. Identify source pixels in the first row
    source_pixels = []
    if rows > 0:
        for c in range(cols):
            color = grid[0, c]
            if color != 0: # Assuming 0 is white/background
                source_pixels.append({'color': color, 'col': c})

    # If no source pixels, return the original grid (or handle as needed)
    if not source_pixels:
        return output_grid

    # 2. Identify all gray (color 5) blocks
    gray_blocks = find_objects(grid, 5)

    # 3. For each gray block, find the closest source and recolor
    for block in gray_blocks:
        if not block:
            continue

        # 3a. Determine the column range of the block
        min_col, max_col = get_block_columns(block)
        
        min_dist = float('inf')
        closest_color = -1 # Default or error color if needed

        # 3b-c. Find the closest source pixel
        for source in source_pixels:
            dist = calculate_horizontal_distance(min_col, max_col, source['col'])
            
            # Update if this source is closer
            if dist < min_dist:
                min_dist = dist
                closest_color = source['color']
            # Tie-breaking: If distances are equal, the original description doesn't specify.
            # Common ARC tie-breakers are first-encountered (leftmost source).
            # Let's stick with the first one found at the minimum distance.
            # If a different tie-breaker is needed, logic would go here.

        # 3d-5. Recolor the block in the output grid
        if closest_color != -1: # Check if a closest color was found
            for r, c in block:
                output_grid[r, c] = closest_color

    # 6. Return the modified output grid
    return output_grid.tolist() # Return as list of lists if required by context