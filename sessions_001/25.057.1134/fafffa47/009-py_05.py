import numpy as np

def describe_changes(input_grid, output_grid, predicted_grid):
    changes = []
    correct = np.array_equal(output_grid, predicted_grid)
    if not correct:
        diff = output_grid != predicted_grid
        diff_coords = np.where(diff)
        for r,c in zip(diff_coords[0], diff_coords[1]):
            changes.append({
              "row": int(r),
              "col": int(c),
              "output_val": int(output_grid[r, c]),
              "predicted_val": int(predicted_grid[r,c]),
            })
    return {
        "grid_dims": input_grid.shape,
        "correct": correct,
        "changes": changes,
    }

task_data = {
    "train": [
        {
            "input": np.array([[0, 0, 0, 0, 0, 0],
                               [0, 0, 9, 0, 0, 0],
                               [0, 9, 9, 9, 0, 0],
                               [0, 0, 9, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0]]),
            "output": np.array([[0, 0, 0],
                                [0, 2, 0],
                                [0, 2, 0]]),
        },
         {
            "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 6, 0, 0],
                                [0, 0, 0, 0, 6, 6, 6, 0],
                                [0, 0, 0, 0, 0, 6, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0],
                                [0, 0, 0, 0, 0, 0, 0, 0]]),
            "output": np.array([[0, 0, 0],
                                 [0, 2, 0],
                                 [0, 2, 0]]),
        },
        {
            "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 3, 0],
                              [0, 0, 0, 0, 0, 0, 3, 3, 3],
                              [0, 0, 0, 0, 0, 0, 0, 3, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0],
                              [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
            "output": np.array([[0, 0, 0],
                                [0, 2, 0],
                                [0, 2, 0]]),
        },
    ],
    "test": [
       {
            "input": np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0],
                               [0, 0, 0, 0, 0, 4, 0, 0, 0],
                               [0, 0, 0, 0, 4, 4, 4, 0, 0],
                               [0, 0, 0, 0, 0, 4, 0, 0, 0],
                               [0, 0, 0, 0, 0, 0, 0, 0, 0]]),
            "output": np.array([[0, 0, 0],
                                [0, 2, 0],
                                [0, 2, 0]]),

        }
    ]
}

# you can use this function in your response
def transform(input_grid):
    # Extract the top 3x3 sub-grid.
    sub_grid = input_grid[:3, :3]

    # Create an output grid initialized with white (0).
    output_grid = np.zeros_like(sub_grid)

    # Find the positions of maroon (9) pixels in the sub-grid.
    maroon_positions = np.where(sub_grid == 9)

    # Iterate through maroon positions and change them to red (2) in the output if they are in the center column.
    for r, c in zip(maroon_positions[0], maroon_positions[1]):
        if c == 1:
          output_grid[r,c] = 2
        else:
          output_grid[r,c] = 0

    # Fill any non-red cells with 0 in the center colum.
    for r in range(3):
      if output_grid[r,1] != 2:
        output_grid[r,1] = 0


    return output_grid

results = []
for example in task_data["train"]:
    predicted_output = transform(example["input"])
    results.append(describe_changes(example["input"], example["output"], predicted_output))

print("Train Set Results:")
for result in results:
    print(result)

print("\nTest Set Results:")
test_results = []

for example in task_data["test"]:
      predicted_output = transform(example["input"])
      test_results.append(describe_changes(example["input"], example["output"], predicted_output))

for result in test_results:
      print(result)