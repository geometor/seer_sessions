import numpy as np
from collections import Counter, deque

"""
Identifies the single non-background object in the input grid, which is composed of exactly two distinct non-background colors.
Creates a new grid based on the input grid.
Erases the original object from the new grid by replacing its pixels with the background color.
Creates a copy of the original object, but swaps its two constituent non-background colors.
Places this color-swapped copy onto the new grid such that its leftmost column is positioned one column to the right of the original object's rightmost column.
The vertical position remains unchanged. Pixels shifted outside the grid boundary are discarded.
"""

def find_background_color(grid):
    """Finds the most frequent color in the grid, assumed to be the background."""
    # Use Counter for efficiency
    counts = Counter(grid.flatten())
    # Handle empty grids
    if not counts:
        return 0 # Default background
    # Background is the most frequent color
    background_color = counts.most_common(1)[0][0]
    return background_color

def find_connected_object(grid, start_r, start_c, background_color, visited):
    """Finds all connected non-background pixels starting from (start_r, start_c) using BFS."""
    rows, cols = grid.shape
    # Use deque for efficient queue operations
    q = deque([(start_r, start_c)])
    object_coords = set()
    object_colors = set()

    # Check if starting point is valid and not background
    if not (0 <= start_r < rows and 0 <= start_c < cols) or grid[start_r, start_c] == background_color:
        return object_coords, object_colors # Return empty sets if start is invalid or background

    while q:
        r, c = q.popleft() # Use popleft for BFS

        # Boundary and visited checks
        if not (0 <= r < rows and 0 <= c < cols) or (r, c) in visited:
            continue

        pixel_color = grid[r, c]
        # Check if current pixel is part of the object (not background)
        if pixel_color == background_color:
            continue

        # Mark as visited and add to object coordinates and colors
        visited.add((r, c))
        object_coords.add((r, c))
        object_colors.add(pixel_color)

        # Explore neighbors (4-connectivity: up, down, left, right)
        for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
            nr, nc = r + dr, c + dc
            # Add valid, unvisited neighbors that are not background to the queue
            if 0 <= nr < rows and 0 <= nc < cols and (nr, nc) not in visited and grid[nr, nc] != background_color:
                 q.append((nr, nc))

    return object_coords, object_colors


def find_the_object(grid, background_color):
    """Finds the single non-background object and its constituent colors in the grid."""
    rows, cols = grid.shape
    visited = set()
    # Iterate through grid to find the first non-background pixel
    for r in range(rows):
        for c in range(cols):
            if grid[r, c] != background_color and (r, c) not in visited:
                # Found the start of an object, find all connected parts and colors
                object_coords, object_colors = find_connected_object(grid, r, c, background_color, visited)
                # Assuming only one object per task description
                if object_coords:
                    return object_coords, object_colors
    # Return None if no non-background object is found
    return None, None


def get_object_bounding_box(object_coords):
    """Calculates bounding box of the object."""
    if not object_coords:
        return None, None, None, None

    # Extract row and column coordinates
    rows = [r for r, c in object_coords]
    cols = [c for r, c in object_coords]

    # Calculate bounding box limits
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)

    return min_row, max_row, min_col, max_col


def transform(input_grid):
    """
    Applies the transformation rule: find object, identify its two colors,
    erase original, place a color-swapped copy immediately to the right.
    """
    # Convert input list of lists to a NumPy array for efficient manipulation
    grid = np.array(input_grid, dtype=int)
    rows, cols = grid.shape

    # 1. Determine the background color
    background_color = find_background_color(grid)

    # 2. Identify the single connected object, its pixels, and its colors
    object_coords, object_colors = find_the_object(grid, background_color)

    # If no object is found (e.g., grid is all background), return the original grid
    if not object_coords:
        return input_grid # Return original as list of lists

    # 3. Identify the two distinct non-background colors and create swap map
    non_background_colors = list(object_colors)
    if len(non_background_colors) != 2:
        # According to the examples, there should always be exactly two.
        # If not, maybe return original or raise error. Returning original for now.
        print(f"Warning: Expected 2 object colors, found {len(non_background_colors)}. Returning original.")
        return input_grid

    color1, color2 = non_background_colors[0], non_background_colors[1]
    color_swap_map = {color1: color2, color2: color1}

    # 4. Calculate the bounding box of the original object
    min_row, max_row, min_col, max_col = get_object_bounding_box(object_coords)

    # 5. Calculate the horizontal shift amount
    # The new copy's minimum column (left edge) should be one column past the original's maximum column
    new_copy_min_col = max_col + 1
    # The shift amount is the difference between the new start column and the original start column
    horizontal_shift = new_copy_min_col - min_col

    # 6. Create a new output grid, initially identical to the input grid
    output_grid = np.copy(grid)

    # 7. Erase the original object from the output grid
    for r, c in object_coords:
        output_grid[r, c] = background_color

    # 8. Create the transformed (color-swapped) copy
    for r, c in object_coords:
        # 8a. Get the original color of this pixel from the input grid
        original_color = grid[r, c]
        # 8b. Use the color mapping to find the corresponding swapped color
        swapped_color = color_swap_map[original_color]
        # 8c. Calculate the destination coordinates
        dest_r, dest_c = r, c + horizontal_shift
        # 8d. If the destination coordinates are within bounds, update the output grid
        if 0 <= dest_r < rows and 0 <= dest_c < cols:
            output_grid[dest_r, dest_c] = swapped_color
        # else: Pixel shifted off-grid is discarded

    # 9. Return the modified output grid as a list of lists
    return output_grid.tolist()