# Conceptual code for analysis - I cannot actually execute this.
import numpy as np

def analyze_results(input_grid, expected_output, predicted_output):
    print("Input Grid:")
    print(input_grid)
    print("Expected Output:")
    print(expected_output)
    print("Predicted Output:")
    print(predicted_output)

    diff = (expected_output != predicted_output).astype(int)
    print("Difference (Expected - Predicted):")
    print(diff)

    num_mismatched_pixels = np.sum(diff)
    print(f"Number of mismatched pixels: {num_mismatched_pixels}")
    print("-" * 20)

# Example usage (replace with actual data loading)
task_examples = [
# example format: (input, expected output)
    (np.array([[0,0,0,0,0],
               [0,1,1,1,0],
               [0,1,0,1,0],
               [0,1,1,1,0],
               [0,0,0,0,0],
               [0,1,1,1,0],
               [0,1,0,1,0],
               [0,1,1,1,0]]),
     np.array([[0,0,0,0,0],
               [0,1,1,1,0],
               [0,1,7,1,0],
               [0,1,1,1,0],
               [0,0,0,0,0],
               [0,1,1,1,0],
               [0,1,2,1,0],
               [0,1,1,1,0]])),
      (np.array([[0,0,0,0,0,0],
               [0,1,1,1,1,0],
               [0,1,0,0,1,0],
               [0,1,0,0,1,0],
               [0,1,1,1,1,0],
               [0,1,0,1,0,0],
               [0,1,1,1,0,0]]),
     np.array([[0,0,0,0,0,0],
               [0,1,1,1,1,0],
               [0,1,7,7,1,0],
               [0,1,7,7,1,0],
               [0,1,1,1,1,0],
               [0,1,2,1,0,0],
               [0,1,1,1,0,0]])),
      (np.array([[0,0,0,0,0,0,0],
               [0,0,1,1,1,0,0],
               [0,0,1,0,1,0,0],
               [0,0,1,1,1,0,0],
               [0,1,1,1,1,1,0],
               [0,1,0,0,0,1,0],
               [0,1,0,0,0,1,0],
               [0,1,1,1,1,1,0]]),
     np.array([[0,0,0,0,0,0,0],
               [0,0,1,1,1,0,0],
               [0,0,1,7,1,0,0],
               [0,0,1,1,1,0,0],
               [0,1,1,1,1,1,0],
               [0,1,2,2,2,1,0],
               [0,1,2,2,2,1,0],
               [0,1,1,1,1,1,0]]))
]

for i, (input_grid, expected_output) in enumerate(task_examples):

    predicted_output = transform(np.copy(input_grid))  # Use the provided transform function
    print(f"Analysis for Example {i + 1}:")
    analyze_results(input_grid, expected_output, predicted_output)