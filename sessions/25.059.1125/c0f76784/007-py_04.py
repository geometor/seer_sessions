import numpy as np

def compare_grids(predicted, actual):
    """
    Compares two grids and returns a difference grid.
    0: Match
    1: Predicted has a value, actual is different or missing
    -1: Actual has a value, prediction is different or missing
    """
    diff_grid = np.zeros_like(predicted, dtype=int)

    height = predicted.shape[0]
    width = predicted.shape[1]

    for y in range(height):
      for x in range(width):
        if predicted[y,x] != actual[y,x]:
          diff_grid[y,x] = 1 if predicted[y,x] != 0 else -1

    return diff_grid

def show_task(task):
  print(f"Task: {task['name']}")

  num_train = len(task['train'])
  num_test = len(task['test'])

  print(f"  Train Examples: {num_train}")
  for i in range(num_train):
    print(f"    Example: {i}")
    print(f"      Input:\n{task['train'][i]['input']}")
    print(f"      Output:\n{task['train'][i]['output']}")

  print(f"  Test Examples: {num_test}")
  for i in range(num_test):
    print(f"    Example: {i}")
    print(f"      Input:\n{task['test'][i]['input']}")
    print(f"      Output:\n{task['test'][i]['output']}")

def show_results(results):
  for task_name, result in results.items():
      print(f"Task: {task_name}")
      print(f"  Success: {result['success']}")
      if 'diff_grids' in result:
        for i, diff_grid in enumerate(result['diff_grids']):
          print(f"    Difference Grid (Example {i}):\n{diff_grid}")

results = {}

task0 = {
    "name":
    "task0",
    "train": [{
        'input':
        np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 5, 5, 5, 5, 5, 0, 0, 0, 0],
                  [0, 5, 5, 5, 5, 5, 0, 0, 0, 0], [0, 5, 5, 5, 5, 5, 0, 0, 0, 0],
                  [0, 5, 5, 5, 5, 5, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        'output':
        np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 5, 5, 5, 8, 5, 0, 0, 0, 0],
                  [0, 5, 5, 7, 7, 5, 0, 0, 0, 0], [0, 5, 5, 7, 7, 5, 0, 0, 0, 0],
                  [0, 5, 5, 5, 6, 5, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    }, {
        'input':
        np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 5, 5, 5, 5, 5, 5, 5, 0, 0],
                  [0, 5, 5, 5, 5, 5, 5, 5, 0, 0], [0, 5, 5, 5, 5, 5, 5, 5, 0, 0],
                  [0, 5, 5, 5, 5, 5, 5, 5, 0, 0], [0, 5, 5, 5, 5, 5, 5, 5, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        'output':
        np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 5, 5, 5, 8, 8, 5, 5, 0, 0],
                  [0, 5, 5, 5, 7, 7, 5, 5, 0, 0], [0, 5, 5, 5, 7, 7, 5, 5, 0, 0],
                  [0, 5, 5, 5, 7, 7, 5, 5, 0, 0], [0, 5, 5, 5, 6, 6, 5, 5, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    }, {
        'input':
        np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 5, 5, 5, 5, 0, 0, 0, 0], [0, 0, 5, 5, 5, 5, 0, 0, 0, 0],
                  [0, 0, 5, 5, 5, 5, 0, 0, 0, 0], [0, 0, 5, 5, 5, 5, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]),
        'output':
        np.array([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 5, 8, 8, 5, 0, 0, 0, 0], [0, 0, 5, 7, 7, 5, 0, 0, 0, 0],
                  [0, 0, 5, 7, 7, 5, 0, 0, 0, 0], [0, 0, 5, 6, 6, 5, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])
    }],
    "test": [{
        'input':
        np.array([[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 5, 5, 0, 0, 0],
                  [0, 0, 0, 5, 5, 0, 0, 0], [0, 0, 0, 5, 5, 0, 0, 0],
                  [0, 0, 0, 5, 5, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]]),
        'output':
        np.array([[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 8, 8, 0, 0, 0],
                  [0, 0, 0, 7, 7, 0, 0, 0], [0, 0, 0, 7, 7, 0, 0, 0],
                  [0, 0, 0, 6, 6, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0],
                  [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]])
    }]
}

for task in [task0]:
    results[task['name']] = {'success': True, 'diff_grids': []}
    for i in range(len(task['train'])):
        predicted_output = transform(task['train'][i]['input'])
        diff_grid = compare_grids(predicted_output, task['train'][i]['output'])
        results[task['name']]['diff_grids'].append(diff_grid)
        if not np.array_equal(predicted_output, task['train'][i]['output']):
            results[task['name']]['success'] = False

show_results(results)