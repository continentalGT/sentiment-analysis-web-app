from transformers import pipeline

def check_sentiment(text):

    pipe = pipeline('sentiment-analysis',model='nlptown/bert-base-multilingual-uncased-sentiment') # Creating a pipeline object for sentiment analysis
    result = pipe(text) # Passing the input text to the pipeline object
    return f'''the sentime of the text is {result[0]['label']} with confidence {result[0]['score']}''' # Returning the sentiment of the text


print(check_sentiment("I am very very happy")) # Calling the function with a positive text