import numpy as np

def print_grid(grid, title="Grid"):
    print(f"\n--- {title} ---")
    for row in grid:
        print(row)

def analyze_results(task):
    print(f"Task: {task['name']}")
    for i, example in enumerate(task['train']):
        input_grid = example['input']
        expected_output_grid = example['output']
        predicted_output_grid = transform(input_grid)
        print(f"\nExample {i+1}:")

        print_grid(input_grid, "Input")
        print_grid(expected_output_grid, "Expected Output")
        print_grid(predicted_output_grid, "Predicted Output")

        if predicted_output_grid == expected_output_grid:
            print("Result: PASS")
        else:
            print("Result: FAIL")

# Hypothetical "task" object (replace with actual task data)
task = {
'name':"example_task",
    'train': [
        {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                   [8, 8, 8, 8, 8, 8, 8, 8, 8, 1],
                   [0, 0, 0, 0, 8, 0, 0, 0, 0, 1],
                   [0, 0, 0, 4, 8, 0, 0, 0, 0, 1],
                   [0, 0, 0, 4, 0, 0, 0, 0, 0, 1],
                   [0, 0, 0, 4, 0, 0, 0, 0, 0, 1],
                   [0, 0, 0, 4, 0, 0, 0, 0, 0, 1],
                   [6, 6, 6, 6, 6, 6, 6, 6, 6, 6],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                   [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        'output': [[0, 0, 0, 0, 8, 0, 0, 0, 0, 1],
                  [0, 0, 0, 0, 8, 0, 0, 0, 0, 1],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 1],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]]},

       {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [8, 8, 8, 8, 8, 8, 8, 8, 8, 1], [0, 0, 0, 4, 8, 0, 0, 0, 0, 1], [0, 0, 0, 4, 0, 0, 0, 0, 0, 1], [0, 0, 0, 4, 0, 0, 0, 0, 0, 1], [6, 6, 6, 6, 6, 6, 6, 6, 6, 6], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]],
        'output': [[0, 0, 0, 0, 8, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 0, 1]]},

       {'input': [[0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 1], [8, 8, 8, 8, 8, 8, 8, 8, 1], [0, 0, 0, 4, 8, 0, 0, 0, 1], [0, 0, 0, 4, 0, 0, 0, 0, 1], [6, 6, 6, 6, 6, 6, 6, 6, 6], [0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        'output': [[0, 0, 0, 0, 8, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 1], [0, 0, 0, 0, 0, 0, 0, 0, 1]]}
    ]
}

analyze_results(task)