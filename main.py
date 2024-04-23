import sys
import importlib

def run():

    list_argv = sys.argv
    if len(list_argv) < 2:
        raise Exception("Must have at least target service name")

    service_name = f"app.{list_argv[1]}_service.run"
    
    service = importlib.import_module(service_name)
    service()

    
if __name__ == "__main__":
    run()