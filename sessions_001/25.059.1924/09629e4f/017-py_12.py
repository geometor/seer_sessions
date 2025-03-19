def code_execution(input_grid, task):
    input_grid = np.array(input_grid)
    rows, cols = input_grid.shape
    gray_lines = [r for r in range(rows) if np.all(input_grid[r] == 5)]
    print(f"Task: {task}")
    print(f"Gray lines (full rows of 5s): {gray_lines}")

    for line_row in gray_lines:
        adjacent_colors = get_adjacent_to_line(input_grid, line_row)
        most_frequent = most_frequent_color(adjacent_colors)
        print(f"  Line {line_row}: Adjacent colors: {adjacent_colors}, Most frequent: {most_frequent}")
    print("-----")

# Assuming 'train' contains the training examples
train = task["train"]

for i, example in enumerate(train):
        code_execution(example['input'],f'{i}')
