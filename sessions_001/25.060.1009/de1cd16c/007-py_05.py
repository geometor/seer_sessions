import numpy as np

def get_color_counts(grid):
    """Counts the occurrences of each unique color in a grid."""
    unique_colors, counts = np.unique(grid, return_counts=True)
    return dict(zip(unique_colors, counts))

#Example Usage for first three examples.
training_examples = [
    {
        "input": [[5, 5, 5], [5, 5, 5], [5, 5, 5]],
        "output": [[5]]
    },
    {
        "input": [[0, 0, 0], [0, 7, 0], [0, 0, 0]],
        "output": [[7]]
    },
       {
        "input": [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 1, 1, 1, 0], [0, 0, 0, 0, 0]],
        "output": [[1]]
    },
]

for i, example in enumerate(training_examples):
    input_grid = example["input"]
    output_grid = example["output"]
    input_color_counts = get_color_counts(np.array(input_grid))
    output_color_counts = get_color_counts(np.array(output_grid))

    print(f"Example {i+1}:")
    print(f"  Input Color Counts: {input_color_counts}")
    print(f"  Output Color Counts: {output_color_counts}")
    print("-" * 20)