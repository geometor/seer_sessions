import numpy as np

# Example Data (replace with actual data from the task)
examples = [
    {
        "input": np.array([[0,0,0],[6,6,6],[0,0,0],[1,1,1],[0,0,0]]),
        "output": np.array([[6,6,6],[1,1,1]])
    },
    {
        "input": np.array([[0,0,0,0,0],[8,8,8,8,8],[0,0,0,0,0],[1,1,1,1,1],[0,0,0,0,0],[2,2,2,2,2]]),
        "output": np.array([[8,8,8,8,8],[1,1,1,1,1],[2,2,2,2,2]])
    },
    {
        "input": np.array([[0,0,0,0],[0,0,2,0],[0,0,0,0],[5,5,5,5],[0,0,0,0],[0,6,0,0],[0,0,0,0]]),
        "output": np.array([[0,0,2,0],[0,6,0,0]])
    },
    {
        "input": np.array([[0,0,0,0,0],[0,0,0,3,0],[0,0,0,0,0],[5,5,5,5,5],[0,0,0,0,0],[0,4,0,0,0],[0,0,0,0,0]]),
        "output": np.array([[0,0,0,3,0],[0,4,0,0,0]])
    },
    {
        "input": np.array([[0,0,0,0,0,0,0],[0,0,0,0,0,2,0],[0,0,0,0,0,0,0],[5,5,5,5,5,5,5],[0,0,0,0,0,0,0],[0,8,0,0,0,0,0],[0,0,0,0,0,0,0],[0,0,0,0,0,0,4]]),
        "output": np.array([[0,0,0,0,0,2,0],[0,8,0,0,0,0,0],[0,0,0,0,0,0,4]])
    }
]

results = []

for i, example in enumerate(examples):
    input_grid = example['input']
    expected_output = example['output']
    predicted_output = transform(input_grid)  # Assuming 'transform' is your function
    is_correct = np.array_equal(predicted_output, expected_output)
    results.append({
        "example_index": i,
        "input_shape": input_grid.shape,
        "output_shape": expected_output.shape,
        "predicted_output_shape": predicted_output.shape,
        "is_correct": is_correct,
        "predicted_output": predicted_output.tolist(),  # For easy viewing
        "expected_output": expected_output.tolist()
    })

for result in results:
    print(result)
