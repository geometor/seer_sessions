import math

"""
Transforms input text by taking two lines of repeating numbers and creating two new lines.
The first output line alternates between the number from the first input line (num1) and the second input line (num2), starting with num1.
The second output line alternates between num2 and num1, starting with num2.
The length of the output lines matches the length of the input lines.
"""

def parse_input_line(line):
    """Parses a line of space-separated numbers, returns the first number and the count."""
    parts = line.split()
    if not parts:
        raise ValueError("Input line cannot be empty")
    num = parts[0] # Assuming all numbers are the same, take the first one
    length = len(parts)
    return num, length

def generate_alternating_sequence(val1, val2, length):
    """Generates a list of alternating values."""
    sequence = []
    for i in range(length):
        if i % 2 == 0:
            sequence.append(val1)
        else:
            sequence.append(val2)
    return sequence

def format_sequence_to_string(sequence):
    """Joins a list of items into a space-separated string."""
    return " ".join(map(str, sequence))

def transform(input_str):
    """
    Applies the transformation rule to the input string.

    Args:
        input_str: A string containing two lines, each with space-separated identical numbers.

    Returns:
        A string containing the two transformed output lines, separated by a newline.
    """
    # Split input into lines
    lines = input_str.strip().split('\n')
    if len(lines) != 2:
        raise ValueError("Input must contain exactly two lines")

    # Parse input lines
    num1, length1 = parse_input_line(lines[0])
    num2, length2 = parse_input_line(lines[1])

    # Validate lengths are consistent
    if length1 != length2:
        raise ValueError("Input lines must have the same length")
    length = length1 # Use the common length

    # Generate Output Line 1: starts with num1
    output_sequence1 = generate_alternating_sequence(num1, num2, length)
    output_line1_str = format_sequence_to_string(output_sequence1)

    # Generate Output Line 2: starts with num2
    output_sequence2 = generate_alternating_sequence(num2, num1, length)
    output_line2_str = format_sequence_to_string(output_sequence2)

    # Combine and return the output lines
    output_grid = f"{output_line1_str}\n{output_line2_str}"

    return output_grid

# Example usage with train_1 data:
input_1 = """4 4 4 4 4 4
8 8 8 8 8 8"""
output_1 = transform(input_1)
print("--- Train 1 ---")
print("Input:\n" + input_1)
print("Output:\n" + output_1)
expected_output_1 = """4 8 4 8 4 8
8 4 8 4 8 4"""
print("Expected:\n" + expected_output_1)
print(f"Matches Expected: {output_1 == expected_output_1}")


# Example usage with train_2 data:
input_2 = """3 3 3 3 3 3
9 9 9 9 9 9"""
output_2 = transform(input_2)
print("\n--- Train 2 ---")
print("Input:\n" + input_2)
print("Output:\n" + output_2)
expected_output_2 = """3 9 3 9 3 9
9 3 9 3 9 3"""
print("Expected:\n" + expected_output_2)
print(f"Matches Expected: {output_2 == expected_output_2}")