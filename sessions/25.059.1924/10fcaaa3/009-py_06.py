import numpy as np

def describe_differences(task, show_examples=False):
    messages = []
    messages.append(f"Differences for task {task['name']}")

    num_train = len(task['train'])
    num_test = len(task['test'])
    messages.append(f"  train pairs: {num_train}")
    messages.append(f"  test pairs: {num_test}")

    for i in range(num_train):
        input_grid = np.array(task['train'][i]['input'])
        expected_output = np.array(task['train'][i]['output'])
        predicted_output = transform(input_grid)
        if not np.array_equal(expected_output, predicted_output):
            messages.append(f"    train[{i}] - mismatch")
            diff = expected_output - predicted_output
            messages.append(f"    train[{i}] - difference:\n{diff}")
            if show_examples:
                messages.append(f"    train[{i}] - input:\n{input_grid}")
                messages.append(f"    train[{i}] - expected:\n{expected_output}")
                messages.append(f"    train[{i}] - predicted:\n{predicted_output}")

        else:
            messages.append(f"    train[{i}] - match")
    return messages