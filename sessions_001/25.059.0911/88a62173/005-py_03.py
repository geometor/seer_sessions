import numpy as np

def transform(input_grid):
    # Create a NumPy array from the input grid for easier manipulation.
    input_np = np.array(input_grid)

    # Extract the top-left 2x2 sub-grid using array slicing.
    output_np = input_np[:2, :2]

    # Convert the NumPy array back to a list.
    output_grid = output_np.tolist()

    return output_grid

# Training examples provided in text:
train_examples = [
    {
        "input": [[5, 5], [5, 5]],
        "output": [[5, 5], [5, 5]],
    },
    {
        "input": [[5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5]],
        "output": [[5, 5], [5, 5]],
    },
    {
        "input": [[5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5], [5, 5, 5, 5]],
        "output": [[5, 5], [5, 5]],
    },
    {
        "input": [[5, 5, 5], [5, 5, 5]],
        "output": [[5, 5], [5, 5]],
    },
    {
        "input": [[5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5], [5, 5, 5, 5, 5]],
        "output": [[5, 5], [5, 5]],
    },
]

results = []
for i, example in enumerate(train_examples):
    predicted_output = transform(example["input"])
    correct = predicted_output == example["output"]
    results.append(
        {
            "example": i + 1,
            "input_shape": np.array(example["input"]).shape,
            "output_shape": np.array(example["output"]).shape,
            "predicted_output_shape": np.array(predicted_output).shape,
            "correct": correct,
        }
    )

print(results)