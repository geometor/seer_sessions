import numpy as np
from collections import deque

# Define constants for background and border colors
BACKGROUND_COLOR = 7
BORDER_COLOR = 8

def find_objects(grid):
    """
    Finds all distinct contiguous objects in the grid.
    An object is a group of connected pixels (8-way connectivity)
    of the same color, excluding background (7) and border (8).

    Args:
        grid (np.array): The input grid.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'color' (int) and 'pixels' (list of tuples (r, c)).
    """
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []
    
    # Iterate through the grid, excluding the border row
    for r in range(height - 1): # Exclude last row (border)
        for c in range(width):
            color = grid[r, c]
            # Check if it's a potential object pixel and not visited
            if color != BACKGROUND_COLOR and color != BORDER_COLOR and not visited[r, c]:
                current_object_pixels = []
                q = deque([(r, c)])
                visited[r, c] = True
                object_color = color

                while q:
                    curr_r, curr_c = q.popleft()
                    current_object_pixels.append((curr_r, curr_c))

                    # Check 8 neighbors (Moore neighborhood)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue # Skip self

                            nr, nc = curr_r + dr, curr_c + dc

                            # Check bounds (importantly, exclude border row nr == height - 1)
                            if 0 <= nr < height - 1 and 0 <= nc < width:
                                # Check if neighbor has the same color and not visited
                                if grid[nr, nc] == object_color and not visited[nr, nc]:
                                    visited[nr, nc] = True
                                    q.append((nr, nc))
                                    
                if current_object_pixels:
                     objects.append({'color': object_color, 'pixels': current_object_pixels})

    return objects


def transform(input_grid):
    """
    Transforms the input grid by moving objects upwards based on their size.

    1. Identifies all distinct contiguous objects (non-background, non-border color).
    2. Calculates the size (number of pixels) P for each object.
    3. Erases the original objects from a copy of the grid.
    4. Draws the objects in their new positions, shifted upwards by P rows.
    The background (Orange, 7) and bottom border (Azure, 8) remain unchanged.
    """
    
    # Convert input list of lists to numpy array for easier manipulation
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape
    
    # Initialize output_grid as a copy of the input grid
    output_grid = np.copy(input_np)

    # Find all objects in the input grid
    objects = find_objects(input_np)

    # Step 1: Erase original objects from the output grid
    # Iterate through each found object
    for obj in objects:
        # Iterate through the pixels of the current object
        for r, c in obj['pixels']:
            # Set the corresponding pixel in the output grid to background color
            output_grid[r, c] = BACKGROUND_COLOR

    # Step 2: Draw objects in their new positions
    # Iterate through each found object again
    for obj in objects:
        obj_color = obj['color']
        obj_pixels = obj['pixels']
        # Calculate the size (number of pixels) P
        size_p = len(obj_pixels)
        # Calculate the upward shift amount S = P
        shift_s = size_p

        # Iterate through the original pixels of the object
        for r, c in obj_pixels:
            # Calculate the new row position
            new_r = r - shift_s
            new_c = c # Column remains the same

            # Check if the new position is within the grid bounds (non-negative row)
            if new_r >= 0:
                # Set the pixel at the new coordinate in the output grid to the object's color
                output_grid[new_r, new_c] = obj_color

    # Convert the result back to a list of lists
    return output_grid.tolist()