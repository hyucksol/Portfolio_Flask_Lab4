import hmac
import os
import re
import secrets

from flask import (Flask, abort, flash, redirect, render_template,
                   request, session, url_for)

import circle
import linked_list
import messages
import queue_work
import sorting
import stack_work
import tree_work
import triangle
import uppercase
from works_info import WORKS, get_work

app = Flask(__name__)
# Set SECRET_KEY in your environment when you deploy. The random fallback is fine for local use.
app.secret_key = os.environ.get('SECRET_KEY') or secrets.token_hex(32)
app.config['MAX_CONTENT_LENGTH'] = 64 * 1024          # no giant form posts


def same(a, b):
    return hmac.compare_digest(a.encode(), b.encode())


IMAGE_TYPES = ('.png', '.jpg', '.jpeg', '.gif', '.webp')


def _plain(text):
    """'Linked-List' / 'linked_list' / 'linked list' -> 'linkedlist' (so names match regardless of formatting)."""
    return re.sub(r'[-_ ]', '', text.lower())


def find_image(folder, name):
    wanted = _plain(os.path.splitext(name)[0])
    path = os.path.join(app.static_folder, 'images', folder)
    if not os.path.isdir(path):
        return None
    for file in sorted(os.listdir(path)):
        stem, ext = os.path.splitext(file)
        if ext.lower() in IMAGE_TYPES and _plain(stem) == wanted:
            parts = [p for p in ('images', folder, file) if p]
            return url_for('static', filename='/'.join(parts))
    return None


@app.context_processor
def inject_globals():
    def csrf_token():
        if 'csrf' not in session:
            session['csrf'] = secrets.token_hex(16)
        return session['csrf']
    return {'csrf_token': csrf_token, 'image_url': find_image}


def work_page(key, template, modules=(), result=None):
    """Render a work page along with its state and result."""
    context = {}
    for module in modules:
        context.update(module.state())
    context.update(result or {})
    # Check inside templates/works/ first; if not there, check templates/ directly
    names = [template, template.split('/')[-1]]
    return render_template(names, work=get_work(key), **context)


# ---------- MAIN PAGES ----------
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/profile')
def profile():
    return render_template('profile.html')


@app.route('/contact', methods=['GET', 'POST'])
def contact():
    form, error = {}, None
    if request.method == 'POST':
        form = request.form
        if not same(session.get('csrf', ''), form.get('csrf', '')) or not session.get('csrf'):
            error = "Your session expired. Please send the message again."
        elif form.get('website'):                      
            flash("Message sent! Thank you.")
            return redirect(url_for('contact'))
        elif messages.rate_limited(request.remote_addr or 'unknown'):
            error = "You've sent a few messages already. Please try again in a little while."
        else:
            clean, error = messages.validate(form)
            if not error:
                error = messages.send(clean)
                if error and app.debug and messages.last_error:     
                    error += f"  [{messages.last_error}]"
            if not error:
                flash("Message sent! Thank you, I'll reply to your email soon.")
                return redirect(url_for('contact'))
    return render_template('contact.html', form=form, error=error,
                           my_email=messages.gmail_address())


# ---------- WORKS ----------
@app.route('/works')
def works():
    return render_template('works.html', works=WORKS)


@app.route('/works/uppercase', methods=['GET', 'POST'])
def works_uppercase():
    result = uppercase.handle(request.form) if request.method == 'POST' else None
    return work_page('uppercase', 'works/uppercase.html', result=result)


@app.route('/works/area')
def works_area_page():
    return work_page('area', 'works/area.html')


@app.route('/works/area/circle', methods=['POST'])
def works_circle():
    return work_page('area', 'works/area.html', result=circle.handle(request.form))


@app.route('/works/area/triangle', methods=['POST'])
def works_triangle():
    return work_page('area', 'works/area.html', result=triangle.handle(request.form))


@app.route('/works/linked-list', methods=['GET', 'POST'])
def works_linked_list():
    result = linked_list.handle(request.form) if request.method == 'POST' else None
    return work_page('linked-list', 'works/linked_list.html', [linked_list], result)


@app.route('/works/stack', methods=['GET', 'POST'])
def works_stack():
    result = stack_work.handle(request.form) if request.method == 'POST' else None
    return work_page('stack', 'works/stack.html', [stack_work], result)


@app.route('/works/queue', methods=['GET', 'POST'])
def works_queue():
    result = queue_work.handle(request.form) if request.method == 'POST' else None
    return work_page('queue', 'works/queue.html', [queue_work], result)


@app.route('/works/sorting')
def works_sorting():
    # The form and Prev/Next/Play links use GET, so read from request.args.
    # If there are no numbers or action yet (first page load), show nothing.
    args = request.args
    result = sorting.handle(args) if ('numbers' in args or 'action' in args) else None
    return work_page('sorting', 'works/sorting.html', [sorting], result)


@app.route('/works/binary-tree', methods=['GET', 'POST'])
def works_binary_tree():
    result = tree_work.handle(request.form) if request.method == 'POST' else None
    return work_page('binary-tree', 'works/binary_tree.html', [tree_work], result)


# ---------- ERRORS ----------
@app.errorhandler(405)
def method_not_allowed(error):
    # POST-only URL opened directly in the address bar (e.g. /works/area/circle) -> redirect back to the work page
    return redirect(request.path.rsplit('/', 1)[0] or url_for('home'))


@app.errorhandler(404)
def not_found(error):
    return render_template('404.html'), 404


if __name__ == '__main__':
    app.run(debug=os.environ.get('FLASK_DEBUG', '1') == '1')