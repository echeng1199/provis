# pull values from .env file in cmd line to be used for program for S3

import os

S3_BUCKET = os.environ.get("S3_BUCKET") # this is not being accessed
S3_KEY = os.environ.get("S3_KEY") # these two as well, if I don't specify it "aws configure" in the cmd line
S3_SECRET_ACCESS_KEY = os.environ.get("S3_SECRET_ACCESS_KEY")