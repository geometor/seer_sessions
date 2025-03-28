import numpy as np
from collections import deque

"""
Identify repeating non-background objects arranged along a diagonal line in the
input grid. Determine the sequence of these objects along the diagonal. Create
an output grid of the same size, initially filled with the background color (0).
Place the objects onto the output grid such that their order along the diagonal
is reversed compared to the input. The shape and colors of the objects remain
unchanged.
"""

def find_objects(grid):
    """
    Finds connected components of non-background pixels (objects).

    Args:
        grid (np.ndarray): The input grid.

    Returns:
        List[Tuple[Tuple[int, int], List[Tuple[int, int]]]]: A list where each
        element represents an object. Each element is a tuple containing:
        - The anchor point (top-left corner, min_row, min_col) of the object's bounding box.
        - A list of pixel coordinates [(row, col), ...] belonging to the object.
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    for r in range(height):
        for c in range(width):
            # If pixel is non-background and not visited, start BFS
            if grid[r, c] != 0 and not visited[r, c]:
                component_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c
                max_r, max_c = r, c

                while q:
                    row, col = q.popleft()
                    component_pixels.append((row, col))
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Check 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue
                            nr, nc = row + dr, col + dc
                            
                            # Check bounds
                            if 0 <= nr < height and 0 <= nc < width:
                                # If neighbor is non-background and not visited
                                if grid[nr, nc] != 0 and not visited[nr, nc]:
                                    visited[nr, nc] = True
                                    q.append((nr, nc))
                
                # Store the object with its anchor (top-left) and pixels
                anchor = (min_r, min_c)
                objects.append((anchor, component_pixels))
                
    return objects

def get_object_shape(anchor, pixels, grid):
    """
    Calculates the shape of an object relative to its anchor point.

    Args:
        anchor (Tuple[int, int]): The (row, col) of the object's anchor (top-left).
        pixels (List[Tuple[int, int]]): List of (row, col) coordinates of the object's pixels.
        grid (np.ndarray): The input grid to get pixel colors.

    Returns:
        List[Tuple[int, int, int]]: A list of (relative_row, relative_col, color)
        tuples defining the object's shape.
    """
    anchor_r, anchor_c = anchor
    shape = []
    for r, c in pixels:
        rel_r = r - anchor_r
        rel_c = c - anchor_c
        color = grid[r, c]
        shape.append((rel_r, rel_c, color))
    # Sort for consistency, although not strictly necessary if comparison handles sets
    shape.sort() 
    return shape

def draw_object(output_grid, anchor, shape):
    """
    Draws the object shape onto the output grid at the specified anchor position.

    Args:
        output_grid (np.ndarray): The grid to draw on (modified in place).
        anchor (Tuple[int, int]): The (row, col) where the object's anchor should be placed.
        shape (List[Tuple[int, int, int]]): The object shape defined by
                                             (rel_r, rel_c, color).
    """
    height, width = output_grid.shape
    anchor_r, anchor_c = anchor
    for rel_r, rel_c, color in shape:
        target_r, target_c = anchor_r + rel_r, anchor_c + rel_c
        # Check bounds before drawing
        if 0 <= target_r < height and 0 <= target_c < width:
            output_grid[target_r, target_c] = color
        # else: Optional: handle cases where object might partially go off-grid if needed

def transform(input_grid):
    """
    Reverses the order of repeating objects found along a diagonal path.

    Args:
        input_grid (np.ndarray): The input grid with objects.

    Returns:
        np.ndarray: The output grid with object order reversed.
    """
    # Find all non-background objects and their anchor points
    objects_data = find_objects(np.array(input_grid))

    # If no objects are found, return a grid filled with background color
    if not objects_data:
        return np.zeros_like(input_grid)

    # Assume all objects have the same shape. Get the shape from the first object found.
    first_object_anchor, first_object_pixels = objects_data[0]
    unique_object_shape = get_object_shape(first_object_anchor, first_object_pixels, np.array(input_grid))
    
    # Extract just the anchor points
    anchors = [data[0] for data in objects_data]

    # Sort anchors based on their position along the diagonal
    # Sorting by (row, col) naturally orders points along diagonals progressing downwards
    sorted_anchors = sorted(anchors, key=lambda p: (p[0], p[1]))

    # The target positions for the output are the original positions but in reversed order
    target_anchors = sorted_anchors[::-1] # Creates a reversed copy

    # Initialize the output grid with the background color
    output_grid = np.zeros_like(input_grid)

    # Draw the unique object shape at each target anchor position
    # The number of target anchors will match the number of original objects
    for anchor_pos in target_anchors:
        draw_object(output_grid, anchor_pos, unique_object_shape)

    return output_grid.tolist() # Convert back to list of lists if needed by the environment