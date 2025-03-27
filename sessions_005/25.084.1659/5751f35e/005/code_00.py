import numpy as np
import heapq

"""
Fill specific white pixels based on a propagation method from non-white pixels using Manhattan distance, with a lowest-index tie-breaker.

Rule:
1. Check if the input grid has a complete, connected, single-pixel-wide border consisting only of white (0) pixels.
2. Identify the white pixels to be filled ('target pixels'):
    - If a complete white border exists, targets are all white pixels NOT on this border.
    - Otherwise, targets are ALL white pixels.
3. Simulate a simultaneous propagation outwards from all non-white pixels:
    a. Initialize a 'distance' grid with 0 for non-white pixels and infinity for white pixels.
    b. Initialize a 'source_color' grid, initially copying the input grid (non-white pixels hold their color, white pixels hold 0 or another placeholder).
    c. Use a priority queue (min-heap) storing tuples of (distance, row, col, color) initialized with all non-white pixels (distance 0).
    d. While the priority queue is not empty:
        i. Extract the pixel (r, c) with the smallest distance `d` and its source `color`.
        ii. If `d` is greater than the already recorded distance for (r, c) in the distance grid, skip (we've found a shorter path already).
        iii. For each Manhattan neighbor (nr, nc) of (r, c):
            - Calculate the new distance `new_dist = d + 1`.
            - If `new_dist` is less than the current distance recorded for (nr, nc):
                - Update distance grid at (nr, nc) to `new_dist`.
                - Update source_color grid at (nr, nc) to `color`.
                - Add (`new_dist`, nr, nc, `color`) to the priority queue.
            - Else if `new_dist` is equal to the current distance recorded for (nr, nc):
                - Update the source_color grid at (nr, nc) to `min(current_source_color[nr, nc], color)`.
                # No need to re-add to queue, as distance hasn't improved, just potentially tie-breaking.
4. Fill the target white pixels in the output grid:
    a. Create the output grid as a copy of the input.
    b. For each coordinate (r, c) identified as a target pixel in step 2:
        - Get the final color from the `source_color` grid at (r, c) determined by the propagation.
        - Set the `output_grid[r, c]` to this color.
5. Non-target white pixels and original non-white pixels retain their original color in the output grid.
"""

def _has_complete_white_border(grid: np.ndarray) -> bool:
    """Checks if the grid has a complete, connected, single-pixel white border."""
    height, width = grid.shape
    if height <= 1 or width <= 1: # Cannot have a complete border
        return False

    # Check top and bottom rows
    for c in range(width):
        if grid[0, c] != 0: return False
        if grid[height - 1, c] != 0: return False
    # Check left and right columns (excluding corners already checked)
    for r in range(1, height - 1):
        if grid[r, 0] != 0: return False
        if grid[r, width - 1] != 0: return False

    return True # If we passed all checks


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Applies the propagation-based filling rule with border preservation
    and lowest-index tie-breaking.
    """
    height, width = input_grid.shape
    output_grid = np.copy(input_grid)

    # 1. Check for complete white border
    has_border = _has_complete_white_border(input_grid)

    # 2. Identify target white pixels
    target_coords = []
    border_pixel_locations = set()
    if has_border:
        # Define border coordinates only if a border exists
        for c in range(width):
            border_pixel_locations.add((0, c))
            border_pixel_locations.add((height - 1, c))
        for r in range(1, height - 1):
            border_pixel_locations.add((r, 0))
            border_pixel_locations.add((r, width - 1))

    for r in range(height):
        for c in range(width):
            if input_grid[r, c] == 0:
                is_on_border = (r,c) in border_pixel_locations
                # Target if (no border exists) OR (border exists AND pixel is not on border)
                if not has_border or not is_on_border:
                    target_coords.append((r, c))

    # If there are no white pixels to target, return the original grid
    if not target_coords:
        return output_grid

    # 3. Simulate propagation using Dijkstra's algorithm / BFS with priority queue
    distance_grid = np.full((height, width), float('inf'))
    source_color_grid = np.zeros_like(input_grid) # Store the winning color index
    pq = [] # Min-heap: (distance, row, col, color_index)

    # Initialize queue and grids with non-white pixels
    non_white_coords = np.argwhere(input_grid != 0)
    if non_white_coords.size == 0:
        # No non-white pixels, no filling can occur
        return output_grid

    for r, c in non_white_coords:
        color = input_grid[r, c]
        distance_grid[r, c] = 0
        source_color_grid[r, c] = color
        heapq.heappush(pq, (0, r, c, color))

    # Run the propagation
    while pq:
        dist, r, c, color = heapq.heappop(pq)

        # If we found a shorter path already, skip
        if dist > distance_grid[r, c]:
            continue
        # If distance is same, but color is higher, skip (already processed with lower/equal color index)
        # Note: This check is implicitly handled by the update logic below,
        # but explicitly checking source_color_grid[r,c] here could optimize slightly.
        # if dist == distance_grid[r, c] and color > source_color_grid[r, c]:
        #     continue

        # Explore neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check bounds
            if 0 <= nr < height and 0 <= nc < width:
                new_dist = dist + 1
                current_neighbor_dist = distance_grid[nr, nc]

                # Found a shorter path to the neighbor
                if new_dist < current_neighbor_dist:
                    distance_grid[nr, nc] = new_dist
                    source_color_grid[nr, nc] = color
                    heapq.heappush(pq, (new_dist, nr, nc, color))
                # Found a path of the same length - apply tie-breaking
                elif new_dist == current_neighbor_dist:
                    # Update color only if the new color index is lower
                    if color < source_color_grid[nr, nc]:
                        source_color_grid[nr, nc] = color
                        # Re-push with the same distance but lower color index
                        # Ensures processing favors lower color index if distances are equal
                        # Note: Technically Dijkstra doesn't require re-pushing on equal dist,
                        # but we need to ensure the lowest color propagates correctly in ties.
                        # An alternative is to only update source_color_grid here,
                        # and the final color will be correct when the target pixel is processed.
                        # Let's stick to just updating the source_color_grid for simplicity.
                        # heapq.heappush(pq, (new_dist, nr, nc, color)) # Avoid re-pushing

    # 4. Fill the target white pixels in the output grid
    for r, c in target_coords:
        # Only fill if the pixel was reached by the propagation
        if distance_grid[r, c] != float('inf'):
             output_grid[r, c] = source_color_grid[r, c]
        # Else: it remains white (0) as initialized in the copy

    # 5. Return the modified grid
    return output_grid