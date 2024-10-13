if __name__ == "__main__":
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
            current = self.head
            while current.next:  # Traverse until the last node
                current = current.head
            current.next = new_node

        def print_list(self):
            current = self.head
            while current:
                print(current.data)
                current = current.next

    # Example usage
    ll = LinkedList()
    ll.append(1)
    ll.append(2)
    ll.append(3)
    ll.print_list()