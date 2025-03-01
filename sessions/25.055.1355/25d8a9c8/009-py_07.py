import numpy as np
examples = [
    {
        "input": np.array([[8, 1, 8], [1, 8, 1], [8, 1, 8]]),
        "output": np.array([[0, 0, 0], [5, 5, 5], [0, 0, 0]]),
    },
    {
        "input": np.array([[8, 8, 8, 8], [8, 1, 1, 8], [8, 8, 8, 8]]),
        "output": np.array([[0, 0, 0, 0], [5, 5, 5, 5], [0, 0, 0, 0]]),
    },
    {
        "input": np.array([[1, 8, 3, 8], [8, 3, 8, 1], [3, 8, 1, 8], [8, 1, 8, 3]]),
        "output": np.array([[0, 0, 0, 0], [5, 5, 5, 5], [0, 0, 0, 0], [0, 0, 0, 0]]),
    },
]

transform_code = """
import numpy as np

def transform(input_grid):
    # Initialize the output grid with the same dimensions as the input, filled with white (0).
    output_grid = np.zeros_like(input_grid)

    # Get the middle row index.
    middle_row_index = input_grid.shape[0] // 2

    # Change the middle row to gray (5).
    output_grid[middle_row_index, :] = 5
    
    return output_grid
"""

results = []
for i, example in enumerate(examples):
    result = code_execution(transform_code, {"input_grid": example["input"]})
    results.append(
        {
            "example": i + 1,
            "input_shape": example["input"].shape,
            "output_shape": example["output"].shape,
            "predicted_output": result["locals"]["output_grid"].tolist()
            if result["success"]
            else None,
            "expected_output": example["output"].tolist(),
            "correct": np.array_equal(
                result["locals"]["output_grid"], example["output"]
            )
            if result["success"]
            else False,
        }
    )
for r in results:
    print(r)
