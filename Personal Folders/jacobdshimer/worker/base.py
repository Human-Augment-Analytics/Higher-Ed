class Worker():
    def work(self, source: str):
        raise NotImplementedError()

    def process_message(self, url: str):
        raise NotImplementedError()
