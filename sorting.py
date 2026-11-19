import math
import random
import re

from markupsafe import Markup, escape

MAX_NUMBERS = 40

def parse_numbers(text):
    """Convert comma-separated text into a list of numbers, e.g.: 64, 25, 12."""
    parts = [part.strip() for part in (text or '').split(',')]
    parts = [part for part in parts if part]
    if not parts:
        raise ValueError("Type some numbers first.")
    if len(parts) > MAX_NUMBERS:
        raise ValueError(f"Please use {MAX_NUMBERS} numbers or fewer.")

    numbers = []
    for part in parts:
        try:
            value = float(part)
        except ValueError:
            raise ValueError(f"'{part}' is not a number. Separate the numbers with commas.")
        if not math.isfinite(value):
            raise ValueError(f"'{part}' is not a valid number.")
        numbers.append(int(value) if value.is_integer() else value)
    return numbers


def out_of_order(a, b, ascending):
    """Return True if `a` (earlier) and `b` (later) should swap places."""
    return a > b if ascending else a < b

class Trace:
    def __init__(self, values, ascending=True):
        self.values = list(values)
        self.asc = ascending
        self.steps = []
        self.comparisons = 0
        self.moves = 0
        self.done = []
        self._sent_done = None
        self.lay = None              # {id: (depth, group)}, used for "Show depth" (insertion and merge only)
        self._sent_lay = None

    def add(self, text, order=None, cmp=(), swap=(), pivot=None, milestone=None, q=0, m=0):
        step = {'t': text, 'c': list(cmp), 's': list(swap), 'p': pivot, 'q': q, 'm': m}
        if order is not None:
            step['o'] = list(order)
        if self.done != self._sent_done:
            step['d'] = list(self.done)
            self._sent_done = list(self.done)
        if self.lay is not None:
            snap = [self.lay.get(i, (0, 0)) for i in range(len(self.values))]
            if snap != self._sent_lay:
                step['g'] = snap
                self._sent_lay = snap
        if milestone:
            step['k'] = milestone
        self.steps.append(step)
        self.comparisons += q
        self.moves += m

    def note(self, text, **kwargs):
        self.add(text, **kwargs)

    def compare(self, a, b, yes, no, pivot=None, intro="Compare {x} and {y}"):
        """Compare two ids. Returns True if they are out of order."""
        x, y = self.values[a], self.values[b]
        bad = out_of_order(x, y, self.asc)
        if bad:
            sign = '>' if self.asc else '<'
        else:
            sign = '≤' if self.asc else '≥'
        result = (yes if bad else no).format(x=x, y=y)
        self.add(f"{intro.format(x=x, y=y)}: {x} {sign} {y}. {result}",
                 cmp=(a, b), pivot=pivot, q=1)
        return bad

    def swap(self, arr, i, j, text, pivot=None):
        """Swap elements at indices i and j in `arr`. {x} = value at i before swap, {y} = value at j."""
        x, y = self.values[arr[i]], self.values[arr[j]]
        arr[i], arr[j] = arr[j], arr[i]
        self.add(text.format(x=x, y=y), order=arr, swap=(arr[i], arr[j]), pivot=pivot, m=1)

    def mark(self, *ids):
        for item in ids:
            if item not in self.done:
                self.done.append(item)

    def finish(self, arr):
        self.done = list(arr)
        self.add("Done! The list is sorted.", order=arr, milestone="Sorted")

def bubble_sort(t, arr):
    n = len(arr)
    word = "larger" if t.asc else "smaller"
    for i in range(n - 1):
        swapped = False
        for j in range(n - 1 - i):
            bad = t.compare(arr[j], arr[j + 1],
                            "Out of order, so swap them.", "Already in order, move on.")
            if bad:
                t.swap(arr, j, j + 1, "Swapped {x} and {y}.")
                swapped = True
        last = arr[n - 1 - i]
        t.mark(last)
        t.note(f"End of pass {i + 1}: {t.values[last]} (the {word} one) bubbled to its final place.",
               order=arr, milestone=f"Pass {i + 1}")
        if not swapped:
            t.done = list(arr)
            t.note("No swaps happened in this pass, so the list is already sorted.",
                   order=arr, milestone="No swaps")
            break


