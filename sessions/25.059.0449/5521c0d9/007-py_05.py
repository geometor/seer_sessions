import numpy as np

# ... (Previous Code - find_objects and transform functions here) ...

def analyze_examples(examples):
    for i, (input_grid, output_grid) in enumerate(examples):
        input_grid = np.array(input_grid)
        output_grid = np.array(output_grid)
        predicted_output = transform(input_grid.tolist())

        objects = find_objects(input_grid)
        print(f"--- Example {i+1} ---")
        print(f"Input Grid:\n{input_grid}")
        print(f"Expected Output Grid:\n{output_grid}")
        print(f"Predicted Output Grid:\n{predicted_output}")

        print(f"Identified Objects: {objects}")

        max_height = 0
        total_width = 0
        for color, (min_row, max_row, min_col, max_col) in objects:
            height = max_row - min_row + 1
            width = max_col - min_col + 1
            max_height = max(max_height, height)
            total_width += width
        print(f"Max Height: {max_height}, Total Width: {total_width}")


# Provide the actual training examples from the task.
examples = [
    (
        [[0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 1, 1], [0, 0, 0, 0, 1, 1]],
        [[1, 1, 0, 0, 0, 0], [1, 1, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0]],
    ),
    (
        [[0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [3, 3, 3, 0, 0, 0, 0, 0], [3, 3, 3, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 2], [0, 0, 0, 0, 0, 0, 0, 2]],
        [[3, 3, 3, 2, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 2, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0, 0]],
    ),
    (
        [[0, 0, 0, 0, 0, 0, 0], [0, 5, 5, 5, 5, 0, 0], [0, 5, 5, 5, 5, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 7, 7], [0, 0, 0, 0, 0, 7, 7]],
        [[5, 5, 5, 5, 7, 7, 0], [0, 0, 0, 0, 7, 7, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0], [0, 0, 0, 0, 0, 0, 0]],
    ),
]
analyze_examples(examples)