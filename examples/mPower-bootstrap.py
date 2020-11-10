import synapseclient
import json

syn = synapseclient.login()

# QUERY THE mPower PROJECT (syn4993293) FOR ALL OF THE TABLES
tables = syn.getChildren('syn4993293', ['table'])
tables = [t for t in tables if t['name'].startswith('Sample')]

# DOWNLOAD 20 OBSERVATIONS FROM EACH OF THE TABLES (RESULTS ARE CACHED LOCALLY)
allData = {table['name']: syn.tableQuery('SELECT * FROM %s LIMIT 20' % table['id']) for table in tables}

# EXTRACT THE TAPPING ACTIVITY TABLE AS A DATA FRAME AND LOOK AT THE FIRST TWO OBSERVATIONS IN TAPPING TABLE
df = allData['Sample Tapping Activity'].asDataFrame()
print(df.head(2))

# FOR TABLES WITH COLUMNS THAT CONTAIN FILES, WE CAN BULK DOWNLOAD THE FILES AND STORE A MAPPING
# THE VALUE IN THE TABLE ABOVE IS CALLED A fileHandleId WHICH REFERENCES A FILE THAT CAN BE
# ACCESSED PROGRAMMATICALLY GET THE FILES THAT CONTAIN SCREEN TAP SAMPLES FROM THE TAPPING EXERCISE
# THIS CACHES THE RETRIEVED FILES AS WELL
tapMap = syn.downloadTableColumns(allData['Sample Tapping Activity'], "tapping_results.json.TappingSamples")

# THE NAMES OF tapMap ARE THE FILEHANDLES STORED IN THE COLUMN "tapping_results.json.TappingSamples" 
# SO CAN ASSOCIATE WITH APPROPRIATE METADATA THESE ARE JSON FILES, SO READ THEM INTO MEMORY
tapResults = {handle: json.load(open(f)) for handle, f in tapMap.items()}
