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

    # Add variables
    temp_var = myobj.add_variable(idx, "Temperature", 25.0)
    pressure_var = myobj.add_variable(idx, "Pressure", 101.3)
    time_var = myobj.add_variable(idx, "Time", time.time())

    # Set all variables to be writable by clients
    temp_var.set_writable()
    pressure_var.set_writable()
    time_var.set_writable()
    
    # Start Server
    server.start()

    print("Server is running, variables are updating...")

    try:
        while True:
            time.sleep(1)
            time_var.set_value(time.time())
    finally:
        #close connection, remove subscription, etc
        server.stop()