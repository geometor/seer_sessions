import numpy as np

def analyze_example(input_grid, output_grid, predicted_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)
    predicted_grid = np.array(predicted_grid)

    metrics = {
        "input_grid_size": input_grid.shape,
        "output_grid_size": output_grid.shape,
        "pixel_changes": {},
        "correct_transformations": 0,
        "incorrect_transformations": 0,
    }

    for i in range(input_grid.shape[0]):
        for j in range(input_grid.shape[1]):
            if input_grid[i, j] != output_grid[i, j]:
                metrics["pixel_changes"][(i, j)] = (
                    input_grid[i, j],
                    output_grid[i, j],
                )
            if predicted_grid.shape == output_grid.shape:  # Ensure shapes are compatible for comparison
                if predicted_grid[i,j] == output_grid[i,j]:
                    metrics["correct_transformations"] +=1
                else:
                    metrics["incorrect_transformations"] +=1

    return metrics

# Example Usage (replace with actual data from task)
task_data = {
    "train": [
        {
            "input": [[5, 0, 5], [0, 5, 0], [5, 0, 5]],
            "output": [[3, 4, 3], [4, 3, 4], [3, 4, 3]],
        },
        {
            "input": [[0, 5, 0, 5, 0], [5, 0, 5, 0, 5], [0, 5, 0, 5, 0]],
            "output": [[4, 3, 4, 3, 4], [3, 4, 3, 4, 3], [4, 3, 4, 3, 4]],
        },
                {
            "input": [[0, 5, 0, 5, 0,5,0], [5, 0, 5, 0, 5,0,5], [0, 5, 0, 5, 0,5,0], [0, 5, 0, 5, 0,5,0]],
            "output": [[4, 3, 4, 3, 4,3,4], [3, 4, 3, 4, 3,4,3], [4, 3, 4, 3, 4,3,4],[4, 3, 4, 3, 4,3,4]],
        },
    ]
}

previous_code = """
import numpy as np

def transform(input_grid):
    output_grid = np.copy(input_grid)
    for i in range(output_grid.shape[0]):
        for j in range(output_grid.shape[1]):
            if output_grid[i, j] == 0:
                output_grid[i, j] = 4
            elif output_grid[i, j] == 5:
                output_grid[i, j] = 3
    return output_grid
"""
exec(previous_code)

results = []
for example in task_data["train"]:
    predicted_output = transform(example["input"])
    analysis = analyze_example(example["input"], example["output"], predicted_output)
    results.append(analysis)

for i, result in enumerate(results):
    print(f"Example {i+1}:")
    print(result)
