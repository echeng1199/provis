# search blueprint searches index for query

from flask import Blueprint, render_template, request, session
from whoosh import index
from whoosh.query import *

from proteomicsdb.posts import get_post

bp = Blueprint('search', __name__, url_prefix='/search')


# View: display search page
@bp.route('/', methods=('GET',))
def search():
    return render_template('search/search_identifier.html')


# View: search entire index (i.e. all posts) for one query
@bp.route('result', methods=['POST'])
def search_index():
    if request.method == 'POST':
        # open index
        index_path = 'proteomicsdb/index_dir'
        ix = index.open_dir(index_path)

        # decide which search parameter is being asked
        # pass in the search term (i.e. gene symbol)
        if request.form['accession']:
            search_query = "accession"  # case sensitive (based on how we create Whoosh schema)
            protein = request.form['accession']
        elif request.form['gene']:
            search_query = "gene"  # case sensitive
            protein = request.form['gene']
        elif request.form['desc']:
            search_query = "description"  # case-insensitive
            protein = request.form['desc']

        # list of dictionaries, where each list is something that matches the query
        # and dictionary is the search result and information
        # HTML doesn't support passing a Whoosh Hit object, so this is the alternative
        all_matches = []

        # run search
        with ix.searcher() as searcher:
            query = And([Term(search_query, protein)])
            results = searcher.search(query, terms=True, limit=None)  # terms=True saves which terms matched

            for result in results:
                all_matches.append(result.fields())

        # dict where key is post_id and value is list of abundances to be plotted
        abun_values = {}

        for match in all_matches:
            abun_list = []
            for key, val in match.items():
                # get abundance values
                # dict contains other information (i.e. accession #, description) that we don't need
                if key.startswith("abun"):
                    abun_list.append(val)
            abun_values[match['post_id']] = abun_list

        # makes these values accessible everywhere in program
        session['data'] = abun_values
        
        return render_template('search/search_result.html',
                               query=protein,
                               results=all_matches,
                               data=abun_values,
                               get_post_func=get_post)


# View: search within a single post/file
@bp.route('<int:id>/search_in_files', methods=['POST'])
def search_in_file(id):
    if request.method == 'POST':
        post = get_post(id)

        # decide which search parameter is being asked
        # pass in the search term or list of terms (i.e. "oasl, s100a6")
        if request.form['accession']:
            search_query = "accession"  # case sensitive (based on how we create Whoosh schema)
            proteins = request.form['accession']
        elif request.form['gene']:
            search_query = "gene"  # case sensitive
            proteins = request.form['gene']

        # create list of proteins from input string
        proteins_list = proteins.split(", ")

        all_matches = get_match_in_post(proteins_list, search_query, id)

        # dictionary where key is gene or accession number and value is abundance value
        # to be plotted
        abun_data = get_post_match_abun(all_matches, search_query)

        session['data'] = abun_data

        return render_template("search/search_file.html",
                               proteins=proteins_list,
                               post=post,
                               all_matches=all_matches,
                               num_matches=len(all_matches),
                               data=abun_data)


# Function: when searching for protein/s in a single post, get protein/s information
# returns list of dictionaries, where each dictionary represents a protein's information
def get_match_in_post(proteins_list, search_query, id):
    index_path = 'proteomicsdb/index_dir'
    ix = index.open_dir(index_path)

    all_matches = []

    for protein in proteins_list:
        with ix.searcher() as searcher:

            # search for protein in which the post id is specified
            query = And([Term(search_query, protein), Term("post_id", str(id))])
            results = searcher.search(query, terms=True, limit=None)  # terms=True saves which terms matched

            # each 'results' object should only have one entry since search terms are limited to strict identifiers
            if results:
                result = results[0].fields()
                all_matches.append(result)

    return all_matches


# Function: when searching for protein/s in a single post, get protein/s abun value only
# returns dictionary where key is gene or accession number, and value is a list of abundance values
def get_post_match_abun(all_matches, search_query):
    abun_values = {}
    for match in all_matches:
        abun_value = []
        for key, val in match.items():
            if key.startswith('abun'):
                abun_value.append(val)
        abun_values[match[search_query]] = abun_value

    return abun_values
