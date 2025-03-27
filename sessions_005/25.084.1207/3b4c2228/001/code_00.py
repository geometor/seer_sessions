"""
This module defines a function to transform an input grid based on counting green (3) and red (2) objects.

The transformation rule is as follows:
1. Identify and count the number of distinct contiguous objects of green pixels (color 3) in the input grid (`num_green`).
2. Identify and count the number of distinct contiguous objects of red pixels (color 2) in the input grid (`num_red`).
3. Determine a value `N` based on the comparison of `num_green` and `num_red`:
    - If `num_green` is less than or equal to `num_red`, `N` = 1.
    - If `num_green` is greater than `num_red`:
        - If the difference (`num_green` - `num_red`) is exactly 1, `N` = 2.
        - If the difference (`num_green` - `num_red`) is 2 or more:
            - If `num_red` is 1, `N` = 2.
            - If `num_red` is 2 or more, `N` = 3.
4. Create a 3x3 output grid initialized with white pixels (color 0).
5. Place `N` blue pixels (color 1) along the main diagonal of the output grid, starting from the top-left corner (0,0) up to (N-1, N-1).
"""

import numpy as np
from collections import deque

def _find_objects(grid, color):
    """
    Finds and counts distinct contiguous objects of a specified color in the grid.

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        int: The number of distinct objects found.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    object_count = 0

    for r in range(rows):
        for c in range(cols):
            # If we find a pixel of the target color that hasn't been visited
            if grid[r, c] == color and not visited[r, c]:
                object_count += 1
                # Start a search (BFS) to find all connected pixels of this object
                queue = deque([(r, c)])
                visited[r, c] = True
                while queue:
                    row, col = queue.popleft()
                    # Check all 4 adjacent neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds and if the neighbor is the same color and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            queue.append((nr, nc))
    return object_count

def transform(input_grid):
    """
    Transforms the input grid based on counting green and red objects.

    Args:
        input_grid (np.array): A 2D numpy array representing the input grid.

    Returns:
        np.array: A 3x3 numpy array representing the transformed output grid.
    """
    # Count green (3) and red (2) objects
    num_green = _find_objects(input_grid, 3)
    num_red = _find_objects(input_grid, 2)

    # Determine the value of N based on the counts
    n_blue_pixels = 0
    if num_green <= num_red:
        n_blue_pixels = 1
    else: # num_green > num_red
        diff = num_green - num_red
        if diff == 1:
            n_blue_pixels = 2
        elif diff >= 2:
            if num_red == 1:
                n_blue_pixels = 2
            elif num_red >= 2:
                n_blue_pixels = 3
            else: # num_red == 0 and diff >= 2 (though this case wasn't explicitly in examples, handle defensively)
                  # Based on train_2 (3g, 1r -> N=2) and train_4 (4g, 2r -> N=3), increasing num_green seems key.
                  # Let's assume if num_red is 0, diff >= 2 implies N=3? 
                  # Re-check logic:
                  # T2: 3g, 1r. diff=2, num_red=1 -> N=2. Correct.
                  # T4: 4g, 2r. diff=2, num_red=2 -> N=3. Correct.
                  # Let's stick to the derived logic. If num_red is 0 and diff >=2, the conditions num_red==1 and num_red>=2 are both false.
                  # What should happen if num_red = 0 and num_green = 2 (diff=2)? Rules say nothing.
                  # What should happen if num_red = 0 and num_green = 3 (diff=3)? Rules say nothing.
                  # Let's trust the derived rules strictly. If neither sub-condition (num_red=1 or num_red>=2) is met, N remains 0.
                  # This seems unlikely given the task structure, let's re-evaluate.
                  # Maybe the logic is simpler:
                  # N = 1 if green <= red
                  # N = 2 if green = red + 1
                  # N = 3 if green >= red + 2  <-- Let's test this simpler hypothesis
                  # T1: 1g, 2r -> N=1. (1 <= 2). Correct.
                  # T2: 3g, 1r -> N=3. (3 >= 1+2). Incorrect. Output is N=2.
                  # T3: 2g, 2r -> N=1. (2 <= 2). Correct.
                  # T4: 4g, 2r -> N=3. (4 >= 2+2). Correct.
                  # T5: 3g, 2r -> N=2. (3 = 2+1). Correct.
                  # The original complex logic seems necessary due to T2. Let's stick with it.
                  # If num_red == 0 and diff >= 2, N should remain 0 according to strict reading.
                  pass # N stays 0 if neither sub-condition matches


    # Initialize a 3x3 output grid with white (0)
    output_grid = np.zeros((3, 3), dtype=int)

    # Place N blue (1) pixels on the main diagonal
    for i in range(n_blue_pixels):
        if i < 3: # Ensure we don't go out of bounds for the 3x3 grid
            output_grid[i, i] = 1

    return output_grid
