```python
import numpy as np
from collections import defaultdict
import collections

"""
Identify all distinct contiguous objects of non-white colors in the input grid using orthogonal adjacency.
Count the number of objects for each color.
Sort the colors based on their object counts in descending order.
Determine the output grid dimensions: height is the number of unique non-white colors, width is the maximum object count.
Create the output grid, initializing with white (0).
For each color in the sorted list, add a row to the output grid.
Each row represents one color, containing 'count' pixels of that color, right-aligned.
"""

def find_objects_by_color(grid):
    """
    Finds all contiguous objects of non-white colors and counts them per color.

    Args:
        grid (np.array): The input grid.

    Returns:
        dict: A dictionary mapping color -> count of objects.
    """
    rows, cols = grid.shape
    visited = np.zeros((rows, cols), dtype=bool)
    object_counts = defaultdict(int)
    
    for r in range(rows):
        for c in range(cols):
            color = grid[r, c]
            # Check if the cell is non-white and not yet visited
            if color != 0 and not visited[r, c]:
                # Found the start of a new object
                object_color = color
                object_counts[object_color] += 1
                
                # Use BFS to find all parts of this object and mark them visited
                q = collections.deque([(r, c)])
                visited[r, c] = True
                
                while q:
                    row, col = q.popleft()
                    
                    # Check neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        
                        # Check bounds, color match, and visited status
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == object_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            
    return object_counts

def transform(input_grid):
    """
    Transforms the input grid by summarizing object counts per color.

    Args:
        input_grid (list[list[int]]): The input grid as a list of lists.

    Returns:
        list[list[int]]: The transformed output grid.
    """
    # Convert input to numpy array for easier processing
    grid_np = np.array(input_grid, dtype=int)
    
    # Step 1, 2, 3: Find objects, group by color, and count
    object_counts = find_objects_by_color(grid_np)

    # Handle cases with no non-white objects (though examples don't show this)
    if not object_counts:
        return [[0]] # Or potentially an empty grid depending on interpretation

    # Step 4: Sort colors by count (descending)
    # Use color value as a secondary sort key for stability if counts are equal (optional but good practice)
    sorted_colors = sorted(object_counts.items(), key=lambda item: (-item[1], item[0]))

    # Step 5: Determine output dimensions
    output_height = len(sorted_colors)
    # Calculate max count, default to 0 if no objects found (handled above)
    output_width = max(count for color, count in sorted_colors) if sorted_colors else 0
    
    # Handle case where output_width might be 0 if somehow counts are zero
    if output_width == 0 and output_height > 0:
         output_width = 1 # Minimum width seems reasonable if colors exist but counts are 0 (unlikely)
    elif output_width == 0 and output_height == 0:
         return [[0]] # Return a single white pixel if no colors and no counts

    # Step 6: Construct the output grid
    # Initialize with background color (white = 0)
    output_grid_np = np.zeros((output_height, output_width), dtype=int)
    
    # Fill the grid row by row based on sorted colors and counts
    for i, (color, count) in enumerate(sorted_colors):
        # Apply color to the rightmost 'count' cells in the current row
        if count > 0: # Ensure we don't try to slice with negative indices if count is 0
             output_grid_np[i, -count:] = color
        
    # Convert back to list of lists format for the ARC standard
    output_grid = output_grid_np.tolist()

    return output_grid
```