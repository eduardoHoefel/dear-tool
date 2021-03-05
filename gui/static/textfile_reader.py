
class TextfileReader():

    def read(path):
        with open(path) as f:
            content = f.read().splitlines()

        return content
