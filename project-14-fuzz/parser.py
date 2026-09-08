"""Mini CSV row parser/serializer (v2: quote-aware state machine)."""


def parse_line(line):
    fields = []
    current = []
    in_quotes = False
    i = 0
    while i < len(line):
        char = line[i]
        if in_quotes:
            if char == '"':
                if i + 1 < len(line) and line[i + 1] == '"':
                    current.append('"')
                    i += 1
                else:
                    in_quotes = False
            else:
                current.append(char)
        elif char == '"':
            in_quotes = True
        elif char == ",":
            fields.append("".join(current))
            current = []
        else:
            current.append(char)
        i += 1
    fields.append("".join(current))
    return fields


def join_row(fields):
    out = []
    for field in fields:
        if "," in field or '"' in field:
            field = '"' + field.replace('"', '""') + '"'
        out.append(field)
    return ",".join(out)
