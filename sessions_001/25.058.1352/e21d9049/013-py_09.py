import numpy as np

def code_execution(input_grid, expected_output, predicted_output):
    input_grid = np.array(input_grid)
    expected_output = np.array(expected_output)
    predicted_output = np.array(predicted_output)

    correct = np.array_equal(expected_output, predicted_output)
    input_pixels = input_grid.size
    output_pixels = expected_output.size
    predicted_pixels = predicted_output.size
    correct_pixels = np.sum(expected_output == predicted_output) if not correct else output_pixels
    accuracy = (correct_pixels / output_pixels) * 100 if output_pixels > 0 else 0.0

    print(f"  Correct: {correct}")
    print(f"  Input Pixels: {input_pixels}")
    print(f"  Output Pixels: {output_pixels}")
    print(f"  Predicted Pixels: {predicted_pixels}")
    print(f"  Correct Pixels: {correct_pixels}")
    print(f"  Accuracy: {accuracy:.2f}%")

# Example Data (replace with actual data from the ARC task)
example_data = [
  {
        "input": [[5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5]],
        "output": [[5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5, 5]],
    },
    {
        "input": [[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]],
        "output": [[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]],
    },
     {
        "input":  [[1, 0, 2, 0, 3, 0, 4, 0],
 [0, 0, 0, 0, 0, 0, 0, 0],
 [5, 0, 6, 0, 7, 0, 8, 0],
 [0, 0, 0, 0, 0, 0, 0, 0],
 [9, 0, 1, 0, 2, 0, 3, 0]],
        "output": [[1, 0, 2, 0, 3, 0, 4, 0],
 [0, 0, 0, 0, 0, 0, 0, 0],
 [5, 0, 6, 0, 7, 0, 8, 0],
 [0, 0, 0, 0, 0, 0, 0, 0],
 [9, 0, 1, 0, 2, 0, 3, 0]],
    },
    {
        "input": [[7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7]],
        "output": [[7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7]]
    },
    {
        "input" : [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]],
        "output": [[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]]
    }
]

from previous_response import transform
for i, example in enumerate(example_data):
    input_grid = example['input']
    expected_output = example['output']
    predicted_output = transform(input_grid)
    print(f"Example {i+1}:")
    code_execution(input_grid, expected_output, predicted_output)
    print("-" * 20)
