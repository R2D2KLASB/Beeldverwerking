from flask import Flask, redirect, request

class App():
    def __init__(self):
        self.app = Flask(__name__, static_url_path='/static')

    def run(self):
        self.app.run()
