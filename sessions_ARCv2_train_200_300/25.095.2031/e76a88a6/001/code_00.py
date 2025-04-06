import numpy as np
import copy
from collections import deque

"""
Identifies the first non-uniform shape (target pattern) found when scanning the grid
top-to-bottom, left-to-right, and applies its internal color pattern to all uniform
shapes composed solely of the number 5. The pattern is applied relative to the
top-left corner of both the pattern shape and the target '5' shapes.

Workflow:
1.  Find all distinct contiguous shapes formed by non-zero numbers in the input grid.
    Keep track of the order they are found (scan top-to-bottom, left-to-right).
2.  For each shape, determine its constituent colors, bounding box, and pixel coordinates.
3.  Identify the *first* shape found that contains more than one distinct non-zero color.
    This is the "target pattern shape".
4.  Extract the internal color pattern from the target pattern shape, storing colors
    relative to its top-left corner coordinate.
5.  Identify all shapes that are composed *exclusively* of the number 5.
6.  Create a copy of the input grid to serve as the output grid.
7.  For each identified shape composed only of 5s:
    a. Iterate through the pixel coordinates (r, c) belonging to this shape.
    b. For each pixel, calculate its relative position (dr, dc) from the shape's
       own top-left corner.
    c. Look up the color in the target pattern using the same relative position (dr, dc).
    d. If a color exists at that relative position in the pattern, update the
       output grid at coordinate (r, c) with this pattern color.
8.  Return the modified output grid.
"""

# Helper function to find connected components (shapes) using Breadth-First Search
def find_shapes(grid: np.ndarray) -> list[dict]:
    """
    Finds all contiguous non-zero shapes in the grid.

    Args:
        grid: A numpy array representing the input grid.

    Returns:
        A list of dictionaries, where each dictionary represents a shape
        and contains 'pixels', 'colors', 'is_uniform', 'bounding_box',
        and 'top_left' keys. Shapes are returned in the order their
        top-left-most pixel is encountered during scanning.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    shapes = []

    for r in range(rows):
        for c in range(cols):
            # If we find a non-zero cell that hasn't been visited, start a BFS
            if grid[r, c] != 0 and not visited[r, c]:
                q = deque([(r, c)])
                visited[r, c] = True
                current_shape_pixels = set([(r, c)])
                current_shape_colors = set()
                min_r, min_c = r, c # Initialize bounding box with the starting cell
                max_r, max_c = r, c

                # Perform BFS to find all connected pixels of the shape
                while q:
                    row, col = q.popleft()
                    pixel_color = grid[row, col]
                    current_shape_colors.add(pixel_color)

                    # Update bounding box
                    min_r = min(min_r, row)
                    min_c = min(min_c, col)
                    max_r = max(max_r, row)
                    max_c = max(max_c, col)

                    # Explore neighbors (4-connectivity: up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds and if the neighbor is part of a shape and not visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] != 0 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            current_shape_pixels.add((nr, nc))

                # Determine if the shape is uniform (only one non-zero color)
                is_uniform = len(current_shape_colors) == 1
                
                # Store shape information
                shape_info = {
                    "pixels": current_shape_pixels,
                    "colors": current_shape_colors,
                    "is_uniform": is_uniform,
                    "bounding_box": (min_r, min_c, max_r, max_c),
                    "top_left": (min_r, min_c) # Use min_r, min_c as the reference point
                }
                shapes.append(shape_info)
    return shapes

# Helper function to get the pattern (relative coordinates to color) from a shape
def get_pattern(grid: np.ndarray, shape: dict) -> dict:
    """
    Extracts the color pattern from a shape relative to its top-left corner.

    Args:
        grid: The numpy array representing the grid.
        shape: The shape dictionary (output from find_shapes).

    Returns:
        A dictionary mapping relative coordinates (dr, dc) to colors.
    """
    pattern = {}
    min_r, min_c = shape['top_left']
    for r, c in shape['pixels']:
        dr = r - min_r # Row difference from top-left
        dc = c - min_c # Column difference from top-left
        pattern[(dr, dc)] = grid[r, c]
    return pattern


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Transforms the input grid by applying the pattern of the first non-uniform
    shape found to all uniform shapes made of the color 5.
    """
    
    # Convert input list of lists to a NumPy array for efficient processing
    grid_np = np.array(input_grid, dtype=int)
    # Create a deep copy for the output grid to avoid modifying the input directly
    output_grid_np = copy.deepcopy(grid_np) 
    
    # Step 1 & 2: Find all shapes and their properties
    all_shapes = find_shapes(grid_np)

    # Step 3: Find the first non-uniform shape to use as the pattern source
    target_pattern_shape = None
    for shape in all_shapes:
        if not shape['is_uniform']:
            target_pattern_shape = shape
            break # Found the first one, stop searching

    # Handle the case where no non-uniform shape is found (optional, based on problem constraints)
    if target_pattern_shape is None:
        # If the problem guarantees a pattern shape, this won't be reached.
        # Otherwise, return the original grid or raise an error.
        return input_grid 

    # Step 4: Extract the color pattern from the target shape
    pattern_map = get_pattern(grid_np, target_pattern_shape)

    # Step 5: Identify all shapes to modify (uniform color 5)
    shapes_to_modify = []
    for shape in all_shapes:
        # Check if the shape is uniform and its only color is 5
        if shape['is_uniform'] and shape['colors'] == {5}:
            shapes_to_modify.append(shape)

    # Step 6 & 7: Apply the pattern to each identified '5' shape
    for shape in shapes_to_modify:
        shape_min_r, shape_min_c = shape['top_left']
        
        # Iterate through each pixel within the current '5' shape
        for r, c in shape['pixels']:
            # Calculate the pixel's relative coordinates within this shape
            dr = r - shape_min_r
            dc = c - shape_min_c
            
            # Find the corresponding color from the pattern using the relative coordinates
            # If the relative coordinate exists in the pattern map, apply the color
            if (dr, dc) in pattern_map:
                output_grid_np[r, c] = pattern_map[(dr, dc)]
            # Else: Implicitly, if a pixel in the shape doesn't have a corresponding
            # relative coordinate in the pattern (e.g., shapes have different relative extents),
            # its value remains unchanged in the output copy. Given the examples,
            # it seems the shapes are expected to map directly.

    # Step 8: Convert the final NumPy array back to a list of lists
    output_grid = output_grid_np.tolist()
    
    return output_grid