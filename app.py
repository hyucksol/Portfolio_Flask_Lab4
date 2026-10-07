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
@app.route('/contact')
def profile():
    return render_template('profile.html')

@app.route('/calculators', methods=['GET', 'POST'])
def calculators():
    circle_area = None
    triangle_area = None
    if request.method == 'POST':
        form_type = request.form.get('form_type')
        if form_type == 'circle':
            radius = float(request.form.get('radius', 0))
            circle_area = round(3.14159 * (radius ** 2), 2)
        elif form_type == 'triangle':
            base = float(request.form.get('base', 0))
            height = float(request.form.get('height', 0))
            triangle_area = round(0.5 * base * height, 2)
    return render_template('calculators.html', circle_area=circle_area, triangle_area=triangle_area)

@app.route('/linkedlist', methods=['GET', 'POST'])
def linkedlist_view():
    if request.method == 'POST':
        item = request.form.get('item')
        if item:
            linked_list.append(item)
    return render_template('linkedlist.html', items=linked_list.get_all())

if __name__ == '__main__':
    app.run(debug=True)