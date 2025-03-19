import numpy as np

# Define the transform function (provided previously)
def get_neighbors(grid, row, col):
    """Gets the valid neighbors (up, down, left, right) of a cell in the grid."""
    rows, cols = grid.shape
    neighbors = []
    if row > 0:
        neighbors.append((row - 1, col))  # Up
    if row < rows - 1:
        neighbors.append((row + 1, col))  # Down
    if col > 0:
        neighbors.append((row, col - 1))  # Left
    if col < cols - 1:
        neighbors.append((row, col + 1))  # Right
    return neighbors

def get_contiguous_region(grid, start_row, start_col, color):
    """Finds a contiguous region of a given color starting from a given cell."""
    region = set()
    queue = [(start_row, start_col)]
    visited = set()

    while queue:
        row, col = queue.pop(0)
        if (row, col) in visited:
            continue
        visited.add((row, col))

        if grid[row, col] == color:
            region.add((row, col))
            neighbors = get_neighbors(grid, row, col)
            queue.extend(neighbors)
    return region

train_inputs = [
    np.array([[9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9, 9, 1, 9], [9, 9, 9, 9, 9, 9, 9], [9, 9, 1, 1, 9, 9, 9], [9, 9, 9, 9, 9, 9, 9]]),
    np.array([[9, 9, 9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 1, 9, 9, 9, 9, 9], [9, 9, 9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 1, 1, 1, 9, 9, 9], [9, 9, 9, 9, 9, 9, 9, 9, 9]]),
    np.array([[9, 9, 9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 1, 9, 9, 1, 9, 9], [9, 9, 9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 1, 9, 9, 1, 9, 9], [9, 9, 9, 9, 9, 9, 9, 9, 9]]),
    np.array([[9, 9, 9, 9, 9, 9], [9, 1, 1, 1, 1, 9], [9, 1, 9, 9, 1, 9], [9, 1, 1, 1, 1, 9], [9, 9, 9, 9, 9, 9]]),
    np.array([[9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 9], [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9], [9, 9, 9, 9, 9, 9, 9, 9, 9, 1, 1, 1, 9], [9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9, 9]])
]

for i, input_grid in enumerate(train_inputs):
    print(f"Example {i+1}:")
    visited = set()
    for row in range(input_grid.shape[0]):
        for col in range(input_grid.shape[1]):
            if input_grid[row, col] == 1 and (row, col) not in visited:
                region = get_contiguous_region(input_grid, row, col, 1)
                visited.update(region)
                print(f"  Blue region at ({row}, {col}): Size = {len(region)}, Coordinates = {region}")
