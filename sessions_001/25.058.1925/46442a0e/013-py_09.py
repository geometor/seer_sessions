import numpy as np

def code_execution(input_grid, expected_output, generated_output):
    input_np = np.array(input_grid)
    expected_np = np.array(expected_output)
    generated_np = np.array(generated_output)

    input_shape = input_np.shape
    expected_shape = expected_np.shape
    generated_shape = generated_np.shape

    correct = np.array_equal(expected_np, generated_np)

    print(f"Input Shape: {input_shape}")
    print(f"Expected Output Shape: {expected_shape}")
    print(f"Generated Output Shape: {generated_shape}")
    print(f"Correct: {correct}")

task = {
    "train": [
        {
            "input": [[8, 5, 1], [5, 0, 5], [1, 5, 8]],
            "output": [
                [8, 8, 5, 5, 1, 1, 1, 1, 5, 5, 8, 8],
                [8, 8, 5, 5, 1, 1, 1, 1, 5, 5, 8, 8],
                [5, 5, 0, 0, 5, 5, 5, 5, 0, 0, 5, 5],
                [5, 5, 0, 0, 5, 5, 5, 5, 0, 0, 5, 5],
                [1, 1, 5, 5, 8, 8, 8, 8, 5, 5, 1, 1],
                [1, 1, 5, 5, 8, 8, 8, 8, 5, 5, 1, 1],
                [1, 1, 5, 5, 8, 8, 8, 8, 5, 5, 1, 1],
                [1, 1, 5, 5, 8, 8, 8, 8, 5, 5, 1, 1],
                [5, 5, 0, 0, 5, 5, 5, 5, 0, 0, 5, 5],
                [5, 5, 0, 0, 5, 5, 5, 5, 0, 0, 5, 5],
                [8, 8, 5, 5, 1, 1, 1, 1, 5, 5, 8, 8],
                [8, 8, 5, 5, 1, 1, 1, 1, 5, 5, 8, 8],
            ],
        },
        {
            "input": [[8, 5, 1]],
            "output": [
                [8, 8, 5, 5, 1, 1, 1, 1, 5, 5, 8, 8],
                [8, 8, 5, 5, 1, 1, 1, 1, 5, 5, 8, 8],
            ],
        },
        {
            "input": [[8], [5], [1]],
            "output": [[8, 8, 8, 8], [8, 8, 8, 8], [5, 5, 5, 5], [5, 5, 5, 5], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [1, 1, 1, 1], [5, 5, 5, 5], [5, 5, 5, 5], [8, 8, 8, 8], [8, 8, 8, 8]],
        },
    ],
    "test": [{"input": [[0, 5, 7], [5, 8, 5], [7, 5, 0]], "output": []}],
}

def transform(input_grid):
    # Create a numpy array from the input grid
    input_array = np.array(input_grid)

    # Get the dimensions of the input grid
    rows, cols = input_array.shape

    # 1. Duplicate each cell to create a 2x2 block.
    duplicated_array = np.repeat(np.repeat(input_array, 2, axis=0), 2, axis=1)
    
    # 2. Mirror horizontally.
    mirrored_horizontal = np.fliplr(duplicated_array)
    
    # 3. Concatenate the original duplicated array with its horizontal mirror.
    intermediate_result = np.hstack((duplicated_array, mirrored_horizontal))

    # 4. Mirror vertically.
    mirrored_vertical = np.flipud(intermediate_result)

    # 5. Concatenate the intermediate result with its vertical mirror.
    output_array = np.vstack((intermediate_result, mirrored_vertical))

    return output_array.tolist()


for i, example in enumerate(task["train"]):
    input_grid = example["input"]
    expected_output = example["output"]
    generated_output = transform(input_grid)

    print(f"Example {i + 1}:")
    code_execution(input_grid, expected_output, generated_output)
    print("-" * 20)
