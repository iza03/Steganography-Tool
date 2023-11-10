from PIL import Image

def encode_message(image_path, message):
    # Open the image
    image = Image.open(image_path)
    image = image.convert("RGB")  # Convert the image to RGB color mode
    width, height = image.size
    # Calculate the total number of available bits
    total_bits = width * height * 3

    # Calculate the number of bits needed for the overhead
    overhead_bits = 16  # Assuming a delimiter of 16 bits

    # Subtract the overhead bits from the total bits
    available_bits = total_bits - overhead_bits

    # Calculate the maximum message length in bytes
    max_message_length = available_bits // 8

    if len(message) > max_message_length:
        raise ValueError(f"The message is too long. Maximum allowed length is {max_message_length} characters.")

    # Convert the message to binary representation
    binary_message = ''.join(format(ord(char), '08b') for char in message)
    binary_message += '1' * 16  # Add a delimiter of 16 consecutive '1' characters at the end

    # Get the pixels of the image
    pixels = image.getdata()
    encoded_pixels = []

    bit_index = 0
    for pixel in pixels:
        if bit_index < len(binary_message):
            r, g, b = pixel

            # Encode the message into the least significant bit of each color channel
            r = (r & 0xFE) | int(binary_message[bit_index])
            bit_index += 1
            if bit_index < len(binary_message):
                g = (g & 0xFE) | int(binary_message[bit_index])
                bit_index += 1
            if bit_index < len(binary_message):
                b = (b & 0xFE) | int(binary_message[bit_index])
                bit_index += 1

            encoded_pixels.append((r, g, b))
        else:
            encoded_pixels.append(pixel)

    # Create a new image with the encoded pixels
    encoded_image = Image.new(image.mode, image.size)
    encoded_image.putdata(encoded_pixels)

    return encoded_image


def decode_message(image_path):
    # Open the image
    image = Image.open(image_path)

    # Get the pixels of the image
    pixels = image.getdata()

    binary_message = ''
    for pixel in pixels:
        r, g, b = pixel

        # Extract the least significant bit from each color channel
        binary_message += str(r & 1)
        binary_message += str(g & 1)
        binary_message += str(b & 1)

        # Check if the delimiter has been reached
        if binary_message[-16:] == '1' * 16:
            break

    message = ''
    for i in range(0, len(binary_message) - 16, 8):
        byte = binary_message[i:i+8]
        message += chr(int(byte, 2))

    return message
