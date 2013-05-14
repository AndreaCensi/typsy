from typsy import HasComponents

def get_all_embedded_examples():
    for cls in HasComponents.klasses.values():
        example = cls.get_parsing_examples()
        examples = example.split('\n')
        for s in examples:
            s = s.strip()
            if s:
                yield s
