from flask import Flask, render_template, request, redirect, url_for, session
from steganography import encode_message, decode_message
import traceback
import os

app = Flask(__name__)
secret_key = os.urandom(16)
app.secret_key = secret_key

# Route for the home page
@app.route('/')
def home():
    return render_template('index.html')

# Route for encoding a message
@app.route('/encode', methods=['GET', 'POST'])
def encode():
    if request.method == 'POST':
        try:
            image_file = request.files['image']
            message = request.form.get('message', '')

            # Save the image file
            image_path = 'uploaded_image.png'
            image_file.save(image_path)

            # Encode the message into the image
            encoded_image = encode_message(image_path, message)

            # Save the encoded image
            encoded_image_path = 'encoded_image.png'
            encoded_image.save(encoded_image_path)

            return render_template('encode.html', encoded_image_path=encoded_image_path)
        except Exception as e:
            print(f"An error occurred during encoding: {str(e)}")
            traceback.print_exc()
            return "Error during encoding. Please try again."

    # Render the encode.html template for GET requests
    return render_template('encode.html')

@app.route('/decode', methods=['GET', 'POST'])
def decode():
    if request.method == 'POST':
        try:
            image_file = request.files['encoded_image']

            # Save the image file
            image_path = 'uploaded_image.png'
            image_file.save(image_path)

            # Decode the message from the image
            decoded_message = decode_message(image_path)

            # Store the decoded message in the session
            session['decoded_message'] = decoded_message

            # Redirect to the show_decoded_message route
            return redirect(url_for('show_decoded_message'))
        except Exception as e:
            print(f"An error occurred during decoding: {str(e)}")
            traceback.print_exc()
            return "Error during decoding. Please try again."

    # Render the decode.html template for GET requests
    return render_template('decode.html')

@app.route('/show_decoded_message')
def show_decoded_message():
    decoded_message = session.pop('decoded_message', '')
    return render_template('decode.html', decoded_message=decoded_message)

@app.route('/clear_decoded_message')
def clear_decoded_message():
    session.pop('decoded_message', None)
    return '', 204
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8080)
