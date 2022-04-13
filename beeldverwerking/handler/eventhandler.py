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