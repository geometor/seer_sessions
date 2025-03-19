import numpy as np

def code_execution(input_grid, actual_output, expected_output):
    """
    Executes code to compare outputs, count differences, and find azure shapes.
    """

    # Difference grids
    diff_actual_expected = np.where(actual_output != expected_output, 1, 0)

    # difference pixels
    diff_pixels_ae = np.sum(diff_actual_expected)

    # azure object counts
    azure_objects_input = len(find_objects(input_grid, 8))

    results = {
        'diff_pixels_ae': int(diff_pixels_ae),
        'azure_objects_input': azure_objects_input,
    }
    return results

# Example data (replace with actual example data)
examples = [
    {
        'input': np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 8, 8, 8, 8, 0, 0],
            [0, 8, 8, 8, 8, 8, 0, 0],
            [0, 8, 8, 8, 8, 8, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0]
        ]),
        'expected': np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 8, 8, 8, 8, 0, 0],
            [0, 8, 8, 8, 8, 8, 0, 0],
            [0, 8, 8, 8, 8, 8, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 1]
        ]),
        'actual': np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 8, 8, 8, 8, 0, 0],
            [0, 8, 8, 8, 8, 8, 0, 0],
            [0, 8, 8, 8, 8, 8, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 1]
        ])
    },
      {
        'input': np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 8, 8, 0, 0, 0, 0],
            [0, 8, 8, 8, 0, 0, 0, 0],
            [0, 8, 8, 8, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 0]
        ]),
        'expected': np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 8, 8, 0, 0, 0, 0],
            [0, 8, 8, 8, 0, 0, 0, 0],
            [0, 8, 8, 8, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 1]
        ]),
        'actual': np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 8, 8, 0, 0, 0, 0],
            [0, 8, 8, 8, 0, 0, 0, 0],
            [0, 8, 8, 8, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 1, 1]
        ])
    },
    {
        'input': np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 8, 8, 8, 8, 0, 0],
            [0, 8, 8, 8, 8, 8, 0, 0],
            [0, 8, 8, 8, 8, 8, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 0, 0]
        ]),
        'expected': np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 8, 8, 8, 8, 0, 0],
            [0, 8, 8, 8, 8, 8, 0, 0],
            [0, 8, 8, 8, 8, 8, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 1, 0]
        ]),
        'actual': np.array([
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 8, 8, 8, 8, 8, 0, 0],
            [0, 8, 8, 8, 8, 8, 0, 0],
            [0, 8, 8, 8, 8, 8, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 2, 0, 0]
        ])
    }
]

results = [code_execution(ex['input'], ex['actual'], ex['expected']) for ex in examples]
print(results)
