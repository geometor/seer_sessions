import numpy as np
from scipy.ndimage import label, binary_dilation, generate_binary_structure

"""
Identifies the largest contiguous non-background (non-white) object in the input grid.
Then, identifies any background (white) pixels that are completely enclosed within this object (holes).
Fills these holes with the color of the largest object.
"""

def find_largest_non_background_object_color(grid: np.ndarray) -> int:
    """
    Finds the color of the largest connected component of non-background pixels.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        The integer color value of the largest non-background object.
        Returns 0 (background color) if no non-background objects are found.
    """
    background_color = 0
    non_background_mask = grid != background_color

    if not np.any(non_background_mask):
        return background_color # No non-background pixels

    # Label connected components of non-background pixels
    # Use connectivity 1 (4-connectivity) to match visual perception of holes better
    structure = generate_binary_structure(2, 1) 
    labeled_array, num_features = label(non_background_mask, structure=structure)

    if num_features == 0:
         return background_color # Should not happen if np.any(non_background_mask) is true

    # Find the size of each component (feature)
    component_sizes = np.bincount(labeled_array.ravel())
    
    # Ignore background label 0 if present in component_sizes
    if len(component_sizes) > 0 and component_sizes[0] > 0:
         component_sizes = component_sizes[1:] # Exclude background count
         
    if len(component_sizes) == 0:
         return background_color # No non-background components found

    # Find the label of the largest component
    # Add 1 back because we sliced off the background label 0 index
    largest_component_label = np.argmax(component_sizes) + 1 
    
    # Find the coordinates of any pixel belonging to the largest component
    coords = np.argwhere(labeled_array == largest_component_label)
    
    if coords.size > 0:
        # Get the color from the original grid at the first coordinate of the largest component
        shape_color = grid[coords[0, 0], coords[0, 1]]
        return int(shape_color)
    else:
         return background_color # Should not happen ideally


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Fills enclosed background regions (holes) within the largest non-background object 
    with the color of that object.

    Args:
        input_grid: A list of lists representing the input grid.

    Returns:
        A list of lists representing the transformed output grid.
    """
    
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy()
    height, width = grid.shape
    background_color = 0

    # 1. Identify the color of the largest contiguous non-background object
    shape_color = find_largest_non_background_object_color(grid)

    # If no shape is found or the shape color is background, return original
    if shape_color == background_color:
        return output_grid.tolist()

    # 2. Identify background pixels connected to the border (exterior background)
    # We use a BFS (Breadth-First Search) approach, effectively a flood fill from the border.
    
    visited = np.zeros_like(grid, dtype=bool)
    queue = []

    # Add all border background pixels to the queue and mark as visited
    for r in range(height):
        if grid[r, 0] == background_color and not visited[r, 0]:
            queue.append((r, 0))
            visited[r, 0] = True
        if grid[r, width - 1] == background_color and not visited[r, width - 1]:
            queue.append((r, width - 1))
            visited[r, width - 1] = True
    for c in range(width):
        if grid[0, c] == background_color and not visited[0, c]:
            queue.append((0, c))
            visited[0, c] = True
        if grid[height - 1, c] == background_color and not visited[height - 1, c]:
            queue.append((height - 1, c))
            visited[height - 1, c] = True
            
    # Perform BFS to find all reachable background pixels from the border
    q_idx = 0
    while q_idx < len(queue):
        r, c = queue[q_idx]
        q_idx += 1

        # Check 4 neighbors (up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc

            # Check if neighbor is within bounds
            if 0 <= nr < height and 0 <= nc < width:
                # Check if neighbor is background and not visited
                if grid[nr, nc] == background_color and not visited[nr, nc]:
                    visited[nr, nc] = True
                    queue.append((nr, nc))

    # 3. Identify and fill the holes
    # Any background pixel that was NOT visited by the BFS is an internal hole.
    for r in range(height):
        for c in range(width):
            if grid[r, c] == background_color and not visited[r, c]:
                # This is an internal hole, fill it with the shape color
                output_grid[r, c] = shape_color

    return output_grid.tolist()
