import numpy as np

def get_grid_info(grid):
    grid = np.array(grid)
    shape = grid.shape
    yellow_count = np.sum(grid == 4)
    white_count = np.sum(grid == 0)
    yellow_positions = np.argwhere(grid == 4).tolist()
    white_positions = np.argwhere(grid == 0).tolist()
    return {
        "shape": shape,
        "yellow_count": yellow_count,
        "white_count": white_count,
        "yellow_positions": yellow_positions,
        "white_positions": white_positions,
    }

def compare_grids(grid1, grid2):
    try:
      diff = np.array(grid1) - np.array(grid2)
    except:
      return "grids of different shapes"
    return np.count_nonzero(diff)

task = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0], [0, 4, 0, 4, 0], [0, 0, 0, 0, 0]],
            "output": [[8, 0, 8, 0, 8, 0], [0, 8, 0, 8, 0, 8], [4, 4, 4, 4, 4, 4], [4, 4, 4, 4, 4, 4], [8, 0, 8, 0, 8, 0], [0, 8, 0, 8, 0, 8]],
        },
        {
            "input": [[0, 0, 0, 0], [0, 0, 4, 0], [0, 0, 0, 0], [0, 0, 0, 0]],
            "output": [[8, 0, 8, 0], [0, 8, 0, 8], [0, 0, 4, 4], [0, 0, 4, 4], [8, 0, 8, 0], [0, 8, 0, 8]],
        },
        {
            "input": [[0, 0, 0], [0, 0, 0], [4, 0, 0], [0, 0, 0], [0, 0, 0]],
            "output": [[8, 0, 8], [0, 8, 0], [4, 4, 4], [4, 4, 4], [8, 0, 8], [0, 8, 0]],
        },
        {
            "input": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 4, 0, 0]],
            "output": [[8, 0, 8, 0], [0, 8, 0, 8], [8, 0, 8, 0], [0, 8, 4, 4], [0, 0, 4, 4], [0, 0, 0, 0]],
        },
    ],
    "test": [{"input": [[0, 0, 0], [0, 0, 0], [0, 4, 0]], "output": [[8, 0, 8], [0, 8, 0], [8, 4, 4], [0, 4, 4]]}],
}
#verify and compare the provided example output with the transform result
for example in task["train"]:
  result = transform(example["input"])
  diff = compare_grids(result, example["output"])
  print (f"Example:  {example['input']} result: {result} differences: {diff}")

results = []
for example in task["train"]:
    input_info = get_grid_info(example["input"])
    output_info = get_grid_info(example["output"])
    results.append(
        {
            "input": input_info,
            "output": output_info,
        }
    )

for i, res in enumerate(results):
    print(f"Example {i+1}:")
    print(f"  Input:  Shape: {res['input']['shape']}, Yellow Count: {res['input']['yellow_count']}, White Count: {res['input']['white_count']}, Yellow Positions: {res['input']['yellow_positions']}, White Positions: {res['input']['white_positions']}")
    print(f"  Output: Shape: {res['output']['shape']}, Yellow Count: {res['output']['yellow_count']}, White Count: {res['output']['white_count']}, Yellow Positions: {res['output']['yellow_positions']}, White Positions: {res['output']['white_positions']}")
