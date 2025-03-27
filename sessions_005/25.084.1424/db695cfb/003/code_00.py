import numpy as np
from collections import Counter

"""
Transformation Rule:

1. Identify all blue pixels (color 1) as sources and magenta pixels (color 6) as potential destinations.
2. Determine the background color: the most frequent color in the input grid, excluding blue (1) and magenta (6). If no such color exists (e.g., grid only contains blue/magenta), default to white (0).
3. If magenta pixels exist, they are the destinations. If not, the blue pixels themselves become the destinations for each other (excluding a pixel being its own destination).
4. Initialize the output grid as a copy of the input grid.
5. For every unique pair of a source pixel and a destination pixel:
    a. If the source and destination are the same pixel, skip this pair.
    b. Determine the color for this path: it's the color of the destination pixel.
    c. Calculate a path from the source towards the destination.
    d. The path progresses one step at a time to an adjacent pixel (including diagonals).
    e. At each step, choose the adjacent pixel that minimizes the Manhattan distance to the destination.
    f. If multiple adjacent pixels have the same minimum distance, prioritize diagonal moves (where both row and column change) over axial moves (where only row or column changes).
    g. If there's still a tie among diagonal or among axial moves, prioritize the move with the smaller row index, and then the smaller column index.
    h. The path calculation stops *before* reaching the destination pixel itself.
    i. For each pixel position along the calculated path (excluding the source pixel): if its current color in the *output grid* is the background color, change its color in the *output grid* to the path color determined in step 5b. This allows paths drawn earlier to potentially block subsequent paths.
6. Return the final modified output grid.
"""

def get_neighbors(r, c, height, width):
    """Gets valid 8-directional neighbors for a given coordinate.

    Returns:
        list: A list of tuples, where each tuple contains:
              ((neighbor_row, neighbor_col), (delta_row, delta_col)).
    """
    neighbors = []
    # Order matters for tie-breaking: check smaller row/col first
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0:
                continue
            nr, nc = r + dr, c + dc
            if 0 <= nr < height and 0 <= nc < width:
                neighbors.append(((nr, nc), (dr, dc)))
    # Sort neighbors for consistent tie-breaking: row, then column
    neighbors.sort(key=lambda x: (x[0][0], x[0][1]))
    return neighbors

def manhattan_distance(p1, p2):
    """Calculates Manhattan distance between two points (tuples)."""
    return abs(p1[0] - p2[0]) + abs(p1[1] - p2[1])

def find_pixels(grid, color):
    """Finds all coordinates (row, col) of pixels with a specific color."""
    return list(zip(*np.where(grid == color)))

def get_background_color(grid):
    """Finds the most common color excluding blue (1) and magenta (6)."""
    counts = Counter(grid.flatten())
    # Remove source and potential destination colors from candidates
    if 1 in counts:
        del counts[1]
    if 6 in counts:
        del counts[6]

    if not counts:
        # Fallback if only blue/magenta exist, or grid is empty
        # Check if 0 exists, otherwise pick most frequent of remaining
        # (though this case seems unlikely based on examples)
        all_counts = Counter(grid.flatten())
        if 0 in all_counts:
             return 0 # Default to white if available
        elif all_counts:
             return all_counts.most_common(1)[0][0] # Most frequent overall
        else:
             return 0 # Default for empty grid

    # Return the most frequent remaining color
    return counts.most_common(1)[0][0]


def transform(input_grid):
    """
    Applies the path-drawing transformation based on blue and magenta pixels.
    """
    output_grid = np.copy(input_grid)
    height, width = input_grid.shape

    # 1. Identify source and potential destination pixels
    source_pixels = find_pixels(input_grid, 1) # Blue
    magenta_pixels = find_pixels(input_grid, 6) # Magenta

    # 2. Determine background color
    background_color = get_background_color(input_grid)

    # 3. Determine actual destination pixels
    if magenta_pixels:
        destination_pixels = magenta_pixels
    else:
        destination_pixels = source_pixels

    # Exit early if no sources or destinations
    if not source_pixels or not destination_pixels:
        return output_grid

    # 5. Iterate through each source-destination pair
    for start_pos in source_pixels:
        for end_pos in destination_pixels:
            # 5a. Skip if source is the same as destination
            if start_pos == end_pos:
                continue

            # 5b. Determine path color (color of destination)
            path_color = input_grid[end_pos] # Get color from original grid

            # 5c-i. Calculate path and color background pixels along it
            current_pos = start_pos
            while True: # Loop until path ends or hits destination
                # 5d. Get neighbors
                neighbors = get_neighbors(current_pos[0], current_pos[1], height, width)

                if not neighbors: # Should not happen in grid > 1x1
                    break

                # 5e. Calculate distances and find minimum
                min_dist = float('inf')
                best_neighbors_dist = []
                for neighbor_pos, move_delta in neighbors:
                    # Don't move into the destination pixel itself
                    if neighbor_pos == end_pos:
                        continue
                    dist = manhattan_distance(neighbor_pos, end_pos)
                    best_neighbors_dist.append({'pos': neighbor_pos, 'delta': move_delta, 'dist': dist})
                    min_dist = min(min_dist, dist)

                # Filter neighbors with minimum distance
                min_dist_neighbors = [n for n in best_neighbors_dist if n['dist'] == min_dist]

                # If no valid moves found (e.g., only move is into destination), stop path
                if not min_dist_neighbors:
                    break

                # 5f. Prioritize diagonal moves
                diagonal_moves = [n for n in min_dist_neighbors if abs(n['delta'][0]) == 1 and abs(n['delta'][1]) == 1]
                if diagonal_moves:
                    candidates = diagonal_moves
                else: # Otherwise consider axial moves
                    axial_moves = [n for n in min_dist_neighbors if abs(n['delta'][0]) != abs(n['delta'][1])]
                    candidates = axial_moves

                # If multiple candidates remain after diagonal/axial split...
                if len(candidates) > 1:
                  # 5g. Tie-break by row, then column (already sorted by get_neighbors)
                  next_step_info = candidates[0]
                elif len(candidates) == 1:
                  next_step_info = candidates[0]
                else:
                    # This case should ideally not happen if min_dist_neighbors was not empty
                    # but handles potential edge cases.
                    break


                next_pos = next_step_info['pos']

                # 5h. Stop *before* reaching the destination pixel
                # Note: This check is redundant due to filtering neighbors earlier,
                # but kept for clarity. The loop condition ensures we don't process
                # the destination pixel.
                # if next_pos == end_pos:
                #    break

                # 5i. Color the pixel if it's background color
                # Check the *current* output grid state
                if output_grid[next_pos] == background_color:
                    output_grid[next_pos] = path_color

                # Update current position for the next iteration
                current_pos = next_pos

                # Defensive break if somehow we get stuck (shouldn't happen with Manhattan)
                if manhattan_distance(current_pos, end_pos) == 0:
                     break


    # 6. Return the modified grid
    return output_grid