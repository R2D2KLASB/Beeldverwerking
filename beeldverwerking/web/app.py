from crypt import methods
from flask import Flask, redirect, request, flash
import json


class App:
    
    def __init__(self, eventHandler):
        self.eventHandler = eventHandler
        self.webApp = Flask(__name__, static_url_path='/static')
        self.webApp.secret_key = b'TEST'
        self.addUrls()

    # Declarage pages
    def addUrls(self):
        self.webApp.add_url_rule('/', 'index', self.home, methods=["GET"])
        self.webApp.add_url_rule('/upload', 'upload', self.upload, methods=['POST'])
        self.webApp.add_url_rule('/image', 'image', self.image)

    # Homepage
    def home(self):
        # File Upload GET
        return '''
                <!doctype html>
                <title>Upload new File</title>
                <h1>Upload new File</h1>
                <form action="/upload" method=post enctype=multipart/form-data>
                    <p><input type=file name=file></p>
                    <input type=submit value=Upload>
                </form>
            '''

    # File Upload POST
    def upload(self):
        file = request.files['file']
        extensions = ['jpg', 'jpeg', 'png']
        # Check if file is an suporrted image otherwise return to home
        if file.filename.split('.')[-1] in extensions:
            # Check the eventHandler and run function if excist
            self.eventHandler.runEvent('upload')(file.filename)
            return '<h1>' + file.filename + ' uploaded</h1>'
        else:
            return '''<script LANGUAGE='JavaScript'>
                        window.alert('File not supported');
                        window.location.href='/';
                    </script>'''
    
    def image(self):
        return '<h1>image</h1>'

    # Run Web Interface
    def run(self):
        self.webApp.run()