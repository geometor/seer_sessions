import numpy as np

def find_squares(grid, size, color):
    squares = []
    for row in range(grid.shape[0] - size + 1):
        for col in range(grid.shape[1] - size + 1):
            subgrid = grid[row:row+size, col:col+size]
            if np.all(subgrid == color):
                squares.append((row, col))
    return squares

def get_blue_pixel_positions(grid):
    return np.array(np.where(grid == 1)).T.tolist()

def analyze_examples(task_data):
    results = []
    for example in task_data['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])

        red_squares = find_squares(input_grid, 2, 2)  # Find 2x2 red squares
        blue_pixels = get_blue_pixel_positions(output_grid) # Find blue pixels.

        results.append({
            'input_shape': input_grid.shape,
            'output_shape': output_grid.shape,
            'red_squares': red_squares,
            'blue_pixels': blue_pixels,
        })
    return results

task_data = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0], [0, 2, 2, 0, 2, 2], [0, 2, 2, 0, 2, 2], [0, 0, 0, 0, 0, 0], [0, 2, 2, 0, 2, 2], [0, 2, 2, 0, 2, 2]],
            "output": [[1, 0, 1]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 2, 0, 0, 0, 2, 2, 0], [0, 2, 2, 0, 0, 0, 2, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 2, 0, 0, 0, 2, 2, 0], [0, 2, 2, 0, 0, 0, 2, 2, 0]],
            "output": [[0, 1, 0, 0, 0, 1, 0]]
        },
		{
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 2, 0, 0, 0, 0, 0, 2, 2, 0], [0, 2, 2, 0, 0, 0, 0, 0, 2, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 2, 0, 0, 0, 0, 0, 2, 2, 0], [0, 2, 2, 0, 0, 0, 0, 0, 2, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 1, 0, 0, 0, 0, 0, 0, 1, 0]]
        }
    ]
}

analysis_results = analyze_examples(task_data)

for i, result in enumerate(analysis_results):
    print(f"Example {i+1}:")
    print(f"  Input shape: {result['input_shape']}")
    print(f"  Output shape: {result['output_shape']}")
    print(f"  Red Squares: {result['red_squares']}")
    print(f"  Blue Pixels: {result['blue_pixels']}")