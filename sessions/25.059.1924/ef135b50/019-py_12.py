def analyze_results(task_name, input_grid, output_grid, predicted_output):
    print(f"--- Analysis of {task_name} ---")
    print(f"Input Grid:\n{input_grid}")
    print(f"Expected Output Grid:\n{output_grid}")
    print(f"Predicted Output Grid:\n{predicted_output}")
    correct = np.array_equal(output_grid, predicted_output)
    print(f"{task_name} correct: {correct}")

    mismatches = np.where(output_grid != predicted_output)
    num_mismatches = len(mismatches[0])
    print(f"Number of mismatches: {num_mismatches}")

    for i in range(num_mismatches):
        row = mismatches[0][i]
        col = mismatches[1][i]
        print(f"Mismatch at ({row}, {col}): Expected {output_grid[row, col]}, Predicted {predicted_output[row, col]}")

    input_white_pixels = np.where(input_grid == 0)
    num_input_white_pixels = len(input_white_pixels[0])
    print(f"Number of white pixels in input: {num_input_white_pixels}")

    output_white_pixels = np.where(output_grid == 0)
    num_output_white_pixels = len(output_white_pixels[0])
    print(f"Number of white pixels in output: {num_output_white_pixels}")

    predicted_white_pixels = np.where(predicted_output == 0)
    num_predicted_white_pixels = len(predicted_white_pixels[0])
    print(f"Number of white pixels in predicted: {num_predicted_white_pixels}")

    input_maroon_pixels = np.where(input_grid == 9)
    num_input_maroon_pixels = len(input_maroon_pixels[0])
    print(f"Number of maroon pixels in input: {num_input_maroon_pixels}")

    output_maroon_pixels = np.where(output_grid == 9)
    num_output_maroon_pixels = len(output_maroon_pixels[0])
    print(f"Number of maroon pixels in output: {num_output_maroon_pixels}")

    predicted_maroon_pixels = np.where(predicted_output == 9)
    num_predicted_maroon_pixels = len(predicted_maroon_pixels[0])
    print(f"Number of maroon pixels in predicted: {num_predicted_maroon_pixels}")

import numpy as np
from task_079010a9 import train

# the previous code is in the file, so we can use transform directly
for i, example in enumerate(train):
    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])
    predicted_output = transform(input_grid)
    analyze_results(f"train_{i}", input_grid, output_grid, predicted_output)
