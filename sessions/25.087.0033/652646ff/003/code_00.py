import numpy as np
from collections import Counter

"""
The transformation rule involves identifying distinct colored shapes (components) in the input grid, excluding the background color and a noise color (gray, 5). For each identified shape component, a 6x6 pixel area starting at the component's top-left bounding box corner is extracted from the input grid. This 6x6 area is then "cleaned" to contain only the pixels matching the component's color (the primary color for this pattern) and the background color; all other pixels within the 6x6 area are replaced with the background color. These cleaned 6x6 patterns are then sorted based on the top-left coordinates of their corresponding components in the original input grid (first by row, then by column). Finally, the sorted, cleaned 6x6 patterns are vertically stacked to form the output grid.
"""

def find_background_color(grid):
    """
    Finds the most frequent color in the grid, ignoring gray (5) unless it's 
    the only non-zero count color besides gray.
    Assumes background is the most prevalent color.
    """
    colors, counts = np.unique(grid, return_counts=True)
    
    # Create a dictionary of counts excluding gray (5)
    counts_without_noise = {color: count for color, count in zip(colors, counts) if color != 5}
    
    if not counts_without_noise:
        # If only gray (5) or nothing else is present, return gray or the most frequent (which would be gray)
        # Or default to 0 if grid is empty or has only 0s? Let's return most frequent overall.
         if len(colors) > 0:
             return colors[np.argmax(counts)]
         else:
             return 0 # Default background for empty grid

    # Find the color with the max count among non-gray colors
    background_color = max(counts_without_noise, key=counts_without_noise.get)
    
    # Handle edge case where background itself might be 0 count if only gray exists beside it
    if counts_without_noise[background_color] == 0 and 5 in colors:
         # This implies only gray and maybe 0s are present. Return gray.
         return 5
         
    return background_color

def find_color_specific_components(grid, target_color):
    """
    Finds connected components of a specific target_color using 8-way adjacency.
    Returns a list of components, where each component is a list of (row, col) tuples.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    components = []

    for r in range(rows):
        for c in range(cols):
            # Check if the pixel is the target color and hasn't been visited
            if grid[r, c] == target_color and not visited[r, c]:
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
                            
                            # Check bounds and if neighbor is the target color and not visited
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               grid[nr, nc] == target_color and \
                               not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                
                if component_pixels: # Should always be true here
                    components.append(component_pixels)
                    
    return components

def get_bounding_box(component):
    """Calculates the bounding box (min_row, min_col, max_row, max_col) for a component."""
    if not component:
        return 0, 0, -1, -1 # Indicate invalid/empty component
    rows = [p[0] for p in component]
    cols = [p[1] for p in component]
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    return min_row, min_col, max_row, max_col

def clean_pattern(raw_pattern, primary_color, background_color):
    """
    Creates a cleaned 6x6 pattern by keeping only the primary color and background color pixels.
    All other pixels are replaced with the background color.
    """
    cleaned = np.full_like(raw_pattern, background_color)
    rows, cols = raw_pattern.shape
    for r in range(rows):
        for c in range(cols):
            if raw_pattern[r, c] == primary_color or raw_pattern[r, c] == background_color:
                cleaned[r, c] = raw_pattern[r, c]
    return cleaned

def transform(input_grid):
    """
    Extracts 6x6 patterns from the input grid based on non-background/non-noise components,
    cleans them, sorts them by position, and stacks them vertically.
    """
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    noise_color = 5

    # 1. Determine background color
    background_color = find_background_color(input_grid)

    # 2. Find all potential component colors
    potential_component_colors = np.unique(input_grid)
    
    patterns_map = {} # Use dict to store patterns keyed by coord to handle overlaps/duplicates simply

    # 3. Find components for each potential color
    for color in potential_component_colors:
        if color == background_color or color == noise_color:
            continue # Skip background and noise colors

        # Find all components of this specific color
        components_of_this_color = find_color_specific_components(input_grid, color)

        # 4. Process each component
        for component in components_of_this_color:
            if not component:
                continue
                
            primary_color = color # The color of this component is the primary color for the pattern

            # 4a. Get bounding box and top-left coordinate
            min_r, min_c, _, _ = get_bounding_box(component)
            coord = (min_r, min_c)

            # 4b. Check if a 6x6 area starting at coord fits in the grid
            if min_r + 6 <= rows and min_c + 6 <= cols:
                # 4c. Extract the raw 6x6 pattern area
                raw_pattern = input_grid[min_r:min_r+6, min_c:min_c+6]
                
                # 4d. Create the cleaned pattern
                cleaned = clean_pattern(raw_pattern, primary_color, background_color)
                
                # 4e. Store the cleaned pattern, keyed by coordinate.
                # If another component starts at the same coord, this will overwrite.
                # Based on examples, this seems acceptable; the first component found (order depends on iteration)
                # or the last component found for a coord will dictate the pattern. Sorting later ensures order.
                patterns_map[coord] = cleaned

    # 5. Sort patterns based on coordinates
    sorted_coords = sorted(patterns_map.keys())
    
    if not sorted_coords:
        # Handle cases where no valid patterns are found. Return an empty grid.
        # Determine output width (should be 6 if any pattern is found, otherwise maybe 0?)
        # Based on tests, returning 0x0 or 0xN seems appropriate. Let's try 0x6.
        return np.empty((0, 6), dtype=int).tolist() 
        
    sorted_patterns = [patterns_map[coord] for coord in sorted_coords]

    # 6. Assemble Output: Vertically stack the sorted patterns
    output_grid = np.vstack(sorted_patterns)

    return output_grid.tolist() # Convert back to list of lists for ARC standard
