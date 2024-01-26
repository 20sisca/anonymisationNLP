class Arret:
    def __init__(self, text, identifier):
        self.text = text
        self.id = identifier
        self.protagonistsPositions = []

    # def add_found_name(self, name):
    #     self.foundNames.append(name)

    def __str__(self):
        return f"Arret ID: {self.id}, Text: {self.text}, Found Names: {', '.join(self.foundNames)}"

