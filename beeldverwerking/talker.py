from .web.app import App
from .web.eventhandler import eventHandler
from .image.editor import editImage
from .publisher_node.publisherNode import Publisher
import rclpy



def main(args=None):
    print(args)
    #Create ROS2 Node
    rclpy.init(args=args)
    publisher = Publisher()

    #Setup eventHandler for the webinterface
    _eventHandler = eventHandler()

    #Python function for webinterface 
        #Image editing
    _eventHandler.createEvent('upload', lambda file: editImage(file))
        #Send over ROS2
    _eventHandler.createEvent('send', lambda image: publisher.send_image(image))

    #Run Web Interface
    webApp = App(_eventHandler)
    webApp.run(8080)

    #Destroy ROS2 Node
    publisher.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()