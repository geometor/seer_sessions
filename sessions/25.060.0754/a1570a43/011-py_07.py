import numpy as np

def describe_grid(grid):
    desc = {
        "shape": grid.shape,
        "colors": {},
        "objects": {},
    }

    unique_colors = np.unique(grid)
    for color in unique_colors:
        desc["colors"][int(color)] = np.sum(grid == color)

    # Detect "objects" (contiguous blocks of the same color)
    visited = np.zeros_like(grid, dtype=bool)
    object_id = 0

    def dfs(x, y, color):
        if x < 0 or x >= grid.shape[0] or y < 0 or y >= grid.shape[1]:
            return
        if visited[x, y] or grid[x, y] != color:
            return
        visited[x, y] = True
        object_coords.append((x,y))
        dfs(x + 1, y, color)
        dfs(x - 1, y, color)
        dfs(x, y + 1, color)
        dfs(x, y - 1, color)

    for x in range(grid.shape[0]):
        for y in range(grid.shape[1]):
            if not visited[x, y]:
                object_coords = []
                dfs(x, y, grid[x, y])
                if object_coords: #only if not empty list
                    object_id += 1
                    desc["objects"][object_id] = {
                        "color": int(grid[x, y]),
                        "coordinates": object_coords,
                        "size": len(object_coords)
                    }    
    return desc

def compare_grids(grid1, grid2):
    comparison = {}
    desc1 = describe_grid(grid1)
    desc2 = describe_grid(grid2)
    
    comparison["shape_match"] = desc1["shape"] == desc2["shape"]
    comparison["color_counts_match"] = desc1["colors"] == desc2["colors"]
    
    # Compare Objects
    obj_ids1 = set(desc1['objects'].keys())
    obj_ids2 = set(desc2['objects'].keys())
    
    comparison['objects_match'] = obj_ids1 == obj_ids2 # Exact match of object IDs
    
    
    # Exact match check:
    comparison["pixel_perfect_match"] = np.array_equal(grid1, grid2)

    if not comparison["pixel_perfect_match"]:
       comparison['differences'] = []

       for i in range(grid1.shape[0]):
           for j in range(grid1.shape[1]):
               if grid1[i,j] != grid2[i,j]:
                   comparison['differences'].append({
                       'coordinate': (i,j),
                       'original': int(grid1[i,j]),
                       'transformed': int(grid2[i,j])
                   })
    return comparison

# Example Data (Replace with your actual data)
# previous transform function
previous_code = """
import numpy as np

def get_red_block(grid):
    # Find coordinates of all red pixels
    red_pixels = np.argwhere(grid == 2)
    return red_pixels

def rotate_coordinates(coords, center, angle_degrees):
    # Rotate coordinates around a center point
    angle_radians = np.radians(angle_degrees)
    rotation_matrix = np.array([
        [np.cos(angle_radians), -np.sin(angle_radians)],
        [np.sin(angle_radians), np.cos(angle_radians)]
    ])
    centered_coords = coords - center
    rotated_coords = np.dot(centered_coords, rotation_matrix)
    return rotated_coords + center

def transform(input_grid):
    # Initialize output grid with zeros
    output_grid = np.zeros_like(input_grid)

    # Get the red block coordinates
    red_block = get_red_block(input_grid)

    # Calculate the center of the grid (assuming it is the center of rotation)
    center = np.array([input_grid.shape[0] // 2, input_grid.shape[1] // 2])

    # Rotate the red block coordinates 90 degrees clockwise
    rotated_red_block = rotate_coordinates(red_block, center, 90)

    # Round the rotated coordinates and convert to integers to use as indices
    rotated_red_block = np.round(rotated_red_block).astype(int)

    # Place the rotated red block into the output grid
    for x, y in rotated_red_block:
        if 0 <= x < output_grid.shape[0] and 0 <= y < output_grid.shape[1]:  # Boundary check
          output_grid[x, y] = 2

    # Copy the green pixels to the output grid
    green_pixels = np.argwhere(input_grid == 3)
    for x, y in green_pixels:
        output_grid[x, y] = 3

    return output_grid
"""

exec(previous_code)

train = [
    (np.array([[3, 3, 3, 3, 3, 3, 3, 3, 3],
       [3, 3, 3, 3, 3, 3, 3, 3, 3],
       [3, 3, 3, 2, 2, 2, 3, 3, 3],
       [3, 3, 3, 3, 3, 3, 3, 3, 3],
       [3, 3, 3, 3, 3, 3, 3, 3, 3]]),
     np.array([[3, 3, 3, 3, 3, 3, 3, 3, 3],
       [3, 3, 3, 3, 2, 3, 3, 3, 3],
       [3, 3, 3, 3, 2, 3, 3, 3, 3],
       [3, 3, 3, 3, 2, 3, 3, 3, 3],
       [3, 3, 3, 3, 3, 3, 3, 3, 3]])
     ),
        (np.array([[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 2, 2, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3]]),
        np.array([[3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3],
        [3, 3, 3, 3, 3, 3, 2, 3, 3, 3, 3, 3]])
     ),
    (
        np.array([[3, 3, 3, 3, 3, 3, 3],
       [3, 3, 3, 3, 3, 3, 3],
       [3, 3, 2, 3, 3, 3, 3],
       [3, 3, 2, 3, 3, 3, 3],
       [3, 3, 2, 3, 3, 3, 3],
       [3, 3, 3, 3, 3, 3, 3]]),
        np.array([[3, 3, 3, 3, 3, 3, 3],
       [3, 3, 3, 3, 3, 3, 3],
       [3, 3, 3, 3, 2, 3, 3],
       [3, 3, 3, 3, 2, 3, 3],
       [3, 3, 3, 3, 2, 3, 3],
       [3, 3, 3, 3, 3, 3, 3]])
        )
]

results = []
for input_grid, expected_output in train:
    transformed_grid = transform(input_grid)
    comparison = compare_grids(expected_output, transformed_grid)
    results.append({
        "input": describe_grid(input_grid),
        "expected_output": describe_grid(expected_output),
        "produced_output": describe_grid(transformed_grid),
        "comparison": comparison,
    })
    print(f"{comparison=}")