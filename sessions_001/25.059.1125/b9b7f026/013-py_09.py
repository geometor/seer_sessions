from pathlib import Path
import json

def load_task(task_path):
    with open(task_path, 'r') as f:
        task = json.load(f)
    return task

def execute_transform(task):
    train_results = []
    for i, example in enumerate(task['train']):
        input_grid = example['input']
        expected_output = example['output']
        predicted_output = transform(input_grid).tolist()
        
        print(f"--- Example {i} ---")
        print(f"Input:\n{np.array(input_grid)}")
        print(f"Expected Output:\n{np.array(expected_output)}")
        print(f"Predicted Output:\n{np.array(predicted_output)}")
        print(f"Rectangles:\n{find_rectangles(np.array(input_grid))}")

        correct = predicted_output == expected_output
        train_results.append(correct)
        
        print(f"Correct: {correct}")


    return train_results

task_path = "e177c539.json"  # task filename.
task = load_task(task_path)
train_results = execute_transform(task)
print(f"Overall Training Accuracy: {sum(train_results)}/{len(train_results)}")