import requests
import uuid
import src.domain.entities.colour as Colour

class ColourHarverster:
    BASE_URL = "https://d30r5p5favh3z8.cloudfront.net/api/"

    def __init__(self):
        pass

    def harvest_colours(self) -> list[Colour.Colour]:
        response = requests.get(f"{self.BASE_URL}colours")
        response.raise_for_status()
        colours = response.json()

        domain_colours = []

        for colour in colours["colours"]:
            domain_colours.append(Colour.Colour(id=int(colour["code"]), name=colour["name"]))
            #print(f"Harvested colour: {colour['name']} with ID {colour['code']}")
        return domain_colours
    
if __name__ == "__main__":
    harverster = ColourHarverster()
    colours = harverster.harvest_colours()
    