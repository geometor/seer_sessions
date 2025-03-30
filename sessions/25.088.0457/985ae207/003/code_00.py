import numpy as np
from collections import deque

"""
Transforms the input grid by finding specific 3x3 patterns and using them to tile adjacent contiguous areas.

1.  **Analyze Input:** Determine the background color (C_bg) by finding the most frequent color in the input grid.
2.  **Find Patterns:** Scan the input grid to identify all 3x3 subgrids that have a perfectly uniform border of color C_frame and a single center pixel of color C_center. Crucially, the frame color C_frame must *not* be the background color (C_bg). Store each valid pattern's 3x3 grid, its C_frame, its C_center, and its top-left location (r_pat, c_pat).
3.  **Find Areas:** Identify all contiguous areas of single colors in the input grid using 4-connectivity. For each area, record its color (C_area), the set of pixel coordinates it occupies, its bounding box (min/max row and column), and whether its color is the background color (C_area == C_bg).
4.  **Identify Targets & Apply Tiling:** Create a copy of the input grid to serve as the output grid. Keep track of pixels that have already been modified. Iterate through each identified pattern P. For pattern P, iterate through all identified contiguous areas A. Check if area A is adjacent (sharing an edge or corner) to the 3x3 bounding box of pattern P. If area A is adjacent, check if its color C_area meets the condition: `C_area == C_center` (matches pattern's center) OR `C_area == C_bg` (is a background area). If both adjacency and color conditions are met, use pattern P's 3x3 grid to fill the pixels belonging to area A in the output grid. The filling uses modulo arithmetic based on the area's top-left corner, ensuring the pattern tiles correctly. Only modify pixels that haven't been modified already by another pattern in this process.
5.  **Finalize:** Return the modified output grid. Pixels not part of any target area remain unchanged from the input grid.
"""

def find_background_color(grid):
    """Finds the most frequent color in the grid."""
    colors, counts = np.unique(grid, return_counts=True)
    return colors[np.argmax(counts)]

def find_patterns(grid, background_color):
    """
    Finds 3x3 patterns with a uniform border color different from the background
    and a single center color.
    """
    patterns_info = []
    height, width = grid.shape
    for r in range(height - 2):
        for c in range(width - 2):
            subgrid = grid[r:r+3, c:c+3]
            
            # Check for uniform border
            frame_color = subgrid[0, 0]
            is_uniform_border = True
            for i in range(3): # Top row
                if subgrid[0, i] != frame_color: is_uniform_border = False; break
            if not is_uniform_border: continue
            for i in range(3): # Bottom row
                if subgrid[2, i] != frame_color: is_uniform_border = False; break
            if not is_uniform_border: continue
            # Check middle row sides (center checked separately)
            if subgrid[1, 0] != frame_color or subgrid[1, 2] != frame_color:
                is_uniform_border = False
            
            if is_uniform_border:
                # Check if frame color is not the background color
                if frame_color != background_color:
                    center_color = subgrid[1, 1]
                    patterns_info.append({
                        'grid': subgrid.copy(),
                        'frame_color': frame_color,
                        'center_color': center_color,
                        'row': r,
                        'col': c
                    })
    return patterns_info

def find_contiguous_areas(grid):
    """
    Finds all contiguous areas of the same color using BFS (4-connectivity).
    Returns a list of dictionaries, each describing an area.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    areas = []
    
    for r in range(height):
        for c in range(width):
            if not visited[r, c]:
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

def is_adjacent(pattern_info, area_info):
    """
    Checks if any pixel in the area is adjacent (8-connectivity) to any 
    pixel in the pattern's 3x3 bounding box.
    """
    pattern_r, pattern_c = pattern_info['row'], pattern_info['col']
    area_coords = area_info['coords']

    # Iterate through all cells within the pattern's 3x3 box
    for r_offset in range(3):
        for c_offset in range(3):
            pr = pattern_r + r_offset
            pc = pattern_c + c_offset
            
            # Check the 8 neighbors of this pattern cell
            for dr in [-1, 0, 1]:
                for dc in [-1, 0, 1]:
                    if dr == 0 and dc == 0:
                        continue # Skip the cell itself
                        
                    nr, nc = pr + dr, pc + dc
                    
                    # If a neighbor's coordinate is in the area's set, they are adjacent
                    if (nr, nc) in area_coords:
                        return True
                        
    return False # No adjacent cell found

def transform(input_grid):
    """
    Applies the pattern tiling transformation based on adjacency and color rules.
    """
    # 1. Analyze Input: Find background color
    background_color = find_background_color(input_grid)
    
    # 2. Find Patterns: Identify relevant 3x3 patterns
    patterns = find_patterns(input_grid, background_color)
    
    # If no relevant patterns are found, return the original grid
    if not patterns:
        return np.copy(input_grid)

    # 3. Find Areas: Identify all contiguous areas
    areas = find_contiguous_areas(input_grid)

    # Initialize output grid and track modified pixels
    output_grid = np.copy(input_grid)
    modified_pixels = set()

    # 4. Identify Targets & Apply Tiling
    for pattern in patterns:
        pattern_grid = pattern['grid']
        pattern_center_color = pattern['center_color']
        
        for area in areas:
            area_color = area['color']
            area_coords = area['coords']
            
            # Check for adjacency
            if is_adjacent(pattern, area):
                # Check color condition: area matches pattern center OR is background
                if area_color == pattern_center_color or area_color == background_color:
                    # This is a target area for this pattern
                    min_row, min_col = area['min_row'], area['min_col']
                    
                    # Tile the pattern onto the target area
                    for r, c in area_coords:
                        # Apply modification only if pixel hasn't been modified yet
                        if (r, c) not in modified_pixels:
                            # Calculate pattern indices using modulo relative to area's top-left
                            pattern_r_idx = (r - min_row) % 3
                            pattern_c_idx = (c - min_col) % 3
                            
                            # Update the output grid
                            output_grid[r, c] = pattern_grid[pattern_r_idx, pattern_c_idx]
                            modified_pixels.add((r, c)) # Mark pixel as modified

    # 5. Finalize
    return output_grid