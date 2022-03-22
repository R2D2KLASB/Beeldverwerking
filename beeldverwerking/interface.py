from .submodules import web

def main(args=None):
    WebApp = web.App()
    WebApp.run()


if __name__ == '__main__':
    main()