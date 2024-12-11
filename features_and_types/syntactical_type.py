from .lexical_item import FeatureBundle


class SyntacticalType:

    # fb means feature bundle

    _fb_seperator = ', '

    def __init__(self, head: FeatureBundle, fb_list: list):

        if type(fb_list) != list:
            raise Exception("feature_list must be a list")

        self.head = head
        # removes empty feature bundles and sorts feature bundles
        self.fb_list = sorted([fb for fb in fb_list if fb.has_features()])

    def __hash__(self):
        hash_value = hash(self.head)
        for fb in self.fb_list:
            hash_value = hash_value ^ hash(fb)
        return hash_value

    def __eq__(self, other):
        return self.head == other.head and self.fb_list == other.fb_list

    def __str__(self):
        fb_list = [str(self.head)] if self.head.has_features() else []
        fb_list.extend([str(fb) for fb in self.fb_list if fb.has_features()])

        fb_list_str = self._fb_seperator.join(fb_list)
        return '<' + fb_list_str + '>'

    # operations

    def calc_merge(self, other):

        new_syntactical_types = set()

        # check if merge is possible
        if self.head.can_merge_other(other.head):
            new_head = self.head.get_copy_without_first_feature()
            new_fb_list = self.fb_list + [other.head.get_copy_without_first_feature()] + other.fb_list

            # check if new_fb_list is valid (contains only negative move features)
            if all([m.has_only_negative_move_features() for m in new_fb_list]):
                new_syntactical_types.add(SyntacticalType(new_head, new_fb_list))

        return new_syntactical_types


    def calc_move(self):

        new_syntactical_types = set()

        # test for every feature bundle in feature bundle list
        # (feature bundle list should contain only feature bundles consisting only of negative move features)
        for i, fb in enumerate(self.fb_list):

            # check if move is possible
            if self.head.can_move_other(fb):
                new_head = self.head.get_copy_without_first_feature()
                new_fb_list = [fb if j != i else fb.get_copy_without_first_feature() for j, fb in enumerate(self.fb_list)]
                new_syntactical_types.add(SyntacticalType(new_head, new_fb_list))

        return new_syntactical_types
