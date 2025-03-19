import numpy as np

def get_background_color(grid):
    unique, counts = np.unique(grid, return_counts=True)
    return unique[np.argmax(counts)]

def transform(input_grid):
    rows, cols = input_grid.shape
    background_color = get_background_color(input_grid)
    output_grid = np.zeros((2, 2), dtype=int)
    corners = [(0, 0), (0, cols - 1), (rows - 1, 0), (rows - 1, cols - 1)]
    output_coords = [(0, 0), (0, 1), (1, 0), (1, 1)]
    for (in_r, in_c), (out_r, out_c) in zip(corners, output_coords):
        if input_grid[in_r, in_c] != background_color:
           output_grid[out_r, out_c] = input_grid[in_r, in_c]
        else:
            for i in range(1,max(rows,cols)):
                if in_r + i < rows and input_grid[in_r+i,in_c] != background_color:
                    output_grid[out_r, out_c] = input_grid[in_r + i, in_c]
                    break
                if in_c + i < cols and input_grid[in_r,in_c+i] != background_color:
                    output_grid[out_r, out_c] = input_grid[in_r, in_c+i]
                    break
                if in_r - i >= 0 and input_grid[in_r-i,in_c] != background_color:
                    output_grid[out_r, out_c] = input_grid[in_r-i, in_c]
                    break
                if in_c - i >= 0 and input_grid[in_r,in_c-i] != background_color:
                    output_grid[out_r, out_c] = input_grid[in_r, in_c-i]
                    break
    return output_grid

task = {
  "train": [
    {
      "input": [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 1, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 2]],
      "output": [[0, 0], [0, 2]]
    },
    {
      "input": [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 3, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]],
      "output": [[0, 0], [3, 0]]
    },
    {
       "input": [[5, 0, 0, 0, 0, 5], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [5, 0, 0, 0, 0, 5]],
       "output": [[5, 5], [5, 5]]
    },
      {
        "input":  [[0, 0, 0, 0, 0, 7], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [7, 0, 0, 0, 0, 0]],
        "output": [[0, 7], [7, 0]]
      }
  ],
  "test": [
    {
      "input": [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 4, 0]],
      "output": [[0, 0], [4, 0]]
    }
  ]
}

results = []
for example in task["train"]:
    input_grid = np.array(example["input"])
    expected_output = np.array(example["output"])
    predicted_output = transform(input_grid)
    match = np.array_equal(predicted_output, expected_output)
    results.append({
        "input_shape": input_grid.shape,
        "background_color": get_background_color(input_grid),
        "corner_colors": [input_grid[r, c] for r, c in [(0, 0), (0, input_grid.shape[1]-1), (input_grid.shape[0]-1, 0), (input_grid.shape[0]-1, input_grid.shape[1]-1)]],
        "predicted_output": predicted_output.tolist(),
        "expected_output": expected_output.tolist(),
        "match": match
    })

for r in results:
    print(r)