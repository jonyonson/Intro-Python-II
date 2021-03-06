class Item:
    def __init__(self, name, description):
        self.name = name
        self.description = description

    def __str__(self):
        return self.name

    def on_take(self):
        print(f"\nYou have picked up a {self.name}. {self.description}")

    def on_drop(self):
        print(f"\nYou have dropped {self.name}")


class LightSource(Item):
    def __init__(self, name, description):
        super().__init__(name, description)

    def on_drop(self):
        print(f"\nIt's not wise to drop your source of light!")
