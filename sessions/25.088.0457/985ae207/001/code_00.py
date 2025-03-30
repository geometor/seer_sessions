import numpy as np
from collections import deque

"""
Transforms the input grid based on identified 3x3 patterns and target areas.

The transformation involves:
1. Identifying all distinct 3x3 patterns in the input grid. A pattern typically 
   consists of a border (frame) of one color and a central pixel of another 
   (potentially the same) color.
2. Storing these patterns, indexed by their frame color.
3. Identifying all contiguous areas in the input grid filled with a single color.
4. For each contiguous area whose color matches the frame color of a stored 
   pattern:
    a. Designate this area as a target area.
    b. Determine the bounding box of the target area.
    c. Fill the target area in the output grid by tiling the corresponding 
       3x3 pattern, starting from the top-left corner of the area's 
       bounding box. Only pixels belonging to the original contiguous area 
       are overwritten.
5. Pixels not part of any modified target area retain their original color from 
   the input grid.
"""

def find_patterns(grid):
    """
    Scans the grid to find all 3x3 subgrids that represent patterns.
    A pattern is defined by a uniform border color and a center color.
    Returns a dictionary mapping frame_color to the 3x3 pattern grid.
    """
    patterns = {}
    height, width = grid.shape
    for r in range(height - 2):
        for c in range(width - 2):
            subgrid = grid[r:r+3, c:c+3]
            # Check if it fits the simple frame + center definition
            # More robust check: ensure all 8 border pixels are the same.
            frame_color = subgrid[0, 0]
            is_pattern = True
            # Check top/bottom row
            for i in range(3):
                if subgrid[0, i] != frame_color or subgrid[2, i] != frame_color:
                    is_pattern = False
                    break
            if not is_pattern: continue
            # Check middle row sides
            if subgrid[1, 0] != frame_color or subgrid[1, 2] != frame_color:
                is_pattern = False
            
            if is_pattern:
                # Store the pattern grid, keyed by its frame color.
                # If multiple patterns have the same frame color, the last one
                # found in the scan will be used (consistent with examples).
                patterns[frame_color] = subgrid.copy()
                
    return patterns

def find_contiguous_areas(grid):
    """
    Finds all contiguous areas of the same color using BFS.
    Ignores the most frequent color (assumed background).
    Returns a list of dictionaries, each describing an area:
    {'color': int, 'coords': set((r, c)), 'min_row': int, 'max_row': int, 'min_col': int, 'max_col': int}
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    areas = []
    
    # Determine background color (most frequent color) to ignore it
    colors, counts = np.unique(grid, return_counts=True)
    background_color = colors[np.argmax(counts)]

    for r in range(height):
        for c in range(width):
            if not visited[r, c] and grid[r, c] != background_color:
                color = grid[r, c]
                coords = set()
                queue = deque([(r, c)])
                min_r, max_r = r, r
                min_c, max_c = c, c
                
                while queue:
                    row, col = queue.popleft()
                    
                    if not (0 <= row < height and 0 <= col < width) or \
                       visited[row, col] or \
                       grid[row, col] != color:
                        continue
                        
                    visited[row, col] = True
                    coords.add((row, col))
                    min_r = min(min_r, row)
                    max_r = max(max_r, row)
                    min_c = min(min_c, col)
                    max_c = max(max_c, col)
                    
                    # Add neighbors (4-connectivity)
                    queue.append((row + 1, col))
                    queue.append((row - 1, col))
                    queue.append((row, col + 1))
                    queue.append((row, col - 1))

                if coords:
                    areas.append({
                        'color': color,
                        'coords': coords,
                        'min_row': min_r,
                        'max_row': max_r,
                        'min_col': min_c,
                        'max_col': max_c
                    })
    return areas


def transform(input_grid):
    """
    Applies the pattern tiling transformation to the input grid.
    """
    # Initialize output_grid as a copy of the input
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # 1. Find all 3x3 patterns
    patterns_by_frame_color = find_patterns(input_grid)
    
    # If no patterns are found, return the original grid
    if not patterns_by_frame_color:
        return output_grid

    # 2. Find all contiguous areas of non-background colors
    contiguous_areas = find_contiguous_areas(input_grid)

    # 3. Iterate through areas and apply patterns if color matches a frame_color
    for area in contiguous_areas:
        area_color = area['color']
        
        # Check if this area's color corresponds to a pattern's frame color
        if area_color in patterns_by_frame_color:
            # Get the corresponding 3x3 pattern
            pattern_grid = patterns_by_frame_color[area_color]
            
            # Get area details
            area_coords = area['coords']
            min_row, max_row = area['min_row'], area['max_row']
            min_col, max_col = area['min_col'], area['max_col']

            # 4. Tile the pattern onto the target area in the output grid
            # Iterate through the bounding box of the area
            for r in range(min_row, max_row + 1):
                for c in range(min_col, max_col + 1):
                    # Only modify pixels that were part of the original contiguous area
                    if (r, c) in area_coords:
                        # Calculate relative coordinates within the bounding box
                        rel_r = r - min_row
                        rel_c = c - min_col
                        
                        # Calculate corresponding indices in the 3x3 pattern grid using modulo
                        pattern_r = rel_r % 3
                        pattern_c = rel_c % 3
                        
                        # Update the output grid with the pattern pixel color
                        output_grid[r, c] = pattern_grid[pattern_r, pattern_c]

    return output_grid
