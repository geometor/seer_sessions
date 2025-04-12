import numpy as np

"""
Identifies a solid red (2) line (row or column) acting as a boundary.
All other non-white (0) objects are shifted towards this boundary.
The shifting continues until an object reaches the cell adjacent to the boundary 
or the cell adjacent to another object that has already been shifted and settled.
The space vacated by the shifted objects becomes white (0).
The red boundary itself remains static.
"""

def find_boundary(grid: np.ndarray) -> tuple[str | None, int | None]:
    """
    Finds a solid red line (row or column).

    Args:
        grid: The input grid as a numpy array.

    Returns:
        A tuple (orientation, index) where orientation is 'row' or 'col',
        and index is the row/column index. Returns (None, None) if no boundary found.
    """
    height, width = grid.shape
    red_color = 2

    # Check rows
    for r in range(height):
        if np.all(grid[r, :] == red_color):
            return 'row', r

    # Check columns
    for c in range(width):
        if np.all(grid[:, c] == red_color):
            return 'col', c

    return None, None

def determine_direction(orientation: str, index: int, height: int, width: int) -> tuple[int, int] | None:
    """
    Determines the direction vector (dr, dc) towards the boundary.

    Args:
        orientation: 'row' or 'col'.
        index: The index of the boundary row/column.
        height: Grid height.
        width: Grid width.

    Returns:
        A tuple (dr, dc) representing the movement direction (e.g., (-1, 0) for up),
        or None if orientation is invalid.
    """
    if orientation == 'row':
        if index == 0:  # Top boundary, move up
            return (-1, 0)
        elif index == height - 1: # Bottom boundary, move down
            return (1, 0)
    elif orientation == 'col':
        if index == 0:  # Left boundary, move left
            return (0, -1)
        elif index == width - 1: # Right boundary, move right
            return (0, 1)
    # Should not happen with valid boundaries, but good practice
    return None # Or perhaps default to down (1, 0)? Example 1 has bottom row implicit boundary? No, the red is explicit.


def transform(input_grid: list[list[int]]) -> list[list[int]]:
    """
    Shifts non-white, non-red objects towards a solid red boundary line until
    they hit the boundary or another settled object.
    """
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    white_color = 0
    red_color = 2

    # Find the boundary
    orientation, boundary_index = find_boundary(input_np)

    if orientation is None:
        # Handle cases where no boundary is found (though examples suggest one always exists)
        # Maybe return input unchanged or raise an error? Returning unchanged for now.
        return input_grid

    # Determine movement direction
    dr, dc = determine_direction(orientation, boundary_index, height, width)

    # Initialize output grid with white
    output_np = np.full_like(input_np, white_color)

    # Copy the boundary to the output grid
    if orientation == 'row':
        output_np[boundary_index, :] = red_color
    else: # orientation == 'col'
        output_np[:, boundary_index] = red_color

    # Determine iteration order based on direction to process objects closer to the boundary first
    rows = range(height)
    cols = range(width)

    if dr > 0: # Moving down
        rows = range(height - 1, -1, -1)
    elif dr < 0: # Moving up
        rows = range(height) # Default order is fine
    
    if dc > 0: # Moving right
        cols = range(width - 1, -1, -1)
    elif dc < 0: # Moving left
        cols = range(width) # Default order is fine

    # Iterate through input grid cells based on calculated order
    for r in rows:
        for c in cols:
            color = input_np[r, c]

            # Skip background, boundary, and already processed parts of the output grid
            if color == white_color or color == red_color:
                continue

            # This pixel belongs to a movable object
            current_r, current_c = r, c

            # Simulate movement step-by-step until collision
            while True:
                next_r, next_c = current_r + dr, current_c + dc

                # Check boundary conditions
                if not (0 <= next_r < height and 0 <= next_c < width):
                    break # Hit grid edge (shouldn't happen before hitting boundary)

                # Check collision with boundary or already settled object in output
                if output_np[next_r, next_c] != white_color:
                     break # Hit boundary or another object

                # Move is valid, update current position
                current_r, current_c = next_r, next_c

            # Place the object's color at the final settled position
            output_np[current_r, current_c] = color

    # Convert back to list of lists
    output_grid = output_np.tolist()
    return output_grid