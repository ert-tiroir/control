
def render (mx, v):
    L = [ "|" ]

    for i, u in enumerate(v):
        L.append(" ")
        L.append(u)
        L.append(" " * (1 + mx[i] - len(u)))
        L.append("|")

    return "".join(L)
def render_sep (mx):
    L = [ "+" ]
    for i in mx:
        L.append("-" * (i + 2))
        L.append("+")
    return "".join(L)
def to_table (fields, values):
    fields = list(map(str, fields))
    values = list(map(lambda x: list(map(str, x)), values))
    mx = [len(u) for u in fields]

    for value in values:
        for idx, v in enumerate(value):
            mx[idx] = max(mx[idx], len(v))
    T = [ render_sep(mx) ]
    T.append(render(mx, fields))
    T.append(render_sep(mx))
    for v in values:
        T.append(render(mx, v))
    T.append(render_sep(mx))
    return "\n".join(T)
