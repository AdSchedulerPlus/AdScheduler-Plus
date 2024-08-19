from flask import Flask, request, jsonify, send_from_directory
import os

app = Flask(__name__)

# Admin email list
ADMIN_EMAILS = {'admin@example.com'}

# Static file serving for frontend
@app.route('/<path:filename>')
def serve_static(filename):
    return send_from_directory('static', filename)

# Admin check decorator
def admin_required(f):
    def wrapper(*args, **kwargs):
        user_email = request.headers.get('User-Email')
        if user_email in ADMIN_EMAILS:
            return f(*args, **kwargs)
        else:
            return jsonify({'message': 'Access denied'}), 403
    return wrapper

@app.route('/payment', methods=['POST'])
def payment():
    amount = request.form.get('amount')
    if not amount:
        return jsonify({'message': 'Amount is required'}), 400

    if 'User-Email' in request.headers and request.headers['User-Email'] in ADMIN_EMAILS:
        return jsonify({'message': 'Payment processed successfully for admin!'}), 200
    else:
        # Here you would integrate with a real payment gateway
        return jsonify({'message': 'Payment processed successfully for non-admin!'}), 200

if __name__ == '__main__':
    app.run(debug=True)
