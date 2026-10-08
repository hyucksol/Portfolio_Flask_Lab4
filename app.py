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
    calc_result = None
    uppercase_text = None
    message = None

    if request.method == 'POST':
        action = request.form.get('action')

        # 1. Circle Area
        if action == 'circle':
            radius = float(request.form.get('radius', 0))
            circle_area = round(3.14159 * (radius ** 2), 2)

        # 2. Triangle Area
        elif action == 'triangle':
            base = float(request.form.get('base', 0))
            height = float(request.form.get('height', 0))
            triangle_area = round(0.5 * base * height, 2)

        # 3. Simple Calculator
        elif action == 'calculator':
            num1 = float(request.form.get('num1', 0))
            num2 = float(request.form.get('num2', 0))
            operation = request.form.get('operation')
            if operation == 'add':
                calc_result = num1 + num2
            elif operation == 'subtract':
                calc_result = num1 - num2
            elif operation == 'multiply':
                calc_result = num1 * num2
            elif operation == 'divide':
                calc_result = num1 / num2 if num2 != 0 else 'Cannot divide by zero'

        # 4. Uppercase Converter
        elif action == 'uppercase':
            text = request.form.get('text_input', '')
            uppercase_text = text.upper()

        # 5. Linked List Operations (Add at Remove/Delete)
        elif action == 'll_append':
            item = request.form.get('item')
            if item:
                linked_list.append(item)
                message = f"Added '{item}' to Linked List."
        elif action == 'll_delete':
            item = request.form.get('item')
            if item:
                removed = linked_list.delete(item)
                if removed:
                    message = f"Removed '{item}' from Linked List."
                else:
                    message = f"Item '{item}' not found in Linked List."

    return render_template(
        'works.html',
        circle_area=circle_area,
        triangle_area=triangle_area,
        calc_result=calc_result,
        uppercase_text=uppercase_text,
        ll_items=linked_list.get_all(),
        message=message
    )

if __name__ == '__main__':
    app.run(debug=True)