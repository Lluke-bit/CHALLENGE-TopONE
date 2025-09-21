from device_info import DeviceEnvironmentSDK

class teste:
    def __init__(self):
        print(self)
    def start(self):
        ip_teste = DeviceEnvironmentSDK.get_network_info(self=self)
        print(ip_teste)

teste.start()