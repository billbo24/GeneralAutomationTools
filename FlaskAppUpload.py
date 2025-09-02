


# A very simple Flask Hello World app for you to get started with...

from flask import Flask, request, jsonify, render_template_string, send_file
from processor import process_data
from EmailScript import send_email
from AlternateCase import alternate_case
from dotenv import load_dotenv
import os
import io

app = Flask(__name__)

HTML = """
<!doctype html>
<title>Upload a Text File</title>
<h1>Upload a .txt file</h1>
<form method=post enctype=multipart/form-data>
  <input type=file name=file>
  <input type=submit value=Upload>
</form>
{% if processed %}
  <h2>Processed Result:</h2>
  <pre>{{ processed }}</pre>
{% endif %}
"""

@app.route("/upload", methods=["GET", "POST"])
def upload_file():
    processed = None
    if request.method == "POST":
        uploaded_file = request.files["file"]
        if uploaded_file and uploaded_file.filename.endswith(".txt"):
            text = uploaded_file.read().decode("utf-8")

            # --- make changes here ---
            processed_text = text.upper()  # example: uppercase everything

           # Create an in-memory file to send back
            output = io.BytesIO()
            output.write(processed_text.encode("utf-8"))
            output.seek(0)

            return send_file(
                output,
                as_attachment=True,
                download_name="processed.txt",
                mimetype="text/plain"
            )

    # Simple upload form
    return """
    <!doctype html>
    <title>Upload a Text File</title>
    <h1>Upload a .txt file to process</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form>
    """



@app.route('/')
def hello_world():
    return 'Hello from Flask!'


@app.route("/webhook", methods=["POST"])
def webhook():
    data = request.get_json(silent=True)  # silent=True prevents exceptions, returns None if invalid
    if data is None:
        return jsonify({'error': 'Invalid or missing JSON'}), 400

    result = process_data(data)
    return jsonify(result)


@app.route("/email", methods=["POST"])
def email():
    data = request.get_json(silent=True)  # silent=True prevents exceptions, returns None if invalid
    if data is None:
        return jsonify({'error': 'Invalid or missing JSON'}), 400


    print("Content-Type:", request.headers.get('Content-Type'))
    print("Raw body:", request.data.decode('utf-8', errors='replace'))

    #Load the .env file
    load_dotenv('/home/billbo24/mysite/.env')

    to_email = data['To']

    from_email = os.getenv('EMAIL')
    password = os.getenv("PASSWORD")

    #from_email = data['From']
    subject = data['Subject']
    body = data['Body']
    #password = data['Password']

    new_body = alternate_case(body)

    send_email(subject, new_body, from_email, to_email, password)

    return jsonify({'Body':'Message Sent!'}),200


if __name__ == "__main__":
    app.run(debug=True)