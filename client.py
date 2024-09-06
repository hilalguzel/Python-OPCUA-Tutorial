import sys
sys.path.insert(0, "..")
from opcua import ua, Client

if __name__ == "__main__":
    client = Client("opc.tcp://localhost:4840/freeopcua/server/")
    # connect using a user
    # client = Client("opc.tcp://localhost:4840/freeopcua/server/")

    try:
        client.connect()
        root = client.get_root_node()
        print("Objects node is: ", root)

        print("Children of root are: ", root.get_children())



        # Getting a variable node using its browse path
        myvar = root.get_child(["0:Objects", "2:MyObject", "2:MyVariable"])
        obj = root.get_child(["0:Objects", "2:MyObject"])
        print("myvar is : ", myvar)
        print("myobj is: ", obj)
        print(myvar.get_value())

    finally:
        client.disconnect()