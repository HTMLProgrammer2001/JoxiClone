from Intefaces.ICommand import ICommand


class DeleteCommand(ICommand):
    deletedObject = None
    index: int = 0

    def __init__(self, app, obj):
        super().__init__(app)

        self.deletedObject = obj

    def execute(self):
        self.index = self.app.objects.index(self.deletedObject)
        self.app.objects.remove(self.deletedObject)

    def unexecute(self):
        self.app.objects.insert(self.index, self.deletedObject)
