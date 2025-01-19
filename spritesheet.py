import pygame
import json

"""
    image_at / images_at
        extracts a single image or multiple images from a spritesheet by coordinates

    image_name / image_names
        extracts a single image or multiple images from a spritesheet by name from a datasheet

    image_sequence
        extracts a sequence of images from a spritesheet by name from a datasheet

    Datasheet

    The datasheet is a JSON file that describes each frame by coordinates and size. It can
    also describe an assembly of frames that are combined into a single image.
"""
class spritesheet(object):
    def __init__(self, imagefile, datafile=None):
        try:
            self.sheet = pygame.image.load(imagefile).convert()             
        except pygame.error as e:
            print(f"Unable to load spritesheet image: {imagefile}")
            print(e)
            raise SystemExit
        self.datafile = datafile
        self.frames = {}
        self.assemblies = {}
        self.colorkey = None
        if datafile:
            with open(datafile, 'r') as f:
                data = json.load(f)
                for frame in data["frames"]:
                    self.frames[frame["name"]] = frame["frame"]
                if "assemblies" in data:
                    for assembly in data["assemblies"]:
                        self.assemblies[assembly["name"]] = {
                            "size" : assembly["size"],
                            "frames" : assembly["frames"]
                        }
                self.colorkey = data["meta"]["colorkey"]
    
    def image_at(self, rectangle, colorkey=None, scale2x=False):
        """ Loads image from rectangle defined as a tuple (x, y, w, h) """
        rect = pygame.Rect(rectangle)
        image = pygame.Surface(rect.size).convert()
        image.blit(self.sheet, (0, 0), rect)
        if colorkey is not None:
            if colorkey == -1:
                colorkey = image.get_at((0,0))
            image.set_colorkey(colorkey, pygame.RLEACCEL)

        if scale2x:
            image = pygame.transform.scale2x(image)
        return image

    def images_at(self, rects, colorkey=None):
        """Loads multiple images, supply a list of coordinates"""
        return [self.image_at(rect, colorkey) for rect in rects]

    def image_name(self, name, scale2x=False):
        """ Loads an image by name using a datasheet """

        if name in self.frames:
            frame = self.frames[name]
            return self.image_at((frame["x"], frame["y"], frame["w"], frame["h"]), 
                                 colorkey=self.colorkey, scale2x=scale2x)

        elif name in self.assemblies:
            assembly = self.assemblies[name]
            size = assembly["size"]

            rect = pygame.Rect((0, 0), (size["w"], size["h"]))
            assembled_image = pygame.Surface(rect.size).convert()

            for frame in assembly["frames"]:
                frame_def = self.frames[frame["name"]]
                image = self.image_at((frame_def["x"], frame_def["y"], frame_def["w"], frame_def["h"]))
                
                assembled_image.blit(image, (frame["offx"], frame["offy"]))

            assembled_image.set_colorkey(self.colorkey, pygame.RLEACCEL)

            if scale2x:
                assembled_image = pygame.transform.scale2x(assembled_image)

            return assembled_image
        
        else:
            print(f"Unable to find frame '{name}' in the datafile '{self.datafile}'")
            raise SystemExit

    def image_names(self, names, scale2x=False):
        """ Loads multiple images by name using a datasheet """
        return {name : self.image_name(name, scale2x=scale2x) for name in names}

    def image_sequence(self, name, scale2x=False):
        """ Loads a sequence of images by name using a datasheet """

        images = []
        idx=1
        frame_name = f"{name}-{idx}"

        while frame_name in self.frames or frame_name in self.assemblies:
            images.append(self.image_name(frame_name, scale2x=scale2x))
            idx += 1
            frame_name = f"{name}-{idx}"

        return images
