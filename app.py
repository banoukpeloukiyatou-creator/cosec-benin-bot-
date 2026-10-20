import os
from flask import Flask, request
app = Flask(__name__)
VERIFY_TOKEN = "COSEC_BENIN_TOKEN_2024"
@app.route('/webhook', methods=['GET', 'POST'])
def webhook():
    if request.method == 'GET':
        mode = request.args.get('hub.mode')
        token = request.args.get('hub.verify_token')
        challenge = request.args.get('hub.challenge')
        if mode == "subscribe" and token == VERIFY_TOKEN:
            return challenge, 200
        else:
            return "Forbidden", 403
    if request.method == 'POST':
        print("Message recu!")
        print(request.json)
        return "OK", 200
@app.route('/')
def home():
    return "COSEC BENIN BOT ACTIF !"
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 3000))
    app.run(host='0.0.0.0', port=port, debug=False)
