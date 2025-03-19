import numpy as np

def analyze_example(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    yellow_count = np.sum(input_grid == 4)
    red_count = np.sum(input_grid == 2)
    output_value = output_grid[0, 0]

    return {
        'yellow_count': int(yellow_count),
        'red_count': int(red_count),
        'output_value': int(output_value),
        'output_color': "white" if output_value == 0 else "blue",
    }

examples = [
    ([
        [4, 4, 4, 4, 4, 4, 4],
        [4, 0, 0, 0, 0, 0, 4],
        [4, 0, 2, 2, 2, 0, 4],
        [4, 0, 2, 2, 2, 0, 4],
        [4, 0, 0, 0, 0, 0, 4],
        [4, 4, 4, 4, 4, 4, 4]
    ], [[1]]),
    ([
        [4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4],
        [4, 4, 4, 4, 4, 4, 4, 4, 4]
    ], [[0]]),
    ([
        [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
        [4, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 4]
    ], [[0]]),
    ([
        [2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2],
        [2, 2, 2, 2, 2, 2, 2, 2]
    ], [[1]]),
    ([
        [4, 4, 4, 4, 4, 4],
        [4, 0, 0, 0, 0, 4],
        [4, 0, 0, 0, 0, 4],
        [4, 0, 0, 0, 0, 4],
        [4, 4, 4, 4, 4, 4]
    ], [[1]])
]

analysis_results = [analyze_example(inp, out) for inp, out in examples]

for i, result in enumerate(analysis_results):
    print(f"Example {i+1}:")
    print(result)