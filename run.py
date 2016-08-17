from cabfansub.config import Config
from cabfansub.main import app

if __name__=="__main__":
    # if len(sys.argv)==1:
    #     print("Starting server as production")
    #     app.config.from_object(config.ProductionConfig)
    # elif len(sys.argv)==2 and sys.argv[1]=="--dev":
    #     print("Starting server as development")
    #     app.config.from_object(config.DevelopmentConfig)
    # else:
    #     print("""
    #         Invalid arguments.
    #
    #         run.py - run cabfansub server
    #         Argument:
    #             --dev: run the server as a development server (with debug features enabled)
    #     """)
    app.run(host="0.0.0.0", port=Config.PORT)
