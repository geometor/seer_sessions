import numpy as np

def get_adjacent_pixels(grid, row, col):
    """
    Gets the values of adjacent pixels (up, down, left, right).
    Returns a dictionary with keys 'up', 'down', 'left', 'right' and
    corresponding pixel values.
    Returns -1 for out-of-bounds neighbors.
    """
    rows, cols = grid.shape
    adjacent = {}

    adjacent['up'] = grid[row - 1, col] if row > 0 else -1
    adjacent['down'] = grid[row + 1, col] if row < rows - 1 else -1
    adjacent['left'] = grid[row, col - 1] if col > 0 else -1
    adjacent['right'] = grid[row, col + 1] if col < cols - 1 else -1

    return adjacent

def transform(input_grid):
    """
    Transforms the input grid according to the specified rule.
    """
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape

    for row in range(rows):
        for col in range(cols):
            if input_grid[row, col] == 5:  # Check if it's a gray pixel
                adjacent = get_adjacent_pixels(input_grid, row, col)

                # Check for two horizontal white neighbors.
                horizontal_white_count = 0
                if adjacent['left'] == 0:
                    horizontal_white_count += 1
                if adjacent['right'] == 0:
                    horizontal_white_count += 1

                # Check for two vertical white neighbors.
                vertical_white_count = 0;
                if adjacent['up'] == 0:
                    vertical_white_count += 1
                if adjacent['down'] == 0:
                    vertical_white_count += 1


                # Apply the replacement rule
                if vertical_white_count == 2 or horizontal_white_count == 2:
                     output_grid[row,col] = 3;


    return output_grid

def compare_grids(grid1, grid2):
    """Compares two grids and returns a list of differences."""
    if grid1.shape != grid2.shape:
        return "Grids have different shapes"
    differences = []
    rows, cols = grid1.shape
    for row in range(rows):
        for col in range(cols):
            if grid1[row, col] != grid2[row, col]:
                differences.append((row, col, grid1[row, col], grid2[row, col]))
    return differences

# Example grids (replace with actual task data later)
train_input_1 = np.array([
    [0, 5, 0],
    [5, 5, 5],
    [0, 5, 0]
])

train_output_1 = np.array([
    [0, 5, 0],
    [5, 3, 5],
    [0, 5, 0]
])

train_input_2 = np.array([
    [0, 5, 0, 5, 0],
    [5, 5, 5, 5, 5],
    [0, 5, 0, 5, 0]
])

train_output_2 = np.array([
    [0, 5, 0, 5, 0],
    [5, 3, 5, 3, 5],
    [0, 5, 0, 5, 0]
])

train_input_3 = np.array([
    [0, 5, 0, 5, 0, 5, 0],
    [5, 5, 5, 5, 5, 5, 5],
    [0, 5, 0, 5, 0, 5, 0]
])

train_output_3 = np.array([
    [0, 5, 0, 5, 0, 5, 0],
    [5, 3, 5, 3, 5, 3, 5],
    [0, 5, 0, 5, 0, 5, 0]
])

train_inputs = [train_input_1, train_input_2, train_input_3]
train_outputs = [train_output_1, train_output_2, train_output_3]

for i, (input_grid, output_grid) in enumerate(zip(train_inputs, train_outputs)):
    transformed_grid = transform(input_grid)
    differences = compare_grids(transformed_grid, output_grid)
    print(f"Example {i+1}:")
    print(f"  Input:\n{input_grid}")
    print(f"  Expected Output:\n{output_grid}")
    print(f"  Transformed Output:\n{transformed_grid}")
    print(f"  Differences: {differences}")