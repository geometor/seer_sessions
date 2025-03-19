def analyze_example(input_grid, expected_output_grid, actual_output_grid):
    """
    Analyzes a single example and provides detailed metrics.

    Args:
        input_grid: The input grid (numpy array).
        expected_output_grid: The expected output grid (numpy array).
        actual_output_grid: The output from the transformation function

    Returns:
        A dictionary containing the analysis results.
    """
    input_non_white = find_non_white_pixels(input_grid)
    expected_non_white = find_non_white_pixels(expected_output_grid)
    actual_non_white = find_non_white_pixels(actual_output_grid)
    input_objects = find_contiguous_objects(input_grid)

    analysis = {
        'input_non_white_count': len(input_non_white),
        'expected_non_white_count': len(expected_non_white),
        'actual_non_white_count': len(actual_non_white),
        'input_objects': input_objects,
        'correct': np.array_equal(expected_output_grid, actual_output_grid)
    }

    return analysis

def find_contiguous_objects(grid):
    """
    Identifies contiguous objects (blocks of same-colored, non-white pixels).

    Args:
        grid: The input grid.

    Returns:
        A list of objects, where each object is a list of (row, col) coordinates.
    """
    visited = set()
    objects = []

    def dfs(row, col, color, current_object):
        if (row, col) in visited or not (0 <= row < grid.shape[0] and 0 <= col < grid.shape[1]) or grid[row, col] != color:
            return
        visited.add((row, col))
        current_object.append((row, col))
        dfs(row + 1, col, color, current_object)
        dfs(row - 1, col, color, current_object)
        dfs(row, col + 1, color, current_object)
        dfs(row, col - 1, color, current_object)

    for r in range(grid.shape[0]):
        for c in range(grid.shape[1]):
            if grid[r, c] != 0 and (r, c) not in visited:
                current_object = []
                dfs(r, c, grid[r, c], current_object)
                objects.append(current_object)
    return objects

from utils import load_task
task = load_task('25d8a9c8', False)  # False for training examples

results = []
for i, example in enumerate(task['train']):
    input_grid = np.array(example['input'])
    expected_output_grid = np.array(example['output'])
    actual_output_grid = transform(input_grid)  # Using the provided transform function
    example_results = analyze_example(input_grid, expected_output_grid, actual_output_grid)
    results.append((i,example_results))
    print(f"Example {i}:")
    print(f"  Input Non-White Pixels: {example_results['input_non_white_count']}")
    print(f"  Expected Non-White Pixels: {example_results['expected_non_white_count']}")
    print(f"  Actual Non-White Pixels: {example_results['actual_non_white_count']}")    
    print(f"  Input Objects: {example_results['input_objects']}")
    print(f"  Correct: {example_results['correct']}")
    print("-" * 20)
print(results)