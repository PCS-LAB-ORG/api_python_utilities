"""
prismacloud-api has many APIs supported but, the payloads are unstructured and thus must be known.

This util defines a transform function to take a class and create the payload dictionary for these.

The class definitions can be used to create the payloads for these requests offering type checking,
required, and default values for attributes.

"""

from dataclasses import asdict


def transform(obj):
    return asdict(obj)


class role:
    def __init__(self):
        pass
