import numpy as np

# Helper functions (from the provided code)
def find_object(grid, color):
    coords = np.argwhere(grid == color)
    return coords

def get_bounding_box(coords):
    min_y = np.min(coords[:, 0])
    max_y = np.max(coords[:, 0])
    min_x = np.min(coords[:, 1])
    max_x = np.max(coords[:, 1])
    return (min_y, min_x), (max_y, max_x)

def expand_bounding_box(grid, top_left, bottom_right):
    # Expands the bounding box to include contiguous white and blue pixels
    min_y, min_x = top_left
    max_y, max_x = bottom_right
    
    
    def is_valid(y, x):
        # check if pixel is in the grid
        return 0 <= y < grid.shape[0] and 0 <= x < grid.shape[1]
    
    def should_expand(y,x):
        # only expand to white or blue
        return (grid[y,x] == 0) or (grid[y,x] == 1)

    
    # Expand upwards
    while min_y > 0 and should_expand(min_y - 1, min_x):
        min_y -= 1
    # Expand downwards
    while max_y < grid.shape[0] - 1 and should_expand(max_y + 1, min_x):
        max_y += 1
    # Expand left
    while min_x > 0 and should_expand(min_y, min_x - 1):
        min_x -= 1
    # Expand Right
    while max_x < grid.shape[1] - 1 and should_expand(min_y, max_x+1):
        max_x += 1
        
    # Expand upwards
    while min_y > 0 and should_expand(min_y - 1, max_x):
        min_y -= 1
    # Expand downwards
    while max_y < grid.shape[0] - 1 and should_expand(max_y + 1, max_x):
        max_y += 1    
        
    # diagonal expansion
    while min_y > 0 and min_x > 0 and should_expand(min_y-1, min_x - 1):
            min_y -= 1
            min_x -= 1    
    while max_y < grid.shape[0] -1 and max_x < grid.shape[1] - 1 and should_expand(max_y + 1, max_x + 1):
        max_y += 1
        max_x += 1

    return (min_y, min_x), (max_y, max_x)

# Example grids (replace with actual data from the task)
input_grids = [
    np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 4, 0, 0, 0, 0, 0]
    ]),
    np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 0, 0, 0, 0, 0, 0, 0, 0]
    ]),
        np.array([
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 0, 0, 0, 0, 0],
        [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4, 0, 0, 0, 0, 0]
    ]),
]
output_grids = [
    np.array([
    [1, 1, 1, 1, 0],
    [1, 1, 1, 1, 4]
    ]),
    np.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4]
    ]),
    np.array([
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4],
    [1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 4]
    ]),
]
for i in range(len(input_grids)):
    input_grid = input_grids[i]
    expected_output = output_grids[i]
    
    yellow_coords = find_object(input_grid, 4)
    print(f"Example {i+1} - Yellow Coords: {yellow_coords}")

    top_left, bottom_right = get_bounding_box(yellow_coords)
    print(f"Example {i+1} - Initial Bounding Box: Top Left: {top_left}, Bottom Right: {bottom_right}")

    expanded_top_left, expanded_bottom_right = expand_bounding_box(input_grid, top_left, bottom_right)
    print(f"Example {i+1} - Expanded Bounding Box: Top Left: {expanded_top_left}, Bottom Right: {expanded_bottom_right}")

    actual_output = input_grid[expanded_top_left[0]:expanded_bottom_right[0]+1, expanded_top_left[1]:expanded_bottom_right[1]+1].copy()
    print(f"actual output shape: {actual_output.shape}")
    print(f"expected output shape: {expected_output.shape}")    
    print(f"Example {i + 1} - Match: {np.array_equal(actual_output, expected_output)}\n")