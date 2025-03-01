import numpy as np

def transform(input_grid):
    # Convert the input list of lists to a NumPy array for easier manipulation
    input_np_grid = np.array(input_grid)

    # Rotate the grid 90 degrees clockwise
    output_np_grid = np.rot90(input_np_grid, k=-1) # k=-1 for clockwise rotation

    # Convert the NumPy array back to a list of lists
    output_grid = output_np_grid.tolist()

    return output_grid

# Example data (replace with actual data from the task)
train_examples = [
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 8, 8, 8, 8, 0, 0], [0, 0, 0, 0, 8, 8, 8, 8, 0, 0], [0, 0, 0, 0, 8, 8, 8, 8, 0, 0], [0, 0, 0, 0, 8, 8, 8, 8, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 8, 8, 8, 8, 0, 0], [0, 0, 0, 0, 8, 8, 8, 8, 0, 0], [0, 0, 0, 0, 8, 8, 8, 8, 0, 0], [0, 0, 0, 0, 8, 8, 8, 8, 0, 0], [0, 0, 0, 0, 8, 8, 8, 8, 0, 0], [0, 0, 0, 0, 8, 8, 8, 8, 0, 0], [0, 0, 0, 0, 8, 8, 8, 8, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 8, 8, 8, 8, 0, 0], [0, 0, 0, 0, 8, 8, 8, 8, 0, 0], [0, 0, 0, 0, 8, 8, 8, 8, 0, 0], [0, 0, 0, 0, 8, 8, 8, 8, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 8, 8, 8, 8, 0, 0], [0, 0, 0, 0, 8, 8, 8, 8, 0, 0], [0, 0, 0, 0, 8, 8, 8, 8, 0, 0], [0, 0, 0, 0, 8, 8, 8, 8, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    },
    {
       "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 8, 8, 8, 8, 0, 0], [0, 0, 0, 0, 8, 8, 8, 8, 0, 0], [0, 0, 0, 0, 8, 8, 8, 8, 0, 0], [0, 0, 0, 0, 8, 8, 8, 8, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output" :[[0, 0, 0, 0, 8, 8, 8, 8, 0, 0], [0, 0, 0, 0, 8, 8, 8, 8, 0, 0], [0, 0, 0, 0, 8, 8, 8, 8, 0, 0], [0, 0, 0, 0, 8, 8, 8, 8, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    }
]

for i, example in enumerate(train_examples):
    input_grid = example["input"]
    correct_output_grid = example["output"]
    predicted_output_grid = transform(input_grid)
    print(f"Example {i+1}:")
    print(f"  Input Grid:\n{np.array(input_grid)}")
    print(f"  Correct Output Grid:\n{np.array(correct_output_grid)}")
    print(f"  Predicted Output Grid:\n{np.array(predicted_output_grid)}")
    print(f"  Correct? {predicted_output_grid == correct_output_grid}")
    print("-" * 20)
