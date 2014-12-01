from event import Event, EventManager

class Card(object):
    """
    Class describing the buff/debuff cards

    """

    def __init__(self, name, id, description, effect, image):
        """
        Args:
            name: The plain English name of the Card
            id: A unique identifier
            description: A plain English description of the effect
            effect: An Event object to be passed to the EventManager when the card is played
            image: The image file to be displayed with the card in the GUI

        """
        assert isinstance(effect, Event)
        self.name = name
        self.id = id
        self.desc = description
        self.effect = effect
        self.image = image

    def trigger(self):
        """
        Activates the card's effect.
        NOT the same as playing a card. This method is in the Hand class.

        """
        EventManager.notify_listeners(self.effect)
