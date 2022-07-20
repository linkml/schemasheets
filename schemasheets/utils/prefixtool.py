from typing import Optional

from bioregistry import get_iri

priority = ["obofoundry", "default", "miriam", "ols", "n2t", "bioportal"]


def guess_prefix_expansion(prefix: str) -> Optional[str]:
    """
    Guesses a prefix expansion using bioregistry

    :param prefix:
    :return:
    """
    try:
        return get_iri(prefix, "", priority=priority)
    except KeyError:
        return None