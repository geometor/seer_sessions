import numpy as np
from collections import deque

"""
Transformation Rule:
1. Identify a solid boundary line (row or column) of red (2) pixels. This line determines the direction of movement for other objects (towards the boundary).
2. Identify all distinct contiguous objects composed of colors other than white (0) or red (2).
3. Sort these objects based on their proximity to the boundary in the direction of movement (objects closer to the boundary are processed first).
4. Initialize an output grid of the same dimensions as the input, filled with white (0), and place the red boundary line onto it.
5. Process the sorted objects one by one:
   a. Simulate moving the entire object as a single unit, one step at a time, in the determined direction.
   b. Movement stops when *any* part of the object would collide with the grid edges, the red boundary, or any part of an object already placed on the output grid.
   c. Place the object onto the output grid at its final resting position.
6. Return the completed output grid.
"""

def find_boundary_and_direction(grid: np.ndarray) -> tuple[str | None, int | None, tuple[int, int] | None]:
    """
    Finds a solid red line (row or column) and determines the movement direction towards it.

    Args:
        grid: The input grid as a numpy array.

    Returns:
        A tuple (orientation, index, direction), where orientation is 'row' or 'col',
        index is the row/column index, and direction is a tuple (dr, dc).
        Returns (None, None, None) if no boundary found.
    """
    height, width = grid.shape
    red_color = 2
    direction = None

    # Check rows
    for r in range(height):
        if np.all(grid[r, :] == red_color):
            orientation = 'row'
            index = r
            if index == 0:  # Top boundary, move up
                direction = (-1, 0)
            elif index == height - 1: # Bottom boundary, move down
                direction = (1, 0)
            # Consider edge case where boundary might not be at edge, though examples don't show this.
            # If needed, determine direction based on centroid distance or similar.
            # For now, assume boundary is always at an edge determining direction.
            if direction: return orientation, index, direction


    # Check columns
    for c in range(width):
        if np.all(grid[:, c] == red_color):
            orientation = 'col'
            index = c
            if index == 0:  # Left boundary, move left
                direction = (0, -1)
            elif index == width - 1: # Right boundary, move right
                direction = (0, 1)
            if direction: return orientation, index, direction

    # Fallback if boundary isn't at an edge (not expected based on examples)
    # or if no boundary is found
    return None, None, None


def get_objects(grid: np.ndarray, background_color: int, boundary_color: int) -> list[tuple[int, list[tuple[int, int]]]]:
    """
    Finds all contiguous objects of colors other than background or boundary.

    Args:
        grid: The input grid as a numpy array.
        background_color: The color to ignore (usually white 0).
        boundary_color: The boundary color to ignore (usually red 2).

    Returns:
        A list of objects, where each object is a tuple: (color, list_of_pixel_coords).
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            color = grid[r, c]
            if color != background_color and color != boundary_color and not visited[r, c]:
                obj_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                current_color = color # Record the color of the object being explored

                while q:
                    row, col = q.popleft()
                    obj_pixels.append((row, col))

                    # Explore neighbors (4-connectivity)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        if 0 <= nr < height and 0 <= nc < width and \
                           not visited[nr, nc] and grid[nr, nc] == current_color:
                            visited[nr, nc] = True
                            q.append((nr, nc))

                if obj_pixels: # Should always be true if we entered the loop
                    objects.append((current_color, obj_pixels))
    return objects

def sort_objects(objects: list[tuple[int, list[tuple[int, int]]]], direction: tuple[int, int]) -> list[tuple[int, list[tuple[int, int]]]]:
    """Sorts objects based on proximity to the boundary in the direction of movement."""
    dr, dc = direction

    def sort_key(obj):
        color, pixels = obj
        if dr > 0: # Moving down
            return max(r for r, c in pixels)
        elif dr < 0: # Moving up
            return min(r for r, c in pixels)
        elif dc > 0: # Moving right
            return max(c for r, c in pixels)
        elif dc < 0: # Moving left
            return min(c for r, c in pixels)
        else: # No movement (should not happen with valid direction)
            return 0

    # Determine reverse sort based on direction
    # Move towards higher index (down/right) -> process higher indices first (reverse=True)
    # Move towards lower index (up/left) -> process lower indices first (reverse=False)
    reverse_sort = (dr > 0 or dc > 0)

    return sorted(objects, key=sort_key, reverse=reverse_sort)


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Shifts non-white, non-red objects towards a solid red boundary line
    until they collide with the boundary or another settled object.
    Objects move as whole units and maintain their shape.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    white_color = 0
    red_color = 2

    # 1. Identify Boundary and Direction
    orientation, boundary_index, direction = find_boundary_and_direction(input_np)

    if direction is None:
        # If no boundary or direction found (unexpected based on examples), return original grid.
        # Or potentially raise an error depending on requirements.
        return input_grid

    dr, dc = direction

    # 2. Identify Objects
    objects = get_objects(input_np, white_color, red_color)

    # 3. Sort Objects
    sorted_objects = sort_objects(objects, direction)

    # 4. Initialize Output Grid and Place Boundary
    output_np = np.full_like(input_np, white_color)
    if orientation == 'row':
        output_np[boundary_index, :] = red_color
    else: # orientation == 'col'
        output_np[:, boundary_index] = red_color

    # 5. Process Sorted Objects
    for color, initial_pixels in sorted_objects:
        current_pixels = list(initial_pixels) # Copy to modify

        # 5a. Simulate movement
        while True:
            can_move = True
            next_pixels = []
            for r, c in current_pixels:
                next_r, next_c = r + dr, c + dc

                # 5b. Check for collisions (boundary, grid edge, other objects)
                if not (0 <= next_r < height and 0 <= next_c < width):
                    can_move = False # Hit grid edge (should be stopped by boundary first ideally)
                    break
                if output_np[next_r, next_c] != white_color:
                    can_move = False # Hit boundary or already settled object
                    break
                next_pixels.append((next_r, next_c))

            if can_move:
                # If all pixels can move, update current position
                current_pixels = next_pixels
            else:
                # If any pixel cannot move, the whole object stops
                break

        # 5c. Place the object onto the output grid at its final position
        for r, c in current_pixels:
            # Sanity check for bounds, though collision logic should prevent out of bounds
            if 0 <= r < height and 0 <= c < width:
                 output_np[r, c] = color
            # else:
                # Optional: Log or handle unexpected out-of-bounds placement
                # print(f"Warning: Attempted to place pixel out of bounds at ({r}, {c})")


    # 6. Return the completed output grid
    output_grid = output_np.tolist()
    return output_grid