import numpy as np

def analyze_transformation(input_grid, expected_output, transformed_output):
    input_grid = np.array(input_grid)
    expected_output = np.array(expected_output)
    transformed_output = np.array(transformed_output)

    input_shape = input_grid.shape
    expected_shape = expected_output.shape
    transformed_shape = transformed_output.shape

    correct_pixels = np.sum(expected_output == transformed_output)
    total_pixels = expected_output.size
    incorrect_pixels = total_pixels - correct_pixels
    accuracy = correct_pixels / total_pixels if total_pixels > 0 else 0.0

    color_palette_expected = set(np.unique(expected_output))
    color_palette_transformed = set(np.unique(transformed_output))
    color_palette_match = color_palette_expected == color_palette_transformed

    return {
        'input_shape': input_shape,
        'expected_shape': expected_shape,
        'transformed_shape': transformed_shape,
        'correct_pixels': correct_pixels,
        'incorrect_pixels': incorrect_pixels,
        'accuracy': accuracy,
        'color_palette_expected': color_palette_expected,
        'color_palette_transformed': color_palette_transformed,
        'color_palette_match': color_palette_match
    }