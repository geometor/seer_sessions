import numpy as np

def describe_grid(grid):
    shape = grid.shape
    colors = np.unique(grid)
    return f"Shape: {shape}, Colors: {colors}"

examples = task_data['train']
for i, example in enumerate(examples):
    input_grid = np.array(example['input'])
    output_grid = np.array(example['output'])
    print(f"Example {i+1}:")
    print(f"  Input: {describe_grid(input_grid)}")
    print(f"  Output: {describe_grid(output_grid)}")

    predicted_output = transform(input_grid)
    print(f"  Predicted: {describe_grid(predicted_output)}")

    #Check for match
    match = "yes" if np.array_equal(output_grid, predicted_output) else "no"
    print(f"  Output Match: {match}")
    
    #inspect column 1 of input
    print(f"  Input column 1: {input_grid[:,1]}")
    #inspect added rows of output
    if (input_grid.shape[0] < output_grid.shape[0]):
        print(f"  Output added rows:\n{output_grid[input_grid.shape[0]:,:]}")
    else:
        print("  no rows added")
