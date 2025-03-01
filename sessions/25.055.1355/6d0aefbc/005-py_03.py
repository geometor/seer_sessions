import numpy as np

def transform(input_grid):
    """
    Transforms the input grid by duplicating each column.

    Args:
        input_grid (list of lists): The input grid represented as a 2D list.

    Returns:
        list of lists: The transformed grid with duplicated columns.
    """
    # Convert the input list to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Get the dimensions of the input array.
    rows, cols = input_array.shape

    # Create a new array with doubled width.
    output_array = np.empty((rows, cols * 2), dtype=input_array.dtype)

    # Iterate through the columns of the input array.
    for i in range(cols):
        # Duplicate each column into the output array.
        output_array[:, 2*i] = input_array[:, i]
        output_array[:, 2*i + 1] = input_array[:, i]

    # Convert the NumPy array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid
    
def wrapped_transform(input_grid, expected_output):
    actual_output = transform(input_grid)
    print(f"Input:\n{input_grid}")
    print(f"Expected Output:\n{expected_output}")
    print(f"Actual Output:\n{actual_output}")
    print(f"Correct: {actual_output == expected_output}")
    return actual_output == expected_output


task = {
    "train": [
        {
            "input": [[5, 5, 5], [5, 5, 5], [5, 5, 5]],
            "output": [[5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5]]
        },
        {
            "input": [[5, 5, 8, 8, 5, 5], [5, 5, 8, 8, 5, 5]],
            "output": [[5, 5, 5, 5, 8, 8, 8, 8, 5, 5, 5, 5], [5, 5, 5, 5, 8, 8, 8, 8, 5, 5, 5, 5]]
        },
        {
            "input": [[7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7]],
            "output": [[7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]]
        },
        {
            "input": [[0, 0, 7, 7, 7, 7, 7, 7, 7], [0, 0, 7, 7, 7, 7, 7, 7, 7], [0, 0, 7, 7, 7, 7, 7, 7, 7], [0, 0, 7, 7, 7, 7, 7, 7, 7]],
            "output": [[0, 0, 0, 0, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [0, 0, 0, 0, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [0, 0, 0, 0, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7], [0, 0, 0, 0, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7]]
        },
        {
            "input": [[6, 6, 6, 6, 8, 8, 8, 8, 6, 6, 6, 6], [6, 6, 6, 6, 8, 8, 8, 8, 6, 6, 6, 6], [6, 6, 6, 6, 8, 8, 8, 8, 6, 6, 6, 6], [6, 6, 6, 6, 8, 8, 8, 8, 6, 6, 6, 6], [6, 6, 6, 6, 8, 8, 8, 8, 6, 6, 6, 6]],
            "output": [[6, 6, 6, 6, 6, 6, 6, 6, 8, 8, 8, 8, 8, 8, 8, 8, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 8, 8, 8, 8, 8, 8, 8, 8, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 8, 8, 8, 8, 8, 8, 8, 8, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 8, 8, 8, 8, 8, 8, 8, 8, 6, 6, 6, 6, 6, 6, 6, 6], [6, 6, 6, 6, 6, 6, 6, 6, 8, 8, 8, 8, 8, 8, 8, 8, 6, 6, 6, 6, 6, 6, 6, 6]]
        }
    ],
    "test": [
        {
            "input": [[5, 5, 8, 8, 8, 5, 5], [5, 5, 8, 8, 8, 5, 5], [5, 5, 8, 8, 8, 5, 5]],
            "output": [[5, 5, 5, 5, 8, 8, 8, 8, 8, 8, 5, 5, 5, 5], [5, 5, 5, 5, 8, 8, 8, 8, 8, 8, 5, 5, 5, 5], [5, 5, 5, 5, 8, 8, 8, 8, 8, 8, 5, 5, 5, 5]]
        }
    ]
}

for example in task["train"]:
    wrapped_transform(example["input"], example["output"])