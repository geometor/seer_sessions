import numpy as np

def analyze_example(example):
    input_grid = example['input']
    output_grid = example['output']
    input_array = np.array(input_grid)
    output_array = np.array(output_grid)
    input_height, input_width = input_array.shape
    output_height, output_width = output_array.shape
    first_col_match = np.array_equal(input_array[:, 0], output_array[:, 0])
    last_col_match = np.array_equal(input_array[:, -1], output_array[:, 1])

    middle_col_index = -1
    for i in range(input_width):
      if np.array_equal(input_array[:,i], output_array[:,2]):
        middle_col_index = i
        break;

    print(f"""
    Input shape: {input_height}x{input_width}
    Output shape: {output_height}x{output_width}
    First column matches: {first_col_match}
    Last column matches: {last_col_match}
    Middle column index in input: {middle_col_index}
    """)


task = {
    "train": [
        {
            "input": [[5, 0, 5, 0, 5, 0, 5, 5, 5], [5, 5, 0, 5, 0, 5, 0, 5, 5], [5, 0, 5, 0, 5, 5, 5, 5, 5], [5, 5, 0, 5, 0, 5, 0, 5, 5], [5, 0, 5, 0, 5, 0, 5, 5, 5]],
            "output": [[5, 5, 0], [5, 5, 5], [5, 5, 0], [5, 5, 5], [5, 5, 0]],
        },
        {
            "input": [[1, 8, 8, 8, 1, 1, 1, 1], [1, 8, 8, 8, 1, 1, 1, 1], [1, 8, 8, 8, 1, 1, 1, 1], [1, 8, 8, 8, 1, 1, 1, 1], [1, 8, 8, 8, 1, 1, 1, 1], [1, 8, 8, 8, 1, 1, 1, 1]],
            "output": [[1, 1, 8], [1, 1, 8], [1, 1, 8], [1, 1, 8], [1, 1, 8], [1, 1, 8]],
        },
        {
            "input": [[7, 0, 7, 7, 0, 7, 0, 7], [7, 0, 7, 7, 0, 7, 7, 7], [7, 0, 7, 7, 0, 7, 0, 7], [7, 0, 7, 7, 0, 7, 7, 7], [7, 0, 7, 7, 0, 7, 0, 7]],
            "output": [[7, 7, 0], [7, 7, 7], [7, 7, 0], [7, 7, 7], [7, 7, 0]],
        },
    ],
    "test": [{"input": [[0, 4, 4, 4, 4, 4, 0], [4, 0, 4, 4, 4, 0, 4], [4, 4, 0, 4, 0, 4, 4], [4, 0, 4, 4, 4, 0, 4], [0, 4, 4, 4, 4, 4, 0]], "output": [[0, 0, 4], [4, 4, 0], [4, 4, 0], [4, 4, 0], [0, 0, 4]]}],
}

for i, example in enumerate(task["train"]):
    print(f"Example {i+1}:")
    analyze_example(example)

print(f"Test Example:")
analyze_example(task["test"][0])