import itertools
from features_and_types import FeatureBundle
from features_and_types import SyntacticalType


_MAX_ITERATIONS = 100


def set_to_str(set_):
    return { str(item) for item in set_ }


def _create_st_set_from_li_list(li_list: list):
    st_set = set()
    for li in li_list:
        st_set.add(SyntacticalType(li, []))
    return st_set


def _calculate_one_step_derivable_st(prev_st_set: set):
    st_combinations = set(itertools.product(prev_st_set, prev_st_set))

    new_st_set = set()
    for st1, st2 in st_combinations:
        # try merging
        new_st_set.update(st1.calc_merge(st2))
        # try moving
        new_st_set.update(st1.calc_move())
    return new_st_set


def _contains_final_st(c: set):
    final_st_set = { SyntacticalType(FeatureBundle.parse('s'), []) }
    return final_st_set.issubset(c)


def check_emptiness(li_list: list, console_output: bool):

    # add all lexical items to M (step 1)

    m_0 = _create_st_set_from_li_list(li_list)

    if console_output:
        print("----------")
        print("iteration 0 (add syntactical types of lexical items)")
        print(f"{set_to_str(m_0)}")
        print("----------")

    # do one step and union until M does not change (step 2)

    m_list = [m_0]

    for i in range(1, _MAX_ITERATIONS):
        prev_st_set = m_list[-1]
        new_st = _calculate_one_step_derivable_st(prev_st_set)
        next_st_set = prev_st_set.union(new_st)

        # break if M did not change (step 3)
        if len(next_st_set.difference(prev_st_set)) == 0:

            if console_output:
                print()
                print(f"m_{i} = m_{i-1}")

            return not _contains_final_st(next_st_set)

        m_list.append(next_st_set)

        if console_output:
            print()
            print("----------")
            print(f"iteration {i} (calculate every single step possible)")
            print(f"m_{i}: {set_to_str(next_st_set)}")
            print(f"new: {set_to_str(next_st_set.difference(prev_st_set))}")
            print("----------")
