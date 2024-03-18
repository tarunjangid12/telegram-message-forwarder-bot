import os, re, time

id_pattern = re.compile(r'^.\d+$')


class Config:

    # Database Config 
    DATABASE_URI = os.environ.get("DATABASE_URI", "mongodb+srv://ROKU:ROKU@cluster0.nxjre0s.mongodb.net/?retryWrites=true&w=majority") # ⚠️ Required
    DATABASE_NAME = os.environ.get("DATABASE_NAME", "Test")
