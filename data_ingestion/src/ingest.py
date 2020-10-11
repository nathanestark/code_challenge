import sys
import json
import base64

from database.review import Review
from database.init import init, get_session
from ingestor import Ingestor, AlreadyRunException

# Process arguments
required_args = [arg for arg in sys.argv[1:] if not arg.startswith('-')]
optional_args = [arg for arg in sys.argv[1:] if arg.startswith('-')]

usage = "\r\n\tUSAGE: py ingest.py <data file> <sql connection | -statistics>"

all_optional = ['-s', '-statistics']

bad_options = [arg for arg in optional_args if arg not in all_optional]
if len(bad_options) > 0: 
    print("Unknown optional argument '"+bad_options[0]+"':" + usage)
    exit(1)

statisticsOnly = "-s" in optional_args or "-statistics" in optional_args

if len(required_args) == 0:
    print("Missing argument 'data file':"+usage) 
    exit(1)
# technically.. this is only required if we are actually loading the DB
if not statisticsOnly and len(required_args) == 1:
    print("Missing argument 'sql connection':"+usage) 
    exit(1)


dataFile = required_args[0]


# Begin our ingestion

ingestor = Ingestor(dataFile)

if not statisticsOnly:
    init(required_args[1])

count = 0
inserts = []
for review in ingestor.ingest_reviews(): 
    if review is None: 
        break
    count += 1
    if count % 10000 == 0: 
        print("Processing Record " + str(count) + "...")
    if not statisticsOnly:
        # Add a new column for continuation tokens
        continuation_token = review['date'] + review['review_id']
        sb64_continuation_token = base64.b64encode(continuation_token.encode("ascii")).decode('ascii')
        review['continuation_token'] = sb64_continuation_token
        # Bulk insert 100 at a time.
        inserts.append(review)
        if len(inserts) == 100:
            session = get_session()
            try:
                session.bulk_insert_mappings(Review, inserts)
                inserts = []
                session.commit()
            except:
                session.rollback()
                raise
            finally:
                session.close()

if statisticsOnly:
    print("Bad Entries", ingestor.bad_entries)
    print("Columns", json.dumps(ingestor.column_details, indent=4))
    
print(str(count) + " entries ingested.")