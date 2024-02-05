def encode128(s):
    s = s.encode('ascii').decode('ascii')

    # Create a boolean map indicating whether each character is a digit
    is_digit_map = [char.isdigit() for char in s]

    # Process consecutive digit sequences: if less than 4 digits, change them to False
    i = 0
    while i < len(is_digit_map):
        if is_digit_map[i]:
            j = i
            while j < len(is_digit_map) and is_digit_map[j]:
                j += 1
            if j - i < 4:
                is_digit_map[i:j] = [False] * (j - i)
        i = j if is_digit_map[i] else i + 1

    # Find the last True before False or the end, and change it to False if the count of digits in its sequence is odd
    i = len(is_digit_map) - 1
    while i >= 0:
        if is_digit_map[i]:
            j = i
            while j >= 0 and is_digit_map[j]:
                j -= 1
            if (i - j) % 2 != 0:
                is_digit_map[i] = False
        i = j if is_digit_map[i] else i - 1

    # Initialize codes with the start code for Code 128B or Code 128C depending on the first character
    codes = [105] if is_digit_map[0] else [104]
    i = 0
    while i < len(s):
        if is_digit_map[i]:
            # Switch to Code 128C if not already in it
            if codes[-1] != 105:
                codes.append(99)
            while i < len(s) and is_digit_map[i]:
                codes.append(int(s[i:i+2], 10))
                i += 2
            # Switch back to Code 128B if not at the end
            if i < len(s):
                codes.append(100)
        else:
            # Use Code 128B
            mapping = dict((chr(c), [98, c + 64] if c < 32 else [c - 32]) for c in range(128))
            codes.extend(mapping[s[i]])
            i += 1

    check_digit = (codes[0] + sum(i * x for i,x in enumerate(codes))) % 103
    codes.append(check_digit)
    codes.append(106) # stop code
    chars = ('Â' + ''.join(chr(i) for i in range(33, 127)) + ''.join(chr(i) for i in range(195, 208))).encode('latin-1')
     #'Â' for libre barcode font, ' ' for code128 font
    return ''.join(chr(chars[x]) for x in codes)
