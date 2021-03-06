"""
This module contains all classes relating to the trains.
"""

import math
import pygame
from seprcph.event import EventManager, Event
from seprcph.renderable import Renderable
from seprcph.effect import Affectable


class Train(Renderable, Affectable):
    """
    Class representing train objects in the game
    """
    def __init__(self, player, speed, capacity, city, current_load, image):
        """
        Args:
            player: The player that owns this train
            speed: The speed of the train
            capacity: The capacity of the train
            city: The city the train is created at
            current_load: The amount of cargo the train is carrying
            image: The pygame surface associated with this train
        """
        self.player = player
        self.speed = speed
        self.capacity = capacity
        self.current_load = current_load
        self.city = city

        # The following are for dealing with train movement
        self.track = None
        self.rotation = None
        self.distance = None
        self.counter = 0

        super(Train, self).__init__(city.pos, image)
        Affectable.__init__(self)

        EventManager.add_listener('goal.completed', self.unload)
        EventManager.add_listener('goal.started', self.load)

    def depart(self, track):
        """
        Method to be called when a train departs from a city

        Args:
            track: a track object which the train should travel along.
        """
        assert self.city in track.cities
        self.track = track
        self.rotation = track.rotation()
        self.distance = track.length()
        self.pos = self.city.pos

        # XXX: Need to set self.city correctly.
        e = Event('train.departure', train=self, city=self.city)
        EventManager.notify_listeners(e)

    def arrive(self, city):
        """
        Method to be called when a train arrived at a city
        
        Args:
            city: the city that the train is arriving in
        """
        self.city = city
        self.track = None
        self.rotation = 0
        self.distance = 0

        e = Event('train.arrival', train=self, city=self.city)
        EventManager.notify_listeners(e)

    def update(self):
        """
        Updates the Train object
        """
        if self.track:
            self.image = pygame.transform.rotate(self.image, self.track.rotation)
        move_distance = (
            math.fabs((self.track.cities[0].pos[0] - self.track.cities[1].pos[0]) /
                self.distance) * self.speed,
            math.fabs((self.track.cities[0].pos[1] - self.track.cities[1].pos[1]) /
                self.distance) * self.speed
        )

        self.counter += self.speed

        if self.counter > self.track.length:
            self.arrive(self.track.cities[0])
        else:
            self.pos[0] += move_distance[0]
            self.pos[1] += move_distance[1]
            
        self.decrement_turns()

    def unload(self, event):
        """
        The handler for when a goal is completed.
        
        Args:
            event: The event raise upon goal completion
        """
        if self.city not in event.goal.end_cities:
            return
            
        self.current_load = 0

    def load(self, event):
        """
        The handler for when a goal is started.
        
        Args:
            event: The event raised when the train is loaded
        """
        if self.city != event.goal.start_city:
            return
            
        # Just fill the train up completely.
        self.current_load = self.capacity
