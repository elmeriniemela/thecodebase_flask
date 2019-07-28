
import json
from datetime import datetime

from flask import request
from flask import flash
from flask import session
from flask import send_file
from flask import render_template
from flask import Blueprint

from thecodebase.lib.sql import Cursor
from thecodebase.lib.refactor_ics import refactor_file
from thecodebase.lib.wrappers import login_required


refactor_ics = Blueprint('refactor_ics', __name__, template_folder='templates')


def refactor_template():

    with Cursor() as cur:
        found = cur.execute("SELECT json FROM Refactor ORDER BY time DESC")
        if found:
            data = json.loads(cur.fetchone()[0].decode('utf-8', 'ignore'))
            lines = [(key, value) for key, value in data.items()]
        else:
            lines = []

    kwargs = dict(
        refactor=True,
        bg='programming_header.jpg',
        page_title='Refactor ICS',
        enumerate=enumerate,
        lines=lines,
    )
    return render_template("refactor-ics.html", **kwargs)


@refactor_ics.route('/refactor-ics/', methods=['GET', 'POST'])
@login_required
def refactor_ics_view():
    if request.method == 'POST':
        if 'ics-file' not in request.files:
            flash('Select file first')
            return refactor_template()

        ics_file = request.files['ics-file']
        if ics_file.filename == '' or not ics_file.filename.endswith('.ics'):
            flash('Select proper filename (.ics)')
            return refactor_template()

        if ics_file:
            try:
                file_io, results = refactor_file(ics_file)
                with Cursor() as cur:
                    cur.execute("INSERT INTO Refactor (json, uid, time) VALUES (%s, %s, %s)",
                                (json.dumps(results, ensure_ascii=False).encode(
                                    'utf-8'), session.get('uid'), datetime.now(),)
                                )
                return send_file(file_io, attachment_filename="refactored.ics", as_attachment=True)
            except ValueError as error:
                refactor_ics.logger.error(
                    "Error processing ics-file: {}\n\nFile content:\n{}".format(error, ics_file.read()))
                flash("Error: Corrupted file")

    return refactor_template()
