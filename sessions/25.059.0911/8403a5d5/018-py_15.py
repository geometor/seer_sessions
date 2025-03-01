def analyze_results(results):
    analysis = []
    for result in results:
        example_index = result['example_index']
        seed_location = result['seed_location']
        is_correct = result['is_correct']
        input_shape = np.array(result['expected_output']).shape

        analysis.append({
            'example_index': example_index,
            'seed_location': seed_location,
            'grid_shape': input_shape,
            'is_correct': is_correct
        })
    return analysis

results = [
    {
        "example_index": 0,
        "seed_location": (1, 3),
        "is_correct": False,
        "predicted_output": [[5, 0, 0, 4, 0, 0], [0, 0, 4, 4, 4, 0], [0, 0, 0, 4, 0, 5]],
        "expected_output": [[5, 0, 0, 4, 0, 0], [0, 0, 4, 4, 4, 0], [0, 0, 0, 4, 0, 5]],
    },
    {
        "example_index": 1,
        "seed_location": (1, 4),
        "is_correct": False,
        "predicted_output": [[5, 0, 0, 4, 4, 4, 0, 5], [0, 0, 4, 4, 4, 4, 4, 0], [0, 0, 0, 4, 4, 4, 0, 0], [0, 0, 0, 4, 4, 4, 0, 5]],
        "expected_output": [[5, 0, 0, 0, 4, 0, 0, 5], [0, 0, 0, 4, 4, 4, 0, 0], [0, 0, 0, 4, 0, 0, 0, 0], [0, 0, 0, 4, 0, 0, 0, 5]],
    },
    {
        "example_index": 2,
        "seed_location": (1, 6),
        "is_correct": False,
        "predicted_output": [[5, 0, 0, 0, 0, 4, 4, 4, 0], [0, 0, 0, 0, 4, 4, 4, 4, 4], [0, 0, 0, 0, 0, 4, 4, 4, 0], [0, 0, 0, 0, 0, 4, 4, 4, 0], [0, 0, 0, 0, 0, 4, 4, 4, 5]],
        "expected_output": [[5, 0, 0, 0, 0, 0, 4, 0, 0], [0, 0, 0, 0, 0, 4, 4, 4, 0], [0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 0, 0, 4, 0, 0, 0], [0, 0, 0, 0, 0, 4, 0, 0, 5]],
    }
]
import numpy as np
analysis = analyze_results(results)
print(analysis)
