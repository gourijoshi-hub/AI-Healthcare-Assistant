import google.generativeai as genai

genai.configure(api_key="AIzaSyC7pruXgt3JAfEL79VdWhQn3aSgI5xzYsY")  # paste your key here temporarily

for model in genai.list_models():
    print(model.name)
