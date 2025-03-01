import numpy as np

def analyze_results(examples, transform_function):
    results = []
    for i, (input_grid, expected_output_grid) in enumerate(examples):
        input_grid = np.array(input_grid)
        expected_output_grid = np.array(expected_output_grid)
        predicted_output_grid = np.array(transform_function(input_grid.tolist()))

        # check sizes match
        size_match = predicted_output_grid.shape == expected_output_grid.shape

        # compare pixel by pixel
        correct_pixels = np.sum(predicted_output_grid == expected_output_grid)
        total_pixels = expected_output_grid.size
        accuracy = correct_pixels / total_pixels if total_pixels > 0 else 0.0


        results.append({
            "example": i + 1,
            "input_shape": input_grid.shape,
            "expected_output_shape": expected_output_grid.shape,
            "predicted_output_shape": predicted_output_grid.shape,
            "size_match": size_match,
            "accuracy": accuracy,
            "correct_pixels": correct_pixels,
            "total_pixels": total_pixels
        })
    return results

# Assuming 'transform' function and 'task' variable (containing examples) are defined
examples = task["train"]

analysis = analyze_results(examples, transform)

for result in analysis:
    print(result)

