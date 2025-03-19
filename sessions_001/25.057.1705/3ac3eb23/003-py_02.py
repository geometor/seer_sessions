import numpy as np

def analyze_example(input_grid, output_grid, predicted_grid):
    changes = []
    for r in range(input_grid.shape[0]):
        for c in range(input_grid.shape[1]):
            if predicted_grid[r,c] != output_grid[r,c]:
                changes.append(
                    {
                        "row": r,
                        "col": c,
                        "input_val": int(input_grid[r, c]),
                        "output_val": int(output_grid[r, c]),
                        "predicted_val": int(predicted_grid[r,c]),
                    }
                )
    return changes

def transform(input_grid):
    output_grid = np.copy(input_grid)
    rows, cols = input_grid.shape
    for r in range(rows):
        for c in range(cols):
            if input_grid[r, c] == 2 or input_grid[r, c] == 8:
                if r + 1 < rows:
                  output_grid[r + 1, c] = input_grid[r, c]
    return output_grid

# Example data (replace with actual data from the task)
examples = [
    (np.array([[0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 2]]),
     np.array([[0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 2, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
              [0, 0, 0, 0, 0, 0, 0, 0, 0, 2]])),
      (np.array([[8, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        np.array([[8, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [8, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 2]])),
      (np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
               [8, 0, 0, 0, 0, 0, 0, 0, 0, 2],
               [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
       np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                [8, 0, 0, 0, 0, 0, 0, 0, 0, 2],
                [8, 0, 0, 0, 0, 0, 0, 0, 0, 2]]))
]
report = []

for i, (input_grid, output_grid) in enumerate(examples):
    predicted_grid = transform(input_grid)
    changes = analyze_example(input_grid, output_grid, predicted_grid)
    report.append(
      {
          "example": i,
          "changes": changes
      }
    )

print(report)