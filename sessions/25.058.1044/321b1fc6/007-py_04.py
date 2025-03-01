import numpy as np

def find_squares(grid):
    squares = []
    for r in range(len(grid) - 1):
        for c in range(len(grid[0]) - 1):
            if grid[r, c] != 0 and grid[r, c+1] != 0 and grid[r+1, c] != 0 and grid[r+1, c+1] != 0:
                squares.append({
                    "top_left": (r, c),
                    "colors": (grid[r, c], grid[r, c+1], grid[r+1, c], grid[r+1, c+1])
                })
    return squares

def transform(input_grid):
    # initialize output_grid
    output_grid = np.copy(input_grid)

    # Find all 2x2 squares
    squares = find_squares(input_grid)

    # Target square and new locations
    target_colors = (7, 6, 4, 9)
    target_square = None

    for square in squares:
      if square["colors"] == target_colors:
        target_square = square
        break

    #Move and duplicate target, if found.
    if target_square:
        # first copy
        row_offset = output_grid.shape[0] - 2 - target_square["top_left"][0]
        output_grid[target_square["top_left"][0] + row_offset, target_square["top_left"][1]] = 7
        output_grid[target_square["top_left"][0] + row_offset, target_square["top_left"][1] + 1] = 6
        output_grid[target_square["top_left"][0] + 1 + row_offset, target_square["top_left"][1]] = 4
        output_grid[target_square["top_left"][0] + 1 + row_offset, target_square["top_left"][1] + 1] = 9
        # second copy
        col_offset = output_grid.shape[1] - 2 - target_square["top_left"][1]

        output_grid[target_square["top_left"][0] + row_offset, target_square["top_left"][1] + col_offset ] = 7
        output_grid[target_square["top_left"][0] + row_offset, target_square["top_left"][1] + 1 + col_offset] = 6
        output_grid[target_square["top_left"][0] + 1 + row_offset, target_square["top_left"][1] + col_offset] = 9
        output_grid[target_square["top_left"][0] + 1 + row_offset, target_square["top_left"][1] + 1 + col_offset] = 4

        # Remove original square
        output_grid[target_square["top_left"][0], target_square["top_left"][1]] = 0
        output_grid[target_square["top_left"][0], target_square["top_left"][1] + 1] = 0
        output_grid[target_square["top_left"][0] + 1, target_square["top_left"][1]] = 0
        output_grid[target_square["top_left"][0] + 1, target_square["top_left"][1] + 1] = 0

    # Remove azure pixels.
    for r in range(output_grid.shape[0]):
      for c in range(output_grid.shape[1]):
        if output_grid[r,c] == 8:
            output_grid[r,c] = 0

    return output_grid

def check_transformations(task):
    correct_count = 0
    for example in task['train']:
        input_grid = np.array(example['input'])
        expected_output = np.array(example['output'])
        transformed_grid = transform(input_grid)
        comparison = np.array_equal(transformed_grid, expected_output)
        print(f"Example: {example['input']} -> {example['output']}")
        print(f"Transformed: {transformed_grid.tolist()}")
        print(f"Correct: {comparison}")
        if comparison:
            correct_count += 1

        # Check for 2x2 squares in input
        squares = find_squares(input_grid)
        print(f"Squares found in input: {squares}")
        print("-" * 20)
    print(f"Total correct: {correct_count}/{len(task['train'])}")

# Example Usage (replace with the actual task data)
task = {
    'train': [
        {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 7, 6, 0, 0, 0], [0, 0, 0, 0, 4, 9, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 8, 0, 0, 0, 0, 0, 0, 0]],
         'output': [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 7, 6, 0], [0, 0, 0, 0, 7, 6, 4, 9, 0]]},

        {'input': [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 7, 6, 0, 0, 0], [0, 0, 0, 4, 9, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
         'output': [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 7, 6, 0], [0, 0, 0, 7, 6, 4, 9, 0]]},

        {'input': [[0, 0, 0, 0, 0, 0, 0], [0, 7, 6, 0, 0, 0, 0], [0, 4, 9, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
         'output': [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 7, 6, 0, 0, 0, 0], [7, 6, 4, 9, 0, 0, 0]]}
    ]
}
check_transformations(task)