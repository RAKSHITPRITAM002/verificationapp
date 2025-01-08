from flask import Flask, render_template, request, jsonify
import random

app = Flask(__name__)

# Generate random numbers for the verification process
def generate_numbers():
    return [random.randint(0, 9) for _ in range(6)]

# Store the generated numbers (for simplicity, in memory)
generated_numbers = generate_numbers()

@app.route("/")
def index():
    return render_template("index.html", numbers=generated_numbers)

@app.route("/validate", methods=["POST"])
def validate():
    global generated_numbers
    user_input = request.json.get("user_input", [])
    if len(user_input) != 6:
        return jsonify({"status": "error", "message": "Invalid input length!"})

    # Check if the input matches the generated numbers
    if all(int(user_input[i]) == generated_numbers[i] for i in range(6)):
        return jsonify({"status": "success", "message": "Verification Successful!"})
    else:
        # Regenerate numbers if validation fails
        generated_numbers = generate_numbers()
        return jsonify({"status": "fail", "message": "Verification Failed! Try Again.", "new_numbers": generated_numbers})

if __name__ == "__main__":
    app.run(debug=True)
