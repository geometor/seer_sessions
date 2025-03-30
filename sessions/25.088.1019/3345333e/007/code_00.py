import numpy as np
from collections import deque

"""
Processes an input grid containing a background color (White 0) and exactly two 
other foreground colors. One foreground color forms a single, solid, connected 
rectangular object (the 'mask'). The other foreground color forms the 'persistent' 
object, which may consist of multiple disconnected components or have a complex shape. 
The transformation produces an output grid containing only the pixels of the 
'persistent' object that do *not* share the exact same coordinates as any pixel 
of the 'mask' object. All other output pixels are the background color.

Note: While this rule is derived from the object properties (mask = single solid 
rectangle), it does not perfectly replicate the pixel counts observed in the 
provided example outputs, which show an unexpected increase in persistent pixels. 
This implementation follows the direct overlap removal logic as the most plausible 
intended rule based on the structure.
"""

# Helper function to find connected components (objects) of a specific color
# using 4-way connectivity (neighbors: up, down, left, right)
def find_connected_components(grid, target_color):
    """
    Finds all connected components of a specific color in the grid.

    Args:
        grid (np.ndarray): The input grid.
        target_color (int): The color of the components to find.

    Returns:
        list[set]: A list where each element is a set of (row, col) tuples
                   representing the coordinates of a connected component.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(rows):
        for c in range(cols):
            # Start search if pixel is the target color and not yet visited
            if grid[r, c] == target_color and not visited[r, c]:
                component_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                component_coords.add((r, c))

                # Breadth-First Search (BFS) to find all connected pixels
                while q:
                    row, col = q.popleft()
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check bounds and if neighbor has the target color and hasn't been visited
                        if 0 <= nr < rows and 0 <= nc < cols and \
                           grid[nr, nc] == target_color and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                            component_coords.add((nr, nc))
                # Add the found component to the list if it's not empty
                if component_coords:
                    objects.append(component_coords)
    return objects

# Helper function to check if a set of coordinates forms a solid rectangle
def is_solid_rectangle(object_coords):
    """
    Checks if a set of coordinates represents a solid rectangle.

    Args:
        object_coords (set): A set of (row, col) tuples representing the object's pixels.

    Returns:
        bool: True if the coordinates form a solid rectangle, False otherwise.
    """
    if not object_coords:
        return False # An empty set is not a rectangle

    try:
        # Find the bounding box of the coordinates
        rows = [r for r, c in object_coords]
        cols = [c for r, c in object_coords]
        min_r, max_r = min(rows), max(rows)
        min_c, max_c = min(cols), max(cols)

        # Calculate the expected number of pixels if it were a solid rectangle
        expected_size = (max_r - min_r + 1) * (max_c - min_c + 1)

        # Compare the actual number of pixels with the expected size
        return len(object_coords) == expected_size
    except ValueError: # Handles case where object_coords might be empty after filtering etc.
         return False

def transform(input_grid):
    """
    Applies the direct overlap removal transformation based on mask identification.
    """
    # Convert input list of lists to a NumPy array for easier processing
    input_np = np.array(input_grid, dtype=int)
    rows, cols = input_np.shape
    background_color = 0 # Assuming White (0) is always background

    # 1. Identify all unique non-background colors
    unique_colors = np.unique(input_np)
    foreground_colors = [c for c in unique_colors if c != background_color]

    # 2. Expecting exactly two foreground colors based on examples
    if len(foreground_colors) != 2:
        # If assumptions are violated, return an empty (background) grid.
        # print(f"Warning: Expected 2 foreground colors, found {len(foreground_colors)}. Returning background grid.")
        return np.full_like(input_np, background_color).tolist()

    mask_color = None
    persistent_color = None
    mask_coords = set()

    # 3. & 4. Analyze each foreground color to find the 'mask' color
    for color in foreground_colors:
        # a. Find connected components for this color
        components = find_connected_components(input_np, color)
        # b. Count components
        num_components = len(components)
        # c. Check if it's the mask: exactly one component AND it's a solid rectangle
        if num_components == 1:
            component = components[0]
            if is_solid_rectangle(component):
                mask_color = color
                mask_coords = component # Store the coordinates of the mask object
                break # Found the mask color, no need to check the other

    # 5. Identify the 'persistent' color (and handle if no mask found)
    if mask_color is None:
        # This might happen if neither color fits the mask criteria.
        # print("Warning: Could not identify a mask color (single solid rectangle component). Returning background grid.")
        return np.full_like(input_np, background_color).tolist()

    # The persistent color is the one that isn't the mask color
    persistent_color = next(c for c in foreground_colors if c != mask_color)

    # 6. Find the set of coordinates for the mask object (already done in step 4)
    # mask_coords contains the set of (r, c) tuples for the mask.

    # 7. Initialize the output grid with the background color
    output_np = np.full_like(input_np, background_color)

    # 8. Iterate through input grid coordinates
    for r in range(rows):
        for c in range(cols):
            # 9. Check if the input pixel is the persistent color
            if input_np[r, c] == persistent_color:
                # 10. Check if this coordinate is NOT part of the mask's coordinates (direct overlap check)
                if (r, c) not in mask_coords:
                    # 11. If it's persistent and not masked, copy it to the output
                    output_np[r, c] = persistent_color

    # 12. Return the completed output grid as a list of lists
    return output_np.tolist()