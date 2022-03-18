from flask import Flask, redirect
from flask import request
import editor
import cv2
import os

app = Flask(__name__, static_url_path='/static')

@app.route('/', methods=['GET', 'POST'])
def UploadFile():

    # File Upload HTML
    html = '''
            <!doctype html>
            <title>Upload new File</title>
            <h1>Upload new File</h1>
            <form action="" method=post enctype=multipart/form-data>
                <p><input type=file name=file></p>
                <input type=submit value=Upload>
            </form>
        '''
    # IF UPLOADED
    if request.method == 'POST':
        file = request.files['file']
        if '.' in file.filename:

            #SAVE UPLOADED IMAGE
            file.save('static/tmp.jpg')
            tmpImage = cv2.imread('static/tmp.jpg')

            # EDIT IMAGE
            images = editor.EditImage(tmpImage)
            for image in images:
                cv2.imwrite('static/'+image['name']+'.jpg', image['image'])
            os.remove("static/tmp.jpg")

            #IMAGES HTML
            htmlImages = '''
                        <!doctype html>
                        <title>Images</title>
                        <h1>Images</h1>
                        '''
            
            for image in images:
                htmlImages+='<a href="/static/' + image['name'] + '.jpg"><img src="/static/' + image['name'] + '.jpg" width="300px" height="auto" /></a>'
            return html + htmlImages
    
    #RETURN WEBPAGE
    return html


app.run()