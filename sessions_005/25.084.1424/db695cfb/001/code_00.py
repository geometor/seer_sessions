import numpy as np

"""
Transformation Rule:

1. Identify all blue pixels (color 1) as sources and magenta pixels (color 6) as potential destinations.
2. If magenta pixels exist, they are the destinations. If not, the blue pixels themselves become the destinations for each other.
3. For every unique pair of a source pixel and a destination pixel:
    a. Calculate a path from the source towards the destination.
    b. The path progresses one step at a time to an adjacent pixel (including diagonals).
    c. At each step, choose the adjacent pixel that minimizes the Manhattan distance to the destination.
    d. If multiple adjacent pixels have the same minimum distance, prioritize diagonal moves over axial moves. If there's still a tie (e.g., two diagonal moves), prioritize the move with the smaller row index, and then the smaller column index.
    e. The path stops *before* reaching the destination pixel itself.
    f. For each pixel along the calculated path (excluding the source and destination): if its original color in the input grid was the background color, change its color to blue (1) in the output grid.
4. The final output grid contains the original blue and magenta pixels, the original background pixels, and the newly added blue pixels along the calculated paths.
"""

def get_neighbors(r, c, height, width):
    """Gets valid 8-directional neighbors for a given coordinate."""
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append(((nr, nc), (dr, dc))) # Store position and move delta
    return neighbors

def manhattan_distance(p1, p2):
    """Calculates Manhattan distance between two points."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def find_pixels(grid, color):
    """Finds all coordinates of pixels with a specific color."""
    return list(zip(*np.where(grid == color)))

def get_background_color(grid, source_coords, dest_coords):
    """Finds the most common color excluding source and destination colors."""
    potential_bgs = []
    source_dest_colors = {1, 6} # Blue and Magenta
    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] not in source_dest_colors:
                return grid[r, c] # Assume first non-source/dest is background
    # Fallback (shouldn't be needed based on examples)
    counts = np.bincount(grid.flatten())
    if len(counts) > 0:
        return np.argmax(counts)
    return 0 # Default to white if grid is empty?

def transform(input_grid):
    """
    Applies the path-drawing transformation based on blue and magenta pixels.
    """
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # 1. Identify source and potential destination pixels
    source_pixels = find_pixels(input_grid, 1) # Blue
    magenta_pixels = find_pixels(input_grid, 6) # Magenta

    # 2. Determine actual destination pixels
    if magenta_pixels:
        destination_pixels = magenta_pixels
    else:
        destination_pixels = source_pixels

    if not source_pixels or not destination_pixels:
        return output_grid # No sources or destinations, return original

    # 5. Identify the background color
    background_color = get_background_color(input_grid, source_pixels, destination_pixels)

    pixels_to_color = set()

    # 6. Iterate through each source pixel
    for start_pos in source_pixels:
        # 7. Iterate through each destination pixel
        for end_pos in destination_pixels:
            # 8. Skip if source is the same as destination
            if start_pos == end_pos:
                continue

            # 9. Calculate the path
            current_pos = start_pos
            path = [] # Store intermediate path coordinates before final coloring check

            while current_pos != end_pos:
                neighbors = get_neighbors(current_pos[0], current_pos[1], height, width)

                if not neighbors: # Should not happen in a grid > 1x1
                    break

                # Calculate distances and find minimum
                min_dist = float('inf')
                best_neighbors = []
                for neighbor_pos, move_delta in neighbors:
                    dist = manhattan_distance(neighbor_pos, end_pos)
                    if dist < min_dist:
                        min_dist = dist
                        best_neighbors = [(neighbor_pos, move_delta)]
                    elif dist == min_dist:
                        best_neighbors.append((neighbor_pos, move_delta))

                # Select the next step based on tie-breaking rules
                if not best_neighbors: # Should not happen
                     break

                # Prioritize diagonal moves
                diagonal_moves = [ (pos, delta) for pos, delta in best_neighbors if abs(delta[0]) == 1 and abs(delta[1]) == 1]
                if diagonal_moves:
                    candidates = diagonal_moves
                else: # Otherwise consider axial moves
                    candidates = best_neighbors

                # Further tie-break by row, then column
                candidates.sort(key=lambda x: (x[0][0], x[0][1])) # Sort by row, then col
                next_pos, _ = candidates[0]

                # Stop before reaching the destination
                if next_pos == end_pos:
                    break

                # Add the step to the potential path
                path.append(next_pos)
                current_pos = next_pos

            # Add valid path pixels to the set to be colored
            for pos in path:
                 if input_grid[pos] == background_color:
                      pixels_to_color.add(pos)


    # Color the identified pixels in the output grid
    for r, c in pixels_to_color:
        output_grid[r, c] = 1 # Change to blue

    return output_grid