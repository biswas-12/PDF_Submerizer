# -*- coding: utf-8 -*-
"""pdf_submerizer.ipynb

Automatically generated by Colab.

Original file is located at
    https://colab.research.google.com/drive/1gjrIWAFEprtj-PnM2wcgKW2KTBiZzd5b
"""

!pip install google-cloud-aiplatform PyPDF2 ratelimit backoff --upgrade --quiet --user

from google.colab import auth
auth.authenticate_user()

import vertexai

PROJECT_ID = "ENTER PROJECT ID"
vertexai.init(project=PROJECT_ID, location="ENTER LOCATION")

import re
import urllib
import warnings
from pathlib import Path

import backoff
import pandas as pd
import PyPDF2
import ratelimit
from google.api_core import exceptions

from vertexai.language_models import TextGenerationModel

warnings.filterwarnings("ignore")

generation_model = TextGenerationModel.from_pretrained("text-bison@002")

# Define a folder to store the files
data_folder = "data"
Path(data_folder).mkdir(parents=True, exist_ok=True)

# Define a pdf link to download and place to store the download file
#pdf_url = "https://services.google.com/fh/files/misc/practitioners_guide_to_mlops_whitepaper.pdf"
pdf_url =  "https://www.franklinboe.org/cms/lib/NJ01000817/Centricity/Domain/699/PFC%20ebook.pdf"
pdf_file = Path(data_folder, pdf_url.split("/")[-1])

# Download the file using `urllib` library
urllib.request.urlretrieve(pdf_url, pdf_file)

ls

# Read the PDF file and create a list of pages
reader = PyPDF2.PdfReader(pdf_file)
pages = reader.pages

# Print pages from the pdf
for i in range(570):
    text = pages[i].extract_text().strip()

#text contains only the text from page 2
#print(f"Page {i}: {text} \n\n")


# Entry string that contains the extacted text
print(f"There are {len(text)} characters in this {i} pages of the pdf")

prompt_template = """
    Write a concise summary of the following text.
    Return your response in bullet points which covers the key points of the text.

    ```{text}```

    BULLET POINT SUMMARY:
"""

# Define the prompt using the prompt template
prompt = prompt_template.format(text=text[:30000])

# Use the model to summarize the text using the prompt
summary = generation_model.predict(prompt=prompt, max_output_tokens=1024)

summary
