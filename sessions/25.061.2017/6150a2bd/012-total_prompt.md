# 6150a2bd • 012 • refine_coder

---

Previous Code:
```python
"""
The input grid is rotated 90 degrees counter-clockwise. All colors and shapes are preserved during the rotation.
"""

import numpy as np

def transform(input_grid):
    # Convert the input grid to a NumPy array for easier manipulation.
    input_array = np.array(input_grid)

    # Rotate the array 90 degrees counter-clockwise.
    output_array = np.rot90(input_array)

    # Convert the rotated array back to a list of lists.
    output_grid = output_array.tolist()

    return output_grid
```

Train Set Results:
Okay, let's analyze the results of the previously generated code and refine the natural language program accordingly.

**General Assessment:**

The initial hypothesis (90-degree counter-clockwise rotation) seems to hold for the training examples, but we should test it on the entire training set to ensure there is no hidden conditions or alternative explanations that were not taken into consideration. The strategy is to meticulously examine each input-output pair, verifying if the rotation rule applies universally. If discrepancies arise, we'll need to identify the specific conditions under which the rule fails and adjust the natural language program to incorporate those conditions.

**Metrics and Observations:**

I will use a loop to inspect all examples and results.

```tool_code
def display_grid(grid, title):
    color_map = {
        0: (238, 238, 238),  # white
        1: (30, 147, 255),  # blue
        2: (220, 50, 40),  # red
        3: (79, 204, 48),  # green
        4: (230, 200, 0),  # yellow
        5: (85, 85, 85),  # gray
        6: (229, 58, 163),  # magenta
        7: (230, 120, 20),  # orange
        8: (135, 216, 241),  # azure
        9: (146, 18, 49),  # maroon
    }
    
    print(title)
    if not grid:
        print("Empty Grid")
        return

    height = len(grid)
    width = len(grid[0]) if height > 0 else 0

    print(f"Dimensions: {width}x{height}")
    for row in grid:
        row_str = ""
        for cell in row:
            row_str += f"{cell:2d}"
        print(row_str)

# Access the 'train' examples from the current task context
train_examples = task["train"]

for i, example in enumerate(train_examples):
    input_grid = example['input']
    output_grid = example['output']
    print("-" *20)
    print(f"Example {i+1}:")
    display_grid(input_grid, 'Input')
    display_grid(output_grid, 'Output')
    
    predicted_output = transform(input_grid)  # Use the transform function
    display_grid(predicted_output, 'Predicted Output')

    if predicted_output == output_grid:
        print("Prediction: Correct")
    else:
        print("Prediction: Incorrect")
```
**INSTRUCTIONS**

- generate a Python module to represent the natural language program 
- follow the template below
- all common math and science libraries are available
- create docstring only at top - but comment the workflow in the function
- use helper functions for common operations like finding objects, counting,
  measuring, moving, etc. 

remember - we are working iteratively - so this code will inform your future
self as we converge on the solution

*template:*

```python
"""
{{ natural language description of the transformation rule }}
"""

{{ imports }}

def transform(input_grid):
    # initialize output_grid

    # change output pixels 

    return output_grid

```