def selection_sort(t, arr):
    n = len(arr)
    word = "smallest" if t.asc else "biggest"
    for i in range(n - 1):
        chosen = i
        t.note(f"Pass {i + 1}: find the {word} number from position {i + 1} onward.", pivot=arr[chosen])
        for j in range(i + 1, n):
            bad = t.compare(arr[chosen], arr[j],
                            "{y} is the new " + word + ".", "Keep {x}.",
                            pivot=arr[chosen], intro="Compare {x} (current " + word + ") with {y}")
            if bad:
                chosen = j
        if chosen != i:
            t.swap(arr, i, chosen, "Swap {x} and {y}: {y} goes to position " + str(i + 1) + ".")
        else:
            t.note(f"{t.values[arr[i]]} is already in position {i + 1}, no swap needed.", pivot=arr[i])
        t.mark(arr[i])
        t.note(f"End of pass {i + 1}: {t.values[arr[i]]} is in its final place.",
               order=arr, milestone=f"Pass {i + 1}")


def insertion_sort(t, arr):
    n = len(arr)

    def layout(sorted_ids, key=None):
        """Depth: sorted items stay on top (0), waiting items sit one level below (1)."""
        t.lay = {item: (1, 2) for item in arr}
        for item in sorted_ids:
            t.lay[item] = (0, 0)
        if key is not None:
            t.lay[key] = (0, 1)

    if n:
        t.done = [arr[0]]
    for i in range(1, n):
        key = arr[i]
        value = t.values[key]
        t.done = list(arr[:i])
        layout(arr[:i], key)
        t.note(f"Take {value} and insert it into the sorted part on the left.", pivot=key)
        j = i - 1
        while j >= 0:
            bad = t.compare(arr[j], key,
                            "{x} is in the wrong place, so {y} moves left.",
                            "{x} is in the right place, so {y} stops here.",
                            pivot=key, intro="Compare {x} with {y}")
            if bad:
                t.swap(arr, j, j + 1, "Swap {x} and {y}: {y} moves one step left.", pivot=key)
                j -= 1
            else:
                break
        t.done = list(arr[:i + 1])
        layout(arr[:i + 1])
        t.note(f"{value} is now in place. The left part is sorted.",
               order=arr, milestone=f"Insert {value}")


def merge_sort(t, arr):
    t.lay = {item: (0, 0) for item in arr}
    next_group = [0]

    def new_group():
        next_group[0] += 1
        return next_group[0]

    def merge(low, mid, high, depth, group):
        left = arr[low:mid + 1]
        right = arr[mid + 1:high + 1]
        merged = []
        i = j = 0

        def view():
            return arr[:low] + merged + left[i:] + right[j:] + arr[high + 1:]

        while i < len(left) and j < len(right):
            bad = t.compare(left[i], right[j],
                            "{y} goes first.", "{x} goes first.",
                            intro="Compare the front of the left half ({x}) with the right half ({y})")
            if bad:
                moved = right[j]
                j += 1
            else:
                moved = left[i]
                i += 1
            merged.append(moved)
            t.add(f"Place {t.values[moved]} into position {low + len(merged)}.",
                  order=view(), swap=(moved,), m=1)
        rest = len(left) - i + len(right) - j
        if rest:
            merged.extend(left[i:])
            merged.extend(right[j:])
            t.add(f"Copy the remaining {rest} number(s) over; they are already in order.", m=rest)
        arr[low:high + 1] = merged
        for item in merged:                       # merge finished; return to the parent depth level
            t.lay[item] = (depth, group)
        t.add(f"Merged positions {low + 1} to {high + 1}.", order=arr,
              milestone=f"Merge positions {low + 1}-{high + 1}")

    def sort(low, high, depth=0, group=0):
        if low >= high:
            return
        mid = (low + high) // 2
        left_group, right_group = new_group(), new_group()
        for item in arr[low:mid + 1]:             # splitting moves down one depth level
            t.lay[item] = (depth + 1, left_group)
        for item in arr[mid + 1:high + 1]:
            t.lay[item] = (depth + 1, right_group)
        t.note(f"Split positions {low + 1} to {high + 1} into two halves: "
               f"{low + 1} to {mid + 1}, and {mid + 2} to {high + 1}.", order=arr)
        sort(low, mid, depth + 1, left_group)
        sort(mid + 1, high, depth + 1, right_group)
        merge(low, mid, high, depth, group)

    sort(0, len(arr) - 1)


