import numpy as np

def analyze_examples(examples):
    for i, example in enumerate(examples):
        input_grid = np.array(example["input"])
        output_grid = np.array(example["output"])
        print(f"Example {i+1}:")
        print("Input Grid:")
        print(input_grid)
        print("Output Grid:")
        print(output_grid)

        #check for simple replacement rules, report a color map if one exists
        color_map = {}
        is_simple_replacement = True
        for row in range(input_grid.shape[0]):
            for col in range(input_grid.shape[1]):
                in_val = input_grid[row, col]
                out_val = output_grid[row, col]
                if in_val in color_map:
                    if color_map[in_val] != out_val:
                        is_simple_replacement = False
                        break
                else:
                    color_map[in_val] = out_val
            if not is_simple_replacement:
                break
        if is_simple_replacement:
            print("  Simple Color Replacement Found:")
            for in_val, out_val in color_map.items():
                print(f"    {in_val} -> {out_val}")
        else:
            print("  No Simple Color Replacement Found.")

        # Check for a border effect
        input_height, input_width = input_grid.shape
        is_border_effect = True
        for row in range(input_height):
            for col in range(input_width):
                if (row == 0 or row == input_height - 1 or col == 0 or col == input_width - 1):
                    if input_grid[row,col] == output_grid[row,col]:
                        is_border_effect = False
                        break
                else: #it is NOT a border element
                    if input_grid[row,col] != output_grid[row,col]:
                        is_border_effect = False
                        break
        if is_border_effect:
                print("Simple Border effect found")

        print("-" * 20)

train_examples = [
    {
        "input": [[5, 1, 5], [1, 5, 1], [5, 1, 5]],
        "output": [[9, 1, 9], [1, 9, 1], [9, 1, 9]],
    },
     {
        "input": [[1, 8, 8, 8, 1], [1, 8, 5, 8, 1], [1, 8, 8, 8, 1]],
        "output": [[1, 2, 2, 2, 1], [1, 2, 9, 2, 1], [1, 2, 2, 2, 1]],
    },
    {
        "input": [[6, 6, 8, 6, 6], [6, 6, 6, 8, 6], [8, 6, 6, 6, 8], [6, 8, 6, 6, 6], [6, 6, 8, 6, 6]],
        "output": [[0, 0, 2, 0, 0], [0, 0, 0, 2, 0], [2, 0, 0, 0, 2], [0, 2, 0, 0, 0], [0, 0, 2, 0, 0]],
    }
]

analyze_examples(train_examples)
