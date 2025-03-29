```python
import collections
import copy

# Define color constants for clarity
WHITE = 0
BLUE = 1
RED = 2
GREEN = 3

def transform(input_grid):
    """
    Performs a constrained flood fill starting from the initial Red (2) pixel(s).
    The fill spreads orthogonally (up, down, left, right) into adjacent White (0) pixels.
    The fill is blocked by Blue (1) pixels, Green (3) pixels, and the grid boundaries.
    All reachable White (0) pixels are changed to Red (2) in the output grid.
    Original Red (2), Blue (1), and Green (3) pixels from the input are preserved
    in their original locations in the output grid.
    """

    # Get grid dimensions
    height = len(input_grid)
    width = len(input_grid[0])

    # Initialize the output grid as a deep copy of the input grid.
    # This ensures that original Red, Blue, and Green pixels are preserved,
    # and we modify a separate grid.
    output_grid = copy.deepcopy(input_grid)

    # Queue for Breadth-First Search (BFS), stores coordinates (row, col).
    queue = collections.deque()

    # Set to keep track of visited coordinates (row, col) to avoid cycles and redundant processing.
    visited = set()

    # --- Step 1: Find all initial Red (2) pixels ---
    # These are the starting points for the flood fill.
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is Red in the *input* grid
            if input_grid[r][c] == RED:
                start_coord = (r, c)
                # Ensure we don't add the same starting coordinate multiple times
                # (though BFS handles cycles, this is slightly cleaner)
                if start_coord not in visited:
                    # Mark the starting Red pixel as visited
                    visited.add(start_coord)
                    # Add the starting Red pixel to the queue to begin the BFS
                    queue.append(start_coord)
                    # Note: We do NOT change the color of the starting Red pixel itself.
                    # The deep copy already preserved its original color in output_grid.

    # Define orthogonal directions for neighbor exploration: (dr, dc)
    # Represents changes in row and column: (down, up, right, left)
    directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

    # --- Step 2: Perform BFS flood fill ---
    while queue:
        # Get the next coordinate from the front of the queue
        current_r, current_c = queue.popleft()

        # Explore orthogonal neighbors of the current cell
        for dr, dc in directions:
            next_r, next_c = current_r + dr, current_c + dc
            next_coord = (next_r, next_c)

            # --- Check 1: Is the neighbor within the grid boundaries? ---
            if 0 <= next_r < height and 0 <= next_c < width:

                # --- Check 2: Has the neighbor already been visited? ---
                if next_coord not in visited:

                    # Mark the neighbor as visited *immediately* to prevent
                    # adding it to the queue multiple times from different paths.
                    visited.add(next_coord)

                    # Get the color of the neighbor cell from the *input* grid
                    neighbor_color = input_grid[next_r][next_c]

                    # --- Check 3: Is the neighbor White (0)? ---
                    # White cells are the ones we can fill.
                    if neighbor_color == WHITE:
                        # If it's White and reachable:
                        # a. Change its color to Red (2) in the output grid
                        output_grid[next_r][next_c] = RED
                        # b. Add this newly colored cell to the queue, so we
                        #    can explore *its* neighbors later.
                        queue.append(next_coord)

                    # --- Check 4: Is the neighbor a barrier (Blue or Green)? ---
                    # elif neighbor_color == BLUE or neighbor_color == GREEN:
                        # If it's a barrier (Blue or Green), the fill stops here for this path.
                        # It's already marked as visited, so we won't process it again.
                        # We do NOT add it to the queue.
                        # pass # Explicitly do nothing

                    # --- Check 5: Other cases (e.g., another Red pixel) ---
                    # else: # Handles Red pixels (already visited or other start points) or unexpected colors
                        # If it's another Red pixel (part of the starting area or already filled),
                        # or any other non-White, non-barrier color, treat it like a barrier
                        # in terms of stopping the fill *propagation*, but allow the fill
                        # to have started *from* it if it was an initial Red pixel.
                        # It's already marked visited. Do not add to queue.
                        # pass # Explicitly do nothing

    # --- Step 3: Return the modified grid ---
    return output_grid
```