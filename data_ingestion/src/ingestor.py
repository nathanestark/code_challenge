import json

class AlreadyRunException(Exception):
    pass

class Ingestor:
    bad_entries = 0
    column_details = {}
    already_run = False

    def __init__(self, file):
        self.file = file


    def ingest_reviews(self):
        if self.already_run: 
            raise AlreadyRunException()
        self.already_run = True

        with open(self.file, 'r', encoding='utf8') as handle:
            for raw in handle:
                j_row = None
                try:
                    j_row = json.loads(raw)
                except:
                    # Record any we couldn't ingest.
                    self.bad_entries += 1
                if j_row is not None:
                    # Keep track of column details
                    for key in j_row.keys():
                        val = j_row[key]
                        if key in self.column_details:
                            column = self.column_details[key]
                            cur = len(val) if type(val) == str else val
                            column['count'] += 1
                            if cur < column['min']:  
                                column['min'] = cur
                            if cur > column['max']:  
                                column['max'] = cur
                        else: 
                            min_max_val = len(val) if type(val) == str else val
                            self.column_details[key] = {
                                'count': 1,
                                'min': min_max_val,
                                'max': min_max_val
                            }

                    yield j_row
