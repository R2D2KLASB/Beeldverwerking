from flask import Flask, redirect, request
from base64 import b64decode


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
        self.webApp.add_url_rule('/make', 'make', self.make, methods=['POST'])

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
            image = self.eventHandler.runEvent('edit')(file.stream.read()).decode("utf-8")
            # If image editing succes
            if image:
                sendButton = '''
                <form action="/make" method=post enctype=multipart/form-data>
                    <input type="text" hidden="true" name="image" value="''' + image + '''">
                    <input type="submit" value="Continue">
                </form>
                '''
                return self.home() + '<h1>Detected lines, ok? click continue</h1><img height="auto" width="400px" src="data:;base64,'+ image +'"/>' + sendButton
            else:
                return self.home() + '<h1>Error image editing</h1>'


    def make(self):
        image = request.form['image']
        svg, path, name = self.eventHandler.runEvent('svg')(image)
        if svg:
            gcode = self.eventHandler.runEvent('gcode')(path, name)
            if gcode:
                htmlSend = '''<p></p>
                    <form action="/send" method=post enctype=multipart/form-data>
                        <input type=submit value=Send>
                        <p></p>
                        <textarea id="gcodetext" name="gcode" rows="200" cols="100">''' + gcode + '''</textarea>
                    </form>
                    '''
                htmlSave = '''<p></p><button id="save-button">Save</button><p></p>'''
                Js = '''<script>
                            function saveTextAsFile() {
                                var textToWrite = document.getElementById('gcodetext').innerHTML;
                                var textFileAsBlob = new Blob([ textToWrite ], { type: 'text/plain' });
                                var fileNameToSaveAs = "image.gcode"; //filename.extension
                                var downloadLink = document.createElement("a");
                                downloadLink.download = fileNameToSaveAs;
                                downloadLink.innerHTML = "Download File";
                                if (window.webkitURL != null) {
                                    downloadLink.href = window.webkitURL.createObjectURL(textFileAsBlob);
                                } else {
                                    downloadLink.href = window.URL.createObjectURL(textFileAsBlob);
                                    downloadLink.onclick = destroyClickedElement;
                                    downloadLink.style.display = "none";
                                    document.body.appendChild(downloadLink);
                                }
                                downloadLink.click();
                            }
                            var button = document.getElementById('save-button');
                            button.addEventListener('click', saveTextAsFile);
                        </script>'''
                return svg + htmlSave + htmlSend + Js 
            else:
                return self.home + "<h1>Error creating GCODE</h1>"
        else:
            return self.home + "<h1>Error creating SVG</h1>"
    
    #Send image over ROS2
    def send(self):
        image = request.form.get('gcode')
        self.eventHandler.runEvent('send')(image)
        return '<h1>Image is sended over ros2</h1>' + self.home()

    # Run Web Interface
    def run(self, port=5000):
        self.webApp.run(port=port)