def analyze_results(example_inputs, example_outputs, generated_outputs):
    """
    Analyzes a set of example inputs, expected outputs, and generated outputs.
    Reports on mismatches, object properties, and potential rule adjustments.
    """
    results = []

    for i, (input_grid, expected_output, generated_output) in enumerate(zip(example_inputs, example_outputs, generated_outputs)):
        # use numpy array comparison
        comparison = (expected_output == generated_output)

        mismatches = np.sum(~comparison)
        match_percentage = (1- (mismatches / comparison.size)) * 100

        results.append(
            {
                "example_index": i,
                "match_percentage": match_percentage,
                "notes": []
            }
        )

        if mismatches > 0:
            # find the locations using where
            mismatch_indices = np.where(~comparison)
            for r, c in zip(mismatch_indices[0], mismatch_indices[1]):
                expected_val = expected_output[r, c]
                generated_val = generated_output[r, c]
                results[i]["notes"].append(
                    f"  Mismatch at ({r},{c}): Expected {expected_val}, Got {generated_val}"
                )
        else:
            results[i]["notes"].append("Perfect Match")
    return results

# Hypothetical execution and results (replace with actual execution)
# training_examples = get_training_examples(task) # task is defined elsewhere
# generated_outputs = [transform(ex[0]) for ex in training_examples]
# example_inputs = [ex[0] for ex in training_examples]
# example_outputs = [ex[1] for ex in training_examples]

# analysis_results = analyze_results(example_inputs, example_outputs, generated_outputs)

# Print results for demonstration
# for result in analysis_results:
#     print(result)