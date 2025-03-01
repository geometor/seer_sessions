import numpy as np

def analyze_results(task):
    """Analyze results for each example in a task."""
    print("Example\tInput Shape\tOutput Shape\tMagenta Input\tMagenta Output")
    for example in task['train']:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        magenta_input_count = np.sum(input_grid == 6)
        magenta_output_count = np.sum(output_grid == 6)
        print(f"  Train\t{input_grid.shape}\t{output_grid.shape}\t{magenta_input_count}\t{magenta_output_count}")

    if 'test' in task:
        for example in task['test']:
            input_grid = np.array(example['input'])
            if 'output' in example:
                output_grid = np.array(example['output'])
                magenta_input_count = np.sum(input_grid == 6)
                magenta_output_count = np.sum(output_grid == 6)
            else:
                magenta_input_count= np.sum(input_grid == 6)
                magenta_output_count=0
            print(f"   Test\t{input_grid.shape}\t\t{magenta_input_count}\t{magenta_output_count}")

task = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0], [0, 0, 0, 6, 0, 0], [0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 6, 6, 0], [0, 0, 0, 6, 0, 0], [0, 0, 0, 0, 0, 0]],
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 6, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 6, 6, 0], [0, 0, 0, 0, 6, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 6, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 6, 6], [0, 0, 0, 0, 0, 0, 6, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
        }

    ],
    "test": [
       {
            "input": [[0, 0, 0, 0, 0], [0, 6, 0, 0, 0], [0, 0, 0, 0, 0]],
            "output": [[0, 6, 6, 0, 0], [0, 6, 0, 0, 0], [0, 0, 0, 0, 0]]
        }
    ],
}
analyze_results(task)