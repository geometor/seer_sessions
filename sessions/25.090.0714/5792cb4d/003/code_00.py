import numpy as np
from collections import deque
import heapq

"""
Identifies the single connected object of non-background pixels (azure, 8).
Finds the two pixels within the object having the minimum number of object neighbors (using 8-way connectivity).
These pixels define the ends of a path that includes all pixels of the object.
Determines the path traversing all object pixels between these two ends.
Extracts the colors along this path, reverses the color sequence, and applies
the reversed sequence back onto the path pixels in the output grid.
The background (azure, 8) remains unchanged.
"""

# --- Helper Functions ---

def get_neighbors(coord, grid_shape, connectivity=8):
    """Gets valid neighbor coordinates for a given coordinate based on connectivity."""
    r, c = coord
    rows, cols = grid_shape
    neighbors = []
    for dr in [-1, 0, 1]:
        for dc in [-1, 0, 1]:
            if dr == 0 and dc == 0: continue
            # Skip diagonals if connectivity is 4
            if connectivity == 4 and abs(dr) + abs(dc) != 1: continue
            nr, nc = r + dr, c + dc
            # Check bounds
            if 0 <= nr < rows and 0 <= nc < cols:
                neighbors.append((nr, nc))
    return neighbors

def find_object_pixels(grid, background_color):
    """Finds all coordinates belonging to non-background objects."""
    object_pixels = set()
    rows, cols = grid.shape
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != background_color:
                object_pixels.add((r, c))
    return object_pixels

def find_min_neighbor_ends(object_pixels, grid_shape, connectivity=8):
    """
    Finds the two pixels within the object that have the minimum number of
    neighbors also belonging to the object. Handles ties by picking the
    first two encountered based on heap ordering (approximates coordinate sort).
    Returns a sorted list of the two endpoint coordinates.
    """
    if not object_pixels: return []
    if len(object_pixels) == 1: return list(object_pixels) # Single pixel object

    neighbor_counts = [] # Store (count, coord) tuples
    neighbor_map = {} # Store {coord: count} for easy lookup

    # Calculate neighbor counts for each object pixel
    for r, c in object_pixels:
        count = 0
        for nr, nc in get_neighbors((r, c), grid_shape, connectivity):
            if (nr, nc) in object_pixels:
                count += 1
        heapq.heappush(neighbor_counts, (count, (r, c)))
        neighbor_map[(r, c)] = count

    if not neighbor_counts: return []

    # Find the minimum count
    min_count = neighbor_counts[0][0]

    # Collect all pixels with the minimum count
    min_count_pixels = [coord for count, coord in neighbor_counts if count == min_count]

    # If there are exactly two, these are our ends
    if len(min_count_pixels) == 2:
        return sorted(min_count_pixels)
    # If there's only one with the minimum count (e.g., start of a line ending in a thicker part)
    # Find the pixel with the second minimum count.
    elif len(min_count_pixels) == 1:
        first_end = min_count_pixels[0]
        second_end = None
        min_count2 = float('inf')
        # Find the minimum count > min_count
        for count, coord in neighbor_counts:
             if count > min_count:
                 min_count2 = min(min_count2, count)

        # Collect all pixels with this second minimum count
        second_min_pixels = [coord for count, coord in neighbor_counts if count == min_count2]

        # If there's one, that's our second end. If multiple, pick the first by sort order.
        if second_min_pixels:
             second_end = sorted(second_min_pixels)[0]
             return sorted([first_end, second_end])
        else: # Should not happen if object size > 1
             return sorted([first_end]) # Only found one end

    # If there are more than two pixels with the minimum count (e.g., corners of a rectangle)
    # We need a tie-breaker. Sorting by coordinates (row, then col) is a common heuristic.
    elif len(min_count_pixels) > 2:
         # Return the two extremes based on coordinate sorting
         sorted_min_pixels = sorted(min_count_pixels)
         return [sorted_min_pixels[0], sorted_min_pixels[-1]]

    return [] # Should not be reached

