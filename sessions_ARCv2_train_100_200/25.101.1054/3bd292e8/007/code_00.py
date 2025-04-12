"""
Transforms an input grid containing Red(2) and Orange(7) pixels based on a 
propagation rule originating from Red pixels.

Rule:
1. Red(2) pixels in the input remain Red(2) in the output.
2. Orange(7) pixels are transformed to either Green(3) or Gray(5).
3. An Orange(7) pixel becomes Gray(5) if it meets either of these conditions:
    a) It is 8-way adjacent (including diagonals) to at least one Red(2) pixel 
       in the input grid. These are considered 'seed' Gray pixels.
    b) It is 4-way adjacent (cardinal directions: up, down, left, right) to 
       another pixel that is already determined to be Gray(5) (either a seed 
       or one turned Gray by this propagation rule).
4. Any Orange(7) pixel that does not become Gray(5) through the above process 
   becomes Green(3).

The process effectively involves:
- Identifying 'seed' Gray pixels (Orange next to Red 8-way).
- Propagating the Gray color outwards from these seeds using 4-way adjacency 
  through the remaining Orange pixels.
- Coloring any untouched Orange pixels Green.
"""

import numpy as np
from collections import deque

def _is_valid(r, c, height, width):
    """Checks if coordinates (r, c) are within the grid bounds."""
    return 0 <= r < height and 0 <= c < width

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    """
    Applies the 8-way seed, 4-way propagation transformation.

    Args:
        input_grid: The input grid as a list of lists.

    Returns:
        The transformed grid as a list of lists.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Initialize output grid: -1 indicates unprocessed Orange pixels.
    output_np = np.full_like(input_np, -1) 
    
    # Queue for Breadth-First Search (BFS) propagation of Gray color
    queue = deque()
    
    # Deltas for neighbor checks
    deltas_8way = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]
    deltas_4way = [(-1, 0), (1, 0), (0, -1), (0, 1)]

    # --- Step 1 & 2: Initialize Output and Identify Seed Gray Pixels ---
    # Iterate through each cell to initialize output and find seeds
    for r in range(height):
        for c in range(width):
            if input_np[r, c] == 2: # Red pixel
                output_np[r, c] = 2 # Copy Red directly
            elif input_np[r, c] == 7: # Orange pixel
                is_adjacent_to_red_8way = False
                # Check 8 neighbors in the *input* grid for Red
                for dr, dc in deltas_8way:
                    nr, nc = r + dr, c + dc
                    if _is_valid(nr, nc, height, width) and input_np[nr, nc] == 2:
                        is_adjacent_to_red_8way = True
                        break # Found a Red neighbor, no need to check further
                
                if is_adjacent_to_red_8way:
                    # This Orange pixel is 8-way adjacent to Red -> Seed Gray pixel
                    output_np[r, c] = 5 # Mark as Gray
                    queue.append((r, c)) # Add to propagation queue
                else:
                    # Not adjacent to Red -> Tentatively mark as Green (will be processed later)
                    # Use the initial -1 placeholder to distinguish from final Green
                    pass # Keep as -1 for now
            else:
                # Copy any other colors directly (if they exist)
                 output_np[r, c] = input_np[r, c]

    # --- Step 3: Propagate Gray using BFS (4-way adjacency) ---
    # Use a set to track items added to the queue to prevent redundant processing
    processed_for_propagation = set(queue) 

    while queue:
        r, c = queue.popleft() # Get coordinates of a current Gray pixel
        
        # Examine 4 cardinal neighbors for propagation
        for dr, dc in deltas_4way:
            nr, nc = r + dr, c + dc
            neighbor_pos = (nr, nc)
            
            # Check if neighbor is valid, is an unprocessed Orange pixel (value -1),
            # and hasn't already been added to the queue
            if _is_valid(nr, nc, height, width) and output_np[nr, nc] == -1 and neighbor_pos not in processed_for_propagation:
                # Propagate Gray: Change unprocessed Orange neighbor to Gray
                output_np[nr, nc] = 5
                # Add the newly Gray pixel to the queue and mark as processed
                queue.append(neighbor_pos)
                processed_for_propagation.add(neighbor_pos)

    # --- Step 4: Finalize - Change remaining unprocessed Orange to Green ---
    # Any cell that was originally Orange (input value 7) but is still -1 
    # in the output grid was not reached by propagation.
    for r in range(height):
        for c in range(width):
            if output_np[r, c] == -1: # Check if it's an unprocessed Orange pixel
                 # Assert input_np[r,c] == 7 # Should be true if logic is correct
                 output_np[r, c] = 3 # Set to Green

    # Convert the final numpy array back to a list of lists
    output_grid = output_np.tolist()
    
    return output_grid