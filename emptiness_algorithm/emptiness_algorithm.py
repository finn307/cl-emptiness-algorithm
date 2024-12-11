from .emptiness_algorithm_v1 import check_emptiness as check_emptiness_v1
from .emptiness_algorithm_v2 import check_emptiness as check_emptiness_v2


def check_emptiness(li_list: list, version: str = 'v2', console_output: bool = True):

    if version == 'v1':
        check_emptiness_v1(li_list, console_output)
    elif version == 'v2':
        check_emptiness_v2(li_list, console_output)
    else:
        raise ValueError(f'check_emptiness parameter version accepts only "v1" or "v2"')
