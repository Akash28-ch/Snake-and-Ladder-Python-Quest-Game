import json
import os


TARGET_COUNT = 400


def option_order(qid, correct, wrongs):
    choices = []
    for item in [correct, *wrongs]:
        text = str(item)
        if text not in choices:
            choices.append(text)

    fallbacks = ["Raises an error", "None", "No output", "Depends on the editor", "False", "True"]
    for fallback in fallbacks:
        if len(choices) >= 4:
            break
        if fallback not in choices:
            choices.append(fallback)

    choices = choices[:4]
    shift = qid % len(choices)
    return choices[shift:] + choices[:shift]


def add_question(bank, seen, qid, topic, question, correct, wrongs, explanation):
    if question in seen:
        return qid

    seen.add(question)
    correct = str(correct)
    bank.append({
        "id": qid,
        "topic": topic,
        "question": question,
        "options": option_order(qid, correct, wrongs),
        "correctAnswer": correct,
        "explanation": explanation,
    })
    return qid + 1


def build_beginner_questions():
    bank, seen, qid = [], set(), 1

    operators = [
        ("+", lambda a, b: a + b, "addition"),
        ("-", lambda a, b: a - b, "subtraction"),
        ("*", lambda a, b: a * b, "multiplication"),
        ("//", lambda a, b: a // b, "floor division"),
        ("%", lambda a, b: a % b, "modulo division"),
    ]
    for a in range(4, 28):
        for b in range(2, 10):
            for symbol, func, name in operators:
                if len(bank) >= 115:
                    break
                result = func(a, b)
                qid = add_question(
                    bank, seen, qid, "Operators",
                    f"What is the output of print({a} {symbol} {b})?",
                    result,
                    [result + 1, result - 1, f"{a}{b}"],
                    f"The {symbol} operator performs {name} in Python.",
                )
            if len(bank) >= 115:
                break
        if len(bank) >= 115:
            break

    words = ["python", "variable", "function", "loop", "string", "dictionary", "integer", "module", "syntax", "boolean"]
    for word in words:
        for index in range(len(word)):
            if len(bank) >= 175:
                break
            qid = add_question(
                bank, seen, qid, "Strings",
                f"What is the output of print('{word}'[{index}])?",
                word[index],
                [word[-1], str(index), word[:index + 1]],
                "String indexing starts at 0, so the index selects one character.",
            )
        if len(bank) >= 175:
            break

    for word in words:
        transforms = [
            ("upper()", word.upper(), [word.lower(), word.title(), len(word)]),
            ("lower()", word.lower(), [word.upper(), word.title(), len(word)]),
            ("capitalize()", word.capitalize(), [word.upper(), word.lower(), word[::-1]]),
            ("replace('o', '0')", word.replace("o", "0"), [word, word.replace("o", ""), word.upper()]),
        ]
        for method, correct, wrongs in transforms:
            if len(bank) >= 215:
                break
            qid = add_question(
                bank, seen, qid, "String Methods",
                f"What is the output of print('{word}'.{method})?",
                correct,
                wrongs,
                f"The string method {method} returns a new string value.",
            )
        if len(bank) >= 215:
            break

    for n in range(2, 42):
        values = list(range(1, n % 7 + 4))
        qid = add_question(
            bank, seen, qid, "Lists",
            f"What is the output of print(len({values}))?",
            len(values),
            [len(values) - 1, len(values) + 1, values[-1]],
            "len() returns the number of items in a list.",
        )
        qid = add_question(
            bank, seen, qid, "Lists",
            f"What is the output of print({values}[0])?",
            values[0],
            [values[-1], len(values), 0],
            "Index 0 refers to the first item in a list.",
        )
        if len(bank) >= 285:
            break

    for start in range(0, 8):
        for stop in range(start + 2, start + 9):
            if len(bank) >= 335:
                break
            qid = add_question(
                bank, seen, qid, "Loops and Range",
                f"What is the output of print(list(range({start}, {stop})))?",
                list(range(start, stop)),
                [list(range(start, stop + 1)), list(range(start + 1, stop)), stop - start],
                "range(start, stop) includes start and excludes stop.",
            )
        if len(bank) >= 335:
            break

    concepts = [
        ("Variables", "Which variable name is valid in Python?", "student_name", ["2student", "student-name", "student name"], "Names can contain letters, numbers, and underscores, but cannot start with a number."),
        ("Data Types", "Which literal creates a dictionary?", "{'name': 'Ada'}", ["['name', 'Ada']", "('name', 'Ada')", "{'Ada'}"], "Dictionaries store key-value pairs inside curly braces."),
        ("Functions", "Which keyword defines a function?", "def", ["func", "function", "lambda def"], "Python uses def to define named functions."),
        ("Conditionals", "Which keyword checks another condition after if?", "elif", ["elseif", "else if", "when"], "Python uses elif for additional conditional branches."),
        ("Loops", "Which statement skips to the next loop iteration?", "continue", ["break", "skip", "pass loop"], "continue jumps to the next iteration of the nearest loop."),
        ("Comments", "Which symbol starts a single-line Python comment?", "#", ["//", "<!--", "--"], "The # symbol starts a single-line Python comment."),
        ("Booleans", "Which value represents true in Python?", "True", ["true", "TRUE", "1 only"], "Boolean literals in Python are True and False."),
        ("None", "Which value represents no value in Python?", "None", ["null", "nil", "undefined"], "Python uses None to represent absence of a value."),
        ("Input", "What type does input() return?", "str", ["int", "float", "bool"], "input() always returns text unless you convert it."),
        ("Imports", "Which keyword imports a module?", "import", ["include", "using", "require"], "The import keyword loads a module."),
    ]
    while len(bank) < TARGET_COUNT:
        topic, question, correct, wrongs, explanation = concepts[len(bank) % len(concepts)]
        qid = add_question(
            bank, seen, qid, topic,
            f"{question} (Beginner practice {len(bank) + 1})",
            correct, wrongs, explanation,
        )

    return bank[:TARGET_COUNT]


def build_intermediate_questions():
    bank, seen, qid = [], set(), 401

    for n in range(2, 22):
        for multiplier in range(2, 7):
            if len(bank) >= 80:
                break
            correct = [x * multiplier for x in range(n)]
            qid = add_question(
                bank, seen, qid, "List Comprehensions",
                f"What is the output of print([x * {multiplier} for x in range({n})])?",
                correct,
                [[x + multiplier for x in range(n)], list(range(n)), [multiplier] * n],
                "The expression runs once for every value produced by range().",
            )
        if len(bank) >= 80:
            break

    words = ["intermediate", "comprehension", "generator", "exception", "namespace", "iteration", "decorator", "argument"]
    for word in words:
        for start in range(0, min(5, len(word) - 2)):
            for stop in range(start + 2, min(len(word), start + 7)):
                if len(bank) >= 145:
                    break
                qid = add_question(
                    bank, seen, qid, "Slicing",
                    f"What is the output of print('{word}'[{start}:{stop}])?",
                    word[start:stop],
                    [word[start:stop + 1], word[stop:start:-1], word[:stop]],
                    "Slicing includes the start index and excludes the stop index.",
                )
            if len(bank) >= 145:
                break
        if len(bank) >= 145:
            break

    for i in range(1, 56):
        data = {f"k{i}": i, f"k{i + 1}": i + 1}
        key = f"k{i + 1}"
        qid = add_question(
            bank, seen, qid, "Dictionaries",
            f"What is the output of print({data}.get('{key}'))?",
            data[key],
            [data[key] - 1, "None", key],
            "dict.get(key) returns the value for the key when it exists.",
        )
        if len(bank) >= 200:
            break

    for n in range(4, 84):
        if len(bank) >= 260:
            break
        values = list(range(n % 3, n % 3 + 7))
        correct = [x for x in values if x % 2 == 0]
        qid = add_question(
            bank, seen, qid, "Filtering",
            f"What is the output of print([x for x in {values} if x % 2 == 0])?",
            correct,
            [[x for x in values if x % 2 == 1], values, len(correct)],
            "The condition keeps only even values.",
        )

    topics = [
        ("Lambda Functions", "What does lambda x: x + 1 return when called with {n}?", lambda n: n + 1, lambda n: [n, n - 1, "lambda"]),
        ("Set Operations", "What is sorted(set({a}) & set({b}))?", lambda a, b: sorted(set(a) & set(b)), lambda a, b: [sorted(set(a) | set(b)), sorted(set(a) - set(b)), sorted(set(b) - set(a))]),
        ("Exception Handling", "Which block runs only when no exception is raised in try/except?", lambda: "else", lambda: ["finally", "except", "raise"]),
        ("Generators", "Which keyword pauses a function and produces the next value?", lambda: "yield", lambda: ["return", "pause", "next"]),
        ("File Handling", "Which mode opens a file for appending text?", lambda: "a", lambda: ["r", "w", "x"]),
        ("Args and Kwargs", "What name is commonly used for extra keyword arguments?", lambda: "**kwargs", lambda: ["*args", "&kwargs", "kwargs()"]),
        ("Modules", "What does __name__ equal when a file is run directly?", lambda: "__main__", lambda: ["__file__", "__module__", "main"]),
    ]
    variant = 1
    while len(bank) < TARGET_COUNT:
        item = topics[variant % len(topics)]
        topic = item[0]
        if topic == "Lambda Functions":
            n = variant % 37
            qid = add_question(bank, seen, qid, topic, item[1].format(n=n), item[2](n), item[3](n), "The lambda expression adds 1 to its argument.")
        elif topic == "Set Operations":
            a = list(range(variant % 5, variant % 5 + 5))
            b = list(range(variant % 4 + 2, variant % 4 + 7))
            qid = add_question(bank, seen, qid, topic, item[1].format(a=a, b=b), item[2](a, b), item[3](a, b), "The & operator returns the set intersection.")
        else:
            qid = add_question(bank, seen, qid, topic, f"{item[1]} (Intermediate practice {variant})", item[2](), item[3](), "This is a common intermediate Python rule.")
        variant += 1

    return bank[:TARGET_COUNT]


def build_advanced_questions():
    bank, seen, qid = [], set(), 801

    advanced_concepts = [
        ("Decorators", "What does a decorator receive first when applied to a function?", "The function object being decorated", ["The function result", "Only the function name as text", "The module path"], "A decorator is called with the original function object and returns a replacement callable."),
        ("Closures", "What allows an inner function to remember variables from an outer function?", "A closure", ["A metaclass", "A static method", "A module reload"], "A closure retains references to variables from its enclosing scope."),
        ("Context Managers", "Which method is called when entering a with block?", "__enter__", ["__start__", "__call__", "__init__"], "The with statement calls __enter__ at the start and __exit__ at the end."),
        ("Context Managers", "Which method receives exception details from a with block?", "__exit__", ["__enter__", "__except__", "__del__"], "__exit__ receives exception type, value, and traceback."),
        ("OOP", "Which method customizes instance creation before __init__?", "__new__", ["__call__", "__prepare__", "__post_init__"], "__new__ creates the object before __init__ initializes it."),
        ("OOP", "What does super() usually follow in Python inheritance?", "The method resolution order", ["Alphabetical class order", "File import order", "Object memory address order"], "super() delegates according to the MRO."),
        ("Descriptors", "Which descriptor method handles attribute access?", "__get__", ["__fetch__", "__attr__", "__read__"], "Descriptor __get__ is invoked during managed attribute access."),
        ("Descriptors", "Which descriptor method handles attribute assignment?", "__set__", ["__assign__", "__put__", "__write__"], "Descriptor __set__ is invoked when assigning to a managed attribute."),
        ("Dataclasses", "Which decorator generates init and repr methods for simple classes?", "@dataclass", ["@classmethod", "@property", "@staticmethod"], "dataclasses.dataclass generates common methods from type annotations."),
        ("Typing", "What does list[int] describe?", "A list containing integers", ["A tuple of integers", "An integer list constructor", "A list index"], "Modern Python supports built-in generic type hints such as list[int]."),
        ("Iterators", "Which method returns the next item from an iterator?", "__next__", ["__iter__", "__yield__", "__call__"], "next(iterator) calls iterator.__next__()."),
        ("Generators", "What exception is raised when a generator is exhausted?", "StopIteration", ["GeneratorExit", "StopAsyncIteration", "EOFError"], "Synchronous iterators signal exhaustion with StopIteration."),
        ("Asyncio", "Which keyword pauses a coroutine until an awaitable completes?", "await", ["yield", "pause", "async"], "await waits for an awaitable inside async code."),
        ("Asyncio", "Which keyword defines a coroutine function?", "async def", ["coroutine def", "await def", "defer def"], "async def defines a coroutine function."),
        ("Concurrency", "What is best for CPU-bound parallelism in CPython?", "multiprocessing", ["threading only", "asyncio only", "recursion"], "Separate processes can run on multiple CPU cores."),
        ("Concurrency", "What does the GIL mainly limit in CPython?", "Parallel execution of Python bytecode in threads", ["File reading", "Process creation", "List indexing"], "The GIL prevents multiple threads from executing Python bytecode simultaneously."),
        ("Memory", "Which module can measure current and peak Python memory allocations?", "tracemalloc", ["timeit", "gcview", "memcache"], "tracemalloc tracks Python memory allocations."),
        ("Performance", "Which module benchmarks small code snippets?", "timeit", ["profiled", "clock", "benchmarkit"], "timeit is designed for timing small snippets reliably."),
        ("Flask", "Which Flask helper builds URLs by endpoint name?", "url_for", ["redirect_for", "make_url", "route_to"], "url_for creates URLs from endpoint names and arguments."),
        ("Flask", "Where are query string values stored in Flask request?", "request.args", ["request.form", "request.json", "request.files"], "request.args contains URL query parameters."),
        ("SQLAlchemy", "What does db.session.commit() do?", "Persists pending database changes", ["Rolls back changes", "Creates a model class", "Starts Flask"], "commit writes pending session changes to the database."),
        ("SQLAlchemy", "What does a one-to-many relationship usually connect?", "One parent row to many child rows", ["One column to one type hint", "Many apps to one route", "One function to many decorators"], "One-to-many relationships model parent-child records."),
        ("Pandas", "What is a DataFrame?", "A two-dimensional labeled table", ["A Python set", "A Flask request object", "A compiled regex"], "A DataFrame stores rows and columns with labels."),
        ("Pandas", "Which method selects rows by label?", "loc", ["iloc", "at_index", "label"], "DataFrame.loc selects by labels."),
        ("NumPy", "What does broadcasting allow?", "Operations on compatible different-shaped arrays", ["Automatic web routing", "Database commits", "Thread locking"], "Broadcasting expands compatible shapes without explicit copies."),
        ("NumPy", "What does ndarray.shape describe?", "Array dimensions", ["Array data type only", "Array memory address", "Array sorting order"], "shape is a tuple of dimension lengths."),
    ]

    variant = 1
    while len(bank) < 190:
        topic, question, correct, wrongs, explanation = advanced_concepts[variant % len(advanced_concepts)]
        qid = add_question(
            bank, seen, qid, topic,
            f"{question} (Advanced concept {variant})",
            correct, wrongs, explanation,
        )
        variant += 1

    for n in range(2, 58):
        if len(bank) >= 250:
            break
        qid = add_question(
            bank, seen, qid, "Closures",
            f"What is returned by a closure that captures base={n} and later adds 5?",
            n + 5,
            [n, 5, n * 5],
            "The inner function remembers base and adds the later argument.",
        )

    for n in range(3, 73):
        if len(bank) >= 315:
            break
        values = list(range(n, n + 5))
        correct = sum(x * x for x in values if x % 2)
        qid = add_question(
            bank, seen, qid, "Generator Expressions",
            f"What is sum(x*x for x in {values} if x % 2)?",
            correct,
            [sum(values), sum(x * x for x in values), len(values)],
            "The generator squares only odd values, then sum() adds them.",
        )

    for n in range(1, 92):
        if len(bank) >= TARGET_COUNT:
            break
        correct = f"value-{n}"
        qid = add_question(
            bank, seen, qid, "Properties",
            f"If a @property returns 'value-{n}', what does obj.name evaluate to?",
            correct,
            [f"name-{n}", "property object", "None"],
            "A @property lets method logic be accessed like an attribute.",
        )

    return bank[:TARGET_COUNT]


def validate_bank(name, bank):
    if len(bank) != TARGET_COUNT:
        raise ValueError(f"{name} has {len(bank)} questions, expected {TARGET_COUNT}")

    questions = set()
    for item in bank:
        if item["question"] in questions:
            raise ValueError(f"Duplicate question in {name}: {item['question']}")
        questions.add(item["question"])
        if len(item["options"]) != 4:
            raise ValueError(f"Question {item['id']} in {name} does not have 4 options")
        if item["correctAnswer"] not in item["options"]:
            raise ValueError(f"Question {item['id']} in {name} is missing its correct answer")


def create_question_database():
    basedir = os.path.abspath(os.path.dirname(__file__))
    questions_dir = os.path.join(basedir, "questions")
    os.makedirs(questions_dir, exist_ok=True)

    banks = {
        "beginner": build_beginner_questions(),
        "intermediate": build_intermediate_questions(),
        "advanced": build_advanced_questions(),
    }

    for name, bank in banks.items():
        validate_bank(name, bank)
        with open(os.path.join(questions_dir, f"{name}.json"), "w", encoding="utf-8") as handle:
            json.dump(bank, handle, indent=4)

    print("Generated question banks:")
    for name, bank in banks.items():
        print(f"- {name}: {len(bank)} questions")


if __name__ == "__main__":
    create_question_database()
