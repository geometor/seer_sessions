"""
Transforms a sequence of digits provided as a space-separated string (initially as bytes).
The transformation identifies a segment bounded by the first and last non-zero digits.
Within this segment, it finds the most frequently occurring digit (the "dominant digit").
All digits within the segment are then replaced by this dominant digit.
Leading and trailing zeros outside the segment are preserved.
If the input consists entirely of zeros, it is returned unchanged.
"""

from collections import Counter
import re # Using re.findall for robustness against variable spacing is better than split()

def _find_non_zero_bounds(int_list):
    """
    Finds the start and end indices (inclusive) of the segment containing non-zero numbers.
    Returns (-1, -1) if no non-zero numbers are found.
    """
    start_index = -1
    end_index = -1
    for i, digit in enumerate(int_list):
        if digit != 0:
            if start_index == -1: # Found the first non-zero digit
                start_index = i
            end_index = i # Update end_index with the latest non-zero digit found
    return start_index, end_index

def _find_dominant_digit(segment):
    """
    Finds the most frequent digit in the given segment list.
    Assumes segment is non-empty.
    """
    if not segment:
        # This case should ideally not be reached if bounds are correctly identified
        # for non-zero sequences, but added for robustness.
        return None 
    counts = Counter(segment)
    # counts.most_common(1) returns a list like [(dominant_digit, count)]
    dominant_digit, _ = counts.most_common(1)[0]
    return dominant_digit

def transform(input_bytes):
    """
    Applies the dominant digit replacement transformation.

    Args:
        input_bytes: Bytes object representing a space-separated string of digits.

    Returns:
        str: The transformed space-separated string of digits.
    """
    # Step 1: Decode bytes to string
    try:
        input_str = input_bytes.decode('utf-8')
    except AttributeError:
         # If input is already a string (e.g., during testing), use it directly
         input_str = input_bytes
    except Exception as e:
        print(f"Error decoding input: {e}")
        # Depending on requirements, could raise error or return specific error string
        return "Error: Decoding Failed"

    # Step 2: Parse the string into a list of integers
    # Using re.findall is more robust to multiple spaces or leading/trailing spaces
    try:
        # digits_str = re.findall(r'\d+', input_str) # findall returns strings
        # digits = [int(d) for d in digits_str]
        # Simpler alternative if spacing is consistent (one space):
        digits = [int(d) for d in input_str.strip().split()]
    except ValueError:
        print(f"Error parsing digits from string: '{input_str}'")
        return "Error: Parsing Failed" # Indicate error
    except Exception as e:
         print(f"Unexpected error during parsing: {e}")
         return "Error: Unexpected Parsing Issue"


    # Step 3: Identify the boundaries of the non-zero segment
    start_index, end_index = _find_non_zero_bounds(digits)

    # Step 4: Handle the case where all digits are zero
    if start_index == -1:
        # Return the original formatted string (handles potential formatting nuances)
        return " ".join(map(str, digits)) # Use original digits list to preserve structure

    # Step 5: Extract the active segment
    active_segment = digits[start_index : end_index + 1]

    # Step 6: Find the dominant digit within the active segment
    dominant_digit = _find_dominant_digit(active_segment)

    # Error check for dominant digit (shouldn't happen with valid segment)
    if dominant_digit is None:
         print(f"Error: Could not determine dominant digit for segment {active_segment}")
         return "Error: Dominant Calculation Failed"

    # Step 7: Construct the output list
    output_digits = []
    # Add leading part (zeros or empty if segment starts at index 0)
    output_digits.extend(digits[:start_index])
    # Add the dominant digit repeated for the length of the segment
    segment_length = end_index - start_index + 1
    output_digits.extend([dominant_digit] * segment_length)
    # Add trailing part (zeros or empty if segment ends at the last index)
    output_digits.extend(digits[end_index + 1:])

    # Step 8: Format the output list back to a space-separated string
    output_str = " ".join(map(str, output_digits))

    return output_str