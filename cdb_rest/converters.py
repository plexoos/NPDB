class HexStringConverter:
    regex = '[0-9a-fA-F]+'

    def to_python(self, value):
        return value

    def to_url(self, value):
        return value
