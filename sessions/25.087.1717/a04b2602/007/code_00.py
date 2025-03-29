import numpy as np
from collections import deque

"""
Transforms an input grid based on adjacency and propagation.

Rule:
1. Initialize the output grid as a copy of the input grid.
2. Identify all green pixels (3) in the input grid that are orthogonally adjacent to at least one red pixel (2) in the input grid.
3. Change these initially identified green pixels to blue (1) in the output grid. Keep track of their locations.
4. Starting from these initial blue pixels, propagate the blue color (1) to any adjacent green pixels (3 in the input grid) that haven't been changed yet.
5. Continue this propagation process until no more adjacent green pixels can be changed to blue. Orthogonal adjacency (up, down, left, right) is used for propagation.
6. Pixels that are not green, or green pixels that are not connected (via a path of green pixels) to an initially identified blue pixel, retain their original color from the input grid.
"""

def transform(input_grid):
    """
    Applies the adjacency and propagation transformation rule to the input grid.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists of integers.

    Returns:
        list of lists: The transformed output grid.
    """
    # Convert input to numpy array for efficient operations and indexing
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Initialize the output grid as a copy of the input grid.
    output_grid = np.copy(input_np)

    # Define orthogonal neighbor offsets.
    neighbor_offsets = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    # Queue for Breadth-First Search (BFS) to manage propagation
    # Stores coordinates (r, c) of pixels that have turned blue and need to propagate
    propagation_queue = deque()

    # --- Step 2 & 3: Find initial green pixels adjacent to red and turn them blue ---
    for r in range(height):
        for c in range(width):
            # Check if the current pixel in the *input* grid is green (3).
            if input_np[r, c] == 3:
                is_adjacent_to_red = False
                # Check each orthogonal neighbor in the *input* grid.
                for dr, dc in neighbor_offsets:
                    nr, nc = r + dr, c + dc
                    # Ensure the neighbor is within the grid boundaries.
                    if 0 <= nr < height and 0 <= nc < width:
                        # Check if the neighbor is red (2) in the *input* grid.
                        if input_np[nr, nc] == 2:
                            is_adjacent_to_red = True
                            break # Found a red neighbor, no need to check others

                # If this green pixel was adjacent to a red one in the input:
                if is_adjacent_to_red:
                    # Change this pixel's color to blue (1) in the *output* grid.
                    output_grid[r, c] = 1
                    # Add this pixel to the queue to start propagation from here.
                    propagation_queue.append((r, c))

    # --- Step 4 & 5: Propagate the blue color using BFS ---
    while propagation_queue:
        r, c = propagation_queue.popleft() # Get a blue pixel coordinate

        # Check its orthogonal neighbors
        for dr, dc in neighbor_offsets:
            nr, nc = r + dr, c + dc

            # Ensure the neighbor is within the grid boundaries
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor was originally green in the input
                # AND is not already blue in the output (to avoid cycles and redundant work)
                if input_np[nr, nc] == 3 and output_grid[nr, nc] == 3:
                    # Change the neighbor to blue in the output grid
                    output_grid[nr, nc] = 1
                    # Add the newly blue neighbor to the queue to continue propagation
                    propagation_queue.append((nr, nc))

    # Convert the final numpy array back to a list of lists as required.
    return output_grid.tolist()