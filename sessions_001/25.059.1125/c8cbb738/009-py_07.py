import numpy as np

def analyze_example(input_grid, expected_output, predicted_output):
    input_grid = np.array(input_grid)
    expected_output = np.array(expected_output)
    predicted_output = np.array(predicted_output)

    input_colors = np.unique(input_grid)
    output_colors = np.unique(expected_output)
    predicted_colors = np.unique(predicted_output)

    print(f"  Input Colors: {input_colors}")
    print(f"  Expected Output Colors: {output_colors}")
    print(f"  Predicted Output Colors: {predicted_colors}")
    print(f"  Match: {np.array_equal(expected_output, predicted_output)}")

    # Check for contiguity within the predicted output.
    if predicted_output.size > 0: #avoid error
        coords = np.argwhere(predicted_output == predicted_output[0,0])
        if len(coords) > 1:
            row_diffs = np.diff(coords[:, 0])
            col_diffs = np.diff(coords[:, 1])
            if np.all(row_diffs <= 1) and np.all(col_diffs <= 1):
                print("  Predicted Output is Contiguous.")
            else:
                print("  Predicted Output is NOT Contiguous.")

# Example Usage (replace with actual data)
# Data from Task

examples = [
    {
        "input": [
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        ],
        "output": [[3]],
    },
    {
        "input": [
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        ],
        "output": [[3]],
    },
    {
        "input": [
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        ],
        "output": [[3]],
    },
     {
        "input": [
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 6, 6, 6, 3, 3, 3, 3, 3, 1, 3],
            [3, 6, 6, 6, 3, 3, 3, 3, 3, 1, 3],
            [3, 6, 6, 6, 3, 3, 3, 3, 3, 1, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 7, 7, 7, 3, 3, 3],
            [3, 3, 3, 3, 3, 7, 7, 7, 3, 3, 3],
        ],
        "output": [[3]],
    },
    {
        "input": [
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
            [3, 3, 3, 5, 5, 5, 5, 5, 3, 3, 3],
            [3, 3, 3, 5, 5, 5, 5, 5, 3, 3, 3],
            [3, 3, 3, 5, 5, 5, 5, 5, 3, 3, 3],
            [3, 3, 3, 5, 5, 5, 5, 5, 3, 3, 3],
            [3, 3, 3, 3, 3, 3, 3, 3, 3, 3, 3],
        ],
        "output": [[3]],
    },
]

for i, example in enumerate(examples):
  print(f"Example {i + 1}:")
  predicted = transform(example["input"])
  analyze_example(example["input"], example["output"], predicted)
  print("-" * 20)