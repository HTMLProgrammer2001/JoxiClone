from Classes.ObjectData.Image.Image import Image
from Classes.ObjectData.Image.ImageDrawContext import ImageDrawContext
from Intefaces.ICommand import ICommand


class CreateImage(ICommand):
    image: Image = None

    def __init__(self, app, path: str):
        self.app = app
        self.path = path

    def execute(self):
        self.image = Image(self.path, ImageDrawContext())
        self.app.objects.append(self.image)

    def unexecute(self):
        self.app.objects.remove(self.image)
