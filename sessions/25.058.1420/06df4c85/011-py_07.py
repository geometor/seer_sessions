import numpy as np

def compare_grids(grid1, grid2):
    if grid1.shape != grid2.shape:
        return "Different Shapes"
    diff = grid1 != grid2
    return np.sum(diff)

def show_grid(grid):
    #shows the grid object as a string for compact view in this tool.
    return str(grid).replace(' [', '').replace('[', '').replace(']', '\n').replace(' ', ',')

train = [
    {
        "input": [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,1,1,1,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
        "output": [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,1,1,1,2,2,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,1,1,1,1,1,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
    },
    {
        "input": [[0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,1,1,1,1,1,1,0,0,0],
                  [0,0,0,1,1,1,1,1,1,0,0,0],
                  [0,0,0,1,1,1,4,1,1,0,0,0],
                  [0,0,0,1,1,1,1,1,1,0,0,0],
                  [0,0,0,1,1,1,1,1,1,0,0,0],
                  [0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0,0,0,0]],
        "output": [[0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,1,1,1,1,1,1,0,0,0],
                  [0,0,0,1,1,1,1,1,1,0,0,0],
                  [0,0,0,1,1,1,4,4,1,1,0,0],
                  [0,0,0,1,1,1,1,1,1,0,0,0],
                  [0,0,0,1,1,1,1,1,1,0,0,0],
                  [0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0,0,0,0]],
    },
        {
        "input": [[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,1,1,1,1,1,1,0,0,0,0],
                  [0,0,0,0,1,1,1,1,1,1,0,0,0,0],
                  [0,0,0,0,1,1,1,8,1,1,0,0,0,0],
                  [0,0,0,0,1,1,1,1,1,1,0,0,0,0],
                  [0,0,0,0,1,1,1,1,1,1,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
        "output": [[0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,1,1,1,1,1,1,0,0,0,0],
                  [0,0,0,0,1,1,1,1,1,1,0,0,0,0],
                  [0,0,0,0,1,1,1,8,8,8,8,1,1,0,0],
                  [0,0,0,0,1,1,1,1,1,1,0,0,0,0],
                  [0,0,0,0,1,1,1,1,1,1,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                  [0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
    },
    {
           "input": [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0],
                     [0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0],
                     [0,0,0,0,1,1,1,9,1,1,1,1,0,0,0,0],
                     [0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0],
                     [0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
           "output": [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0],
                     [0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0],
                     [0,0,0,0,1,1,1,9,9,9,9,1,1,1,1,0,0],
                     [0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0],
                     [0,0,0,0,1,1,1,1,1,1,1,1,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
    },
    {
           "input": [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,1,1,1,3,1,1,1,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]],
           "output": [[0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,1,1,1,3,3,1,1,1,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,1,1,1,1,1,1,1,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                     [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]]
    }

]

for i, example in enumerate(train):
    input_grid = np.array(example["input"])
    output_grid = np.array(example["output"])
    predicted_output = transform(input_grid)  # Apply the transform function
    diff_count = compare_grids(output_grid, predicted_output)
    print(f"Example {i+1}:")
    print(f"  Differences: {diff_count}")
    if diff_count != 0:

        print(f"expected:\n{show_grid(output_grid)}")
        print(f"predicted:\n{show_grid(predicted_output)}")