def quick_sort(t, arr):
    def partition(low, high):
        pivot = arr[high]
        pv = t.values[pivot]
        i = low - 1
        t.note(f"Pick {pv} (the last number) as the pivot.", pivot=pivot)
        for j in range(low, high):
            bad = t.compare(arr[j], pivot,
                            "It belongs on the right side of the pivot.",
                            "It belongs on the left side of the pivot.",
                            pivot=pivot, intro="Compare {x} with the pivot {y}")
            if not bad:
                i += 1
                if i != j:
                    t.swap(arr, i, j, "Swap {x} and {y} to move the small side together.", pivot=pivot)
        if i + 1 != high:
            t.swap(arr, i + 1, high, "Swap {x} and the pivot {y}: the pivot goes between the two sides.",
                   pivot=pivot)
        t.mark(pivot)
        t.note(f"Pivot {pv} is now in its final place.", order=arr, milestone=f"Pivot {pv}")
        return i + 1

    def sort(low, high):
        if low < high:
            pivot_index = partition(low, high)
            sort(low, pivot_index - 1)
            sort(pivot_index + 1, high)
        elif low == high:
            t.mark(arr[low])
            t.note(f"{t.values[arr[low]]} is alone, so it is already in place.", order=arr)

    sort(0, len(arr) - 1)


ALGORITHMS = {
    'bubble':    ("Bubble Sort",    bubble_sort,    "Best O(n), worst O(n²)"),
    'selection': ("Selection Sort", selection_sort, "Always O(n²)"),
    'insertion': ("Insertion Sort", insertion_sort, "Best O(n), worst O(n²)"),
    'merge':     ("Merge Sort",     merge_sort,     "Always O(n log n)"),
    'quick':     ("Quick Sort",     quick_sort,     "Average O(n log n), worst O(n²)"),
}

ABOUT = {
    'bubble':    "Compares neighbors and swaps them when they are out of order. Each pass, one number bubbles to its final place at the end.",
    'selection': "Each pass finds the smallest (or biggest) number in the unsorted part and swaps it into its place.",
    'insertion': "Takes one number at a time and slides it left until it fits in the sorted part.",
    'merge':     "Splits the list into halves, sorts each half, then merges the halves back together in order.",
    'quick':     "Picks a pivot, puts numbers that belong before it on its left and the rest on its right, then repeats on each side.",
}


DEPTH_HUES = [200, 340, 175, 270, 315, 225, 10, 190]      

DEPTH_NOTE = {
    'insertion': "Depth view: the sorted part stays on top. The numbers still waiting are one level lower. The number being placed (purple) climbs up to the top, then slides left into its spot.",
    'merge':     "Depth view: every split goes one level down, and each half has its own color. When two halves are merged they climb back up one level.",
}


def make_milestones(trace):
    """Build pass/stage summary entries: (label, step number, chips)."""
    milestones = []
    order, done = [], []
    for number, step in enumerate(trace.steps):
        order = step.get('o', order)
        done = step.get('d', done)
        if step.get('k'):
            chips = [(trace.values[item], item in done) for item in order]
            milestones.append({'label': step['k'], 'step': number, 'chips': chips})
    return milestones


def run_sort(numbers, key, ascending=True):
    name, function, complexity = ALGORITHMS[key]
    trace = Trace(numbers, ascending)
    arr = list(range(len(numbers)))
    trace.add("Original list. Press ▶ Play to watch it get sorted.", order=arr, milestone="Original")
    function(trace, arr)
    trace.finish(arr)
    return {
        'key': key,
        'name': name,
        'complexity': complexity,
        'about': ABOUT[key],
        'original': list(numbers),
        'sorted': [numbers[item] for item in arr],
        'comparisons': trace.comparisons,
        'moves': trace.moves,
        'trace': {'values': list(numbers), 'steps': trace.steps},
        'milestones': make_milestones(trace),
    }


def to_int(value, default, low, high):
    """Safely convert a URL/form value to a clamped integer."""
    try:
        number = int(value)
    except (TypeError, ValueError):
        number = default
    return max(low, min(high, number))


def text_with_numbers(text):
    """Wrap numbers in explanation text with a 'num' span so the number font applies."""
    parts = re.split(r'(-?\d+(?:\.\d+)?)', text)
    html = ''.join(f'<span class="num">{escape(part)}</span>' if index % 2 else str(escape(part))
                   for index, part in enumerate(parts))
    return Markup(html)


