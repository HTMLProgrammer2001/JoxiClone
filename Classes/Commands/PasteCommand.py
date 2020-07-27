from Intefaces.ICommand import ICommand


class PasteCommand(ICommand):
    insertedObject = None

    def __init__(self, app, obj):
        super().__init__(app)

        self.insertedObject = obj

    def execute(self):
        self.app.objects.append(self.insertedObject)

    def unexecute(self):
        self.app.objects.remove(self.insertedObject)
