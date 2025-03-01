import numpy as np

def report(description, input_grid, output_grid, expected_grid):
    correct = np.array_equal(output_grid,expected_grid)
    print(f"--- {description} ---")
    print(f"Input:\n{input_grid}")
    print(f"Output:\n{output_grid}")
    print(f"Expected:\n{expected_grid}")
    print(f"Correct: {correct}")
    return correct

def find_maroon_block(grid):
    """
    Finds the contiguous block of maroon pixels using a breadth-first search.
    """
    maroon_pixels = np.argwhere(grid == 9)
    if maroon_pixels.size == 0:
        return []

    start_pixel = tuple(maroon_pixels[0])
    block = set()
    queue = [start_pixel]

    while queue:
        current_pixel = queue.pop(0)
        if current_pixel in block:
            continue
        block.add(current_pixel)
        row, col = current_pixel

        # Check adjacent pixels (up, down, left, right)
        neighbors = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        for r, c in neighbors:
            if 0 <= r < grid.shape[0] and 0 <= c < grid.shape[1] and grid[r, c] == 9 and (r, c) not in block:
                queue.append((r, c))

    return list(block)

def transform(input_grid):
    """
    Transforms the input grid by removing the maroon block and shifting down other pixels column-wise.
    """
    # initialize output_grid
    output_grid = input_grid.copy()

    # Find and remove the maroon block
    maroon_block = find_maroon_block(output_grid)
    for row, col in maroon_block:
        output_grid[row, col] = 0  # Set to background color

    # Column-wise shift
    for col in range(output_grid.shape[1]):
        # Extract the column
        column = output_grid[:, col]

        # Find non-zero (non-background) pixels
        non_zero_indices = np.nonzero(column)[0]
        non_zero_values = column[non_zero_indices]


        # Create a new column with non-zero values shifted down
        new_column = np.zeros_like(column)
        new_column[len(new_column) - len(non_zero_values):] = non_zero_values

        # Update the column in the output grid
        output_grid[:, col] = new_column

    return output_grid

# Example Grids (replace with your actual data)
train_input_0 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 9, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 9, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 9, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 9, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 9, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
train_output_0 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
train_input_1 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 5, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 9, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 9, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 9, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 9, 0, 0, 0, 0, 0],
                          [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
train_output_1 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 5, 0, 0, 0, 0, 0],
                           [1, 1, 1, 1, 1, 1, 1, 1, 1, 1],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
train_input_2 = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 9, 9, 9, 0, 0],
                          [0, 0, 0, 9, 9, 9, 0, 0],
                          [0, 0, 0, 9, 9, 9, 0, 0],
                          [0, 0, 1, 1, 1, 1, 1, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0]])
train_output_2 = np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 1, 1, 1, 1, 1, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0]])
train_input_3 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 9, 0, 0, 0, 6, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 9, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                          [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
train_output_3 = np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 6, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

# Perform transformations and check against expected outputs

output_grid_0 = transform(train_input_0)
report("Example 0", train_input_0, output_grid_0, train_output_0)

output_grid_1 = transform(train_input_1)
report("Example 1", train_input_1, output_grid_1, train_output_1)

output_grid_2 = transform(train_input_2)
report("Example 2", train_input_2, output_grid_2, train_output_2)

output_grid_3 = transform(train_input_3)
report("Example 3", train_input_3, output_grid_3, train_output_3)
