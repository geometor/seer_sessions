```python
import numpy as np
from scipy.ndimage import label, generate_binary_structure
from collections import deque

"""
Identifies the largest contiguous non-background object (using 4-way connectivity).
Identifies background pixels (color 0) that are not reachable from the grid border via a 4-connected path of background pixels (i.e., enclosed holes).
Fills these enclosed holes with the color of the largest object.
"""

def _find_largest_non_background_object_color(grid: np.ndarray) -> int:
    """
    Finds the color of the largest 4-connected component of non-background pixels.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        The integer color value of the largest non-background object.
        Returns 0 (background color) if no non-background objects are found.
    """
    background_color = 0
    non_background_mask = grid != background_color

    if not np.any(non_background_mask):
        return background_color  # No non-background pixels

    # Label connected components using 4-connectivity
    structure = generate_binary_structure(2, 1) 
    labeled_array, num_features = label(non_background_mask, structure=structure)

    if num_features == 0:
        # This case should technically be covered by the np.any check, but included for safety
        return background_color 

    # Find the size of each component (feature)
    # np.bincount counts occurrences of each label (0, 1, 2, ...)
    # Label 0 corresponds to the background or pixels not part of any labeled component
    component_sizes = np.bincount(labeled_array.ravel())

    # Exclude the count for label 0 (background)
    if len(component_sizes) > 0:
         component_sizes[0] = 0 
    
    # Find the label of the largest component (if multiple largest, argmax returns the first)
    if np.all(component_sizes == 0):
        return background_color # No non-background components found

    largest_component_label = np.argmax(component_sizes)
    
    # Find coordinates of any pixel belonging to the largest component
    # Using np.argwhere is robust but potentially slow for large grids. We only need one pixel.
    # Faster alternative: find the first occurrence.
    coords = np.transpose(np.nonzero(labeled_array == largest_component_label))
    
    if coords.size > 0:
        # Get the color from the original grid at the first coordinate of the largest component
        first_coord = coords[0]
        shape_color = grid[first_coord[0], first_coord[1]]
        return int(shape_color)
    else:
         # Should not happen if largest_component_label > 0, but handle defensively
         return background_color


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by filling enclosed background regions (holes) 
    within the largest non-background object with the color of that object.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    height, width = grid.shape
    background_color = 0

    # 1. Identify the color of the largest contiguous non-background object (4-connectivity)
    shape_color = _find_largest_non_background_object_color(grid)

    # If no shape is found or the shape color is background, return original
    if shape_color == background_color:
        return output_grid.tolist()

    # 2. Identify background pixels connected to the border (external background)
    # Use Breadth-First Search (BFS) starting from border background pixels.
    
    is_external = np.zeros_like(grid, dtype=bool)
    queue = deque()

    # Add all border background pixels to the queue and mark as external
    for r in range(height):
        if grid[r, 0] == background_color and not is_external[r, 0]:
            queue.append((r, 0))
            is_external[r, 0] = True
        if grid[r, width - 1] == background_color and not is_external[r, width - 1]:
            queue.append((r, width - 1))
            is_external[r, width - 1] = True
            
    # Check cols separately to avoid adding corners twice
    for c in range(1, width - 1): # Exclude corners already checked
        if grid[0, c] == background_color and not is_external[0, c]:
            queue.append((0, c))
            is_external[0, c] = True
        if grid[height - 1, c] == background_color and not is_external[height - 1, c]:
            queue.append((height - 1, c))
            is_external[height - 1, c] = True
            
    # Perform BFS to find all reachable background pixels from the border
    while queue:
        r, c = queue.popleft()

        # Check 4 orthogonal neighbors
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if neighbor is within bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if neighbor is background and not yet marked as external
                if grid[nr, nc] == background_color and not is_external[nr, nc]:
                    is_external[nr, nc] = True
                    queue.append((nr, nc))

    # 3. Identify and fill the holes
    # Any background pixel that was NOT marked as external is an internal hole.
    for r in range(height):
        for c in range(width):
            if grid[r, c] == background_color and not is_external[r, c]:
                # This is an internal hole, fill it with the shape color
                output_grid[r, c] = shape_color

    # 4. Convert back to list of lists and return
    return output_grid.tolist()
```