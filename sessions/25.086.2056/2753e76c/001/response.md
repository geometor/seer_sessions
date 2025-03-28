```python
import numpy as np
from collections import defaultdict, deque

"""
Identifies distinct, contiguous objects of non-white colors in the input grid.
Counts the number of objects for each color.
Sorts the colors based on their object count (descending) and then by color value (ascending) for ties.
Creates an output grid where:
  - The number of rows equals the number of distinct non-white colors found.
  - The number of columns equals the maximum object count found for any single color.
  - Each row corresponds to a unique color from the sorted list.
  - In row 'i' corresponding to color 'C' with count 'N', the last 'N' cells are filled with 'C', and the preceding cells are white (0).
"""

def find_object_counts(grid):
    """
    Finds connected components (objects) of non-white colors and counts them per color.

    Args:
        grid (np.array): The input grid.

    Returns:
        dict: A dictionary mapping color (int) to object count (int).
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    color_counts = defaultdict(int)
    
    # Directions for 4-way connectivity (up, down, left, right)
    directions = [(0, 1), (0, -1), (1, 0), (-1, 0)]

    for r in range(rows):
        for c in range(cols):
            # Check if the cell is non-white and hasn't been visited yet
            if grid[r, c] != 0 and not visited[r, c]:
                color = grid[r, c]
                # Found the start of a new object of this color
                color_counts[color] += 1
                
                # Perform BFS to find all parts of this object and mark them visited
                queue = deque([(r, c)])
                visited[r, c] = True
                
                while queue:
                    curr_r, curr_c = queue.popleft()
                    
                    # Explore neighbors
                    for dr, dc in directions:
                        nr, nc = curr_r + dr, curr_c + dc
                        
                        # Check bounds
                        if 0 <= nr < rows and 0 <= nc < cols:
                            # Check if neighbor is part of the same object and not visited
                            if grid[nr, nc] == color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                queue.append((nr, nc))
                                
    return dict(color_counts)


def transform(input_grid: np.ndarray) -> np.ndarray:
    """
    Transforms the input grid based on counts of colored objects.

    Args:
        input_grid (np.array): The input 2D numpy array.

    Returns:
        np.array: The transformed 2D numpy array.
    """
    # 1. Find and count distinct objects for each color
    color_counts = find_object_counts(input_grid)

    # Handle edge case: no non-white objects found
    if not color_counts:
        return np.zeros((1, 1), dtype=int) # Or potentially an empty grid np.array([[]]) depending on expected ARC behavior

    # 2. Get list of (color, count) pairs
    counts_list = list(color_counts.items())

    # 3. Sort the list: primary key = count (descending), secondary key = color (ascending)
    #    We sort by color ascending first, then by count descending (stable sort preserves previous order for ties)
    counts_list.sort(key=lambda item: item[0]) # Sort by color ascending
    counts_list.sort(key=lambda item: item[1], reverse=True) # Sort by count descending (stable)

    # 4. Determine output grid dimensions
    num_colors = len(counts_list)
    # Find max count, default to 1 if list is somehow non-empty but counts are 0 (shouldn't happen with find_object_counts)
    max_count = max(count for _, count in counts_list) if counts_list else 1 
    
    output_height = num_colors
    output_width = max_count

    # 5. Initialize the output grid with background color (0)
    output_grid = np.zeros((output_height, output_width), dtype=int)

    # 6. Populate the output grid row by row based on the sorted list
    for i, (color, count) in enumerate(counts_list):
        # Fill the last 'count' cells of row 'i' with 'color'
        # Calculate the start column index for the colored segment
        start_col = output_width - count
        # Fill the cells
        output_grid[i, start_col:output_width] = color
        
    return output_grid

```