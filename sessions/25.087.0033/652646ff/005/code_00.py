import numpy as np
from collections import Counter

"""
1. **Analyze Input:** Determine the `background_color` by finding the most frequent color in the input grid, excluding gray (color 5). Note that gray (5) acts as `noise_color`.
2. **Find Significant Shapes:** Identify all connected components (using 8-way adjacency) of any color that is *not* the `background_color` and *not* the `noise_color` (gray). From these, select only the "significant components" which are defined as components having more than 4 pixels.
3. **Extract and Clean Patterns:** For each significant component identified:
    * Find its top-left bounding box coordinate, `(min_r, min_c)`.
    * Check if a 6x6 area starting at `(min_r, min_c)` fits within the input grid dimensions.
    * If it fits, extract the 6x6 subgrid (the "raw pattern"). Let the color of this significant component be the `primary_color`.
    * Create a new 6x6 "cleaned pattern" grid. Fill it by copying pixels from the raw pattern only if they match the `primary_color` or the `background_color`. Replace all other pixels with the `background_color`.
    * Store this cleaned pattern along with its origin coordinate `(min_r, min_c)`.
4. **Sort:** Arrange the generated cleaned patterns in order based on their `(min_r, min_c)` coordinates, sorting primarily by row (`min_r`) and secondarily by column (`min_c`).
5. **Combine:** Vertically stack the sorted cleaned patterns to produce the final output grid. If no significant components were found that fit the 6x6 extraction criteria, the output is an empty grid with 0 rows and 6 columns.
"""

def find_background_color(grid):
    """
    Finds the most frequent color in the grid, ignoring gray (5) unless it's 
    the only significant color present besides potentially black/white (0).
    Assumes background is the most prevalent color after filtering noise.
    """
    colors, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(colors, counts))
    noise_color = 5

    # Filter out noise color for background calculation, unless it's dominant
    potential_bg_colors = {c: count for c, count in color_counts.items() if c != noise_color}

    if not potential_bg_colors:
        # Only noise color (and maybe 0) present, background is noise color or 0
        if noise_color in color_counts:
            return noise_color
        else: 
            return 0 # Default for empty or all-zero grid
            
    # Find the color with the highest count among non-noise colors
    background_color = max(potential_bg_colors, key=potential_bg_colors.get)
    
    return background_color

def find_components(grid, colors_to_find):
    """
    Finds all connected components for a set of target colors using 8-way adjacency.
    Returns a list of tuples: (color, component_pixels), where component_pixels 
    is a list of (row, col) tuples.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    all_components = []

    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # Check if the pixel is one of the target colors and hasn't been visited
            if color in colors_to_find and not visited[r, c]:
                component_pixels = []
                q = [(r, c)]
                visited[r, c] = True
                
                # Start BFS for this component
                while q:
                    row, col = q.pop(0)
                    component_pixels.append((row, col))
                    
                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            
                            # Check bounds and if neighbor is the same color and not visited
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               grid[nr, nc] == color and \
                               not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                
                if component_pixels: # Should always be true here
                    all_components.append({'color': color, 'pixels': component_pixels})
                    
    return all_components

def get_bounding_box(component_pixels):
    """Calculates the bounding box (min_row, min_col, max_row, max_col) for a component."""
    if not component_pixels:
        return 0, 0, -1, -1 # Indicate invalid/empty component
    rows = [p[0] for p in component_pixels]
    cols = [p[1] for p in component_pixels]
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    return min_row, min_col, max_row, max_col

def clean_pattern(raw_pattern, primary_color, background_color):
    """
    Creates a cleaned 6x6 pattern. Keeps only the primary color and background 
    color pixels. All other pixels are replaced with the background color.
    """
    cleaned = np.full_like(raw_pattern, background_color)
    rows, cols = raw_pattern.shape
    for r in range(rows):
        for c in range(cols):
            pixel_color = raw_pattern[r, c]
            if pixel_color == primary_color or pixel_color == background_color:
                cleaned[r, c] = pixel_color
    return cleaned

def transform(input_grid):
    """
    Transforms the input grid based on extracting, cleaning, sorting, and 
    stacking 6x6 patterns from significant components.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    noise_color = 5
    min_component_size = 4 # Significant components must have > 4 pixels

    # 1. Identify Background and Noise colors
    background_color = find_background_color(input_grid)

    # 2. Find potential component colors (all colors except background and noise)
    present_colors = np.unique(input_grid)
    component_colors_to_find = {c for c in present_colors if c != background_color and c != noise_color}

    # 3. Find all components for the target colors
    all_found_components = find_components(input_grid, component_colors_to_find)

    # 4. Filter for significant components and extract/clean patterns
    pattern_data = [] # List to store ((min_r, min_c), cleaned_pattern)
    
    for comp_info in all_found_components:
        component_pixels = comp_info['pixels']
        primary_color = comp_info['color']
        
        # Check if component is significant (size > min_component_size)
        if len(component_pixels) > min_component_size:
            # Get bounding box and top-left coordinate
            min_r, min_c, _, _ = get_bounding_box(component_pixels)
            coord = (min_r, min_c)

            # Check if a 6x6 area starting at coord fits within the grid
            if min_r + 6 <= rows and min_c + 6 <= cols:
                # Extract the raw 6x6 pattern area
                raw_pattern = input_grid[min_r:min_r+6, min_c:min_c+6]
                
                # Create the cleaned pattern
                cleaned = clean_pattern(raw_pattern, primary_color, background_color)
                
                # Store the coordinate and the cleaned pattern
                pattern_data.append((coord, cleaned))

    # 5. Sort patterns based on coordinates (row, then column)
    pattern_data.sort(key=lambda item: item[0])

    # 6. Assemble Output: Vertically stack the sorted patterns
    if not pattern_data:
        # If no significant components were found or fit, return empty 0x6 grid
        output_grid = np.empty((0, 6), dtype=int)
    else:
        # Extract just the cleaned patterns in sorted order
        sorted_patterns = [item[1] for item in pattern_data]
        # Stack them vertically
        output_grid = np.vstack(sorted_patterns)

    # Convert back to list of lists for ARC standard output format
    return output_grid.tolist()