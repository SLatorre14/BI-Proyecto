from flask import Flask, request, render_template, send_file, make_response
import os
import joblib
from functions import lecturaDatos, limpiezayTokenDatos, normalizacion, seleccion, pipeLimpieza
import pandas as pd
import csv
import shutil
import io

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
PROCESSED_FOLDER = 'processed'

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['PROCESSED_FOLDER'] = PROCESSED_FOLDER

@app.route('/')
def index():
    return render_template('upload.html')

@app.route('/process', methods=['POST'])
def process_document():
    uploaded_file = request.files['document']
    if uploaded_file:
        # Save the uploaded document
        document_path = os.path.join(app.config['UPLOAD_FOLDER'], uploaded_file.filename)
        uploaded_file.save(document_path)

        # Process the document (You need to implement your processing pipeline here)
        # Replace this with your actual processing code
        response = ""
        processed_document = process_pipeline(uploaded_file.filename)
        df = pd.read_csv(processed_document, header=None)

       
        for row_index, row in df.iterrows():
            rows =  f'Texto {row_index+1} \n'
            for col_index, value in enumerate(row):
                if col_index == 0:  # Check if the col_index is 0
                    modified_value = 3
                elif col_index == 1:  # Check if the col_index is 1
                    modified_value = 4
                elif col_index == 2:  # Check if the col_index is 2
                    modified_value = 5
                rows += f'Probabilidad de etiqueta {modified_value}: {float(value)} \n'
            response += rows
            response += "------------------------------------- \n"
    
        # Return the processed document to the user
        return render_template('upload.html', result=response)
    

def process_pipeline(filename):
    

  
        # Process the document using the loaded pipeline
    data=pd.read_excel("./uploads/" + filename)
    processed_document = pipeLimpieza.fit_transform(data)
    pipe_predict = joblib.load("pipePredict.joblib")
    final = pipe_predict.predict_proba(processed_document["palabras"])

    # Save the processed document
    

    # Create a CSV file in memory
    
    df = pd.DataFrame(final)
    
    df.to_csv('myarray.csv', index=False, header=False)
    return "myarray.csv"
 

if __name__ == '__main__':
    app.run(debug=True)
