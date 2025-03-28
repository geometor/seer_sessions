import numpy as np
from collections import deque

"""
Recolor blue (1) objects based on an ordered palette of other colors present in the grid.

1.  **Identify Palette Colors**: Scan the input grid row by row, from top to bottom, and within each row, from left to right. Record the unique colors encountered that are neither white (0) nor blue (1). Maintain the order in which these colors are first encountered. This ordered list is the `palette`. Let M be the number of colors in the `palette`.
2.  **Identify Blue Objects**: Find all distinct contiguous objects composed of blue (1) pixels, considering pixels connected horizontally, vertically, or diagonally as part of the same object.
3.  **Order Blue Objects**: Determine the top-leftmost pixel for each blue object. Sort the blue objects based on these coordinates (first by row index, then by column index). This creates an ordered list of blue objects `B`. Let N be the number of blue objects.
4.  **Check Applicability**: If no blue objects are found (N=0) or no palette colors are found (M=0), return the input grid unchanged.
5.  **Initialize Output Grid**: Create a copy of the input grid to serve as the output grid.
6.  **Recolor First Blue Object**: Recolor all pixels of the first blue object (`B[0]`) in the output grid using the first palette color (`palette[0]`).
7.  **Recolor Subsequent Blue Objects (if N > 1)**:
    a.  **Recolor Last Blue Object**:
        *   If the number of blue objects equals the number of palette colors (N == M), recolor the last blue object (`B[N-1]`) using the last palette color (`palette[M-1]`).
        *   Otherwise (if N != M), recolor the last blue object (`B[N-1]`) using the first palette color (`palette[0]`).
    b.  **Recolor Intermediate Blue Objects (if N > 2)**:
        *   If there is only one palette color (M == 1), recolor all intermediate blue objects (`B[1]` through `B[N-2]`) using the first (and only) palette color (`palette[0]`).
        *   If there is more than one palette color (M > 1), recolor all intermediate blue objects (`B[1]` through `B[N-2]`) using the second palette color (`palette[1]`).
8.  **Return Output**: Return the modified output grid.
"""

def find_objects(grid, target_colors):
    """
    Finds contiguous objects of specified colors in a grid.

    Args:
        grid (np.array): The input grid.
        target_colors (set): A set of colors to find objects for.

    Returns:
        list: A list of objects, where each object is a set of (row, col) tuples.
              The list is sorted by the top-leftmost coordinate of each object.
    """
    rows, cols = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    # Iterate through the grid to find starting points of objects
    for r in range(rows):
        for c in range(cols):
            # If a pixel has a target color and hasn't been visited yet, start a BFS
            if grid[r, c] in target_colors and not visited[r, c]:
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                min_r, min_c = r, c # Track the top-leftmost coordinate

                # Breadth-First Search to find all connected pixels of the same object
                while q:
                    row, col = q.popleft()
                    obj_coords.add((row, col))

                    # Keep track of the top-leftmost coordinate for sorting later
                    if row < min_r:
                        min_r, min_c = row, col
                    elif row == min_r and col < min_c:
                        min_c = col

                    # Explore 8 neighbors (including diagonals)
                    for dr in [-1, 0, 1]:
                        for dc in [-1, 0, 1]:
                            if dr == 0 and dc == 0:
                                continue # Skip self
                            nr, nc = row + dr, col + dc
                            # Check bounds and if the neighbor is a valid part of the object
                            if 0 <= nr < rows and 0 <= nc < cols and \
                               grid[nr, nc] in target_colors and not visited[nr, nc]:
                                visited[nr, nc] = True
                                q.append((nr, nc))
                
                # Store the object's coordinates and its top-left coordinate
                objects.append({'coords': obj_coords, 'top_left': (min_r, min_c)})

    # Sort objects based on their top-left coordinate (row, then column)
    objects.sort(key=lambda obj: obj['top_left'])
    
    # Return just the coordinate sets in the sorted order
    return [obj['coords'] for obj in objects]


def transform(input_grid):
    """
    Transforms the input grid by recoloring blue objects based on palette colors.
    
    Args:
        input_grid (np.array): The input 2D array.

    Returns:
        np.array: The transformed 2D array.
    """
    # 1. Identify and order palette colors (non-white 0, non-blue 1)
    rows, cols = input_grid.shape
    palette_first_coords = {} # Dictionary to store first encountered coordinate for each palette color
    for r in range(rows):
        for c in range(cols):
            color = input_grid[r, c]
            if color != 0 and color != 1:
                if color not in palette_first_coords:
                    palette_first_coords[color] = (r, c)
    
    # Sort the found palette colors by their first appearance coordinates
    sorted_palette_items = sorted(palette_first_coords.items(), key=lambda item: item[1])
    palette_colors_ordered = [color for color, coords in sorted_palette_items]
    num_palette_colors = len(palette_colors_ordered) # M

    # 2. & 3. Identify and order blue objects
    blue_objects = find_objects(input_grid, {1}) # Find objects with color 1 (blue)
    num_blue_objects = len(blue_objects) # N

    # 4. Check Applicability: If no blue objects or no palette colors, return original grid
    if num_blue_objects == 0 or num_palette_colors == 0:
        return np.copy(input_grid) 

    # 5. Initialize Output Grid
    output_grid = np.copy(input_grid)

    # 6. Recolor First Blue Object (B[0]) with first palette color (P[0])
    first_object_coords = blue_objects[0]
    first_palette_color = palette_colors_ordered[0]
    for r, c in first_object_coords:
        output_grid[r, c] = first_palette_color

    # 7. Recolor Subsequent Blue Objects (only if N > 1)
    if num_blue_objects > 1:
        # 7a. Recolor Last Blue Object (B[N-1])
        last_object_coords = blue_objects[-1]
        last_object_target_color = -1 # Placeholder

        # Condition: N == M vs N != M
        if num_blue_objects == num_palette_colors:
            # If N == M, use the last palette color P[M-1]
            last_object_target_color = palette_colors_ordered[-1] 
        else: # N != M
            # If N != M, use the first palette color P[0]
            last_object_target_color = palette_colors_ordered[0] 

        # Apply the determined color to the last object
        for r, c in last_object_coords:
            output_grid[r, c] = last_object_target_color

        # 7b. Recolor Intermediate Blue Objects (B[1] to B[N-2]) (only if N > 2)
        if num_blue_objects > 2:
            intermediate_target_color = -1 # Placeholder

            # Condition: M == 1 vs M > 1
            if num_palette_colors == 1:
                # If only one palette color (M=1), use it (P[0])
                intermediate_target_color = palette_colors_ordered[0]
            else: # M > 1
                # If multiple palette colors, use the second one (P[1])
                intermediate_target_color = palette_colors_ordered[1] 

            # Apply the determined color to all intermediate objects
            # Loop from the second object (index 1) up to (but not including) the last object (index N-1)
            for i in range(1, num_blue_objects - 1):
                intermediate_obj_coords = blue_objects[i]
                for r, c in intermediate_obj_coords:
                    output_grid[r, c] = intermediate_target_color

    # 8. Return the modified output grid
    return output_grid