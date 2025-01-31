class BibtexObject:

    supported_cff_versions = ['1.0.3', '1.1.0']
    supported_bibtex_props = ['author', 'doi', 'month', 'title', 'url', 'year']

    def __init__(self, cff_object, reference='YourReferenceHere', initialize_empty=False):
        self.cff_object = cff_object
        self.reference = reference
        self.author = None
        self.doi = None
        self.month = None
        self.title = None
        self.url = None
        self.year = None
        if initialize_empty:
            # clause for testing purposes
            pass
        else:
            self.check_cff_object().add_all()

    def __str__(self):
        items = [item for item in [self.author,
                                   self.title,
                                   self.month,
                                   self.year,
                                   self.doi,
                                   self.url] if item is not None]
        s = ',\n'.join(items)
        return '@misc{' + self.reference + ',\n' + s + '\n}\n'

    def add_all(self):
        self.add_author()   \
            .add_doi()      \
            .add_month()    \
            .add_title()    \
            .add_url()      \
            .add_year()
        return self

    def add_author(self):
        if 'authors' in self.cff_object.keys():
            fullnames = []
            for author in self.cff_object['authors']:
                keys = author.keys()
                nameparts = [
                    author['given-names'] if 'given-names' in keys else None,
                    author['name-particle'] if 'name-particle' in keys else None,
                    author['family-names'] if 'family-names' in keys else None,
                    author['name-suffix'] if 'name-suffix' in keys else None
                ]
                fullname = ' '.join([namepart for namepart in nameparts if namepart is not None])
                if fullname == '' and 'alias' in keys and author['alias'] is not None:
                    fullname = author['alias'] if author['alias'] != '' else None
                if fullname is not None and fullname != '':
                    fullnames.append(fullname)
            self.author = 'author = {' + ' and '.join(fullnames) + '}'
        return self

    def add_doi(self):
        version = self.cff_object['cff-version']
        if version in ['1.0.3', '1.1.0']:
            if 'doi' in self.cff_object.keys():
                self.doi = 'doi = {' + self.cff_object['doi'] + '}'

        if version in ['1.1.0']:
            if 'identifiers' in self.cff_object.keys():
                identifiers = self.cff_object['identifiers']
                for identifier in identifiers:
                    if identifier['type'] == 'doi':
                        self.doi = 'doi = {' + identifier['value'] + '}'
                        break
        return self

    def add_month(self):
        if 'date-released' in self.cff_object.keys():
            self.month = 'month = {' + str(self.cff_object['date-released'].month) + '}'
        return self

    def add_title(self):
        if 'title' in self.cff_object.keys():
            self.title = 'title = {' + self.cff_object['title'] + '}'
        return self

    def add_url(self):
        if 'repository-code' in self.cff_object.keys():
            self.url = 'url = {' + self.cff_object['repository-code'] + '}'
        return self

    def add_year(self):
        if 'date-released' in self.cff_object.keys():
            self.year = 'year = {' + str(self.cff_object['date-released'].year) + '}'
        return self

    def check_cff_object(self):
        if not isinstance(self.cff_object, dict):
            raise ValueError('Expected cff_object to be of type \'dict\'.')
        elif 'cff-version' not in self.cff_object.keys():
            raise ValueError('Missing key "cff-version" in CITATION.cff file.')
        elif self.cff_object['cff-version'] not in BibtexObject.supported_cff_versions:
            raise ValueError('\'cff-version\': \'{}\' isn\'t a supported version.'
                             .format(self.cff_object['cff-version']))
        else:
            return self

    def print(self):
        return self.__str__()

