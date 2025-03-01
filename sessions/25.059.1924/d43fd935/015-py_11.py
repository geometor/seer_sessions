import numpy as np
from typing import List, Tuple

# COLOR_MAP (Provided in the prompt, I am placing it here for easy access)
COLOR_MAP = {
    0: (238, 238, 238),  # white
    1: (30, 147, 255),  # blue
    2: (220, 50, 40),  # red
    3: (79, 204, 48),  # green
    4: (230, 200, 0),  # yellow
    5: (85, 85, 85),  # gray
    6: (229, 58, 163),  # magenta
    7: (230, 120, 20),  # orange
    8: (135, 216, 241),  # azure
    9: (146, 18, 49),  # maroon
}

def get_objects(grid, color):
    """Finds objects of a specific color in the grid."""
    objects = []
    visited = set()
    rows, cols = grid.shape

    def dfs(r, c, current_object):
        if (r, c) in visited or not (0 <= r < rows and 0 <= c < cols) or grid[r, c] != color:
            return
        visited.add((r, c))
        current_object.append((r, c))
        dfs(r + 1, c, current_object)
        dfs(r - 1, c, current_object)
        dfs(r, c + 1, current_object)
        dfs(r, c - 1, current_object)

    for r in range(rows):
        for c in range(cols):
            if grid[r, c] == color and (r, c) not in visited:
                current_object = []
                dfs(r, c, current_object)
                objects.append(current_object)
    return objects

def compare_grids(grid1, grid2):
    """Compares two grids and returns the coordinates where they differ."""
    if grid1.shape != grid2.shape:
        return "Grids have different shapes"
    diff_coords = []
    for r in range(grid1.shape[0]):
        for c in range(grid1.shape[1]):
            if grid1[r, c] != grid2[r, c]:
                diff_coords.append((r, c))
    return diff_coords

def transform(input_grid):
    """Transforms the input grid according to the rules."""
    rows, cols = input_grid.shape
    output_grid = np.zeros_like(input_grid)

    # Copy green blocks (color 3) - assumes relative position means we can copy directly
    for r in range(rows):
        for c in range(cols):
            if input_grid[r,c] == 3:
                output_grid[r,c] = 3

    # Mirror orange (color 7)
    orange_objects = get_objects(input_grid, 7)
    for obj in orange_objects:
        for r, c in obj:
            output_grid[c, r] = 7

    # Mirror azure (color 8)
    azure_objects = get_objects(input_grid, 8)
    for obj in azure_objects:
        # Find the center of the object for mirroring
        coords = np.array(obj)
        min_c = np.min(coords[:, 1])
        max_c = np.max(coords[:, 1])
        center_c = (min_c + max_c) / 2

        for r, c in obj:
            # reflect across the center axis
            mirrored_c = int(2 * center_c - c)
            if 0 <= mirrored_c < cols:
                # only fill if there was not already a color 8 there
                if input_grid[r, mirrored_c] != 8:
                    output_grid[r, mirrored_c] = 8

    return output_grid

# Example data (replace with your actual data)
train_ex = [
    (np.array([[8, 8, 8, 7, 7], [8, 8, 8, 7, 7], [3, 3, 8, 7, 7], [3, 3, 8, 7, 7]]),
     np.array([[8, 8, 8, 7, 7], [8, 8, 8, 7, 7], [3, 3, 8, 7, 7], [3, 3, 8, 7, 7]])),
    (np.array([[8, 8, 8, 8, 8, 8, 8, 7, 7], [8, 8, 8, 8, 8, 8, 8, 7, 7], [3, 3, 8, 8, 8, 8, 8, 7, 7], [3, 3, 8, 8, 8, 8, 8, 7, 7]]),
     np.array([[7, 7, 8, 8, 8, 8, 8, 8, 8], [7, 7, 8, 8, 8, 8, 8, 8, 8], [7, 7, 8, 8, 8, 8, 8, 3, 3], [7, 7, 8, 8, 8, 8, 8, 3, 3]])),
    (np.array([[8, 8, 8, 8, 8, 8, 8, 8, 7, 7, 7, 7], [8, 8, 8, 8, 8, 8, 8, 8, 7, 7, 7, 7], [8, 8, 8, 8, 8, 8, 8, 8, 7, 7, 7, 7], [3, 3, 8, 8, 8, 8, 8, 8, 8, 7, 7, 7], [3, 3, 8, 8, 8, 8, 8, 8, 8, 7, 7, 7]]),
     np.array([[7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8], [7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8], [7, 7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 8], [7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 3, 3], [7, 7, 7, 8, 8, 8, 8, 8, 8, 8, 3, 3]])),
]

# Generate and print reports
for i, (input_grid, expected_output_grid) in enumerate(train_ex):
    predicted_output_grid = transform(input_grid)
    diff_coords = compare_grids(predicted_output_grid, expected_output_grid)

    print(f"--- Example {i+1} ---")
    print(f"Input Shape: {input_grid.shape}")
    print(f"Output Shape: {expected_output_grid.shape}")
    print(f"  Differences: {diff_coords}")
    for color in sorted(COLOR_MAP.keys()):
        objects = get_objects(input_grid, color)
        if objects:
            print(f"Objects of color {color} ({(COLOR_MAP[color])}): {objects}")
