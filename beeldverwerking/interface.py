from ast import Lambda
from .web.app import *
from .image.editor import editImage

class eventHandler():
    def __init__(self):
        self.events = []

    def createEvent(self, name, func):
        self.events+=[{
            'name': name,
            'func': func,
        }]

    def runEvent(self, name):
        for index in range(len(self.events)):
            if self.events[index]['name'] == name:
                return self.events[index]['func']
        print('EventHandler: Nothing found')
        return None

def test(name):
    print(name)

def main(args=None):
    _eventHandler = eventHandler()
    _eventHandler.createEvent('upload', lambda file: test(file))
    webApp = App(_eventHandler)
    webApp.run()

if __name__ == '__main__':
    main()