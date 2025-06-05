def map_range(value, start1, stop1, start2, stop2):
    """
    Map a value from one range to another range.

    Parameters:
        value (float): The value to be mapped.
        start1 (float): Lower bound of the input range.
        stop1 (float): Upper bound of the input range.
        start2 (float): Lower bound of the output range.
        stop2 (float): Upper bound of the output range.

    Returns:
        float: The mapped value.
    """
    return start2 + (stop2 - start2) * ((value - start1) / (stop1 - start1))