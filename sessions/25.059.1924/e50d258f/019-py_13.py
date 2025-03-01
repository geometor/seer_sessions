def grid_to_string(grid):
    return '\n'.join(''.join(str(cell) for cell in row) for row in grid)

def analyze_examples(task):
    print(f"Task: {task['name']}")
    for i, example in enumerate(task['train']):
        input_grid = example['input']
        output_grid = example['output']
        input_str = grid_to_string(input_grid)
        output_str = grid_to_string(output_grid)
        
        print(f"\nExample {i+1}:")
        print(f"Input:\n{input_str}")
        print(f"Output:\n{output_str}")

        # using the generated code
        pred = transform(input_grid)
        pred_str = grid_to_string(pred)
        print(f"Predicted:\n{pred_str}")
        print(f"Prediction is correct: {pred == output_grid}")


task = {
    "name": "crop_smallest_rectangle",
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 2, 2, 0], [0, 0, 0, 2, 2, 0], [0, 0, 0, 0, 0, 0]],
            "output": [[2, 2], [2, 2]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 3, 3, 3, 0], [0, 0, 0, 0, 3, 3, 3, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[3, 3, 3], [3, 3, 3]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 8, 8, 8, 0, 0, 0], [0, 0, 0, 8, 8, 8, 0, 0, 0], [0, 0, 0, 8, 8, 8, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[8, 8, 8], [8, 8, 8], [8, 8, 8]]
        },
		{
            "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 7, 0, 0, 0, 0, 0], [0, 0, 7, 7, 7, 0, 0, 0, 0], [0, 0, 0, 7, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[7, 0, 0], [7, 7, 7], [0, 7, 0]]
        }
    ]
}
analyze_examples(task)