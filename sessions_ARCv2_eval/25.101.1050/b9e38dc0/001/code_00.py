import collections
import numpy as np
from collections import Counter

"""
Identifies the background color, fill color, and boundary colors based on frequency and adjacency.
Performs a fill operation starting from pixels with the fill color.
The fill type is determined by the background color:
- If the background color is 0 (white), a leftward directional fill is performed.
- Otherwise, a 4-directional flood fill is performed.
The fill replaces background-colored pixels with the fill color, stopping at boundary colors or grid edges.

Color Identification Heuristic:
1. Background Color: The most frequent color in the input grid.
2. Interface Colors: Colors adjacent (4-way) to any background pixel.
3. Fill Color: The interface color with the minimum frequency (count) in the input grid.
4. Boundary Colors: All colors present in the input grid except for the background and fill colors.
"""

def get_neighbors(r, c, height, width):
    """Generates valid 4-way neighbors for a given cell."""
    neighbors = []
    if r > 0: neighbors.append((r - 1, c))
    if r < height - 1: neighbors.append((r + 1, c))
    if c > 0: neighbors.append((r, c - 1))
    if c < width - 1: neighbors.append((r, c + 1))
    return neighbors

def flood_fill(grid, start_coords, fill_color, background_color, boundary_colors):
    """Performs a 4-directional flood fill."""
    height = len(grid)
    width = len(grid[0])
    q = collections.deque(start_coords)
    
    # Mark initial seeds as filled if they are on background color 
    # (though typically seeds are already fill_color)
    # Add seeds to queue regardless to start the process.
    processed_seeds = set()
    
    while q:
        r, c = q.popleft()
        
        # Process neighbors
        for nr, nc in get_neighbors(r, c, height, width):
            if grid[nr][nc] == background_color:
                grid[nr][nc] = fill_color
                q.append((nr, nc))
                
    return grid


def left_fill(grid, start_coords, fill_color, background_color, boundary_colors):
    """Performs a directional fill propagating only leftwards."""
    height = len(grid)
    width = len(grid[0])
    
    changed = True
    while changed:
        changed = False
        # Iterate from right to left, top to bottom might be more intuitive for left fill propagation
        for r in range(height):
            for c in range(width): 
                # If a pixel to the right has the fill color, and this pixel is background
                if grid[r][c] == background_color:
                    if c < width - 1 and grid[r][c+1] == fill_color:
                         grid[r][c] = fill_color
                         changed = True
                    # Also consider the case where the initial seed triggers the fill
                    # This check ensures pixels left of initial seeds are filled
                    # Redundant if initial seeds are correctly handled? Let's test.
                    # Simplified: propagate from existing fill_color pixels leftwards.
                    
    # Second pass to ensure propagation from original seeds works correctly
    # The previous loop might only work if a fill_color pixel exists to the right.
    # Need to propagate from initial seeds too.
    
    # Reset and use a different approach: Scan repeatedly leftwards from any fill_color pixel.
    
    # Create a working copy to avoid issues with loop order
    new_grid = [row[:] for row in grid] 
    
    changed = True
    while changed:
        changed = False
        current_grid = [row[:] for row in new_grid] # snapshot before pass
        for r in range(height):
            for c in range(1, width): # Start from second column
                # If the pixel to the right is fill_color and current is background
                if current_grid[r][c] == background_color and current_grid[r][c-1] == fill_color:
                    if new_grid[r][c] != fill_color: # check if already changed in this pass
                         new_grid[r][c] = fill_color
                         changed = True
                         
    # The above logic is backward (fills pixel c if c-1 is filled). Needs correction.
    # Correct logic: Fill pixel c-1 if pixel c is filled.
    
    new_grid = [row[:] for row in grid] # Start fresh with initial grid + seeds
    changed = True
    while changed:
        changed = False
        grid_before_pass = [row[:] for row in new_grid]
        for r in range(height):
            for c in range(1, width): # Iterate columns from left to right
                # If current pixel is fill_color and pixel to the left is background
                if grid_before_pass[r][c] == fill_color and grid_before_pass[r][c-1] == background_color:
                     if new_grid[r][c-1] != fill_color: # Check if not already filled
                        new_grid[r][c-1] = fill_color
                        changed = True
    
    return new_grid


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid based on identified colors and fill logic.
    """
    height = len(input_grid)
    width = len(input_grid[0])
    
    # 1. Calculate color counts and find all unique colors
    color_counts = Counter()
    all_colors = set()
    for r in range(height):
        for c in range(width):
            color = input_grid[r][c]
            color_counts[color] += 1
            all_colors.add(color)
            
    if not color_counts:
        return input_grid # Should not happen with ARC constraints

    # 2. Identify Background Color (most frequent)
    background_color = color_counts.most_common(1)[0][0]
    
    # 3. Find Interface Colors and their frequencies
    interface_colors = {} # color -> count
    background_pixels = []
    for r in range(height):
        for c in range(width):
            if input_grid[r][c] == background_color:
                background_pixels.append((r,c))
                for nr, nc in get_neighbors(r, c, height, width):
                    neighbor_color = input_grid[nr][nc]
                    if neighbor_color != background_color:
                        interface_colors[neighbor_color] = color_counts[neighbor_color]

    if not interface_colors:
         # No interface colors found, maybe grid is single color or only BG + disconnected colors
         # Or maybe the heuristic needs adjustment (e.g. if BG itself is small)
         # For now, assume no fill needed if no interface.
         return [row[:] for row in input_grid] 
         
    # 4. Identify Fill Color (least frequent interface color)
    # Sort interface colors by frequency (ascending)
    sorted_interface_colors = sorted(interface_colors.items(), key=lambda item: item[1])
    
    if not sorted_interface_colors:
         # Should be caught by `if not interface_colors` above, but as safeguard:
         return [row[:] for row in input_grid]
         
    fill_color = sorted_interface_colors[0][0]

    # 5. Identify Boundary Colors
    boundary_colors = all_colors - {background_color, fill_color}

    # 6. Determine Fill Type
    fill_type = "left" if background_color == 0 else "flood"
    
    # 7. Create output grid copy
    output_grid = [row[:] for row in input_grid]

    # 8. Find initial seed coordinates for the fill color
    start_coords = []
    for r in range(height):
        for c in range(width):
            if output_grid[r][c] == fill_color:
                start_coords.append((r, c))
                
    if not start_coords:
        # No fill seeds found, return copy of input
        return output_grid

    # 9. Execute the fill
    if fill_type == "flood":
        output_grid = flood_fill(output_grid, start_coords, fill_color, background_color, boundary_colors)
    elif fill_type == "left":
        # Note: Left fill implementation needs care. Initial seeds are already fill_color.
        # We need to fill background pixels adjacent (left) to fill_color pixels.
        output_grid = left_fill(output_grid, start_coords, fill_color, background_color, boundary_colors)

    return output_grid