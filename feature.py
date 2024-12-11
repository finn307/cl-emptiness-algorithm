class Feature:

    _prefix_list = ['=', '+', '-', '']
    _stripped_prefix_list = ['=', '+', '-']

    def __init__(self, prefix: str, name: str):

        # check if prefix is valid
        if prefix not in self._prefix_list:
            raise Exception(f"{prefix} is not a valid prefix")

        # check if no prefix symbols are in feature name
        if not all([p not in name for p in Feature._stripped_prefix_list]):
            raise Exception(f"feature name must not contain any item of {Feature._stripped_prefix_list}")

        self.prefix = prefix
        self.name = name

    def __hash__(self):
        return hash(self.prefix) ^ hash(self.name)

    def __eq__(self, other):
        return self.prefix == other.prefix and self.name == other.name

    def __str__(self):
        return self.prefix + self.name

    # parsing methods

    @classmethod
    def parse(cls, s):

        if s[0] in cls._prefix_list:
            prefix = s[0]
            name = s[1:]
        else:
            prefix = ''
            name = s

        # check if no prefix symbols are in feature name
        if not all([p not in name for p in cls._stripped_prefix_list]):
            raise Exception(f"feature name must not contain any item of {cls._stripped_prefix_list}")

        return cls(prefix, name)
