# Example execution for metrics (Illustrative - for a real run, we'd use the provided execution environment)
import numpy as np

def calculate_accuracy(predicted, expected):
    predicted_arr = np.array(predicted)
    expected_arr = np.array(expected)
    if predicted_arr.shape != expected_arr.shape:
      return 0, 0, 0

    correct_pixels = np.sum(predicted_arr == expected_arr)
    total_pixels = predicted_arr.size
    accuracy = correct_pixels / total_pixels if total_pixels > 0 else 0
    return correct_pixels, total_pixels, accuracy

# Dummy data mimicking the task structure.  Replace with actual data in a real run.
examples = [
    {
        "input": [[5, 5, 5], [5, 1, 5], [5, 5, 5]],
        "output": [[5, 5], [5, 1]],
    },
   {
        "input": [[8, 8, 8, 8, 8], [8, 8, 5, 8, 8], [8, 8, 8, 2, 8], [8, 8, 8, 8, 8], [8, 8, 6, 8, 8]],
        "output": [[8, 8], [8, 5]]
    },
  {
        "input": [[6, 0, 6, 6, 0, 6, 6, 0, 6, 6, 0, 6, 6, 0, 6, 6], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [6, 0, 6, 6, 0, 6, 6, 0, 6, 6, 0, 6, 6, 0, 6, 6], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [6, 0, 6, 6, 0, 6, 6, 0, 6, 6, 0, 6, 6, 0, 6, 6], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [6, 0, 6, 6, 0, 6, 6, 0, 6, 6, 0, 6, 6, 0, 6, 6], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [6, 0, 6, 6, 0, 6, 6, 0, 6, 6, 0, 6, 6, 0, 6, 6], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [6, 0, 6, 6, 0, 6, 6, 0, 6, 6, 0, 6, 6, 0, 6, 6], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [6, 0, 6, 6, 0, 6, 6, 0, 6, 6, 0, 6, 6, 0, 6, 6], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [6, 0, 6, 6, 0, 6, 6, 0, 6, 6, 0, 6, 6, 0, 6, 6], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[6, 0], [0, 0]]
    },
   {
        "input": [[1, 0, 2, 4], [0, 0, 0, 0], [3, 0, 4, 5]],
        "output": [[1, 0], [0, 0]]
    }
]

for i, example in enumerate(examples):
  predicted_output = transform(example["input"])
  correct_pixels, total_pixels, accuracy = calculate_accuracy(predicted_output, example["output"])
  print(f"Example {i}: Input Shape: {np.array(example['input']).shape}, Output Shape: {np.array(example['output']).shape}, Correct Pixels: {correct_pixels}, Total Pixels: {total_pixels}, Accuracy: {accuracy}")
