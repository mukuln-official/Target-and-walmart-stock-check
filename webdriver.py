from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')

def home():
  return 'M GOOD'

def run():
    app.run(host="0.0.0.0", port=0000)

def keep_alive():
    runner = Thread(target=run)
    runner.start()