class Node:
    """A node in a binary tree."""
    def __init__(self, value,left=None, right=None):
        self.value = value
        self.left = None
        self.right = None

class BinaryTree:
    """A binary tree data structure."""
    def __init__(self, root_value=None):
        self.root = Node(root_value) if root_value is not None else None

    def insert_left(self, current_node, value):
        """Insert a node as the left child of the current node."""
        if current_node.left is None:
            current_node.left = Node(value)
        else:
            new_node = Node(value)
            new_node.left = current_node.left
            current_node.left = new_node

    def insert_right(self, current_node, value):
        """Insert a node as the right child of the current node."""
        if current_node.right is None:
            current_node.right = Node(value)
        else:
            new_node = Node(value)
            new_node.right = current_node.right
            current_node.right = new_node

    def preorder_traversal(self, start,traversal):
        """Traverse the tree in preorder (root, left, right)."""
        if start:
            traversal += (str(start.value) + " ")
            traversal = self.preorder_traversal(start.left,traversal)
            traversal = self.preorder_traversal(start.right,traversal)
        return traversal    

    def inorder_traversal(self, start,traversal):
        """Traverse the tree in inorder (left, root, right)."""
        if start:
            traversal = self.inorder_traversal(start.left,traversal)
            traversal += (str(start.value) + " ")
            traversal = self.inorder_traversal(start.right,traversal)
        return traversal    

    def postorder_traversal(self, start,traversal):
        """Traverse the tree in postorder (left, right, root)."""
        if start:
            traversal = self.postorder_traversal(start.left, traversal)
            traversal = self.postorder_traversal(start.right, traversal)
            traversal += (str(start.value) + " ")
        return traversal


# Example usage
if __name__ == "__main__":
   
    tree = BinaryTree("R")
    
    # Insert nodes
    tree.insert_left(tree.root, "A")
    tree.insert_right(tree.root, "B")
    tree.insert_left(tree.root.left, "C")
    tree.insert_right(tree.root.left, "D")
    tree.insert_left(tree.root.right, "E")
    tree.insert_right(tree.root.right, "F")
    tree.insert_left(tree.root.right.right, "G")
    
    print()

    print("Preorder traversal: " + tree.preorder_traversal(tree.root,""))
    ##tree.preorder_traversal(tree.root,"")
    print("\n\nInorder traversal: " + tree.inorder_traversal(tree.root,""))
    # tree.inorder_traversal(tree.root)
    print("\n\nPostorder traversal: " + tree.postorder_traversal(tree.root,""))
 
    # tree.postorder_traversal(tree.root)
    print()