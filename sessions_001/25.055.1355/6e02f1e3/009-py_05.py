import numpy as np

def report_results(inputs, outputs, predicted_outputs):
    """
    This function assumes that inputs, outputs and predicted_outputs
    are lists of numpy arrays.
    """
    report = ""
    num_examples = len(inputs)
    if not (num_examples == len(outputs) and num_examples == len(predicted_outputs)):
      return "ERROR: inputs, outputs, and predicted_outputs must be the same length"

    for i in range(num_examples):
      input_grid = inputs[i]
      expected_grid = outputs[i]
      predicted_grid = predicted_outputs[i]

      report += f"Example {i+1}:\n"
      report += f"  Input:\n{input_grid}\n"
      report += f"  Expected Output:\n{expected_grid}\n"
      report += f"  Predicted Output:\n{predicted_grid}\n"

      comparison = (expected_grid == predicted_grid).all()
      report += f"  Match: {comparison}\n\n"
    print(report)