# 'make_index' specifies functions to create search index
# when first file uploaded, Whoosh index is created, such that each entry in index is a row in the file
# subsequent files will be indexed and the entries added to the initial index
# NOTE: not a very efficient method of indexing, have not yet figured out a better way


# use Whoosh API to make (and later, search) index
from whoosh.fields import Schema, TEXT, ID, KEYWORD, NUMERIC, STORED
from whoosh import index, analysis
import os.path
import shutil


# files are to be uploaded as Excel files with a specified format

# Function: deletes index directory (thus deleting index and contents) and make new index folder
# Only runs when cmd line arg "flask init-db" is run [see proteomicsdb/db.py]
# better way would be to delete on contents of index folder
def clear_index():
    index_path = "proteomicsdb/index_dir"

    # delete and make it directory
    if os.path.exists(index_path):
        shutil.rmtree(index_path)
        os.mkdir(index_path)
    # if there was no directory to begin with make directory
    else:
        os.mkdir(index_path)


# Function: format files
def format_file(df):
    df.fillna("", inplace=True)  # remove NaN values b/c Whoosh can't work with it

    # if a cell has two values (i.e. Gene Symbol = 'X, Y'), Whoosh will only know that the gene symbol
    # is both X and Y if there is a comma
    df.replace(";", ",", regex=True, inplace=True)
    return df


# Function: convert df to dict where key is col name and value is col data as a list
# Whoosh document writer works with lists (thus dict being converted to list is can easily be done)
def make_dict(df):
    df_dict = {k: list(df[k]) for k in df.columns}
    return df_dict


# Class: to allow index to be searched regardless of query case matches index case
class CaseSensitivizer(analysis.Filter):
    def __call__(self, tokens):
        for t in tokens:
            yield t
            if t.mode == "index":
                low = t.text.lower()
                if low != t.text:
                    t.text = low
                    yield t


myanalyzer = analysis.RegexTokenizer() | CaseSensitivizer()


# Function: make Whoosh schema that specifies type of information that needs to be indexed and how
def create_schema():
    schema = Schema(post_id=ID(stored=True),
                    condition=STORED,
                    accession=ID(stored=True, analyzer=myanalyzer),
                    description=TEXT(stored=True, analyzer=myanalyzer),
                    gene=KEYWORD(stored=True, scorable=True, commas=True, analyzer=myanalyzer),
                    fdr=TEXT(stored=True),
                    species=TEXT(stored=True),
                    mw=NUMERIC,
                    peptides=NUMERIC,
                    psm=NUMERIC,
                    uniq_peptides=NUMERIC,
                    abun_t1=STORED,
                    abun_t2=STORED,
                    abun_t3=STORED,
                    abun_t4=STORED,
                    abun_t5=STORED,
                    q_value=NUMERIC,
                    pep=NUMERIC
                    )
    return schema


# Function: create Whoosh index
def create_index(postid, condition, file_dict, schema_name, num_pro):
    index_path = 'proteomicsdb/index_dir'

    # make Whoosh index in directory from scratch if does not yet exist
    if not os.listdir(index_path):
        ix = index.create_in(index_path, schema_name)

    # else if there's already an index, just open it and add
    else:
        ix = index.open_dir(index_path)

    # add elements to index
    writer = ix.writer()
    for i in range(num_pro):
        writer.add_document(post_id=postid,
                            condition=condition,
                            accession=list(file_dict.values())[0][i],
                            description=list(file_dict.values())[1][i],
                            gene=list(file_dict.values())[2][i],
                            fdr=list(file_dict.values())[3][i],
                            species=list(file_dict.values())[4][i],
                            mw=list(file_dict.values())[5][i],
                            peptides=list(file_dict.values())[6][i],
                            psm=list(file_dict.values())[7][i],
                            uniq_peptides=list(file_dict.values())[8][i],
                            abun_t1=list(file_dict.values())[9][i],
                            abun_t2=list(file_dict.values())[10][i],
                            abun_t3=list(file_dict.values())[11][i],
                            abun_t4=list(file_dict.values())[12][i],
                            abun_t5=list(file_dict.values())[13][i],
                            q_value=list(file_dict.values())[14][i],
                            pep=list(file_dict.values())[15][i]
                            )

    writer.commit(merge=False)  # "merge=False" means when adding multiple files worth of entries, keep files separate

    pass  # run function but return nothing


# Function: removes documents associated with post when post is deleted
# Doesn't actually delete index contents, only prevents their return when querying
def remove_doc(post_id):
    # open index
    index_path = 'proteomicsdb/index_dir'
    ix = index.open_dir(index_path)
    # delete
    ix.delete_by_term('post_id', post_id)
    pass
