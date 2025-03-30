import numpy as np
from collections import deque

"""
Processes multi-colored objects composed of nested rectangular layers by swapping the colors of symmetric layers.

1. Initialize the output grid as a copy of the input grid.
2. Identify all distinct connected components (objects) formed by non-white (0) pixels in the input grid.
3. For each identified object:
    a. Determine the sequence of layers and their corresponding colors, starting from the outermost layer and proceeding inwards. This is done by iteratively identifying and "peeling" the boundary pixels of the remaining object part.
    b. Extract the sequence of colors corresponding to these layers.
    c. Create a reversed sequence of these layer colors.
    d. Iterate through the identified layers (from outermost to innermost) and the reversed color sequence simultaneously.
    e. For each layer, update the color of all pixels belonging to that layer in the output grid using the corresponding color from the reversed sequence.
4. Return the modified output grid.
"""

def get_neighbors(r, c, h, w, connectivity=4):
    """ Get valid neighbors for a cell """
    neighbors = []
    if connectivity == 4:
        moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
    # Add connectivity=8 if needed later
    # elif connectivity == 8:
    #     moves = [(0, 1), (0, -1), (1, 0), (-1, 0), (1, 1), (1, -1), (-1, 1), (-1, -1)]
    else:
        raise ValueError("Unsupported connectivity")

    for dr, dc in moves:
        nr, nc = r + dr, c + dc
        if 0 <= nr < h and 0 <= nc < w:
            neighbors.append((nr, nc))
    return neighbors

def find_objects(grid):
    """ Finds connected components of non-background (0) pixels """
    h, w = grid.shape
    visited = np.zeros_like(grid, dtype=bool)
    objects = []

    for r in range(h):
        for c in range(w):
            if grid[r, c] != 0 and not visited[r, c]:
                # Start BFS for a new object
                obj_coords = set()
                q = deque([(r, c)])
                visited[r, c] = True
                while q:
                    curr_r, curr_c = q.popleft()
                    obj_coords.add((curr_r, curr_c))
                    for nr, nc in get_neighbors(curr_r, curr_c, h, w):
                        if grid[nr, nc] != 0 and not visited[nr, nc]:
                            visited[nr, nc] = True
                            q.append((nr, nc))
                if obj_coords:
                    objects.append(obj_coords)
    return objects

def transform(input_grid_list):
    """
    Transforms the input grid by swapping the colors of symmetric layers within each object.
    """
    input_grid = np.array(input_grid_list, dtype=int)
    output_grid = np.copy(input_grid)
    h, w = input_grid.shape

    # Find all distinct objects (connected components of non-zero pixels)
    objects = find_objects(input_grid)

    for obj_coords in objects:
        # Process each object to find its layers and swap colors

        # Make a working copy of the object's pixel coordinates
        current_object_pixels = obj_coords.copy()
        layers_data = [] # Stores tuples: (set_of_layer_pixels, layer_color)

        while current_object_pixels:
            # Identify boundary pixels of the *remaining* object part
            # Boundary pixels are adjacent (4-way) to a pixel NOT in current_object_pixels
            boundary_pixels = set()
            for r, c in current_object_pixels:
                is_boundary = False
                for nr, nc in get_neighbors(r, c, h, w):
                    if (nr, nc) not in current_object_pixels:
                        is_boundary = True
                        break
                if is_boundary:
                    boundary_pixels.add((r, c))
            
            if not boundary_pixels:
                 # This might happen if the remaining object is fully contained
                 # Or if it's the very last pixel(s)
                 boundary_pixels = current_object_pixels.copy() # Treat remaining as the last layer


            # Assume layer has uniform color (as per examples)
            # Get color from one of the boundary pixels
            if boundary_pixels:
              layer_color = input_grid[list(boundary_pixels)[0]]
              layers_data.append((boundary_pixels, layer_color))
              # Remove the found layer pixels for the next iteration
              current_object_pixels -= boundary_pixels
            else:
              # Should not happen with the fix above, but as a safeguard
              break


        # Now we have layers_data = [(layer1_pixels, color1), (layer2_pixels, color2), ...]
        # Extract colors and reverse them
        layer_colors = [color for _, color in layers_data]
        reversed_layer_colors = layer_colors[::-1]

        # Apply the reversed colors back to the layers in the output grid
        if len(layers_data) == len(reversed_layer_colors):
            for i, (layer_pixels, _) in enumerate(layers_data):
                new_color = reversed_layer_colors[i]
                for r, c in layer_pixels:
                    output_grid[r, c] = new_color
        else:
            # This case indicates an issue in layer detection or assumptions
            print("Warning: Mismatch between detected layers and reversed colors. Skipping transformation for this object.")


    return output_grid.tolist()