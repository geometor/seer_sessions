import numpy as np

def describe_grid(grid):
    unique, counts = np.unique(grid, return_counts=True)
    color_counts = dict(zip(unique, counts))
    return color_counts

def analyze_results(task):
    results = []
    for example in task["train"]:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        predicted_output = transform(np.copy(input_grid))  # Use the provided transform function

        input_colors = describe_grid(input_grid)
        output_colors = describe_grid(output_grid)
        predicted_colors = describe_grid(predicted_output)

        correct = np.array_equal(output_grid, predicted_output)

        results.append({
            "example_id": example.get("id", "unknown"),
            "input_colors": input_colors,
            "output_colors": output_colors,
            "predicted_colors": predicted_colors,
            "correct": correct
        })
    return results

task = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0], [0, 0, 6, 0, 6, 0, 0], [0, 0, 0, 5, 0, 0, 0], [0, 6, 6, 6, 6, 6, 0], [0, 0, 0, 5, 0, 0, 0], [0, 0, 6, 0, 6, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0], [0, 0, 6, 0, 0, 0, 0], [0, 0, 6, 0, 0, 0, 0], [0, 6, 6, 0, 6, 6, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
            "id": "example_1",
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 6, 0, 0, 0], [0, 0, 0, 0, 6, 0, 0, 0], [0, 5, 5, 5, 6, 0, 0, 0], [0, 0, 0, 0, 6, 6, 6, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 6, 6, 6, 0, 0, 0], [0, 0, 0, 0, 6, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
            "id": "example_2",
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 6, 0], [0, 0, 0, 0, 0, 0, 0, 6, 0], [0, 0, 0, 0, 0, 0, 0, 6, 0], [0, 0, 0, 5, 5, 0, 6, 6, 6], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 6, 0, 0, 0, 0, 0], [0, 0, 0, 6, 0, 0, 0, 0, 0], [0, 0, 0, 6, 0, 0, 0, 0, 0], [0, 0, 0, 6, 6, 6, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "id": "example_3",
        },
    ]
}

results = analyze_results(task)
for result in results:
    print(result)