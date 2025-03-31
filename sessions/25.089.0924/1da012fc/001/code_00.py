import numpy as np
from collections import Counter

"""
Identify the palette colors: these are non-white (0), non-gray (5) pixels that are adjacent (4-connectivity) to at least one gray (5) pixel.
Sort these palette colors by their position (top-to-bottom, then left-to-right) to get an ordered list of replacement colors.
Identify the target color: this is the most frequent color in the grid among pixels that are non-white (0), non-gray (5), and are *not* adjacent to any gray (5) pixel.
Identify target objects: find all distinct connected components (objects) made solely of the target color using 4-connectivity.
Sort these target objects based on the position of their top-most, then left-most pixel.
Create a copy of the input grid.
Map the sorted target objects to the sorted replacement colors in order. For the i-th target object, change the color of all its pixels in the copied grid to the i-th replacement color.
Return the modified grid.
"""

def find_objects(grid, color):
    """
    Finds all connected components (objects) of a specific color in the grid.
    Uses 4-connectivity (up, down, left, right).

    Args:
        grid (np.array): The input grid.
        color (int): The color of the objects to find.

    Returns:
        list: A list of sets, where each set contains the (row, col) tuples
              of the pixels belonging to a single connected object.
              Returns an empty list if the color is None or no objects are found.
    """
    if color is None: # Handle cases where no target color is identified
        return []
    height, width = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(height):
        for c in range(width):
            # If it's the right color and not yet visited, start a search (BFS)
            if grid[r, c] == color and not visited[r, c]:
                obj_coords = set()
                q = [(r, c)] # Queue for BFS
                visited[r, c] = True
                while q:
                    row, col = q.pop(0)
                    obj_coords.add((row, col))
                    # Check 4 neighbors (up, down, left, right)
                    for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                        nr, nc = row + dr, col + dc
                        # Check grid boundaries
                        if 0 <= nr < height and 0 <= nc < width:
                            # Check if neighbor has the target color and hasn't been visited
                            if grid[nr, nc] == color and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                # Add the found object coordinates set to the list of objects
                if obj_coords:
                    objects.append(obj_coords)
    return objects

def get_object_top_left(obj_coords):
    """
    Finds the top-most, then left-most coordinate of an object.
    This is used for sorting objects.

    Args:
        obj_coords (set): A set of (row, col) tuples representing the object.

    Returns:
        tuple: The (row, col) of the top-left pixel.
               Returns (infinity, infinity) for an empty set to ensure it sorts last.
    """
    if not obj_coords:
        # Should not happen with valid objects from find_objects
        return (float('inf'), float('inf'))
    # Find the minimum row index present in the object coordinates
    min_row = min(r for r, c in obj_coords)
    # Among pixels in that minimum row, find the minimum column index
    min_col = min(c for r, c in obj_coords if r == min_row)
    return (min_row, min_col)

def transform(input_grid):
    """
    Transforms the input grid by identifying palette colors near gray areas,
    identifying target objects not near gray areas, and recoloring the target
    objects using the palette colors based on sorted order.

    Args:
        input_grid (list of lists): The input grid represented as a list of lists of integers.

    Returns:
        list of lists: The transformed output grid.
    """
    grid = np.array(input_grid, dtype=int)
    output_grid = np.copy(grid) # Start with a copy to modify
    height, width = grid.shape

    # --- 1. Identify Palette Colors and their Positions ---
    # Palette colors are non-white(0), non-gray(5), and adjacent (4-connectivity) to gray(5).
    palette_colors_data = []
    # Create a boolean mask indicating pixels adjacent to gray
    is_near_gray = np.zeros_like(grid, dtype=bool)

    # Iterate through the grid to find gray pixels
    for r in range(height):
        for c in range(width):
            if grid[r, c] == 5: # If this pixel is gray
                # Check its 4 neighbors
                for dr, dc in [(0, 1), (0, -1), (1, 0), (-1, 0)]:
                    nr, nc = r + dr, c + dc
                    # If neighbor is within bounds, mark it as being near gray
                    if 0 <= nr < height and 0 <= nc < width:
                        is_near_gray[nr, nc] = True

    # Iterate again to find pixels matching palette color criteria
    for r in range(height):
        for c in range(width):
             color = grid[r,c]
             # Conditions: color is not white(0), not gray(5), AND it is near gray
             if color != 0 and color != 5 and is_near_gray[r,c]:
                 # Store the color and its position
                 palette_colors_data.append({'color': color, 'row': r, 'col': c})

    # Sort the identified palette colors: primarily by row, secondarily by column
    palette_colors_data.sort(key=lambda x: (x['row'], x['col']))
    # Extract just the color values in the sorted order
    replacement_colors = [p['color'] for p in palette_colors_data]

    # --- 2. Identify Target Color ---
    # Target color is the most frequent color that is:
    # Not white(0), Not gray(5), and NOT adjacent to gray.
    color_counts = Counter()
    for r in range(height):
        for c in range(width):
            color = grid[r,c]
            # Conditions: color is not white(0), not gray(5), AND it is NOT near gray
            if color != 0 and color != 5 and not is_near_gray[r,c]:
                 # Increment count for this color
                 color_counts[color] += 1

    # Determine the most frequent color among the candidates
    target_color = None
    if color_counts:
        # most_common(1) returns a list like [ (color, count) ], we need the color.
        target_color = color_counts.most_common(1)[0][0]

    # --- 3. Identify and Order Target Objects ---
    # Find all distinct connected objects composed of the identified target_color.
    # Pass the grid and the determined target_color to the helper function.
    target_objects_coords = find_objects(grid, target_color)

    # If no target objects were found (e.g., target_color was None or no objects exist),
    # return the unmodified grid.
    if not target_objects_coords:
        return output_grid.tolist()

    # Sort the list of target objects. The key for sorting is the
    # top-left coordinate of each object (obtained via get_object_top_left).
    target_objects_coords.sort(key=get_object_top_left)

    # --- 4. Apply Transformation ---
    # Check if the number of target objects matches the number of replacement colors found.
    # This is expected based on the examples. If not, print a warning.
    # The `zip` function will handle mismatches by stopping when the shorter list is exhausted.
    if len(target_objects_coords) != len(replacement_colors):
         # This warning helps in debugging if the assumption doesn't hold for new cases.
         print(f"Warning: Number of target objects ({len(target_objects_coords)}) "
               f"does not match number of palette colors ({len(replacement_colors)}).")

    # Pair up the sorted target objects with the sorted replacement colors.
    for obj_coords, new_color in zip(target_objects_coords, replacement_colors):
        # For each object (represented by its set of coordinates),
        # iterate through its pixels.
        for r, c in obj_coords:
            # Update the corresponding pixel in the output grid with the new color.
            output_grid[r, c] = new_color

    # Convert the final numpy array back to a standard Python list of lists format.
    return output_grid.tolist()