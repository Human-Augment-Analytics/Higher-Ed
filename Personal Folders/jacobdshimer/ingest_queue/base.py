class BaseQueue():
    def enqueue(self, source, search):
        raise NotImplementedError()

    def dequeue(self, source: str, **kwargs):
        raise NotImplementedError()
