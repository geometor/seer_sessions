import numpy as np

def analyze_results(task):
    results = []
    for example in task["train"]:
        input_grid = np.array(example['input'])
        output_grid = np.array(example['output'])
        predicted_output = transform(input_grid.copy())

        correct = np.array_equal(predicted_output, output_grid)
        
        #basic metrics
        input_green_pixels = np.sum(input_grid == 3)
        output_green_pixels = np.sum(output_grid == 3)
        predicted_green_pixels = np.sum(predicted_output == 3)

        results.append({
            "example_id": example.get('id', 'unknown'),
            "correct": correct,
            "input_green_pixels": input_green_pixels,
            "output_green_pixels": output_green_pixels,
            "predicted_green_pixels": predicted_green_pixels
        })
    return results

task = {
    "train": [
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 3, 0, 0, 0],
                      [0, 0, 0, 3, 3, 3, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 0, 3, 0, 0, 0],
                       [0, 0, 0, 3, 3, 3, 0, 0],
                       [0, 0, 3, 3, 3, 3, 3, 0],
                       [0, 3, 3, 3, 3, 3, 3, 3]]
        },
       {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 3, 3, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 0, 3, 3, 0, 0, 0, 0],
                       [0, 0, 3, 3, 0, 0, 0, 0],
                       [0, 0, 3, 3, 0, 0, 0, 0],
                       [0, 0, 3, 3, 0, 0, 0, 0]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 3, 3, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0, 0, 0],
                       [0, 3, 3, 0, 0, 0, 0, 0],
                       [0, 3, 3, 0, 0, 0, 0, 0],
                       [0, 3, 3, 0, 0, 0, 0, 0],
                       [0, 3, 3, 0, 0, 0, 0, 0]]
        },
        {
            "input": [[0, 0, 0, 0, 0, 0],
                      [0, 0, 0, 3, 0, 0],
                      [0, 0, 0, 0, 0, 0]],
            "output": [[0, 0, 0, 0, 0, 0],
                       [0, 0, 0, 3, 0, 0],
                       [0, 0, 0, 3, 0, 0]]
        }

    ]
}

results = analyze_results(task)
print(results)