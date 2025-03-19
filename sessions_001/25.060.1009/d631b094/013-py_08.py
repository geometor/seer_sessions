import numpy as np

def analyze_grids(task):
    results = []
    for example in task["train"]:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        predicted_output = transform(input_grid.tolist())  # Use the provided transform function

        input_red_pixels = np.argwhere(input_grid == 2)
        output_red_pixels = np.argwhere(output_grid == 2)

        results.append({
            "input_shape": input_grid.shape,
            "output_shape": output_grid.shape,
            "input_red_count": len(input_red_pixels),
            "output_red_count": len(output_red_pixels),
            "predicted_output": predicted_output,
            "correct": np.array_equal(np.array(predicted_output), output_grid)
        })
    return results

task = {
    "train": [
        {
            "input": [[5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 2, 5], [5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 2]],
            "output": [[2, 2]]
        },
        {
            "input": [[0, 5, 0, 0, 0, 0, 5, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[2]]
        },
        {
            "input": [[1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 1, 1, 1], [1, 1, 1, 1, 1, 2, 1, 1]],
            "output": [[2]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[2]]
        },
        {
            "input": [[5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5]],
            "output": [[5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5], [5, 5, 5, 5, 5, 5, 5, 5]]
        }
    ]
}

results = analyze_grids(task)

for i, res in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Input Shape: {res['input_shape']}")
    print(f"  Output Shape: {res['output_shape']}")
    print(f"  Input Red Pixels: {res['input_red_count']}")
    print(f"  Output Red Pixels: {res['output_red_count']}")
    print(f"  Predicted Output Correct: {res['correct']}")
    print(f"  Predicted Output: {res['predicted_output']}")
    print("-" * 20)