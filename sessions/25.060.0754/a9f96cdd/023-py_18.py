def describe_task(task):
    print(f"Task: {task['name']}")
    for i, example in enumerate(task['train']):
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        
        # Find the red pixel in the input
        red_pos = np.argwhere(input_grid == 2)
        if len(red_pos) > 0:
            red_row, red_col = red_pos[0]
        else:
            red_row, red_col = None, None  # Handle cases where red might be absent (shouldn't happen in valid tasks)
            print(f"Example {i+1}: No red pixel found in input.")
            continue

        print(f"  Example {i+1}:")
        print(f"    Red pixel position (input): ({red_row}, {red_col})")

        # Find output colors and calculate offsets
        colors = {3: "Green", 6: "Magenta", 8: "Azure", 7: "Orange"}
        for color_val, color_name in colors.items():
            color_pos = np.argwhere(output_grid == color_val)
            if len(color_pos) > 0:
                color_row, color_col = color_pos[0]
                row_offset = color_row - red_row
                col_offset = color_col - red_col
                print(f"    {color_name} pixel position (output): ({color_row}, {color_col}), Offset: ({row_offset}, {col_offset})")
            else:
                print(f"    {color_name} pixel not found in output.")
        print("-" * 40)

# example task definition (replace with your actual task data)
tasks = [
    {
        "name": "Task 1",
        "train": [
            {'input': [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 2, 0, 0]], 'output': [[0, 0, 3, 0, 6], [0, 0, 0, 0, 0], [0, 0, 8, 0, 7]]},
            {'input': [[0, 0, 0, 0, 0], [0, 2, 0, 0, 0], [0, 0, 0, 0, 0]], 'output': [[0, 3, 0, 0, 6], [0, 0, 0, 0, 0], [0, 8, 0, 0, 7]]},
            {'input': [[0, 0, 0, 0, 2], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], 'output': [[0, 0, 3, 0, 6], [0, 0, 0, 0, 0], [0, 0, 8, 0, 7]]}
        ]
    },
    {
      "name": "Task 2",
      "train": [
        {'input': [[0, 0, 2, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], 'output': [[0, 0, 8, 0, 7], [0, 0, 0, 0, 0], [0, 0, 3, 0, 6]]},
        {'input': [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 2, 0, 0]], 'output': [[0, 0, 8, 0, 7], [0, 0, 0, 0, 0], [0, 0, 3, 0, 6]]},
        {'input': [[0, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 2, 0]], 'output': [[0, 0, 8, 0, 7], [0, 0, 0, 0, 0], [0, 0, 3, 0, 6]]}
        ]
    }
]
for task in tasks:
  describe_task(task)