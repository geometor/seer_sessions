import numpy as np

def evaluate_transformation(transform_func, examples):
    results = []
    for example in examples:
        input_grid = example['input']
        expected_output_grid = example['output']
        actual_output_grid = transform_func(input_grid)

        input_shape = np.array(input_grid).shape
        expected_output_shape = np.array(expected_output_grid).shape
        actual_output_shape = np.array(actual_output_grid).shape

        shapes_equal = expected_output_shape == actual_output_shape
        arrays_equal = np.array_equal(np.array(expected_output_grid), np.array(actual_output_grid))
        results.append({
            'input_shape': input_shape,
            'expected_output_shape': expected_output_shape,
            'actual_output_shape': actual_output_shape,
            'shapes_equal': shapes_equal,
            'arrays_equal': arrays_equal
        })
    return results