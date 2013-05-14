from typsy import HasComponents
from typsy.parseables import Parseable

def get_all_embedded_examples():
    for cls in HasComponents.klasses.values():
        if not issubclass(cls, Parseable):
            continue
        example = cls.get_parsing_examples()
        examples = example.split('\n')
        for s in examples:
            s = s.strip()
            if s:
                yield s
