import numpy as np

def analyze_results(task):
    print(f"Task: {task['name']}")
    results = []
    for example in task["train"]:
        input_grid = np.array(example['input'])
        expected_output_grid = np.array(example['output'])
        predicted_output_grid = transform(input_grid)  # Assuming 'transform' is defined as before

        # Basic grid info
        input_rows, input_cols = input_grid.shape
        output_rows, output_cols = expected_output_grid.shape

        # Compare expected and predicted outputs
        comparison = (expected_output_grid == predicted_output_grid)
        correct_pixels = np.sum(comparison)
        total_pixels = comparison.size  # Use .size for total elements, not shape
        accuracy = (correct_pixels / total_pixels) * 100 if total_pixels > 0 else 0.0

        results.append({
            'input_shape': (input_rows, input_cols),
            'output_shape': (output_rows, output_cols),
            'correct_pixels': correct_pixels,
            'total_pixels': total_pixels,
            'accuracy': accuracy
        })
    for i, res in enumerate(results):
        print(f"\nExample {i + 1}:")
        for k, v in res.items():
            print(f"  {k}: {v}")
    print("-" * 20)

# example of the task structure - replace as necessary
task1 = {
    "name": "Task 1",
    "train": [
        {
            "input": [[6, 0, 0, 6, 0], [0, 6, 0, 0, 6], [0, 0, 6, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
            "output": [[6, 0, 0, 6, 0], [0, 6, 0, 0, 6], [0, 0, 6, 0, 0], [0, 0, 0, 0, 0], [0, 0, 4, 0, 0]]
        },
        {
            "input": [[6, 0, 0, 0, 6], [0, 6, 0, 6, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
            "output": [[6, 0, 0, 0, 6], [0, 6, 0, 6, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [4, 0, 0, 0, 4]]
        },
		{
            "input": [[6, 6, 0, 0, 0], [6, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]],
            "output": [[6, 6, 0, 0, 0], [6, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [4, 4, 0, 0, 0]]
        }
    ]
}

analyze_results(task1)