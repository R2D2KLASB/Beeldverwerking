from flask import Flask, redirect, request

class App:
    
    def __init__(self, eventHandler):
        self.eventHandler = eventHandler
        self.webApp = Flask(__name__, static_url_path='/static')
        self.addUrls()

    # Declarage pages
    def addUrls(self):
        self.webApp.add_url_rule('/', 'index', self.home, methods=["GET"])
        self.webApp.add_url_rule('/upload', 'upload', self.uploaded, methods=['POST'])
        self.webApp.add_url_rule('/send', 'send', self.send, methods=['POST'])

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
    def uploaded(self):
        file = request.files['file']
        extensions = ['jpg', 'jpeg', 'png']
        # Check if file is an suporrted image otherwise return to home
        if file.filename.split('.')[-1] in extensions:
            # Check the eventHandler and run function if excist
            response = self.eventHandler.runEvent('upload')(file.stream.read())
            # Render button for sending gcode data over ROS2
            htmlSend = '''
                <form action="/send" method=post enctype=multipart/form-data>
                    <textarea name="gcode" rows="200" cols="100">''' + response['gcode'] + '''</textarea>
                    <input type=submit value=Send>
                </form>
            '''
            return self.home() + '<h1>' + file.filename + ' uploaded</h1>' + response['image'] + htmlSend
        else:
            # Return to home
            return '''<script LANGUAGE='JavaScript'>
                        window.alert('File not supported');
                        window.location.href='/';
                    </script>'''
    
    #Send image over ROS2
    def send(self):
        image = request.form.get('gcode')
        self.eventHandler.runEvent('send')(image)
        return '<h1>Image is sended over ros2</h1>' + self.home()

    # Run Web Interface
    def run(self, port=5000):
        self.webApp.run(port=port)