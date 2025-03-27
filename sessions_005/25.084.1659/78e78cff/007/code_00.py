import numpy as np
from collections import Counter, deque

"""
Identifies three distinct colors: background (most frequent), seed (unique), and boundary (third).
Determines the row and column of the seed pixel.
Initiates a flood fill starting from the seed pixel's location AND all background pixels in the seed's row and column.
The flood fill uses the seed color, spreads only onto adjacent background pixels, and is blocked by boundary pixels.
The final output grid has the area reached by the flood fill colored with the seed color, while other pixels retain their original colors.
"""

def _find_colors(input_grid):
    """
    Identifies background, seed, and boundary colors and seed location based on frequency and uniqueness.

    Args:
        input_grid (np.array): The input grid.

    Returns:
        tuple: (background_color, seed_color, seed_loc, boundary_color)
               Returns None for any value if identification fails based on assumptions.
    
    Raises:
        ValueError: If the assumptions about color counts (most frequent, unique, exactly 3 distinct) are not met.
    """
    color_counts = Counter(input_grid.flatten())
    
    if len(color_counts) != 3:
         raise ValueError(f"Expected exactly 3 distinct colors, found {len(color_counts)}.")

    # Find background color (most frequent)
    background_color = color_counts.most_common(1)[0][0]

    # Find seed color and location (appears exactly once)
    seed_color = -1
    seed_loc = None
    unique_colors = [color for color, count in color_counts.items() if count == 1]

    if len(unique_colors) == 1:
        seed_color = unique_colors[0]
        seed_indices = np.where(input_grid == seed_color)
        # Ensure it's truly unique location-wise as well
        if len(seed_indices[0]) == 1: 
             seed_loc = (seed_indices[0][0], seed_indices[1][0])
        else:
             # Should not happen if count is 1, but safety check
             raise ValueError("Seed color found in multiple locations despite unique count.")
    else:
        raise ValueError(f"Expected exactly one unique color (seed), found {len(unique_colors)}.")


    # Find boundary color (the one that's not background or seed)
    boundary_color = -1
    remaining_colors = set(color_counts.keys()) - {background_color, seed_color}
    # Since we checked for exactly 3 colors, there must be exactly one remaining
    boundary_color = list(remaining_colors)[0]
         
    return background_color, seed_color, seed_loc, boundary_color


def _flood_fill(grid, start_coords, allowed_color, boundary_color):
    """
    Performs a flood fill to find all reachable coordinates with the allowed_color,
    starting from start_coords, without crossing boundary_color.

    Args:
        grid (np.array): The input grid.
        start_coords (iterable): An iterable of (row, col) tuples to start the fill from.
        allowed_color (int): The color of pixels that can be visited and included (background).
        boundary_color (int): The color of pixels that block the fill.

    Returns:
        set: A set of (row, col) tuples representing the reachable coordinates
             (including starting coordinates if they match allowed_color or are the original seed).
             Note: The start_coords are added explicitly even if not allowed_color, 
             as per the logic needing the seed and cross shape as starting points.
    """
    height, width = grid.shape
    queue = deque()
    visited = set()

    # Initialize queue and visited set with all starting points
    # The fill logic will handle spreading only through allowed_color later.
    for r, c in start_coords:
        if 0 <= r < height and 0 <= c < width and (r, c) not in visited:
             visited.add((r, c))
             # We only queue up if the starting point itself allows spreading (is background)
             # OR if it's the original seed (even if seed isn't background).
             # In this revised logic, we know fill_starts includes the seed + bg pixels on cross.
             # We want the fill to emanate *from* all these points.
             # If a start point is boundary, it won't spread. If it's seed, it won't spread further
             # unless its neighbors are background. If it's background, it spreads.
             # Adding all visited points initially is fine, the queue handles valid spread.
             if grid[r,c] == allowed_color:
                 queue.append((r, c))
             # Consider if the seed itself needs explicit queuing if it wasn't BG color.
             # Since seed_loc is added to visited, and neighbors are checked, it implicitly works.

    while queue:
        r, c = queue.popleft()

        # Explore neighbors (cardinal directions)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            neighbor_loc = (nr, nc)

            # Check bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check not visited
                if neighbor_loc not in visited:
                    # Check neighbor has the allowed color (is not boundary or other)
                    if grid[nr, nc] == allowed_color:
                        visited.add(neighbor_loc)
                        queue.append(neighbor_loc)
                        
    return visited


def transform(input_grid):
    """
    Transforms the input grid by identifying background, seed, and boundary colors,
    then performing a flood fill starting from the seed location and background pixels
    in the seed's row/column. The fill uses the seed color, spreads through the
    background color, and is blocked by the boundary color.
    """
    height, width = input_grid.shape
    output_grid = np.copy(input_grid)

    # Step 1: Analyze Colors
    try:
        background_color, seed_color, seed_loc, boundary_color = _find_colors(input_grid)
    except ValueError as e:
        print(f"Color identification failed: {e}. Returning input grid.")
        # Fallback: return the original grid if color assumptions fail
        return output_grid 

    seed_row, seed_col = seed_loc

    # Step 2: Determine Fill Starting Points
    fill_starts = set()
    # Add the seed location itself
    fill_starts.add(seed_loc)
    # Add background pixels in the seed's row
    for c in range(width):
        if input_grid[seed_row, c] == background_color:
            fill_starts.add((seed_row, c))
    # Add background pixels in the seed's column
    for r in range(height):
        if input_grid[r, seed_col] == background_color:
            fill_starts.add((r, seed_col))

    # Step 3: Calculate Fill Area using Flood Fill
    # The fill spreads TO background color, FROM the starting points, stops AT boundary
    fill_area_coords = _flood_fill(input_grid, list(fill_starts), background_color, boundary_color)

    # Step 4: Generate Output Grid
    # Change the color of all pixels in the fill area to the seed color
    for r, c in fill_area_coords:
        # Ensure coordinates are valid just in case, though flood fill should guarantee it
        if 0 <= r < height and 0 <= c < width:
             output_grid[r, c] = seed_color
             
    # Ensure the original seed location is always the seed color in the output
    # (This covers cases where the seed might have been overwritten if it wasn't background)
    output_grid[seed_loc] = seed_color


    return output_grid