WORKS = [
    {'key': 'uppercase',   'title': 'toUpperCase',        'endpoint': 'works_uppercase',   'emoji': '🔤'},
    {'key': 'area',        'title': 'Area Calculator',    'endpoint': 'works_area_page',   'emoji': '📐'},
    {'key': 'linked-list', 'title': 'Linked List',        'endpoint': 'works_linked_list', 'emoji': '🔗'},
    {'key': 'stack',       'title': 'Stack',              'endpoint': 'works_stack',       'emoji': '📚'},
    {'key': 'queue',       'title': 'Queue and Dequeue',  'endpoint': 'works_queue',       'emoji': '🚶'},
    {'key': 'sorting',     'title': 'Sorting Visualizer', 'endpoint': 'works_sorting',     'emoji': '📊'},
    {'key': 'binary-tree', 'title': 'Binary Tree',        'endpoint': 'works_binary_tree', 'emoji': '🌳'},
]


def get_work(key):
    for work in WORKS:
        if work['key'] == key:
            return work
    return None