def find_full_path_dfs(start, end, object_pixels, grid_shape, connectivity=8):
    """
    Finds a path using Depth First Search that starts at 'start', ends at 'end',
    and visits every pixel in 'object_pixels' exactly once.
    """
    if not object_pixels: return None
    # Handle single pixel object case
    if start == end: return [start] if start in object_pixels else None
    if start not in object_pixels or end not in object_pixels: return None

    target_path_len = len(object_pixels)
    stack = [(start, [start])] # Stack stores (current_node, path_list_so_far)

    while stack:
        (current_node, path) = stack.pop()

        # Check if we reached the target end and the path includes all object pixels
        if current_node == end and len(path) == target_path_len:
            # Verify all object pixels are indeed in the path (sanity check)
            if set(path) == object_pixels:
                return path
            else:
                 # This case indicates an issue, maybe disconnected components mistakenly treated as one object?
                 continue # Continue searching

        # Explore neighbors
        # Get neighbors and filter for those within the object
        potential_neighbors = [n for n in get_neighbors(current_node, grid_shape, connectivity) if n in object_pixels]

        for neighbor in potential_neighbors:
            # If the neighbor hasn't been visited in the current path attempt
            if neighbor not in path:
                new_path = path + [neighbor]
                # Check again if we just reached the end with the correct length
                if neighbor == end and len(new_path) == target_path_len:
                     if set(new_path) == object_pixels:
                         return new_path
                     else:
                         continue
                # If not the end, or path too short, push to stack to explore further
                # Optimization: Don't push if path is already too long (shouldn't happen with 'not in path' check)
                elif len(new_path) <= target_path_len:
                     stack.append((neighbor, new_path))

    # If the loop finishes without returning, no valid path covering all pixels was found
    print(f"DFS Warning: Could not find a path from {start} to {end} covering all {target_path_len} pixels.")
    return None

# --- Main Transformation Function ---

def transform(input_grid):
    """
    Reverses the color sequence along the path covering all pixels of the
    single non-background object, defined by its min-neighbor endpoints.
    """
    # Convert input to numpy array for easier handling
    input_grid_np = np.array(input_grid, dtype=int)
    output_grid = np.copy(input_grid_np)
    grid_shape = input_grid_np.shape

    # Define background color (assuming 8 based on examples)
    background_color = 8
    # Define connectivity (assuming 8 based on examples)
    connectivity = 8

    # 1. Identify the object pixels
    object_pixels = find_object_pixels(input_grid_np, background_color)

    # If no object, return original grid
    if not object_pixels:
        return output_grid.tolist()

    # Handle single-pixel object: color remains the same
    if len(object_pixels) == 1:
        return output_grid.tolist()

    # 2. Find the two 'end' pixels (those with minimum object neighbors)
    endpoints = find_min_neighbor_ends(object_pixels, grid_shape, connectivity)

    # Expect exactly two endpoints for a reversible path covering all pixels
    if len(endpoints) != 2:
        print(f"Warning: Expected 2 endpoints, found {len(endpoints)}: {endpoints}. Returning original grid.")
        # Or potentially handle single endpoint for loops if needed? For now, return original.
        return output_grid.tolist()

    # Endpoints are already sorted by find_min_neighbor_ends
    start_node, end_node = endpoints[0], endpoints[1]

    # 3. Determine the path covering all object pixels between endpoints using DFS
    path_coords = find_full_path_dfs(start_node, end_node, object_pixels, grid_shape, connectivity)

    # If DFS couldn't find a path covering all pixels (might happen for complex shapes)
    if path_coords is None:
        # Try reversing the start/end points just in case DFS implementation has directional bias
        # although a correct DFS shouldn't theoretically need this if a path exists.
        print(f"Retrying DFS with reversed endpoints: {end_node} -> {start_node}")
        path_coords = find_full_path_dfs(end_node, start_node, object_pixels, grid_shape, connectivity)

    if path_coords is None or len(path_coords) != len(object_pixels):
        print(f"Error: Failed to find a valid path covering all object pixels. Path length found: {len(path_coords) if path_coords else 0}, Object size: {len(object_pixels)}. Returning original grid.")
        return output_grid.tolist()

    # 4. Extract the list of colors along the found path
    path_colors = [input_grid_np[r, c] for r, c in path_coords]

    # 5. Reverse the order of the colors
    reversed_colors = path_colors[::-1]

    # 6. Create the output grid (already copied)
    # 7. Replace colors along the path coordinates with the reversed colors
    for i, (r, c) in enumerate(path_coords):
        output_grid[r, c] = reversed_colors[i]

    # Return the modified grid as a list of lists
    return output_grid.tolist()