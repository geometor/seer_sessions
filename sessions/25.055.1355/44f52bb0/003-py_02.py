import numpy as np

def analyze_examples(examples):
    results = []
    for i, example in enumerate(examples):
        input_grid = example["input"]
        output_grid = example["output"]
        input_array = np.array(input_grid)
        output_array = np.array(output_grid)

        red_count_input = np.count_nonzero(input_array == 2)
        grey_count_output = np.count_nonzero(output_array == 5)

        results.append({
            "example_index": i,
            "red_count_input": red_count_input,
            "grey_count_output": grey_count_output,
            "red_equals_grey": red_count_input == grey_count_output
        })
    return results

#Dummy Examples - replace with real examples when run in notebook
examples = [
    {"input": [[0, 0, 0], [0, 2, 0], [0, 2, 0], [2, 0, 2]], "output": [[5], [5], [5], [5]]},
    {"input": [[2, 0, 0], [0, 0, 0], [0, 0, 2]], "output": [[5], [5]]},
    {"input": [[0, 0, 0, 2], [0, 0, 0, 0]], "output": [[5]]},
    {"input": [[0, 0, 0, 0], [0, 0, 0, 0], [0, 2, 0, 0]], "output": [[5]]},
    {"input": [[2, 0, 0, 0, 0], [0, 0, 0, 0, 0], [0, 0, 0, 0, 0]], "output": [[5]]},
]

analysis_results = analyze_examples(examples)
print(analysis_results)
