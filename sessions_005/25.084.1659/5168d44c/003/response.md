```python
import numpy as np
from typing import List, Tuple, Optional

"""
Identifies a 3x3 'Red Cross' object (red border, green center) and other isolated 'Green Dots' in the input grid.
Calculates the average position of the Green Dots relative to the Red Cross center.
Determines a primary movement direction (Up, Down, Left, Right) based on the larger absolute difference between the average dot position and the cross center (row or column).
Calculates the target position by moving the Red Cross center 2 steps in the determined direction.
If the target 3x3 area for the Red Cross is fully within the grid boundaries:
  - Clears the red border pixels (value 2) of the original Red Cross position to white (0), leaving the original green center pixel (value 3) untouched.
  - Draws the complete 3x3 Red Cross pattern at the target position, overwriting any existing pixels.
If no Red Cross is found, no Green Dots are found, the average dot position is equidistant in row and column from the cross center, or the target position is outside the grid boundaries, the grid remains unchanged.
Green Dots themselves never move.
"""

def find_red_cross(grid: np.ndarray) -> Optional[Tuple[int, int]]:
    """
    Finds the center coordinates of the 3x3 Red Cross object.

    Args:
        grid: The input grid as a numpy array.

    Returns:
        A tuple (row, col) of the center coordinates, or None if not found.
    """
    height, width = grid.shape
    for r in range(height - 2):
        for c in range(width - 2):
            # Check center pixel first (must be green)
            if grid[r + 1, c + 1] == 3:
                # Check border pixels (must be red)
                is_cross = True
                for i in range(3):
                    for j in range(3):
                        if i == 1 and j == 1: # Skip center
                            continue
                        if grid[r + i, c + j] != 2:
                            is_cross = False
                            break
                    if not is_cross:
                        break
                if is_cross:
                    return (r + 1, c + 1) # Return center coordinates
    return None

def find_green_dots(grid: np.ndarray, cross_center: Optional[Tuple[int, int]]) -> List[Tuple[int, int]]:
    """
    Finds the coordinates of all green dots, excluding the cross center if found.

    Args:
        grid: The input grid as a numpy array.
        cross_center: The coordinates of the red cross center, if found.

    Returns:
        A list of (row, col) tuples for each green dot found.
    """
    green_dots = []
    height, width = grid.shape
    for r in range(height):
        for c in range(width):
            if grid[r, c] == 3:
                # Exclude the cross center if it exists and matches current position
                if cross_center is None or (r, c) != cross_center:
                    green_dots.append((r, c))
    return green_dots

def transform(input_grid: List[List[int]]) -> List[List[int]]:
    """
    Applies the transformation rule to the input grid.

    Args:
        input_grid: The input grid as a list of lists.

    Returns:
        The transformed output grid as a list of lists.
    """
    # Convert input to numpy array for easier manipulation
    grid = np.array(input_grid, dtype=int)
    output_grid = grid.copy() # Create a copy to modify
    height, width = grid.shape

    # 1. Find the Red Cross object and its center
    cross_center = find_red_cross(grid)

    # If no Red Cross is found, return the original grid
    if cross_center is None:
        # print("No Red Cross found.")
        return input_grid

    # 2. Find all other Green Dots
    green_dots = find_green_dots(grid, cross_center)

    # 3. If there are no Green Dots, return the original grid
    if not green_dots:
        # print("No Green Dots found.")
        return input_grid

    # 4. Calculate the average position of Green Dots
    avg_row = sum(r for r, c in green_dots) / len(green_dots)
    avg_col = sum(c for r, c in green_dots) / len(green_dots)

    # 5. Calculate differences relative to the Red Cross center
    cross_r, cross_c = cross_center
    row_diff = avg_row - cross_r
    col_diff = avg_col - cross_c

    # 6. Determine movement direction and calculate movement vector (distance is 2)
    move_row, move_col = 0, 0
    move_distance = 2
    if abs(row_diff) > abs(col_diff):
        # Vertical movement is primary
        move_row = move_distance if row_diff > 0 else -move_distance
    elif abs(col_diff) > abs(row_diff):
        # Horizontal movement is primary
        move_col = move_distance if col_diff > 0 else -move_distance
    # Else (abs(row_diff) == abs(col_diff)), no movement -> move_row, move_col remain 0

    # 7. Check if movement is required
    if move_row == 0 and move_col == 0:
        # print("No movement required (equidistant or zero diff).")
        return input_grid # No movement, return original grid

    # 8. Calculate the potential new center and boundaries
    new_cross_r = cross_r + move_row
    new_cross_c = cross_c + move_col
    new_r_start = new_cross_r - 1
    new_c_start = new_cross_c - 1
    new_r_end = new_r_start + 3 # Exclusive end index for slicing
    new_c_end = new_c_start + 3 # Exclusive end index for slicing

    # 9. Boundary Check: Ensure the *entire* 3x3 new cross fits within the grid
    if (0 <= new_r_start and new_r_end <= height and
            0 <= new_c_start and new_c_end <= width):
        # print(f"Moving cross from {cross_center} to ({new_cross_r}, {new_cross_c})")

        # 10. Clear the *border* of the original Red Cross location
        orig_r_start = cross_r - 1
        orig_c_start = cross_c - 1
        for r_offset in range(3):
            for c_offset in range(3):
                # Skip the center pixel
                if r_offset == 1 and c_offset == 1:
                    continue
                # Clear only if it was a red border pixel
                if output_grid[orig_r_start + r_offset, orig_c_start + c_offset] == 2:
                     output_grid[orig_r_start + r_offset, orig_c_start + c_offset] = 0 # Set to white

        # 11. Draw the Red Cross at the new location (overwrite)
        cross_pattern = np.array([
            [2, 2, 2],
            [2, 3, 2],
            [2, 2, 2]
        ])
        output_grid[new_r_start:new_r_end, new_c_start:new_c_end] = cross_pattern

    else:
        # print(f"Skipping move: New position ({new_r_start}:{new_r_end}, {new_c_start}:{new_c_end}) out of bounds ({height}x{width}).")
        return input_grid # New position is invalid, return original grid


    # Convert the final numpy array back to a list of lists
    return output_grid.tolist()
```