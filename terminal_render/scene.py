from camera import Camera
from objects import Light, Object
import logging


class Scene(object):
    def __init__(self, objects = []):
        self.objects = objects
        self.lights = None
        self.solids = None
        self.light_force = None
        self.filter_objects()

        self.cameras = None
        self.camera = None
        self.camera_index = -1

    def add_object(self, new_object):
        self.objects.append(new_object)
        self.filter_objects()

    def add_objects(self, *new_objects):
        self.objects += new_objects
        self.filter_objects()

    def filter_objects(self):
        self.lights = []
        self.solids = []
        self.light_force = None
        for obj in self.objects:
            if isinstance(obj, Light):
                self.lights.append(obj)
            elif isinstance(obj, Object):
                self.solids.append(obj)

    def get_light_force(self):
        if self.light_force is None:
            self.light_force = sum([x.force for x in self.lights])
        return self.light_force

    def get_camera(self, index = -1):
        if self.cameras is None:
            self.cameras = []
            for obj in self.objects:
                if isinstance(obj, Camera):
                    self.cameras.append(obj)

            if len(self.cameras) == 0:
                raise RuntimeError("There is no camera in the scene.")

        if self.camera is None or index != self.camera_index:
            self.camera_index = index

            if index >= len(self.cameras):
                raise IndexError("Bad index for camera")

            if index < 0:
                if len(self.cameras) > 1:
                    logging.warning("Use non-negative camera index for scenes with multiple cameras. Using first by default.")
                index = 0

            self.camera = self.cameras[index]

        return self.camera


    def intersect(self, ray):
        results = filter(None, [x.intersect(ray) for x in self.solids])
        best = ray.get_closest_index([x[0] for x in results])
        return results[best] if best is not None else None