def build_view(result, step, speed, depth=False):
    values = result['trace']['values']
    steps = result['trace']['steps']
    count = len(values)

    frames, order, done, comparisons, moves = [], [], [], 0, 0
    layout = [(0, 0)] * count
    has_depth = any('g' in item for item in steps)
    for item in steps:
        order = item.get('o', order)
        done = item.get('d', done)
        layout = item.get('g', layout)
        comparisons += item['q']
        moves += item['m']
        frames.append((order, done, comparisons, moves, layout))

    last = len(steps) - 1
    step = max(0, min(last, step))
    current = steps[step]
    order, done, comparisons, moves, layout = frames[step]
    before = frames[step - 1][0] if step > 0 else order
    before_pos = {item: pos for pos, item in enumerate(before)}

    low, high = min(values), max(values)
    span = high - low
    bars = []
    for item, value in enumerate(values):
        pos = order.index(item)
        if item in current['s']:
            color = 'swap'
        elif item in current['c']:
            color = 'cmp'
        elif current['p'] == item:
            color = 'pivot'
        elif item in done:
            color = 'done'
        else:
            color = ''
        bars.append({
            'value': value,
            'height': 70 if span == 0 else round(20 + (value - low) / span * 66),
            'left': round(pos * 100 / count, 3),
            'k': before_pos[item] - pos,
            'dep': layout[item][0],
            'hue': DEPTH_HUES[layout[item][1] % len(DEPTH_HUES)],
            'cls': (color + (' is-pivot' if current['p'] == item else '')).strip(),
        })

    max_depth = max(bar['dep'] for bar in bars)
    milestones = []
    active = None
    for index, mile in enumerate(result['milestones']):
        if mile['step'] <= step:
            active = index
    for index, mile in enumerate(result['milestones']):
        milestones.append(dict(mile, active=(index == active)))

    delay = round(2.4 * 0.78 ** (speed - 1), 2)           # seconds before advancing to the next step
    return {
        'step': step,
        'last': last,
        'total': len(steps),
        'percent': round(step * 100 / last) if last else 100,
        'text': text_with_numbers(current['t']),
        'comparisons': comparisons,
        'moves': moves,
        'bars': bars,
        'width': round(100 / count, 3),
        'count': count,
        'positions': list(range(1, count + 1)),
        'delay': delay,
        'duration': round(min(0.9, delay * 0.8), 2),      # bar slide transition duration
        'milestones': milestones,
        'has_depth': has_depth,
        'depth_on': bool(depth and has_depth),
        'max_depth': max_depth,
        'depth_note': DEPTH_NOTE.get(result['key'], ''),
    }


def handle(form):
    """Read from request.values: supports both GET forms and Prev/Next/Play navigation links."""
    text = form.get('numbers', '')
    key = form.get('algorithm', 'bubble')
    if key not in ALGORITHMS:
        key = 'bubble'
    order = 'desc' if form.get('order') == 'desc' else 'asc'
    action = form.get('action', 'sort')
    step = to_int(form.get('step'), 0, 0, 10 ** 6)
    speed = to_int(form.get('speed'), 5, 1, 10)
    play = form.get('play') == '1'
    depth = form.get('depth') == '1'
    context = {'sort_input': text, 'sort_algo': key, 'sort_order': order, 'sort_speed': speed, 'sort_depth': depth}

    if action == 'random':
        numbers = random.sample(range(1, 100), 10)
        text = ', '.join(str(n) for n in numbers)
        context['sort_input'] = text
        action, step = 'sort', 0                          # immediately show sorting for the newly generated numbers

    try:
        numbers = parse_numbers(text)
        ascending = (order != 'desc')

        if action == 'compare':
            results = [run_sort(numbers, k, ascending) for k in ALGORITHMS]
            fewest = min(r['comparisons'] for r in results)
            context['sort_compare'] = [
                {
                    'name': r['name'],
                    'comparisons': r['comparisons'],
                    'moves': r['moves'],
                    'complexity': r['complexity'],
                    'best': r['comparisons'] == fewest,
                }
                for r in results
            ]
            context['sort_sorted'] = results[0]['sorted']
        else:
            result = run_sort(numbers, key, ascending)
            view = build_view(result, step, speed, depth)
            context['sort_result'] = result
            context['sort_view'] = view
            context['sort_play'] = play and view['step'] < view['last']
    except ValueError as error:
        context['sort_error'] = str(error)

    return context


def state():
    return {'sort_algorithms': [(key, info[0]) for key, info in ALGORITHMS.items()]}