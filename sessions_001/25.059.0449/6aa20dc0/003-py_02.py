import numpy as np

def compare_grids(predicted_output, expected_output):
    """
    Compares two grids and returns the coordinates and values where they differ.
    """
    predicted_output = np.array(predicted_output)
    expected_output = np.array(expected_output)

    if predicted_output.shape != expected_output.shape:
        return "Shapes are different", predicted_output.shape, expected_output.shape

    differences = []
    for r in range(predicted_output.shape[0]):
        for c in range(predicted_output.shape[1]):
            if predicted_output[r, c] != expected_output[r, c]:
                differences.append(
                    {
                        "row": r,
                        "col": c,
                        "predicted": int(predicted_output[r, c]),
                        "expected": int(expected_output[r, c]),
                    }
                )
    return differences

# Example usage (assuming 'transform' function and example data are available)
task = {
    "train": [
        {
            "input": [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 2, 2, 2], [1, 1, 1, 1, 1, 1, 1, 2, 2, 2], [1, 1, 1, 1, 1, 1, 1, 2, 2, 2], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 3, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 8, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]],
            "output": [[1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 2, 2, 8], [1, 1, 1, 1, 1, 1, 1, 2, 2, 8], [1, 1, 1, 1, 1, 1, 1, 2, 2, 8], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 8, 3, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 8, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]
        },
        {
            "input": [[4, 4, 4, 4, 4, 4, 4, 4], [4, 2, 2, 4, 4, 6, 6, 4], [4, 2, 2, 4, 4, 6, 6, 4], [4, 4, 4, 4, 4, 4, 4, 4], [4, 4, 4, 1, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4, 4, 4]],
            "output": [[4, 4, 4, 4, 4, 4, 4, 4], [4, 2, 2, 4, 4, 6, 6, 4], [4, 2, 2, 4, 4, 6, 6, 4], [4, 4, 4, 4, 4, 4, 4, 4], [4, 4, 4, 1, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4, 4, 4]]
        },
        {
            "input": [[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 3, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 4, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]],
            "output": [[8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 3, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 4, 8], [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8]]
        }
    ],
    "test": [
       {"input": [[7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 0, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7], [7, 7, 7, 7, 7, 7, 7, 6, 7], [7, 7, 7, 7, 7, 7, 7, 7, 7]]}
    ]
}

train_results = []
for example in task["train"]:
    predicted = transform(example["input"])
    differences = compare_grids(predicted, example["output"])
    train_results.append(
        {
            "input": example["input"],
            "expected_output": example["output"],
            "predicted_output": predicted,
            "differences": differences,
        }
    )

print(train_results)