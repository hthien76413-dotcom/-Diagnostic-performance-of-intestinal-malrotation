"""American spelling for the JACR submission (AMA Manual of Style).

The manuscript was drafted in British spelling for a European journal. JACR
follows AMA style, so every English text that reaches a submission document
passes through us(): the Markdown sources were converted once with it, and the
builders apply it to table text read from the analysis JSON, which the analysis
scripts still write in the original spelling. Reference titles are quoted as
published and are never converted.
"""
import re

_MAP = {
    'paediatric': 'pediatric', 'caecal': 'cecal', 'caecum': 'cecum',
    'colour': 'color', 'centre': 'center', 'centres': 'centers',
    'multicentre': 'multicenter', 'favourable': 'favorable',
    'generalise': 'generalize', 'generalised': 'generalized',
    'generalises': 'generalizes', 'summarise': 'summarize',
    'summarised': 'summarized', 'characterise': 'characterize',
    'characterised': 'characterized', 'harmonised': 'harmonized',
    'penalised': 'penalized', 'protocolised': 'protocolized',
    'pseudonymised': 'pseudonymized', 'anonymised': 'anonymized',
    'randomised': 'randomized', 'standardised': 'standardized',
    'recognised': 'recognized', 'categorised': 'categorized',
    'labelled': 'labeled', 'labelling': 'labeling', 'cancelled': 'canceled',
    'haemangioma': 'hemangioma', 'towards': 'toward',
    'analysed': 'analyzed', 'analyse': 'analyze',
    'acknowledgement': 'acknowledgment', 'acknowledgements': 'acknowledgments',
}
_RX = re.compile(r'\b(' + '|'.join(sorted(_MAP, key=len, reverse=True)) + r')\b',
                 re.IGNORECASE)


def _sub(m):
    w = m.group(0)
    out = _MAP[w.lower()]
    if w.isupper():
        return out.upper()
    if w[0].isupper():
        return out[0].upper() + out[1:]
    return out


def us(text):
    """Return text in American spelling; non-str values pass through."""
    if not isinstance(text, str):
        return text
    return _RX.sub(_sub, text)


_P = re.compile(r'(?<![\w*])[pP]\s*([=<>≤≥])\s*(\d*\.\d+)')


def ama_p(text):
    """P values in AMA style: italic capital P (marked *P* for the writers), no
    leading zero, spaces around the operator; P = 1.000 becomes P > .99."""
    if not isinstance(text, str):
        return text
    def f(m):
        op, v = m.group(1), m.group(2)
        if float(v) >= 0.995 and op == '=':
            return '*P* > .99'
        return f'*P* {op} {v.lstrip("0")}'
    return _P.sub(f, text)


def us_table(data):
    """Apply us() and AMA P-value style to every cell of a list-of-rows table."""
    return [[ama_p(us(c)) for c in row] for row in data]


def british_left(text):
    """Words from the map still present, for the pre-submission scan."""
    return sorted({m.group(0) for m in _RX.finditer(text)})
