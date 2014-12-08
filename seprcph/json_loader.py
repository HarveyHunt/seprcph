import json
import pygame


def objs_from_json_file(file_path, cls):
    """
    Create a list of objects that are defined within a JSON file.

    The json file needs to contain a list of the objects, with parameters that
    match up to those defined in cls.

    Args:
        file_path: The location of the JSON file to be read.
        cls: The Class that the object will be created from.
    """

    def _sprite_hook(kwargs):
        """
        Load an image using the filepath passed as image.

        Args:
            kwargs: A dictionary of elements from the json file.
        """
        if 'image' in kwargs:
            kwargs['image'] = pygame.image.load(kwargs['image'])
        return cls(**kwargs)

    with open(file_path, 'r') as json_file:
        return json.load(json_file, object_hook=_sprite_hook)
