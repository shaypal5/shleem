"""MongoDB-related utilities used by the shleem package."""

import csv

from strct.dicts import flatten_dict
from bson.json_util import (
    dumps,
    loads,
)


def dump_document_cursor_to_csv(doc_cursor, file_path, fieldnames=None,
                                missing_val=None, flatten=False):
    """Writes documents in a pymongo cursor into a csv file.

    Documents are dumped in the order they are returned from the cursor.

    Arguments
    ---------
    doc_cursor : pymongo.cursor.Cursor
        A pymongo document cursor returned by commands like find or aggregate.
    file_path : str
        The full path of the file into which cursor documents are dumped.
    fieldnames : sequence, optional
        The list of field names used as headers of the resulting csv file. If
        not given, the lexicographically-sorted field names of the first
        document in the cursor are used. Fields only found in subsequent
        documents will be ignored, while fields missing in subsequent documents
        will be filled with the given missing value string parameter.
    missing_val : str, optional
        The value used to fill missing fields in documents. Defaults to "NA".
    flatten : bool, optional
        If set to True, documents are flattened to dicts of depth one before
        writing them to file. Defaults to False.
    """
    def doc_trans(doc): return doc
    if missing_val is None:
        missing_val = "NA"
    if flatten:
        def doc_trans(doc): return flatten_dict(
            dict_obj=doc, separator='.', flatten_lists=True)
    first_doc = None
    if fieldnames is None:
        first_doc = doc_cursor.next()
        fieldnames = sorted(list(doc_trans(first_doc).keys()))
    with open(file_path, 'w+') as file_obj:
        writer = csv.DictWriter(file_obj, fieldnames, restval=missing_val,
                                extrasaction='ignore', dialect='excel')
        writer.writeheader()
        if first_doc:
            writer.writerow(doc_trans(first_doc))
            print(doc_trans(first_doc))
        for document in doc_cursor:
            writer.writerow(doc_trans(document))


def dump_document_cursor_to_json(doc_cursor, file_path):
    """Writes documents in a pymongo cursor into a json file.

    Arguments
    ---------
    doc_cursor : pymongo.cursor.Cursor
        A pymongo document cursor returned by commands like find or aggregate.
    file_path : str
        The full path of the file into which cursor documents are dumped.
    """
    with open(file_path, 'w+') as dump_json:
        dump_json.write('[\n')
        dump_json.write(dumps(doc_cursor.next()))
        for doc in doc_cursor:
            dump_json.write(',\n')
            dump_json.write(dumps(doc))
        dump_json.write('\n]')


def load_document_iterator_from_json(file_path):
    """Creates a lazy iterator over documents from a json file.

    Arguments
    ---------
    file_path : str
        The full path of the file from which documents are read.
    """
    with open(file_path, 'r') as load_json:
        line = load_json.readline()
        while line:
            if line not in ('[\n', ']'):  # ignore start and end of array
                try:  # skip trailing , and one \n
                    yield loads(line[:-2])
                except JSONDecodeError:  # last line has no , so just \n
                    yield loads(line[:-1])
            line = load_json.readline()
        raise StopIteration
