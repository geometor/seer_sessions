import numpy as np
from collections import deque, Counter
import sys

# Increase recursion depth for deep object searches if needed, though BFS is usually fine.
# sys.setrecursionlimit(2000) 

"""
Identify the background color as the most frequent color in the input grid.
Find connected components (objects) of non-background pixels using 8-connectivity (including diagonals).
For each object, check if it contains both azure (8) pixels and at least one yellow (4) pixel. These are 'target objects'.
If an object is a target object:
  Find the location (specifically the column index) of *any* yellow (4) pixel within it. Use the first one found during traversal as the 'anchor pixel'.
  Determine the grid's vertical midpoint column index (width // 2). Integer division is used.
  If the anchor pixel's column index is strictly less than the midpoint column index, the entire object is shifted 3 columns to the right (+3).
  If the anchor pixel's column index is greater than or equal to the midpoint column index, the entire object is shifted 3 columns to the left (-3).
Pixels shifted outside the grid boundaries are discarded.
All other objects (those not containing both azure and yellow) and the background pixels remain in their original positions.
The output grid is constructed by placing the shifted target objects and the unchanged non-target objects onto a grid initialized with the background color.
"""

def find_most_frequent_color(grid_np):
    """
    Determines the most frequent color in the grid.

    Args:
        grid_np (np.array): The input grid as a NumPy array.

    Returns:
        int: The color value that appears most frequently.
    """
    # Handle empty or invalid input gracefully, though ARC constraints usually prevent this.
    if grid_np.size == 0:
        return 0 # Default to white/0 if grid is empty

    counts = Counter(grid_np.flatten())
    # most_common(1) returns a list of tuples [(color, count)], so we extract the color.
    most_common_color = counts.most_common(1)[0][0]
    return int(most_common_color) # Ensure it's an int


def find_objects(grid_np, background_color):
    """
    Finds connected objects of non-background pixels using BFS and 8-connectivity.

    Args:
        grid_np (np.array): The input grid.
        background_color (int): The color considered as background.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'pixels' (list of (r, c, color)), 'has_azure',
              'has_yellow', and 'yellow_loc' (first found (r, c) tuple).
              Returns an empty list if no non-background objects are found.
    """
    height, width = grid_np.shape
    visited = np.zeros_like(grid_np, dtype=bool)
    all_objects = []

    for r in range(height):
        for c in range(width):
            # If this pixel is background or already visited, skip
            if grid_np[r, c] == background_color or visited[r, c]:
                continue

            # Start BFS for a new object
            current_object_pixels = []
            q = deque([(r, c)])
            visited[r, c] = True
            has_azure = False
            has_yellow = False
            yellow_pixel_loc = None # Store the first yellow pixel found (r, c)

            while q:
                row, col = q.popleft()
                color = grid_np[row, col]
                current_object_pixels.append((row, col, color))

                # Check object properties
                if color == 8: # azure
                    has_azure = True
                if color == 4: # yellow
                    has_yellow = True
                    if yellow_pixel_loc is None: # Store only the first one encountered
                         yellow_pixel_loc = (row, col)

                # Explore neighbors (8-connectivity: includes diagonals)
                for dr in [-1, 0, 1]:
                    for dc in [-1, 0, 1]:
                        if dr == 0 and dc == 0:
                            continue
                        nr, nc = row + dr, col + dc

                        # Check bounds and if neighbor is part of the object (non-background and not visited)
                        if 0 <= nr < height and 0 <= nc < width and \
                           grid_np[nr, nc] != background_color and \
                           not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))

            # Store the found object and its properties if it contains any pixels
            if current_object_pixels:
                 all_objects.append({
                     "pixels": current_object_pixels,
                     "has_azure": has_azure,
                     "has_yellow": has_yellow,
                     "yellow_loc": yellow_pixel_loc
                 })

    return all_objects


def transform(input_grid):
    """
    Transforms the input grid based on shifting rules applied to specific objects.
    Objects containing both azure (8) and yellow (4) pixels are shifted horizontally
    based on the column of a yellow pixel relative to the grid's vertical midpoint.
    The background color is determined dynamically as the most frequent color.
    """
    # Convert input to numpy array for efficient operations
    input_np = np.array(input_grid, dtype=int)
    height, width = input_np.shape

    # Determine the background color dynamically
    background_color = find_most_frequent_color(input_np)

    # Determine midpoint column and shift amount
    midpoint_col = width // 2
    shift_amount = 3

    # Initialize output grid with the determined background color
    output_np = np.full_like(input_np, background_color)

    # Find all connected objects of non-background colors
    objects = find_objects(input_np, background_color)

    # Process each found object
    for obj_data in objects:
        obj_pixels = obj_data["pixels"]
        # Check if the object is a 'target object' (contains both azure and yellow)
        is_target_object = obj_data["has_azure"] and obj_data["has_yellow"]

        if is_target_object and obj_data["yellow_loc"] is not None:
            # This is a target object, determine shift based on the first yellow pixel found
            _ , anchor_col = obj_data["yellow_loc"] # Get column of the yellow anchor pixel

            # Determine shift direction based on anchor column relative to midpoint
            if anchor_col < midpoint_col:
                shift = shift_amount # Shift right
            else:
                shift = -shift_amount # Shift left

            # Apply shift to each pixel in the object and draw it on the output grid
            for r, c, color in obj_pixels:
                new_c = c + shift
                # Draw the pixel only if the new column is within the grid bounds
                if 0 <= new_c < width:
                     # Check row bounds too, although they don't change
                     if 0 <= r < height:
                        output_np[r, new_c] = color
        else:
            # This is not a target object (or somehow a target object without a yellow pixel - shouldn't happen based on logic),
            # draw it in its original position
            for r, c, color in obj_pixels:
                 # Basic bounds check (should always be true for original positions)
                 if 0 <= r < height and 0 <= c < width:
                    output_np[r, c] = color

    # Convert the result back to a standard list of lists format
    return output_np.tolist()