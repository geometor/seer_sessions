import numpy as np
from collections import deque, Counter

"""
Transforms an input grid based on a unique 'trigger' number.

1. Identifies a unique non-zero integer ('trigger number', T) in the input grid and its location (r_t, c_t).
2. Determines a starting corner (r_s, c_s) for a fill process based on the quadrant of the trigger number's location.
   - Top-Left quadrant -> Bottom-Right corner
   - Bottom-Right quadrant -> Top-Left corner
   - Bottom-Left quadrant -> Top-Right corner
   - Top-Right quadrant -> Bottom-Left corner
3. Initializes the output grid as a copy of the input grid.
4. Sets the cell at the original trigger location (r_t, c_t) in the output grid to 0.
5. Performs a flood fill (BFS) starting from the determined corner (r_s, c_s):
   - The fill uses the trigger number T as the fill value.
   - The fill propagates only through cells that were originally 0 in the input grid.
   - The fill stops when it encounters a non-zero cell from the input grid.
6. Returns the modified output grid.
"""

def _find_trigger(grid_np):
    """Finds the unique non-zero number and its location in the grid."""
    counts = Counter(grid_np.flatten())
    trigger_num = -1
    for num, count in counts.items():
        if num != 0 and count == 1:
            trigger_num = num
            break
    
    if trigger_num == -1:
        # Fallback: In case the 'unique' logic needs adjustment (e.g., based on examples like train_4 where 8 appears many times)
        # Let's find any non-zero number that isn't the most frequent non-zero number.
        # This handles cases where there might be a background number like 8.
        non_zero_counts = {k: v for k, v in counts.items() if k != 0}
        if not non_zero_counts:
             raise ValueError("No non-zero numbers found in the input grid.")
        # Find the number with the minimum count among non-zero numbers
        trigger_num = min(non_zero_counts, key=non_zero_counts.get)
        if non_zero_counts[trigger_num] != 1:
             print(f"Warning: No strictly unique non-zero number found. Using {trigger_num} as trigger.")


    locations = np.where(grid_np == trigger_num)
    if len(locations[0]) == 0:
         raise ValueError(f"Trigger number {trigger_num} not found in the grid, something went wrong.")
         
    trigger_loc = (locations[0][0], locations[1][0])
    return trigger_num, trigger_loc

def transform(input_grid):
    """
    Applies the transformation rule to the input grid.
    """
    # Convert input to numpy array for easier processing
    grid_np = np.array(input_grid, dtype=int)
    H, W = grid_np.shape

    # Initialize output_grid as a copy of the input
    output_grid = grid_np.copy()

    # 1. Find the trigger number and its location
    try:
        trigger_num, (r_t, c_t) = _find_trigger(grid_np)
    except ValueError as e:
        print(f"Error finding trigger: {e}")
        return input_grid # Return original grid if trigger identification fails

    # 2. Determine the starting corner based on trigger location quadrant
    if r_t < H / 2 and c_t < W / 2: # Top-Left quadrant
        start_corner = (H - 1, W - 1) # Bottom-Right corner
    elif r_t >= H / 2 and c_t >= W / 2: # Bottom-Right quadrant
        start_corner = (0, 0) # Top-Left corner
    elif r_t >= H / 2 and c_t < W / 2: # Bottom-Left quadrant
        start_corner = (0, W - 1) # Top-Right corner
    else: # Top-Right quadrant (r_t < H/2 and c_t >= W/2)
        start_corner = (H - 1, 0) # Bottom-Left corner

    # 4. Set the original trigger location in the output grid to 0
    output_grid[r_t, c_t] = 0

    # 5. Perform BFS flood fill from the start corner
    queue = deque([start_corner])
    visited = set()

    while queue:
        r, c = queue.popleft()

        # Check bounds
        if not (0 <= r < H and 0 <= c < W):
            continue

        # Check if visited
        if (r, c) in visited:
            continue
        visited.add((r, c))

        # Check the value in the *original* input grid
        if grid_np[r, c] == 0:
            # Fill the cell in the output grid
            output_grid[r, c] = trigger_num
            
            # Add neighbors to the queue for propagation
            for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                nr, nc = r + dr, c + dc
                if (nr, nc) not in visited: # Add only if not visited yet
                     queue.append((nr, nc))
        # If the original cell was non-zero, the fill stops here for this path

    # Convert back to list of lists if needed (often desired format)
    return output_grid.tolist()