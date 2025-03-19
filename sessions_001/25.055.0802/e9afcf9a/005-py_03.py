def compare_grids(expected, actual):
    if expected.shape != actual.shape:
        return "Different Shapes"
    else:
        return np.sum(expected != actual)

# Example usage (conceptual):
# for i in range(len(train_examples)):
#     errors = compare_grids(train_examples[i]["output"], transform(train_examples[i]["input"]))
#     print(f"Example {i+1}: Errors = {errors}")