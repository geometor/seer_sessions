"""
Performs a circular right shift on a sequence of 12 digits provided as a space-separated byte string.
The last digit moves to the first position, and all other digits shift one position to the right.
The output is returned as a standard space-separated string.
"""

# No specific imports needed beyond standard operations

def transform(input_data):
    """
    Transforms the input byte string by performing a circular right shift on the sequence of digits.

    Args:
        input_data (bytes or str): A byte string (or standard string for testing) 
                                   containing 12 digits separated by spaces.

    Returns:
        str: The transformed string with digits shifted circularly to the right by one position,
             separated by spaces. Returns an empty string or raises error on invalid input.
    """

    # --- Input Handling and Decoding ---
    decoded_str = None
    # Check if input is bytes and decode it
    if isinstance(input_data, bytes):
        try:
            # Decode using UTF-8, replace errors to handle potential issues gracefully
            decoded_str = input_data.decode('utf-8', errors='replace')
        except UnicodeDecodeError as e:
            # Handle unexpected decoding errors
            raise ValueError(f"Failed to decode input bytes: {e}")
    # Check if input is already a string
    elif isinstance(input_data, str):
        decoded_str = input_data
    # Handle unexpected input types
    else:
        raise TypeError(f"Input must be bytes or string, received {type(input_data)}")

    # --- Parsing ---
    # Split the decoded string into a list of elements based on spaces
    elements = decoded_str.split()

    # --- Validation (Optional but Recommended) ---
    # Check if the expected number of elements (digits) were found
    # Based on examples, we expect 12 digits.
    if len(elements) != 12:
        # Decide how to handle unexpected input length.
        # Options: return empty string, raise error, or try to process anyway.
        # For now, let's raise an error for clarity, though based on task constraints
        # it might be safe to assume valid input.
        # If processing should continue, remove or comment out this check.
        # Consider logging a warning instead if strict failure isn't desired.
        # raise ValueError(f"Input expected 12 space-separated elements, found {len(elements)}")
        # If we want to be robust to empty input:
        if not elements:
            return "" # Return empty string for genuinely empty input

    # --- Transformation: Circular Right Shift ---
    # If the list is not empty, perform the shift
    if elements:
        # Identify the last element
        last_element = elements[-1]
        # Get all elements except the last one
        remaining_elements = elements[:-1]
        # Create the new list with the last element moved to the front
        shifted_elements = [last_element] + remaining_elements
    else:
        # If elements was empty after split (e.g., input was just spaces)
        shifted_elements = []


    # --- Formatting Output ---
    # Join the elements of the shifted list back into a single string, separated by spaces
    output_str = " ".join(shifted_elements)

    return output_str