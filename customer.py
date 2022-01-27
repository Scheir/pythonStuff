import json
class Customer:
    def __init__(self, data):
        try:
            self.name = data.get("name")
            self.type = data.get("type")
        except:
            print("Failed to create Customer", data)
            raise TypeError

    def __del__(self):
        pass
        
    def dictify(self) -> str:
        return {"name":self.name,"type":self.type}