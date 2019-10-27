__example_payload__ = "' AND 1=1 '"
__type__ = "changing the spaces in the payload into a plus sign"


def space2plus(payload, **kwargs):
    modifier = "+"
    return str(payload).replace(" ", modifier)
