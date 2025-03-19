import numpy as np

# ARC task data - training examples (replace with actual data)
examples = [
    {
        "input": np.array([[0, 0, 0, 2, 0],
                           [0, 2, 0, 0, 0],
                           [0, 0, 0, 0, 0]]),
        "output": np.array([[3]])
    },
   {
        "input": np.array([[0, 0, 0, 0, 0],
                           [0, 0, 2, 0, 0],
                           [0, 0, 0, 0, 0],
                           [0, 2, 0, 0, 0],
                           [0, 0, 0, 0, 2]]),
        "output": np.array([[4, 4],
                            [4, 4]])
    },
    {
        "input": np.array([[0, 0, 0, 0, 0, 0, 0],
                           [0, 2, 0, 0, 0, 0, 0],
                           [0, 0, 0, 0, 0, 0, 0]]),
        "output": np.array([[2]])
    }

]

def analyze_examples(examples):
    results = []
    for i, example in enumerate(examples):
        input_grid = example["input"]
        output_grid = example["output"]
        red_pixel_count = np.sum(input_grid == 2)
        output_height, output_width = output_grid.shape
        output_values = np.unique(output_grid)
        results.append({
            "example": i + 1,
            "red_count": red_pixel_count,
            "red_count_plus_one": red_pixel_count + 1,
            "output_height": output_height,
            "output_width": output_width,
           "output_values": output_values,

        })
    return results

analysis = analyze_examples(examples)
print(analysis)