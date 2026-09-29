import re

from NumWord import NumberToWord, WordToNumber

_number_to_word = NumberToWord()
_word_to_number = WordToNumber()


def _word_variant(text: str) -> str:
    """Spell out each digit run in text, e.g. '8:30' -> 'eight:thirty'."""
    return re.sub(r"\d+", lambda m: _number_to_word.convert(int(m.group())), text)


def _word_runs(text: str) -> list[tuple[int, int]]:
    """Maximal spans of letter-tokens joined by single spaces, e.g. 'twenty three'."""
    tokens = list(re.finditer(r"[A-Za-z]+(?:-[A-Za-z]+)*", text))
    runs = []
    i = 0
    while i < len(tokens):
        start, end = tokens[i].start(), tokens[i].end()
        j = i + 1
        while j < len(tokens) and text[end:tokens[j].start()] == " ":
            end = tokens[j].end()
            j += 1
        runs.append((start, end))
        i = j
    return runs


def _as_digits(words: str) -> str | None:
    """Convert a number phrase to digits, or None if it isn't (all) numbers."""
    try:
        value = _word_to_number.convert(words)
    except ValueError:
        return None
    if isinstance(value, float) and value.is_integer():
        value = int(value)
    return str(value)


def _number_variant(text: str) -> str:
    """Turn number words back into digits, e.g. 'eight:thirty' -> '8:30'."""
    pieces = []
    last = 0
    for start, end in _word_runs(text):
        run_text = text[start:end]
        replaced = _as_digits(run_text)
        if replaced is None:
            # Not one clean number phrase — fall back word by word so
            # 'between six and eight' still becomes 'between 6 and 8'.
            out, changed = [], False
            for word in run_text.split(" "):
                digits = _as_digits(word)
                if digits is None:
                    out.append(word)
                else:
                    out.append(digits)
                    changed = True
            replaced = " ".join(out) if changed else None
        if replaced is not None:
            pieces.append(text[last:start])
            pieces.append(replaced)
            last = end
    pieces.append(text[last:])
    return "".join(pieces)


def judge(question: str, expects: str, answer: str, results) -> bool:
    if not expects:
        return False

    expects_norm = expects.strip().lower()
    answer_norm = (answer.strip() or "").lower()

    variants = {
        expects_norm,
        _word_variant(expects_norm),
        _number_variant(expects_norm),
    }
    return any(variant in answer_norm for variant in variants)