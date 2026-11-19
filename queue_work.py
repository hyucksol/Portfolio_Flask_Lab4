class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class Queue:
    def __init__(self):
        self.front = None
        self.rear = None

    def enqueue(self, data):
        new_node = Node(data)
        if self.rear is None:
            self.front = new_node
            self.rear = new_node
        else:
            self.rear.next = new_node
            self.rear = new_node

    def dequeue(self):
        if self.front is None:
            return None
        data = self.front.data
        self.front = self.front.next
        if self.front is None:
            self.rear = None
        return data

    def peek(self):
        if self.front is None:
            return None
        return self.front.data

    def is_empty(self):
        return self.front is None

    def clear(self):
        self.front = None
        self.rear = None

    def get_all(self):
        items = []
        current = self.front
        while current:
            items.append(current.data)
            current = current.next
        return items

class DNode:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None

class Deque:
    def __init__(self):
        self.head = None
        self.tail = None

    def add_front(self, data):
        new_node = DNode(data)
        if self.head is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

    def add_rear(self, data):
        new_node = DNode(data)
        if self.tail is None:
            self.head = new_node
            self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

    def remove_front(self):
        if self.head is None:
            return None
        data = self.head.data
        self.head = self.head.next
        if self.head is None:
            self.tail = None
        else:
            self.head.prev = None
        return data

    def remove_rear(self):
        if self.tail is None:
            return None
        data = self.tail.data
        self.tail = self.tail.prev
        if self.tail is None:
            self.head = None
        else:
            self.tail.next = None
        return data

    def peek_front(self):
        return None if self.head is None else self.head.data

    def peek_rear(self):
        return None if self.tail is None else self.tail.data

    def is_empty(self):
        return self.head is None

    def clear(self):
        self.head = None
        self.tail = None

    def get_all(self):
        items = []
        current = self.head
        while current:
            items.append(current.data)
            current = current.next
        return items


queue = Queue()
deque = Deque()

DEQUE_ACTIONS = {'add_front', 'add_rear', 'remove_front', 'remove_rear',
                 'peek_front', 'peek_rear', 'dq_clear'}


def handle_queue(action, value):
    if action == 'enqueue':
        if value:
            queue.enqueue(value)
            return f"Enqueued '{value}' at the rear."
        return "Type a value to enqueue."

    if action == 'dequeue':
        if queue.is_empty():
            return "Queue is empty. Nothing to dequeue."
        return f"Dequeued '{queue.dequeue()}' from the front."

    if action == 'q_peek':
        if queue.is_empty():
            return "Queue is empty."
        return f"Front element: '{queue.peek()}'"

    if action == 'q_clear':
        queue.clear()
        return "The queue was cleared."

    return None


def handle_deque(action, value):
    if action == 'add_front':
        if value:
            deque.add_front(value)
            return f"Added '{value}' at the front."
        return "Type a value first."

    if action == 'add_rear':
        if value:
            deque.add_rear(value)
            return f"Added '{value}' at the rear."
        return "Type a value first."

    if action == 'remove_front':
        if deque.is_empty():
            return "Deque is empty."
        return f"Removed '{deque.remove_front()}' from the front."

    if action == 'remove_rear':
        if deque.is_empty():
            return "Deque is empty."
        return f"Removed '{deque.remove_rear()}' from the rear."

    if action == 'peek_front':
        return "Deque is empty." if deque.is_empty() else f"Front element: '{deque.peek_front()}'"

    if action == 'peek_rear':
        return "Deque is empty." if deque.is_empty() else f"Rear element: '{deque.peek_rear()}'"

    if action == 'dq_clear':
        deque.clear()
        return "The deque was cleared."

    return None


def handle(form):
    action = form.get('action')
    value = form.get('value', '').strip()

    if action in DEQUE_ACTIONS:
        return {'deque_message': handle_deque(action, value)}
    return {'queue_message': handle_queue(action, value)}


def state():
    return {'queue_items': queue.get_all(), 'deque_items': deque.get_all()}