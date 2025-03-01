import numpy as np

def analyze_example(input_grid, expected_output, predicted_output):
    input_shape = input_grid.shape
    input_orange_count = np.sum(input_grid == 7)
    input_magenta_count = np.sum(input_grid == 6)
    input_white_count = np.sum(input_grid==0)

    diff = expected_output - predicted_output
    diff_count = np.sum(diff != 0)
    

    print(f"  Input Shape: {input_shape}")
    print(f"  Input Orange Count: {input_orange_count}")
    print(f"  Input Magenta Count: {input_magenta_count}")
    print(f"  Input White Count: {input_white_count}")
    print(f"  Difference (pixels): {diff_count}")
    print(f"  Difference array:\n{diff}\n")

# provided data
examples = [
    {
        "input": [
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 7, 7, 7, 7, 0, 0],
            [0, 0, 7, 6, 6, 7, 0, 0],
            [0, 0, 7, 6, 6, 7, 0, 0],
            [0, 0, 7, 7, 7, 7, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ],
        "output": [
            [6, 6, 6, 6, 6, 6, 6, 6],
            [6, 6, 6, 6, 6, 6, 6, 6],
            [6, 6, 0, 0, 0, 0, 6, 6],
            [6, 6, 0, 7, 7, 0, 6, 6],
            [6, 6, 0, 7, 7, 0, 6, 6],
            [6, 6, 0, 0, 0, 0, 6, 6],
            [6, 6, 6, 6, 6, 6, 6, 6],
            [6, 6, 6, 6, 6, 6, 6, 6]
        ]
    },
    {
        "input": [
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 7, 7, 7, 7, 0, 0, 0],
            [0, 0, 0, 7, 6, 6, 7, 0, 0, 0],
            [0, 0, 0, 7, 6, 6, 7, 0, 0, 0],
            [0, 0, 0, 7, 7, 7, 7, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ],
        "output": [
            [6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
            [6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
            [6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
            [6, 6, 6, 0, 0, 0, 0, 6, 6, 6],
            [6, 6, 6, 0, 7, 7, 0, 6, 6, 6],
            [6, 6, 6, 0, 7, 7, 0, 6, 6, 6],
            [6, 6, 6, 0, 0, 0, 0, 6, 6, 6],
            [6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
            [6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
            [6, 6, 6, 6, 6, 6, 6, 6, 6, 6]
        ]
    }
]

# assume that transform(input) is available
for i, example in enumerate(examples):
    input_grid = np.array(example["input"])
    expected_output = np.array(example["output"])
    predicted_output = transform(input_grid)  # Apply the current transformation
    print(f"Example {i+1}:")
    analyze_example(input_grid, expected_output, predicted_output)
