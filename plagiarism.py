from flask import Flask, render_template, request
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

app = Flask(__name__)

def detect_plagiarism(documents):
    # Vectorize the documents
    vectorizer = TfidfVectorizer()
    tfidf_matrix = vectorizer.fit_transform(documents)
    # Calculate cosine similarity
    similarity_matrix = cosine_similarity(tfidf_matrix)
    similarity_df = pd.DataFrame(similarity_matrix, 
                                  columns=[f'Doc {i+1}' for i in range(len(documents))],
                                  index=[f'Doc {i+1}' for i in range(len(documents))])
    return similarity_df

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        files = request.files.getlist('files')
        documents = []
        for file in files:
            if file.filename.endswith('.txt'):
                documents.append(file.read().decode('utf-8'))
        
        if documents:
            similarity_report = detect_plagiarism(documents)
            return render_template('report.html', tables=[similarity_report.to_html(classes='data')])
    
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
