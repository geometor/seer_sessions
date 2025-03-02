import numpy as np

def analyze_example(input_grid, output_grid, predicted_output):
    white_pixels = np.sum(input_grid == 0)
    yellow_pixels_input = np.sum(input_grid == 4)
    yellow_pixels_output = np.sum(output_grid == 4)
    magenta_pixels_input = np.sum(input_grid == 6)
    magenta_pixels_output = np.sum(output_grid == 6)
    predicted_matches_output = np.array_equal(predicted_output, output_grid)

    print(f"  White Pixels: {white_pixels}")
    print(f"  Yellow Pixels (Input): {yellow_pixels_input}")
    print(f"  Yellow Pixels (Output): {yellow_pixels_output}")
    print(f"  Magenta Pixels (Input): {magenta_pixels_input}")
    print(f"  Magenta Pixels (Output): {magenta_pixels_output}")
    print(f"  Predicted Output Matches Expected Output: {predicted_matches_output}")

# Assuming 'task' variable holds the task data, as in the testing environment
for i, example in enumerate(task["train"]):
    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])
    predicted_output = transform(input_grid)
    print(f"Example {i+1}:")
    analyze_example(input_grid, output_grid, predicted_output)
