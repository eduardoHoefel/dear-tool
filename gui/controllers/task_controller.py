from storage import Storage

class TaskController():

    def set(task):
        Storage().set('task', task)

    def remove():
        TaskController.set(None)

