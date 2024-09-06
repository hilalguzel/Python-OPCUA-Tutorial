# Define library
import sys
sys.path.insert(0, "..")
import time
from opcua import ua, Server

if __name__ == "__main__":
    # Set Server
    server = Server()
    server.set_endpoint("opc.tcp://0.0.0.0:4840/freeopcua/server/")

    # Crate own namespce
    uri = "http://examples.freeocpua.github.io"
    idx = server.register_namespace(uri)

    # Create Objects node
    objects = server.get_objects_node()

    # Add object and variable
    myobj = objects.add_object(idx, "MyObject")
    myvar = myobj.add_variable(idx, "MyVariable", 6.7)
    myvar.set_writable()   #Set MyVariable to be Writable by clients


    # Start Server
    server.start()

    try:
        count = 0
        while True:
            time.sleep(1)
            count += 0.1
            myvar.set_value(count)
    finally:
        #close connection, remove subscription, etc
        server.stop()