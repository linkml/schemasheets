from bioregistry import get_iri

priority = ["obofoundry", "default", "miriam", "ols", "n2t", "bioportal"]

def guess_prefix_expansion(pfx) -> str:
    return get_iri(pfx, "", priority=priority)