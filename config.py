import os, re, time

id_pattern = re.compile(r'^.\d+$')


class Config:


    # Database Config 
    DATABASE_URI = os.environ.get("DATABASE_URI", "mongodb+srv://ROKU:ROKU@cluster0.nxjre0s.mongodb.net/?retryWrites=true&w=majority") # ⚠️ Required
    DATABASE_NAME = os.environ.get("DATABASE_NAME", "Test")
    COLLECTION_NAME = os.environ.get('COLLECTION_NAME', 'Data')
    USERDATA = os.environ.get('USERDATA', 'USER_DATA')
    FORCE_SUB = os.environ.get('FORCE_SUB', '-1002093365834') #
    AUTH_CHANNEL = int(FORCE_SUB) if FORCE_SUB and id_pattern.search(
    FORCE_SUB) else None 
    LOG_CHANNEL = int(os.environ.get("LOG_CHANNEL", "-1002093365834"))
