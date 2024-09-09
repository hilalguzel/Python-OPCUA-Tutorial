import sys
sys.path.insert(0, "..")
import time
from opcua import ua, Client
from opcua.common.subscription import Subscription


class SubHandler(object):
    def datachange_notification(self, node, val, data):
        print(f"Change: {node} - New value: {val}")

if __name__ == "__main__":
    client = Client("opc.tcp://localhost:4840/freeopcua/server/")

    try:
        client.connect()

        root = client.get_root_node()
        print("Objects node is: ", root)
        print("Children of root are: ", root.get_children())


        # Getting a variable node using its browse path
        temp_var = root.get_child(["0:Objects", "2:MyObject", "2:Temperature"])
        pressure_var = root.get_child(["0:Objects", "2:MyObject", "2:Pressure"])
        time_var = root.get_child(["0:Objects", "2:MyObject", "2:Time"])

        # Read values from server
        print("Initial values: ")
        print("Temperature: ", temp_var.get_value())
        print("Pressure: ", pressure_var.get_value())
        print("Time: ", time_var.get_value())

        #Create Subscription
        handler = SubHandler()
        sub = client.create_subscription(500, handler) 

        # Subscribe server
        sub.subscribe_data_change(temp_var)
        sub.subscribe_data_change(pressure_var)
        sub.subscribe_data_change(time_var)

        print("Subscribed to the server, listening for changes...")

        while True:
            # If you want change values
            time.sleep(5)
            new_temp = 36.0
            temp_var.set_value(new_temp) # Update Temprature
            print(f"New Temprature value {temp_var.get_value()}")

    finally:
        client.disconnect()