import unittest, random

import pygame

from seprcph.deck import Deck
from seprcph.hand import Hand
from seprcph.card import Card
from seprcph.event import EventManager, Event

x = 0
def _func(_):
    global x
    x = 1

class TestHandMethods(unittest.TestCase):

    def setUp(self):
        image = pygame.Surface((10, 10))
        self.card1 = Card("card1", None, None, None, image)
        self.card2 = Card("card2", None, None, None, image)
        self.card3 = Card("card3", None, None, None, image)
        self.card4 = Card("card4", None, None, None, image)
        self.card5 = Card("card5", None, None, _func, image)
        self.deck = Deck(None, [self.card1, self.card2, self.card3,
                                self.card4], None)
        self.hand = Hand([self.card5], self.deck, 1)

    def test_draw_cards(self):
        self.hand.draw_cards(2)
        self.assertEqual(self.hand.cards, [self.card5, self.card4, self.card3])

    def test_discard(self):
        self.hand.discard(0)
        self.assertEqual(self.hand.deck.discard, [self.card5])

    def test_play(self):
        EventManager.add_listener('card.triggered', _func)
        self.hand.play(Event('card.played', card=self.card5, hand=self.hand))
        self.assertEqual(x, 1)
