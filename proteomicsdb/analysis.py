from flask import Blueprint, render_template, session, request
import ast

bp = Blueprint('analysis', __name__, url_prefix='/analysis')


# View: after searching for protein/s in single post/file, display graph
@bp.route('/post', methods=('GET',))
def display_graph_post():
    data = session['data']  # abundance values to plot
    legend = list(data.keys())

    return render_template('analysis/graph_from_post.html',
                           legend=legend,
                           data=data)


# View: after searching for and selecting protein in entire index, display graph
@bp.route('/index', methods=["POST"])
def display_graph_index():
    if request.method == "POST":
        checks = request.form.getlist("result")  # list of strings (the strings are supposed to be dicts)

        new_checks = []  # list of dictionaries

        abun_cond = {}  # dict where key is post_id, val is list of abundance values

        for check in checks:
            new_check = ast.literal_eval(check)  # converts string rep of dict to actual dict
            new_checks.append(new_check)

            # get the dictionary values for keys beginning with 'abun'

            # new_check is a dict like so
            # {'abun_t1': 99.7, 'abun_t2': 102.7, 'abun_t3': 101.1, 'abun_t4': 80.8, 'abun_t5': 79.1, etc}.

            some_list = []  # save abundance value to list

            condition = ''
            for key, val in new_check.items():
                if key.startswith("abun"):
                    some_list.append(val)
                condition = new_check.get("condition")
                protein = new_check.get("gene")

            abun_cond[condition] = some_list

        legend = list(abun_cond.keys())
        data = abun_cond

    return render_template('analysis/graph_from_all.html', val=abun_cond, legend=legend, data=data, protein=protein)
