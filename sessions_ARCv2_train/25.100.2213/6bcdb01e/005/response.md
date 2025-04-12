```python
import collections
import copy

"""
Transforms an input grid using a constrained iterative fill process originating from 
cells containing the digit 3. The fill spreads like a flood fill (specifically, 
using Breadth-First Search - BFS) to adjacent (horizontally and vertically) cells 
that contain the digit 7. Cells containing the digit 8 act as immutable barriers, 
preventing the fill from passing through them. The process continues iteratively 
until no more '7' cells can be converted to '3' according to the known rules.

Note: Based on comparison with provided examples, this standard flood fill 
implementation tends to "overfill" the grid, converting more '7's to '3's than 
expected. This suggests an additional, currently unidentified constraint exists 
that prevents certain reachable '7' cells from changing. The code below implements 
the understood BFS flood fill mechanism.
"""

def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Applies a constrained flood fill transformation to the input grid.

    Args:
        input_grid: A 2D list of integers representing the input grid.

    Returns:
        A 2D list of integers representing the transformed grid.
    """
    # Handle empty grid case
    if not input_grid or not input_grid[0]:
        # Return a deep copy to maintain consistency in returning new objects
        return copy.deepcopy(input_grid) 

    # Get grid dimensions
    rows = len(input_grid)
    cols = len(input_grid[0])

    # Initialize output_grid as a deep copy of the input grid.
    # Transformations will be applied to this copy.
    output_grid = [row[:] for row in input_grid]

    # Initialize a queue (FIFO) for the Breadth-First Search (BFS) flood fill.
    # This will store the coordinates of cells that are '3' and whose neighbors 
    # need to be checked.
    queue = collections.deque()

    # Step 2: Identify initial source cells (value 3) and add them to the queue.
    # These are the starting points for the spread.
    for r in range(rows):
        for c in range(cols):
            if output_grid[r][c] == 3:
                queue.append((r, c))

    # Define the four cardinal directions (horizontal and vertical neighbors)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)] # Right, Left, Down, Up

    # Step 3: Perform the iterative spreading (flood fill) using BFS
    while queue:
        # 3.a: Dequeue a cell whose neighbors need processing
        r, c = queue.popleft()

        # 3.b: Examine Neighbors
        for dr, dc in directions:
            nr, nc = r + dr, c + dc

            # 3.b.i: Check Validity (neighbor is within grid boundaries)
            if 0 <= nr < rows and 0 <= nc < cols:
                
                # 3.b.ii: Check Fillability 
                # Is the neighbor cell currently a '7' in the output grid?
                # Note: '8' cells will fail this check, acting as barriers.
                # Note: Cells already turned to '3' will also fail, preventing re-processing.
                if output_grid[nr][nc] == 7:
                    
                    # 3.b.iii: Apply Constraints (Step 1: Barrier 8 is implicit in check above)
                    # Step 2: Apply Unknown Constraint - THIS STEP IS MISSING.
                    # The current logic assumes any adjacent '7' can be filled.
                    # This is where the logic likely differs from the target transformation.
                    
                    # 3.b.iv: Fill and Enqueue (if constraints are met)
                    # Change the '7' to a '3' in the output grid
                    output_grid[nr][nc] = 3
                    # Add the newly filled cell to the queue so its neighbors can be checked
                    queue.append((nr, nc))

    # Step 4: Finalize - The queue is empty, meaning the spread is complete.
    # Return the modified grid.
    return output_grid
```