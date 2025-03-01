# Example Usage (Replace with actual data from the task)
task_data = [
    {
        "input": [[0, 0, 5, 0, 0, 0, 0, 5, 0], [0, 0, 7, 0, 0, 0, 0, 7, 0], [0, 0, 5, 0, 0, 0, 0, 5, 0]],
        "output": [[0, 0, 5, 5, 0, 0, 0, 5, 5, 0], [0, 0, 7, 7, 0, 0, 0, 7, 7, 0], [0, 0, 5, 5, 0, 0, 0, 5, 5, 0]]
    },
    {
        "input": [[0, 5, 0, 0, 0, 0, 0, 0, 0], [0, 7, 0, 0, 0, 0, 0, 2, 0], [0, 5, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0], [0, 7, 7, 0, 0, 0, 0, 0, 2, 2, 0], [0, 5, 5, 0, 0, 0, 0, 0, 0, 0, 0]]
    },
    {
        "input": [[0, 0, 0, 0, 0, 0, 0, 0, 0], [5, 0, 0, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0]],
        "output": [[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [5, 5, 0, 0, 0, 0, 0, 0, 0, 2, 2], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]
    }
]
results = [code_execution(example["input"], example["output"], transform) for example in task_data]

for i, result in enumerate(results):
    print(f"Example {i+1}:")
    print(result)