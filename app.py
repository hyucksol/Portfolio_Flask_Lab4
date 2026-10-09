import math
from flask import Flask, render_template, request

app = Flask(__name__)

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def delete(self, data):
        curr = self.head

        if curr and curr.data == data:
            self.head = curr.next
            return True

        prev = None
        while curr and curr.data != data:
            prev = curr
            curr = curr.next

        if curr:
            prev.next = curr.next
            return True

        return False

    def get_all(self):
        items = []
        curr = self.head
        while curr:
            items.append(curr.data)
            curr = curr.next
        return items

linked_list = LinkedList()

TAB_FOR_ACTION = {
    'circle': 'circle',
    'triangle': 'triangle',
    'uppercase': 'upper',
    'll_append': 'll',
    'll_delete': 'll',
}

def to_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return None


@app.route('/')
def home():
    return render_template('index.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/contact')
def contact():
    return render_template('contact.html')

@app.route('/works', methods=['GET', 'POST'])
def works():
    circle_area = None
    triangle_area = None
    uppercase_text = None
    message = None
    active_tab = None         

    if request.method == 'POST':
        action = request.form.get('action')
        active_tab = TAB_FOR_ACTION.get(action)

        # 1. Circle Area
        if action == 'circle':
            radius = to_float(request.form.get('radius'))
            if radius is None or radius < 0:
                circle_area = 'Invalid input'
            else:
                circle_area = round(math.pi * radius ** 2, 2)

        # 2. Triangle Area
        elif action == 'triangle':
            base = to_float(request.form.get('base'))
            height = to_float(request.form.get('height'))
            if base is None or height is None or base < 0 or height < 0:
                triangle_area = 'Invalid input'
            else:
                triangle_area = round(0.5 * base * height, 2)

        # 3. Uppercase Converter
        elif action == 'uppercase':
            text = request.form.get('text_input', '')
            uppercase_text = text.upper()

        # 4. Linked List Operations (Add / Remove)
        elif action == 'll_append':
            item = request.form.get('item', '').strip()
            if item:
                linked_list.append(item)
                message = f"Added '{item}' to Linked List."
        elif action == 'll_delete':
            item = request.form.get('item', '').strip()
            if item:
                if linked_list.delete(item):
                    message = f"Removed '{item}' from Linked List."
                else:
                    message = f"Item '{item}' not found in Linked List."

    return render_template(
        'works.html',
        circle_area=circle_area,
        triangle_area=triangle_area,
        uppercase_text=uppercase_text,
        ll_items=linked_list.get_all(),
        message=message,
        active_tab=active_tab
    )

if __name__ == '__main__':
    app.run(debug=True)