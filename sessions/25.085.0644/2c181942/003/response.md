```python
import numpy as np
from scipy.ndimage import label

"""
Applies gravity to whole objects in the input grid.

Identifies connected objects of non-background colors (anything other than azure - 8). 
Each object falls downwards as a single unit, maintaining its shape. 
An object stops falling when any part of its bottom edge reaches the bottom of the grid 
or lands on top of any part of another object that has already settled in the output grid. 
Objects do not move horizontally. The relative vertical order of pixels within an object 
is preserved, and the relative horizontal positions of objects are preserved.
The output grid is initially filled with the background color (azure - 8), and the 
objects are drawn in their final settled positions.
"""

def find_connected_components(grid, background_color):
    """
    Finds connected components (objects) of non-background colors using 8-connectivity.

    Args:
        grid (np.ndarray): The input grid.
        background_color (int): The color considered as background.

    Returns:
        list: A list of dictionaries, where each dictionary represents an object
              and contains 'color', 'coords' (a set of (r, c) tuples of absolute
              coordinates), 'rel_coords' (a set of (r, c) tuples relative to the
              bounding box top-left), and 'bbox' (min_r, min_c, max_r, max_c).
    """
    mask = grid != background_color
    # structure=np.array([[1,1,1],[1,1,1],[1,1,1]]) defines 8-connectivity (including diagonals)
    labeled_grid, num_labels = label(mask, structure=np.array([[1,1,1],[1,1,1],[1,1,1]]))

    objects = []
    for i in range(1, num_labels + 1):
        # Find all pixels belonging to the current label
        obj_mask = labeled_grid == i
        coords = set(tuple(coord) for coord in np.array(np.where(obj_mask)).T) # set of (row, col) tuples

        if not coords: # Should not happen with labels > 0, but good practice
            continue

        # Get the color from the first pixel of the component (all pixels in a component have the same color)
        first_coord = next(iter(coords))
        obj_color = grid[first_coord]

        # Calculate bounding box
        rows, cols = zip(*coords)
        min_r, max_r = min(rows), max(rows)
        min_c, max_c = min(cols), max(cols)

        # Calculate coordinates relative to the top-left corner of the bounding box
        rel_coords = set((r - min_r, c - min_c) for r, c in coords)

        objects.append({
            'color': obj_color,
            'coords': coords, # Absolute coordinates in the original grid
            'rel_coords': rel_coords, # Coordinates relative to bbox top-left
            'bbox': (min_r, min_c, max_r, max_c) # Bounding box: top, left, bottom, right
        })
    return objects


def transform(input_grid):
    """
    Applies gravity simulation to non-background objects in the grid.

    Args:
        input_grid (np.ndarray): A 2D numpy array representing the input grid.

    Returns:
        np.ndarray: A 2D numpy array representing the transformed grid with objects settled by gravity.
    """
    background_color = 8
    height, width = input_grid.shape

    # 1. Identify all distinct non-background objects
    objects = find_connected_components(input_grid, background_color)

    # 2. Sort objects primarily by their bottom edge (max_r), then top edge (min_r).
    # This helps in processing objects that should settle lower first.
    objects.sort(key=lambda obj: (obj['bbox'][2], obj['bbox'][0]))

    # 3. Initialize the output grid with the background color
    output_grid = np.full((height, width), background_color, dtype=int)

    # 4. Process each object to determine its final position after falling
    for obj in objects:
        color = obj['color']
        rel_coords = obj['rel_coords']
        min_r, min_c, _, _ = obj['bbox'] # Original top-left position

        # Determine the maximum distance the object can fall vertically
        fall_distance = 0
        while True:
            # Assume it can fall one step further
            can_fall_further = True
            # Calculate the potential vertical offset for the next step down
            next_r_offset = fall_distance + 1

            # Check collision for every pixel of the object at the potential new position
            for rel_r, rel_c in rel_coords:
                # Calculate the target row and column in the grid for this pixel
                target_r = min_r + rel_r + next_r_offset
                target_c = min_c + rel_c

                # Check if the target row hits or exceeds the grid bottom
                if target_r >= height:
                    can_fall_further = False
                    break # Collision with bottom

                # Check if the target cell in the output grid is already occupied by another settled object
                if output_grid[target_r, target_c] != background_color:
                    can_fall_further = False
                    break # Collision with another object

            # If no collision detected for any pixel at the next step down
            if can_fall_further:
                fall_distance += 1 # Increment the fall distance
            else:
                # Collision detected or bottom reached, stop checking further fall for this object
                break

        # 5. Calculate the final top-left position of the object after falling
        final_r = min_r + fall_distance
        final_c = min_c # Object only moves vertically

        # 6. Place the object onto the output grid at its final settled position
        for rel_r, rel_c in rel_coords:
            # Draw each pixel of the object using its relative coordinates and final position
            output_grid[final_r + rel_r, final_c + rel_c] = color

    # 7. Return the final grid with all objects settled
    return output_grid
```