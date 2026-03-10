def bytes_comparison(expected, received):
    expected_len = len(expected) #11
    received_len = len(received) #62

    for i in range(received_len - expected_len + 1):
        if received[i:i + expected_len] == expected:
            print(f"Match found at index {i}")
            return i
    print("No match found.")
    return -1