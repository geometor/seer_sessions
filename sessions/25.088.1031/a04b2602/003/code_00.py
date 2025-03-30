import numpy as np
from collections import deque

def transform(input_grid):
    """
    Transforms the input grid by changing green pixels (3) to blue (1) if they 
    are part of a contiguous green region that is adjacent (orthogonally or 
    diagonally) to any red pixel (2). The change propagates through the 
    connected green region. All other pixels retain their original color.

    Args:
        input_grid (list[list[int]]): A 2D list representing the input grid.

    Returns:
        list[list[int]]: A 2D list representing the transformed output grid.
    """
    # Convert input list of lists to a NumPy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    # Create a copy to modify, preserving the original input
    output_np = np.copy(input_np)
    height, width = input_np.shape

    # Define the relative coordinates for 8 neighbors (orthogonal and diagonal)
    neighbor_offsets = [
        (-1, -1), (-1, 0), (-1, 1),
        (0, -1),          (0, 1),
        (1, -1), (1, 0), (1, 1)
    ]

    # Queue for Breadth-First Search (BFS) propagation
    queue = deque()
    # Set to keep track of green pixels already turned blue or queued
    processed_or_queued = set()

    # --- Initialization Step ---
    # Find initial green pixels adjacent to red pixels
    for r in range(height):
        for c in range(width):
            # Check if the current pixel is green in the original input
            if input_np[r, c] == 3:
                is_adjacent_to_red = False
                # Check all 8 neighbors in the original input grid
                for dr, dc in neighbor_offsets:
                    nr, nc = r + dr, c + dc
                    # Check if the neighbor coordinates are within the grid bounds
                    if 0 <= nr < height and 0 <= nc < width:
                        # Check if the neighbor in the *original* input grid is red (2)
                        if input_np[nr, nc] == 2:
                            is_adjacent_to_red = True
                            break  # Found a red neighbor

                # If adjacent to red, mark it blue in output, add to queue and processed set
                if is_adjacent_to_red:
                    if (r, c) not in processed_or_queued:
                         output_np[r, c] = 1
                         queue.append((r, c))
                         processed_or_queued.add((r, c))

    # --- Propagation Step (BFS) ---
    while queue:
        # Get the next blue pixel coordinate from the queue
        curr_r, curr_c = queue.popleft()

        # Check its 8 neighbors
        for dr, dc in neighbor_offsets:
            nr, nc = curr_r + dr, curr_c + dc

            # Check if the neighbor coordinates are valid (within bounds)
            if 0 <= nr < height and 0 <= nc < width:
                # Check if the neighbor is green in the *current output grid* 
                # and hasn't been processed or queued yet
                if output_np[nr, nc] == 3 and (nr, nc) not in processed_or_queued:
                    # Change the neighbor to blue
                    output_np[nr, nc] = 1
                    # Add the neighbor to the queue for further propagation
                    queue.append((nr, nc))
                    # Mark neighbor as processed/queued
                    processed_or_queued.add((nr, nc))

    # Convert the output NumPy array back to a list of lists
    output_grid = output_np.tolist()
    return output_grid