class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    # ---------- INSERT ----------
    def insert_at_beginning(self, data):
        new_node = Node(data)
        new_node.next = self.head
        self.head = new_node

    def insert_at_end(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        last = self.head
        while last.next:
            last = last.next
        last.next = new_node

    def insert_after(self, target, data):
        curr = self.head
        while curr and curr.data != target:
            curr = curr.next
        if curr is None:
            return False
        new_node = Node(data)
        new_node.next = curr.next
        curr.next = new_node
        return True

    # ---------- SEARCH ----------
    def search(self, data):
        curr = self.head
        index = 0
        while curr:
            if curr.data == data:
                return index
            curr = curr.next
            index += 1
        return -1

    # ---------- DELETE ----------
    def delete_first(self):
        if self.head is None:
            return None
        data = self.head.data
        self.head = self.head.next
        return data

    def delete_last(self):
        if self.head is None:
            return None
        if self.head.next is None:
            data = self.head.data
            self.head = None
            return data
        prev = self.head
        while prev.next.next:
            prev = prev.next
        data = prev.next.data
        prev.next = None
        return data

    def delete_value(self, data):
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

    # ---------- LIST ----------
    def clear(self):
        self.head = None

    def load_sample(self):
        self.clear()
        for value in ['10', '20', '30', '40', '50']:
            self.insert_at_end(value)

    def get_all(self):
        items = []
        curr = self.head
        while curr:
            items.append(curr.data)
            curr = curr.next
        return items


linked_list = LinkedList()


def handle(form):
    action = form.get('action')
    value = form.get('value', '').strip()
    after = form.get('after_value', '').strip()
    message = None
    found = None

    if action == 'insert_begin':
        if value:
            linked_list.insert_at_beginning(value)
            message = f"Inserted '{value}' at the beginning."
        else:
            message = "Type a value first."

    elif action == 'insert_end':
        if value:
            linked_list.insert_at_end(value)
            message = f"Inserted '{value}' at the end."
        else:
            message = "Type a value first."

    elif action == 'insert_after':
        if not value or not after:
            message = "Type both the value and the 'after value'."
        elif linked_list.insert_after(after, value):
            message = f"Inserted '{value}' after '{after}'."
        else:
            message = f"'{after}' was not found in the list."

    elif action == 'search':
        if not value:
            message = "Type a value to search."
        else:
            index = linked_list.search(value)
            if index == -1:
                message = f"'{value}' was not found."
            else:
                found = index
                message = f"Found '{value}' at position {index + 1}."

    elif action == 'delete_first':
        removed = linked_list.delete_first()
        message = "The list is empty." if removed is None else f"Deleted the first node ('{removed}')."

    elif action == 'delete_last':
        removed = linked_list.delete_last()
        message = "The list is empty." if removed is None else f"Deleted the last node ('{removed}')."

    elif action == 'delete_value':
        if not value:
            message = "Type a value to delete."
        elif linked_list.delete_value(value):
            message = f"Deleted '{value}'."
        else:
            message = f"'{value}' was not found."

    elif action == 'load_sample':
        linked_list.load_sample()
        message = "Loaded sample: 10 → 20 → 30 → 40 → 50."

    elif action == 'clear':
        linked_list.clear()
        message = "The list was cleared."

    return {'ll_message': message, 'll_found': found}


def state():
    return {'ll_items': linked_list.get_all(), 'll_found': None}