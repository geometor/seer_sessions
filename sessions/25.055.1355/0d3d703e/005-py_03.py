def describe_grid(grid):
    import numpy as np
    np_grid = np.array(grid)
    dimensions = np_grid.shape
    unique_values = np.unique(np_grid).tolist()
    return dimensions, unique_values

examples = [
    {"input": [[0, 1, 2], [3, 4, 5], [6, 7, 8]], "output": [[1, 2, 3], [4, 5, 6], [7, 8, 9]]},
    {"input": [[9, 8, 7], [6, 5, 4], [3, 2, 1]], "output": [[0, 9, 8], [7, 6, 5], [4, 3, 2]]},
    {"input": [[5, 5, 5], [5, 5, 5], [5, 5, 5]], "output": [[6, 6, 6], [6, 6, 6], [6, 6, 6]]},
    {"input" : [[1]], "output": [[2]]}
]

results = []
for example in examples:
  input_dims, input_vals = describe_grid(example["input"])
  output_dims, output_vals = describe_grid(example["output"])
  results.append(
      {
          "input_dimensions": input_dims,
          "input_unique_values": input_vals,
          "output_dimensions": output_dims,
          "output_unique_values": output_vals,
      }
  )
print (results)
