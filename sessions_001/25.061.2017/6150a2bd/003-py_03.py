task_examples = [
    {'input': [[1, 2, 3], [4, 5, 6]], 'output': [[4, 1], [5, 2], [6, 3]]},
    {'input': [[7,8],[9,1]], 'output': [[9, 7], [1, 8]]},
    {'input': [[1,2,3,4]], 'output': [[1], [2], [3], [4]]},
    {'input': [[1],[2],[3]], 'output': [[1, 2, 3]]}
]

metrics = calculate_metrics(task_examples)
print(metrics)