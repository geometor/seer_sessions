import numpy as np

def code_execution(input_grid, predicted_output, true_output):
    print("Input Grid:")
    print(input_grid)
    print("\nPredicted Output:")
    print(predicted_output)
    print("\nTrue Output:")
    print(true_output)
    print("\nCorrect Prediction:", np.array_equal(predicted_output, true_output))

# Example usage with the provided training data (replace with actual data)

training_examples = [
    (np.array([[7, 7, 7, 7, 7, 7, 7, 7, 7],
               [7, 7, 7, 7, 7, 7, 7, 7, 7],
               [7, 7, 7, 7, 7, 7, 7, 7, 7],
               [7, 7, 7, 1, 1, 1, 7, 7, 7],
               [7, 7, 7, 1, 1, 1, 7, 7, 7],
               [7, 7, 7, 1, 1, 1, 7, 7, 7],
               [7, 7, 7, 7, 7, 7, 7, 7, 7],
               [7, 7, 7, 7, 7, 7, 7, 7, 7],
               [7, 7, 7, 7, 7, 7, 7, 7, 7]]),
     np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5],
               [5, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5],
               [5, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5],
               [5, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5],
               [5, 7, 7, 7, 1, 1, 1, 7, 7, 7, 5],
               [5, 7, 7, 7, 1, 1, 1, 7, 7, 7, 5],
               [5, 7, 7, 7, 1, 1, 1, 7, 7, 7, 5],
               [5, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5],
               [5, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5],
               [5, 7, 7, 7, 7, 7, 7, 7, 7, 7, 5],
               [5, 5, 5, 5, 5, 5, 5, 5, 5, 5, 5]])),
    (np.array([[8, 0, 0, 0, 0, 8, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 0, 1, 1, 1, 0, 0],
               [0, 0, 1, 1, 1, 0, 0],
               [0, 0, 1, 1, 1, 0, 0],
               [0, 0, 0, 0, 0, 0, 0],
               [0, 3, 0, 0, 0, 3, 0]]),
     np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5],
               [5, 8, 0, 0, 0, 0, 8, 0, 5],
               [5, 0, 0, 0, 0, 0, 0, 0, 5],
               [5, 0, 0, 1, 1, 1, 0, 0, 5],
               [5, 0, 0, 1, 1, 1, 0, 0, 5],
               [5, 0, 0, 1, 1, 1, 0, 0, 5],
               [5, 0, 0, 0, 0, 0, 0, 0, 5],
               [5, 0, 3, 0, 0, 0, 3, 0, 5],
               [5, 5, 5, 5, 5, 5, 5, 5, 5]])),
    (np.array([[6, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 2],
               [0, 0, 1, 1, 1, 0, 0],
               [0, 0, 1, 1, 1, 0, 0],
               [0, 0, 1, 1, 1, 0, 0],
               [4, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0]]),
     np.array([[5, 5, 5, 5, 5, 5, 5, 5, 5],
               [5, 6, 0, 0, 0, 0, 0, 0, 5],
               [5, 0, 0, 0, 0, 0, 0, 2, 5],
               [5, 0, 0, 1, 1, 1, 0, 0, 5],
               [5, 0, 0, 1, 1, 1, 0, 0, 5],
               [5, 0, 0, 1, 1, 1, 0, 0, 5],
               [5, 4, 0, 0, 0, 0, 0, 0, 5],
               [5, 0, 0, 0, 0, 0, 0, 0, 5],
               [5, 5, 5, 5, 5, 5, 5, 5, 5]]))
]

from previous_code import transform

for input_grid, true_output in training_examples:
    predicted_output = transform(input_grid)
    code_execution(input_grid, predicted_output, true_output)
    print("-" * 30)

