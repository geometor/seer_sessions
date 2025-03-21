def analyze_example(input_grid, output_grid):
    input_grid = np.array(input_grid)
    output_grid = np.array(output_grid)

    initial_diagonal = []
    for i in range(min(input_grid.shape)):
        if input_grid[i, i] == 2:
            initial_diagonal.append((i, i))
        else:
            break

    diagonal_length = len(initial_diagonal)
    input_dims = input_grid.shape
    output_dims = output_grid.shape
    other_colors = np.unique(input_grid)
    other_colors = other_colors[other_colors != 2]

    print(f"  Input Dimensions: {input_dims}")
    print(f"  Output Dimensions: {output_dims}")
    print(f"  Initial Diagonal Length: {diagonal_length}")
    print(f"  Other Colors: {other_colors}")
    print("-" * 20)


task_data = [
    {
        "input": [[2, 0, 0, 0, 0, 0, 0, 0], [0, 2, 0, 0, 0, 0, 0, 0], [0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0], [0, 0, 0, 0, 0, 2, 0, 0], [0, 0, 0, 0, 0, 0, 2, 0], [0, 0, 0, 0, 0, 0, 0, 2]],
        "output": [[2, 0, 0, 0, 2, 0, 0, 0], [0, 2, 0, 0, 0, 2, 0, 0], [0, 0, 2, 0, 0, 0, 2, 0], [0, 0, 0, 2, 0, 0, 0, 2], [2, 0, 0, 0, 2, 0, 0, 0], [0, 2, 0, 0, 0, 2, 0, 0], [0, 0, 2, 0, 0, 0, 2, 0], [0, 0, 0, 2, 0, 0, 0, 2]]
    },
    {
        "input": [[2, 0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 2, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0, 2]],
        "output": [[2, 0, 0, 0, 0, 2, 0, 0, 0], [0, 2, 0, 0, 0, 0, 2, 0, 0], [0, 0, 2, 0, 0, 0, 0, 2, 0], [0, 0, 0, 2, 0, 0, 0, 0, 2], [0, 0, 0, 0, 2, 0, 0, 0, 0], [2, 0, 0, 0, 0, 2, 0, 0, 0], [0, 2, 0, 0, 0, 0, 2, 0, 0], [0, 0, 2, 0, 0, 0, 0, 2, 0], [0, 0, 0, 2, 0, 0, 0, 0, 2]]
    },
    {
        "input": [[2, 0, 0, 0, 0, 0], [0, 2, 0, 0, 0, 0], [0, 0, 2, 0, 0, 0], [0, 0, 0, 2, 0, 0], [0, 0, 0, 0, 2, 0], [0, 0, 0, 0, 0, 2]],
        "output": [[2, 0, 0, 2, 0, 0], [0, 2, 0, 0, 2, 0], [0, 0, 2, 0, 0, 2], [2, 0, 0, 2, 0, 0], [0, 2, 0, 0, 2, 0], [0, 0, 2, 0, 0, 2]]
    },
    {
        "input" : [[2,0,0,0,0,0,0],[0,2,0,0,0,0,0],[0,0,2,0,0,0,0],[0,0,0,2,0,0,0],[0,0,0,0,2,0,0],[0,0,0,0,0,2,0],[0,0,0,0,0,0,2]],
        "output": [[2, 0, 0, 0, 2, 0, 0], [0, 2, 0, 0, 0, 2, 0], [0, 0, 2, 0, 0, 0, 2], [0, 0, 0, 2, 0, 0, 0], [2, 0, 0, 0, 2, 0, 0], [0, 2, 0, 0, 0, 2, 0], [0, 0, 2, 0, 0, 0, 2]]
    },
    {
       "input": [[2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 2]],
       "output": [[2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0], [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2], [2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0], [0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0, 0], [0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2, 0], [0, 0, 0, 0, 0, 2, 0, 0, 0, 0, 0, 2]]
    }
]

for i, example in enumerate(task_data):
    print(f"Example {i+1}:")
    analyze_example(example["input"], example["output"])