from feature import Feature


class FeatureBundle:

    _feature_seperator = '.'

    def __init__(self, feature_list: list):
        self.feature_list = feature_list

    def __lt__(self, other):
        return str(self) < str(other)

    def __hash__(self):
        hash_value = 0
        for feature in self.feature_list:
            hash_value = hash_value ^ hash(feature)
        return hash_value

    def __eq__(self, other):
        return self.feature_list == other.feature_list

    def __str__(self):
        return f"{self._feature_seperator.join([str(f) for f in self.feature_list])}"

    def has_features(self):
        return len(self.feature_list) > 0

    def has_only_negative_move_features(self):
        return all([f.prefix == '-' for f in self.feature_list])

    def can_merge_other(self, other):
        if len(self.feature_list) == 0 or len(other.feature_list) == 0:
            return False
        else:
            return (
                self.feature_list[0].prefix == '='
                and other.feature_list[0].prefix == ''
                and self.feature_list[0].name == other.feature_list[0].name
            )

    def can_move_other(self, other):
        if len(self.feature_list) == 0 or len(other.feature_list) == 0:
            return False
        else:
            return (
                self.feature_list[0].prefix == '+'
                and other.feature_list[0].prefix == '-'
                and self.feature_list[0].name == other.feature_list[0].name
            )

    # operation methods

    def get_copy_without_first_feature(self):
        if len(self.feature_list) > 0:
            return FeatureBundle(self.feature_list[1:])
        else:
            return []

    # parsing methods

    @classmethod
    def _parse_feature_str(cls, s):
        feature_str_list = s.split(cls._feature_seperator)
        feature_list = [Feature.parse(feature_str) for feature_str in feature_str_list]
        return feature_list

    @classmethod
    def parse(cls, s):
        feature_list = cls._parse_feature_str(s)
        return cls(feature_list)


# todo may be deleted
class LexicalItem(FeatureBundle):

    def __init__(self, pronunciation: str, feature_list: list):
        super().__init__(feature_list)
        self.pronunciation = pronunciation

    def __str__(self):
        return f"{self.pronunciation}: {'.'.join([str(f) for f in self.feature_list])}"

    # parsing methods

    @classmethod
    def parse(cls, name, s):
        feature_list = cls._parse_feature_str(s)
        return cls(name, feature_list)
