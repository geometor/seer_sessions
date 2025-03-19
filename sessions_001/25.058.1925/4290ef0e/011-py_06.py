import numpy as np

def summarize_grid(grid):
    """
    Provides a summary of a grid, including its dimensions and the unique colors present.
    """
    dimensions = grid.shape
    unique_colors = np.unique(grid)
    color_counts = {color: np.count_nonzero(grid == color) for color in unique_colors}
    return {
        "dimensions": dimensions,
        "unique_colors": unique_colors.tolist(),
        "color_counts": color_counts,
    }

def analyze_example(input_grid, output_grid, predicted_grid):
    """
    Analyzes a single example, comparing the expected output with the predicted output.

    """
    input_summary = summarize_grid(input_grid)
    output_summary = summarize_grid(output_grid)
    predicted_summary = summarize_grid(predicted_grid)
    correct = np.array_equal(output_grid,predicted_grid)

    return {
        "input": input_summary,
        "output": output_summary,
        "predicted": predicted_summary,
        "correct": correct
    }

# Example usage with the provided training data (assuming it's stored in a list called 'train_examples'):
# train_examples is a list of dictionaries.
# each dictionary has a key "input" for the input grid and a key "output" for the
# correct output grid.

train_examples = [
    {
        "input": np.array([
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [8, 8, 8, 8, 8, 8, 8, 1, 8, 8],
            [8, 8, 8, 8, 8, 8, 8, 1, 8, 8],
            [8, 8, 8, 8, 8, 8, 8, 1, 8, 8],
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [8, 8, 8, 8, 4, 4, 8, 8, 8, 8],
            [8, 8, 8, 8, 4, 4, 8, 8, 8, 8],
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [8, 8, 8, 8, 8, 8, 8, 8, 2, 8],
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
        ]),
        "output": np.array([
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 1, 0, 0, 0, 0],
            [0, 0, 1, 0, 4, 4, 0],
            [0, 0, 1, 0, 4, 4, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 2],
        ]),
    },
    {
        "input": np.array([
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 2],
        ]),
        "output": np.array([
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 2],
        ]),
    },
    {
       "input": np.array([
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 8],
            [8, 8, 8, 8, 8, 8, 8, 8, 8, 8, 3],
        ]),
        "output": np.array([
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 0],
            [0, 0, 0, 0, 0, 0, 3],
        ]),
    }
]

results = []
for example in train_examples:
    predicted_output = transform(example["input"])
    analysis = analyze_example(example["input"], example["output"], predicted_output)
    results.append(analysis)

for i, result in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Input Summary: {result['input']}")
    print(f"  Output Summary: {result['output']}")
    print(f"  Predicted Summary: {result['predicted']}")
    print(f"  Correct: {result['correct']}")
    print("-" * 20)