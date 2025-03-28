```python
import numpy as np
from collections import defaultdict

"""
Identify all distinct object patterns within the input grid. An object pattern is defined as the smallest rectangular subgrid (bounding box) enclosing a connected component of non-background (non-zero) pixels, including any background (zero) pixels within that rectangle. Count the occurrences of each unique pattern. Select the pattern that appears exactly two times. If multiple patterns appear twice, this rule might need refinement, but based on examples, we assume only one does. Among the two instances of the selected pattern, identify the one whose top-left corner has the minimum row index, breaking ties with the minimum column index. The output grid is this specific instance's pattern subgrid.
"""

def _find_patterns_and_locations(grid):
    """
    Finds all object patterns and their locations in the grid.

    An object is a connected component of non-background pixels.
    A pattern is the rectangular bounding box containing the object,
    including any background pixels within the box.

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        dict: A dictionary where keys are pattern tuples (tuple of tuples)
              and values are lists of (row, col) tuples representing the
              top-left coordinates of each occurrence.
    """
    patterns = defaultdict(list)
    visited = set()
    height, width = grid.shape

    for r in range(height):
        for c in range(width):
            # Check if the cell is non-background and not yet visited as part of an object
            if grid[r, c] != 0 and (r, c) not in visited:
                # Found the start of a potential new object
                component_cells = set()
                q = [(r, c)]
                visited.add((r, c))
                component_cells.add((r,c))
                min_r, max_r = r, r
                min_c, max_c = c, c

                # Perform BFS to find all connected non-background cells (8-way connectivity)
                while q:
                    curr_r, curr_c = q.pop(0)

                    # Update bounding box coordinates
                    min_r = min(min_r, curr_r)
                    max_r = max(max_r, curr_r)
                    min_c = min(min_c, curr_c)
                    max_c = max(max_c, curr_c)

                    # Explore neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = curr_r + dr, curr_c + dc

                            # Check bounds and if neighbor is non-background and not visited
                            if 0 <= nr < height and 0 <= nc < width and \
                               grid[nr, nc] != 0 and (nr, nc) not in visited:
                                visited.add((nr, nc))
                                component_cells.add((nr, nc))
                                q.append((nr, nc))

                # Extract the pattern (bounding box)
                pattern_grid = grid[min_r:max_r+1, min_c:max_c+1]
                # Convert numpy array to tuple of tuples for hashability
                pattern_tuple = tuple(map(tuple, pattern_grid))

                # Record the pattern and its top-left location
                patterns[pattern_tuple].append((min_r, min_c))

    return patterns


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Identifies the unique object pattern occurring exactly twice in the input grid
    and returns the instance that appears first (top-most, then left-most).

    Args:
        input_grid (np.ndarray): The input grid.

    Returns:
        np.ndarray: The extracted output grid corresponding to the first instance
                    of the pattern that occurs exactly twice.
    """
    # 1. Find all distinct patterns and their locations
    patterns_locations = _find_patterns_and_locations(input_grid)

    # 2. Identify the pattern that occurs exactly twice
    target_pattern_tuple = None
    target_locations = []
    for pattern, locations in patterns_locations.items():
        if len(locations) == 2:
            target_pattern_tuple = pattern
            target_locations = locations
            break # Assume only one such pattern exists per examples

    if target_pattern_tuple is None:
        # Handle the case where no pattern occurs exactly twice (e.g., return empty or raise error)
        # Based on the examples, this shouldn't happen for valid inputs.
        print("Warning: No pattern found occurring exactly twice.")
        # Returning the input might be a safe default, or an empty grid. Let's return empty.
        return np.array([[]], dtype=int)


    # 3. Sort the locations to find the first occurrence (min row, then min col)
    # The sort key is a tuple (row, col), Python sorts tuples element by element.
    sorted_locations = sorted(target_locations)
    first_location = sorted_locations[0] # Not strictly needed, just for clarity

    # 4. The output grid is the pattern itself
    # Convert the target pattern tuple back to a numpy array
    output_grid = np.array(target_pattern_tuple, dtype=int)

    return output_grid

```