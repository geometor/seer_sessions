import numpy as np

def analyze_example(example_number, input_grid, output_grid, expected_output, result):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    expected_output = np.array(expected_output)

    input_height, input_width = input_grid.shape
    output_height, output_width = output_grid.shape
    expected_height, expected_width = 0, 0
    if expected_output.size > 0:
        expected_height, expected_width = expected_output.shape
        
    analysis = {
        'example_number': example_number,
        'input_dimensions': (input_height, input_width),
        'output_dimensions': (output_height, output_width),
        'expected_dimensions': (expected_height, expected_width),
        'result': result,
    }
    return analysis

# previous examples
examples = [
    (
        1,
        [[5, 8, 8], [5, 8, 8], [5, 8, 8], [5, 8, 8], [5, 8, 8], [5, 8, 8], [5, 8, 8], [5, 8, 8], [5, 8, 8]],
        [[5, 8, 8], [5, 8, 8], [5, 8, 8]],
        [[5, 8, 8], [5, 8, 8], [5, 8, 8]],
        'pass',
    ),
    (
        2,
        [[5, 8, 8], [5, 8, 8], [5, 8, 8], [5, 8, 8], [5, 8, 8], [5, 8, 8], [1, 1, 1], [1, 1, 1], [1, 1, 1]],
        [[5, 8, 8], [5, 8, 8], [5, 8, 8]],
        [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
        'fail',
    ),
    (
        3,
        [[1, 1, 1], [1, 1, 1], [1, 1, 1], [5, 8, 8], [5, 8, 8], [5, 8, 8], [5, 8, 8], [5, 8, 8], [5, 8, 8]],
        [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
        [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
        'pass'
    ),
    (
        4,
        [[5, 8, 8], [5, 8, 8], [5, 8, 8], [5, 8, 8], [5, 8, 8], [5, 8, 8], [5, 8, 8], [5, 8, 8], [5, 8, 8]],
        [[5, 8, 8], [5, 8, 8], [5, 8, 8]],
        [[5, 8, 8], [5, 8, 8], [5, 8, 8]],
        'pass'
    ),
     (
        5,
        [[0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0], [0, 0, 0]],
        [[0,0,0],[0,0,0],[0,0,0]],
        [[0,0,0],[0,0,0],[0,0,0]],
        'pass'
    ),
      (
        6,
        [[1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 2, 3], [4, 5, 6], [7, 8, 9], [1, 2, 3], [4, 5, 6], [7, 8, 9]],
        [[1, 2, 3], [4, 5, 6], [7, 8, 9]],
        [],
        'fail'
    )
]
results = [analyze_example(*example) for example in examples]
for result in results:
  print(result)