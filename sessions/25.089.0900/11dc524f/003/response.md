```python
import numpy as np

"""
Identifies a mobile red object (color 2) and a static gray target object (color 5) against an orange background (color 7).
The red object is moved iteratively one step at a time towards the gray object.
The direction of movement in each step is determined by the axis (vertical 'y' or horizontal 'x') corresponding to the largest absolute difference between the objects' bounding box centers. Vertical movement is prioritized if the absolute differences are equal.
The movement stops when any pixel of the red object becomes adjacent (horizontally, vertically, or diagonally) to any pixel of the gray object.
The shape of the red object is preserved throughout the movement. The gray object and the background remain unchanged.
"""

def find_object_pixels(grid, color):
    """Finds all (row, col) coordinates of pixels with the given color."""
    rows, cols = np.where(grid == color)
    # Return as a list of tuples, which is easier to work with than two separate arrays
    return list(zip(rows, cols))

def get_bounding_box_center(coords):
    """Calculates the geometric center of the bounding box for a set of coordinates."""
    if not coords:
        return None
    # Unzip the list of tuples into separate lists/tuples of rows and columns
    rows, cols = zip(*coords)
    min_row, max_row = min(rows), max(rows)
    min_col, max_col = min(cols), max(cols)
    # Calculate center using floating point division
    center_row = (min_row + max_row) / 2.0
    center_col = (min_col + max_col) / 2.0
    return center_row, center_col

def is_adjacent(coords1, coords2):
    """Checks if any coordinate pair from coords1 is adjacent (including diagonals) to any pair in coords2."""
    if not coords1 or not coords2:
        return False
    # Convert lists of coordinates to sets for potentially faster lookups if needed,
    # although for small objects, iteration might be just as fast or faster.
    # Here, nested loops are clear and sufficient for typical ARC object sizes.
    for r1, c1 in coords1:
        for r2, c2 in coords2:
            # Check if the Chebyshev distance (max coordinate difference) is 1 or less.
            # <= 1 covers the pixel itself and its 8 neighbours.
            # Since we compare pixels from two *different* objects, distance 0 is impossible
            # unless they overlap, and distance 1 means adjacency.
            if max(abs(r1 - r2), abs(c1 - c2)) <= 1:
                return True
    return False

def transform(input_grid):
    """
    Moves the red object towards the gray object until they are adjacent.
    """
    # Define colors
    BACKGROUND_COLOR = 7
    MOBILE_COLOR = 2 # red
    TARGET_COLOR = 5 # gray

    # Create a copy of the input grid to modify
    output_grid = np.copy(input_grid)
    grid_height, grid_width = output_grid.shape

    # Locate the objects
    current_mobile_coords = find_object_pixels(output_grid, MOBILE_COLOR)
    target_coords = find_object_pixels(output_grid, TARGET_COLOR)

    # If either object is missing, return the original grid
    if not current_mobile_coords or not target_coords:
        return output_grid

    # Set a maximum number of iterations to prevent potential infinite loops
    max_iterations = grid_height * grid_width # A safe upper bound

    for iteration in range(max_iterations):
        # --- Check Stopping Condition ---
        if is_adjacent(current_mobile_coords, target_coords):
            # Objects are adjacent, movement stops, return current grid state
            break

        # --- Calculate Movement Direction ---
        mobile_center = get_bounding_box_center(current_mobile_coords)
        target_center = get_bounding_box_center(target_coords)

        # This check should technically not be needed if objects were found initially, but good for robustness
        if mobile_center is None or target_center is None:
             break # Should not happen

        # Calculate vector from mobile center to target center
        delta_row = target_center[0] - mobile_center[0]
        delta_col = target_center[1] - mobile_center[1]

        # Determine step direction (dr, dc)
        dr, dc = 0, 0
        # Prioritize movement along the axis with the largest absolute difference
        # If differences are equal, prioritize vertical movement (row change)
        if abs(delta_row) >= abs(delta_col):
            if abs(delta_row) > 1e-6: # Add tolerance for float comparison
               dr = int(np.sign(delta_row))
            elif abs(delta_col) > 1e-6: # If row diff is effectively zero, try col
               dc = int(np.sign(delta_col))
            # If both are zero (centers coincide), dr=0, dc=0 -> no move
        else: # abs(delta_col) > abs(delta_row)
             if abs(delta_col) > 1e-6:
                dc = int(np.sign(delta_col))
             elif abs(delta_row) > 1e-6: # If col diff is effectively zero, try row
                dr = int(np.sign(delta_row))
             # If both are zero, dr=0, dc=0 -> no move

        # If no move direction is determined (e.g., centers coincide perfectly but not adjacent)
        if dr == 0 and dc == 0:
             # This might indicate an issue or that the objects are aligned but not touching.
             # Since adjacency is checked first, this state implies no further valid move exists
             # according to the center-based rule. Stop iteration.
             break

        # --- Apply Movement ---

        # 1. Calculate the potential next coordinates
        next_mobile_coords = []
        valid_move = True
        for r, c in current_mobile_coords:
            nr, nc = r + dr, c + dc
            # Check grid boundaries
            if 0 <= nr < grid_height and 0 <= nc < grid_width:
                # Check for overlap with the *static* target object
                if output_grid[nr, nc] == TARGET_COLOR:
                    # This move would cause an overlap. Since we stop at adjacency,
                    # this state shouldn't be reached if the logic is correct.
                    # Stop movement *before* this overlap occurs.
                    valid_move = False
                    # print("Warning: Preventing move that would overlap target.")
                    break # Break inner loop (coordinate calculation)
                next_mobile_coords.append((nr, nc))
            else:
                # Move goes out of bounds
                valid_move = False
                # print("Warning: Preventing move out of bounds.")
                break # Break inner loop (coordinate calculation)

        # If the move was deemed invalid (out of bounds or overlap), stop the entire process.
        if not valid_move:
            break # Break outer loop (iterations)

        # 2. Erase the mobile object from its old position
        for r, c in current_mobile_coords:
            # Only erase if it wasn't part of the target (shouldn't happen, but safety)
            if output_grid[r, c] == MOBILE_COLOR:
                output_grid[r, c] = BACKGROUND_COLOR

        # 3. Draw the mobile object at its new position
        for nr, nc in next_mobile_coords:
            output_grid[nr, nc] = MOBILE_COLOR

        # 4. Update the coordinates for the next iteration
        current_mobile_coords = next_mobile_coords

    # Return the final state of the grid
    return output_grid
```