```python
import numpy as np
from collections import deque

"""
Transforms an input grid containing Red(2) and Orange(7) pixels.
Red(2) pixels remain unchanged.
Orange(7) pixels become Gray(5) if they are either 8-way adjacent to a Red(2) pixel 
or 8-way adjacent to another Orange pixel that becomes Gray(5). This creates a 
propagation effect where Gray 'spreads' from Red-adjacent Orange pixels.
Orange(7) pixels not reached by this Gray propagation become Green(3).

The transformation follows these steps:
1. Initialize an output grid, copying Red pixels and tentatively marking Orange pixels as Green.
2. Identify initial 'seed' Gray pixels: Orange pixels directly 8-way adjacent to Red pixels. Mark them as Gray in the output and add them to a propagation queue.
3. Propagate Gray: While the queue is not empty, take a Gray pixel coordinate, check its 8 neighbors. If a neighbor is currently marked Green, change it to Gray and add it to the queue.
4. Final Output: The grid after propagation is complete.
"""

def _is_valid(r, c, height, width):
    """Checks if coordinates are within grid bounds."""
    return 0 <= r < height and 0 <= c < width

def transform(input_grid: list[list[int]]) -> list[list[int]]:  
    """
    Applies the propagation-based transformation.

    Args:
        input_grid: The input grid as a list of lists.

    Returns:
        The transformed grid as a list of lists.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Initialize output grid: -1 for placeholder, will be filled
    output_np = np.full_like(input_np, -1) 
    
    # Queue for Breadth-First Search (BFS) propagation
    queue = deque()
    
    # Deltas for 8-way neighbors
    deltas = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

    # --- Step 1 & 2: Initialize Output and Identify Seed Gray Pixels ---
    for r in range(height):
        for c in range(width):
            if input_np[r, c] == 2: # Red pixel
                output_np[r, c] = 2
            elif input_np[r, c] == 7: # Orange pixel
                is_adjacent_to_red = False
                # Check 8 neighbors in the *input* grid for Red
                for dr, dc in deltas:
                    nr, nc = r + dr, c + dc
                    if _is_valid(nr, nc, height, width) and input_np[nr, nc] == 2:
                        is_adjacent_to_red = True
                        break
                
                if is_adjacent_to_red:
                    # This Orange pixel is adjacent to Red -> Seed Gray pixel
                    output_np[r, c] = 5 # Mark as Gray
                    queue.append((r, c)) # Add to propagation queue
                else:
                    # Not adjacent to Red -> Tentatively mark as Green
                    output_np[r, c] = 3 
            else:
                # Copy any other colors directly (though not expected based on examples)
                 output_np[r, c] = input_np[r, c]

    # --- Step 3: Propagate Gray using BFS ---
    while queue:
        r, c = queue.popleft() # Get coordinates of a Gray pixel
        
        # Examine 8 neighbors
        for dr, dc in deltas:
            nr, nc = r + dr, c + dc
            
            # Check if neighbor is valid and is currently marked as Green (3)
            if _is_valid(nr, nc, height, width) and output_np[nr, nc] == 3:
                # Propagate Gray: Change Green neighbor to Gray
                output_np[nr, nc] = 5
                # Add the newly Gray pixel to the queue to continue propagation
                queue.append((nr, nc))

    # --- Step 4: Final Output ---
    # The output_np grid now holds the final state.
    # Any pixel initially marked -1 should have been filled.
    # Convert back to list of lists
    output_grid = output_np.tolist()
    
    return output_grid
```