import yaml

"""
    Goals:
        -   To be better than SQL for deeply nested data
        -   To offer logic on temporary abstractions without large latency overhead

    Basic Rules Engine API designed to be part of an event driven solution architecture.
    This API will configurable to both:
        -   http
        -   pubsub

    This is designed for NoSQL data but will be configurable to multiple backends

    Input:
        raw_data: dict


"""


def rules_engine(raw_data: dict) -> dict:

    return {}
