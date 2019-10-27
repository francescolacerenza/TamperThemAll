import uuid

__example_payload__ = "' AND 1=1 OR 2=2"
__type__ = "changing the payload spaces to obfuscated hashes with a newline"


def space2hash(payload, **kwargs):
    modifier = "%%23{}%%0A".format(uuid.uuid4().hex[1:5])
    retval = ""
    for char in payload:
        if char == " ":
            retval += modifier
        else:
            retval += char
    return retval
