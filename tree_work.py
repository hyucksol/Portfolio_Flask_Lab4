from binary_tree import BinaryTree, Node    

tree = BinaryTree()


def find_node(node, value):
    if node is None:
        return None
    if str(node.value) == value:
        return node
    found = find_node(node.left, value)
    if found is not None:
        return found
    return find_node(node.right, value)


def to_dict(node):
    if node is None:
        return None
    return {'value': node.value, 'left': to_dict(node.left), 'right': to_dict(node.right)}


def load_sample():
    tree.root = Node("R")
    tree.insert_left(tree.root, "A")
    tree.insert_right(tree.root, "B")
    tree.insert_left(tree.root.left, "C")
    tree.insert_right(tree.root.left, "D")
    tree.insert_left(tree.root.right, "E")
    tree.insert_right(tree.root.right, "F")
    tree.insert_left(tree.root.right.right, "G")


def handle(form):
    action = form.get('action')
    value = form.get('value', '').strip()
    parent_value = form.get('parent', '').strip()
    message = None

    if action == 'tree_root':
        if not value:
            message = "Type a value for the root."
        elif tree.root is not None:
            message = "The tree already has a root. Clear the tree to start over."
        else:
            tree.root = Node(value)
            message = f"Root '{value}' created."

    elif action in ('tree_left', 'tree_right'):
        side = 'left' if action == 'tree_left' else 'right'
        if tree.root is None:
            message = "Create the root first."
        elif not value or not parent_value:
            message = "Type both the new value and the parent value."
        else:
            parent = find_node(tree.root, parent_value)
            if parent is None:
                message = f"Parent '{parent_value}' was not found."
            else:
                if side == 'left':
                    tree.insert_left(parent, value)
                else:
                    tree.insert_right(parent, value)
                message = f"Inserted '{value}' as the {side} child of '{parent_value}'."

    elif action == 'tree_sample':
        load_sample()
        message = "Loaded the sample tree from sir's example."

    elif action == 'tree_clear':
        tree.root = None
        message = "The tree was cleared."

    return {'tree_message': message}


def state():
    return {
        'tree_data': to_dict(tree.root),
        'tree_pre': tree.preorder_traversal(tree.root, "").strip(),
        'tree_in': tree.inorder_traversal(tree.root, "").strip(),
        'tree_post': tree.postorder_traversal(tree.root, "").strip(),
    }