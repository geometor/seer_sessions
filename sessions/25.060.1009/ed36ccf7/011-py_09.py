import numpy as np

def analyze_grid(grid):
    magenta_count = np.sum(grid == 6)
    white_count = np.sum(grid == 0)
    return magenta_count, white_count

task_examples = [
    {
        "input": np.array([[0, 0, 0], [0, 6, 0], [0, 6, 0]]),
        "output": np.array([[6, 0, 0], [6, 0, 0], [6, 6, 0]]),
    },
    {
        "input": np.array([[0, 0, 0], [0, 0, 0], [6, 6, 6]]),
        "output": np.array([[6, 0, 0], [6, 0, 0], [6, 0, 0]]),
    },
    {
        "input": np.array([[6, 0, 0], [0, 0, 0], [0, 0, 6]]),
        "output": np.array([[6, 0, 0], [6, 0, 0], [0, 0, 0]]),
    },
     {
        "input": np.array([[0, 0, 6], [0, 0, 6], [0, 0, 6]]),
        "output": np.array([[6, 0, 0], [6, 0, 0], [6, 0, 0]]),
    },
    {
        "input": np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]),
        "output": np.array([[0, 0, 0], [0, 0, 0], [0, 0, 0]]),
    }

]

for i, example in enumerate(task_examples):
    input_magenta, input_white = analyze_grid(example["input"])
    output_magenta, output_white = analyze_grid(example["output"])
    print(f"Example {i+1}:")
    print(f"  Input: Magenta={input_magenta}, White={input_white}")
    print(f"  Output: Magenta={output_magenta}, White={output_white}")
