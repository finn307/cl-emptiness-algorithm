from lexical_item import FeatureBundle
from syntactical_type import SyntacticalType


_MAX_ITERATIONS = 100


def set_to_str(set_):
    return { str(item) for item in set_ }


def _create_st_set_from_li_list(li_list: list):
    st_set = set()
    for li in li_list:
        st_set.add(SyntacticalType(li, []))
    return st_set


def _calculate_one_step_derivable_st(s: SyntacticalType, c: set):
    new_st = set()
    for s_ in c:
        # try merge in both directions
        new_st.update(s.calc_merge(s_))
        new_st.update(s_.calc_merge(s))
        # try move
        new_st.update(s.calc_move())
    return new_st


def _contains_final_st(c: set):
    final_st_set = { SyntacticalType(FeatureBundle.parse('s'), []) }
    return final_st_set.issubset(c)


def check_emptiness(li_list: list, console_output: bool):

    # list of iteration data
    # each iteration data is a tuple (C, N) where C and N are sets
    set_list = [
        (set(), _create_st_set_from_li_list(li_list))
    ]

    if console_output:
        print()
        print("----------")
        print("Initialization")
        print(f"C: {set_to_str(set_list[0][0])}")
        print(f"N: {set_to_str(set_list[0][1])}")
        print("----------")

    for i in range(1, _MAX_ITERATIONS):

        c, n = set_list[-1][0].copy(), set_list[-1][1].copy()

        # if n is empty, end
        if len(n) == 0:
            is_empty = not _contains_final_st(c)

            if console_output:
                print()
                print("----------")
                print(f"Iteration: {i}")
                print("N is empty")
                print("----------")

                print()
                print(f"<s> **{'is not' if is_empty else 'is'}** in N")
                print(f"given grammar **{'is' if is_empty else 'is not'}** empty")

            return not _contains_final_st(c)

        # remove syntactical type s from n
        s = n.pop()

        # calculate one step derivable syntactical types and add those to n that are not already in  c
        n.update(_calculate_one_step_derivable_st(s, c).difference(c))

        # add s to c
        c.add(s)

        print()
        print("----------")
        print(f"Iteration {i} (s: {str(s)})")
        print(f"C: {set_to_str(c)}")
        print(f"N: {set_to_str(n)}")
        print("----------")

        set_list.append((c, n))
