from flask import Flask

app = Flask(__name__)

@app.route('/')
def home():
    return '''
    <html>
    <body style="font-family:Arial; text-align:center; padding:50px; background:#f0f4f8">
        <h1>🚀 CI/CD Pipeline Demo</h1>
        <p>Deployed automatically via Jenkins → Docker → Kubernetes</p>
        <p style="color:blue; font-size:40px">✅ Version 1.0 — Live on AWS!</p>
    </body>
    </html>
    '''

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=9000)