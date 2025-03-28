import numpy as np
from collections import Counter

def get_neighbours(grid, r, c):
    """
    Gets the colors of the 8 neighbours of a cell (r, c) in the grid.
    Handles boundary conditions.
    """
    neighbours = []
    rows, cols = grid.shape
    for dr in range(-1, 2):
        for dc in range(-1, 2):
            if dr == 0 and dc == 0:
                continue  # Skip the cell itself
            nr, nc = r + dr, c + dc
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbours.append(grid[nr, nc])
    return neighbours

def transform(input_grid):
    """
    Identifies the 'noise' color (least frequent) in the input grid.
    Counts how many noise pixels are associated with each 'background' color
    (determined by the most frequent color among the noise pixel's neighbours).
    Returns the background color associated with the maximum number of noise pixels.
    If there's a tie, returns the background color with the highest numerical value.
    """
    
    grid = np.array(input_grid)
    rows, cols = grid.shape

    # Step 1 & 2: Scan the input grid and count occurrences to find the noise color
    color_counts = Counter(grid.flatten())
    
    # Handle edge case of uniform grid (no distinct noise) - return the single color?
    # Based on examples, there's always a noise color.
    # If multiple colors have the same minimum count, the problem description is ambiguous.
    # Let's assume a unique minimum count color based on examples.
    noise_color = min(color_counts, key=color_counts.get)

    # Step 3: Initialize counters for potential background colors
    background_colors = {color: 0 for color in color_counts if color != noise_color}
    
    # If there are no background colors (grid only has noise color), return noise color?
    # This seems unlikely based on the task structure. If it happens, maybe return 0 or noise color.
    if not background_colors:
        # Or perhaps return the most frequent color if counts were tied for minimum?
        # Let's return the noise_color itself for now if no other colors exist.
        return noise_color 


    # Step 4 & 5: Iterate through grid, find noise pixels, and count associations
    for r in range(rows):
        for c in range(cols):
            # Step 5: If the current pixel is noise color
            if grid[r, c] == noise_color:
                # Step 5a: Get neighbours
                neighbours = get_neighbours(grid, r, c)
                
                # Step 5b: Determine local background color (most frequent neighbour)
                if neighbours:
                    neighbour_counts = Counter(n for n in neighbours if n != noise_color) # Exclude noise color itself just in case
                    if neighbour_counts:
                       # Find the most frequent neighbor color. Handle ties by max value if needed, but often one dominates.
                       # For simplicity now, take the most common. If counts are equal, Counter returns one arbitrarily.
                       local_background_color = neighbour_counts.most_common(1)[0][0]
                       
                       # Step 5c: Increment counter for the associated background color
                       if local_background_color in background_colors:
                           background_colors[local_background_color] += 1
                # If a noise pixel has no non-noise neighbours, it's not associated with any background. Skip.


    # Step 6: Find the maximum count among background colors
    if not background_colors: # Should have been caught earlier, but double check
         # This case means only noise color existed or noise pixels had no non-noise neighbors.
         # Returning 0 might be a safe default if no association is found.
         return 0 
         
    max_count = 0
    if background_colors: # Ensure dictionary is not empty before finding max
        max_count = max(background_colors.values()) if background_colors else 0


    # Step 7 & 8: Identify all background colors with the maximum count
    max_colors = [color for color, count in background_colors.items() if count == max_count]

    # Step 9: Apply tie-breaker (select highest numerical value)
    result_color = max(max_colors) if max_colors else 0 # Default to 0 if no colors found (edge case)

    # Step 10: Output the result color value (as a 1x1 grid or just the integer?)
    # The examples show a single integer as output.
    return result_color