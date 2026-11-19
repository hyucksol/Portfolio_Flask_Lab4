import re

from stack import Stack          

stack = Stack()

PRECEDENCE = {'+': 1, '-': 1, '*': 2, '/': 2, '%': 2, '^': 3}
RIGHT_ASSOCIATIVE = {'^'}
TOKEN = re.compile(r'\s*(\d+(?:\.\d+)?|[A-Za-z_]\w*|[-+*/%^()])')


def stack_to_list(a_stack):
    items = []
    current = a_stack.top
    while current:
        items.append(current.data)
        current = current.next
    return items


def tokenize(expression):
    tokens = []
    text = expression.strip()
    position = 0
    while position < len(text):
        match = TOKEN.match(text, position)
        if not match:
            bad = text[position:].lstrip()[0]
            raise ValueError(f"Invalid character '{bad}'.")
        tokens.append(match.group(1))
        position = match.end()
    return tokens


def infix_to_postfix(expression):
    tokens = tokenize(expression)
    if not tokens:
        raise ValueError("Type an expression first.")

    operators = Stack()
    output = []
    steps = []
    expect_operand = True

    def record(token):
        steps.append({
            'token': token,
            'stack': ' '.join(reversed(stack_to_list(operators))) or '(empty)',
            'output': ' '.join(output) or '-',
        })

    for token in tokens:
        if token == '(':
            if not expect_operand:
                raise ValueError("Missing operator before '('.")
            operators.push(token)

        elif token == ')':
            if expect_operand:
                raise ValueError("Missing operand before ')'.")
            while operators.peek() is not None and operators.peek() != '(':
                output.append(operators.pop())
            if operators.peek() != '(':
                raise ValueError("Mismatched parentheses.")
            operators.pop()

        elif token in PRECEDENCE:
            if expect_operand:
                raise ValueError(f"Missing operand before '{token}'.")
            while operators.peek() is not None and operators.peek() != '(':
                top = operators.peek()
                if PRECEDENCE[top] > PRECEDENCE[token] or (
                        PRECEDENCE[top] == PRECEDENCE[token] and token not in RIGHT_ASSOCIATIVE):
                    output.append(operators.pop())
                else:
                    break
            operators.push(token)
            expect_operand = True

        else:  # operand (number or letter)
            if not expect_operand:
                raise ValueError("Missing operator between operands.")
            output.append(token)
            expect_operand = False

        record(token)

    if expect_operand:
        raise ValueError("The expression ends with an operator.")

    while operators.peek() is not None:
        top = operators.pop()
        if top == '(':
            raise ValueError("Mismatched parentheses.")
        output.append(top)
        record(f"pop {top}")

    return ' '.join(output), steps


def handle(form):
    action = form.get('action')
    context = {}

    if action == 'infix':
        expression = form.get('expression', '')
        context['infix_input'] = expression
        try:
            postfix, steps = infix_to_postfix(expression)
            context['postfix_result'] = postfix
            context['postfix_steps'] = steps
        except ValueError as error:
            context['postfix_error'] = str(error)

    elif action == 'st_push':
        item = form.get('stack_item', '').strip()
        if item:
            stack.push(item)
            context['stack_message'] = f"Pushed '{item}' onto the stack."
        else:
            context['stack_message'] = "Type a value to push first."

    elif action == 'st_pop':
        if stack.top is None:
            context['stack_message'] = "Stack is empty. Nothing to pop."
        else:
            context['stack_message'] = f"Popped '{stack.pop()}' from the stack."

    elif action == 'st_peek':
        if stack.top is None:
            context['stack_message'] = "Stack is empty. Nothing to peek."
        else:
            context['stack_message'] = f"Top element: '{stack.peek()}'"

    return context


def state():
    return {'stack_items': stack_to_list(stack)}