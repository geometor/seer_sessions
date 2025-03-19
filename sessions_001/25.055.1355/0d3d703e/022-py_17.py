import numpy as np

# Example data (replace with your actual example data)
examples = [
    {
        "input": np.array([[9, 9, 9], [9, 9, 9], [9, 9, 9]]),
        "output": np.array([[8, 8, 8], [8, 8, 8], [8, 8, 8]])
    },
     {
        "input": np.array([[4, 4, 4], [4, 4, 4], [4, 4, 4]]),
        "output": np.array([[3, 3, 3], [3, 3, 3], [3, 3, 3]])
    },
    {
        "input": np.array([[4, 9, 4], [2, 9, 4], [4, 4, 9]]),
        "output": np.array([[3, 8, 3], [6, 8, 3], [3, 3, 8]])
    },
    {
        "input": np.array([[1, 9, 1], [1, 9, 1], [1, 9, 1]]),
        "output": np.array([[1, 8, 1], [1, 8, 1], [1, 8, 1]])
    },
    {
        "input": np.array([[2, 9, 2], [4, 9, 4], [2, 9, 2]]),
        "output": np.array([[6, 8, 6], [3, 8, 3], [6, 8, 6]])
    }

]
# color changes
color_changes = {}

for example in examples:
    input_grid = example['input']
    output_grid = example['output']
    for input_val, output_val in zip(input_grid.flatten(), output_grid.flatten()):
        if input_val != output_val:
            if input_val not in color_changes:
                color_changes[input_val] = {}
            color_changes[input_val][output_val]= color_changes[input_val].get(output_val,0) + 1
print(color_changes)
