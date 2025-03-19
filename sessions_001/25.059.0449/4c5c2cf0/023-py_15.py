import numpy as np

# Provided transform function and helper functions (find_object) would be here

def calculate_mismatched_pixels(predicted_output, expected_output):
    """Calculates the number of mismatched pixels between two grids."""
    return np.sum(predicted_output != expected_output)

# Dummy data for demonstration (replace with actual task data). I will use actual data from the files, once.
train_data = [
    {
        "input": np.array([[8, 8, 8, 0, 0],
                           [8, 8, 8, 0, 0],
                           [8, 8, 8, 0, 0],
                           [0, 0, 0, 1, 0],
                           [0, 0, 0, 0, 0]]),
        "output": np.array([[8, 8, 8, 0, 0, 0, 0, 0],
                            [8, 8, 8, 0, 0, 0, 0, 0],
                            [8, 8, 8, 0, 0, 0, 0, 0],
                            [0, 0, 0, 1, 0, 0, 1, 0],
                            [0, 0, 0, 0, 0, 0, 0, 0]])
    },
    {
        "input": np.array([[8, 8, 8, 8, 0, 0, 0],
                           [8, 8, 8, 8, 0, 0, 0],
                           [8, 8, 8, 8, 0, 0, 1],
                           [8, 8, 8, 8, 0, 0, 0]]),
        "output": np.array([[8, 8, 8, 8, 0, 0, 0, 1, 0, 0, 0],
                            [8, 8, 8, 8, 0, 0, 0, 0, 0, 0, 0],
                            [8, 8, 8, 8, 0, 0, 1, 1, 0, 0, 0],
                            [8, 8, 8, 8, 0, 0, 0, 0, 0, 0]])
    },
    {
         "input": np.array([[0, 0, 0, 0, 0, 8, 8, 8],
                            [0, 0, 0, 0, 0, 8, 8, 8],
                            [0, 1, 0, 0, 0, 8, 8, 8],
                            [0, 0, 0, 0, 0, 8, 8, 8],
                            [0, 0, 0, 0, 0, 8, 8, 8]]),
        "output": np.array([[0, 0, 0, 0, 0, 8, 8, 8, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 8, 8, 8, 0, 0, 0, 0, 0],
                            [0, 1, 0, 0, 0, 8, 8, 8, 0, 0, 0, 1, 0],
                            [0, 0, 0, 0, 0, 8, 8, 8, 0, 0, 0, 0, 0],
                            [0, 0, 0, 0, 0, 8, 8, 8, 0, 0, 0, 0, 0]])
    }
]

mismatched_counts = []
for example in train_data:
  predicted = transform(example["input"])
  mismatched = calculate_mismatched_pixels(predicted, example["output"])
  mismatched_counts.append(mismatched)
print(mismatched_counts)