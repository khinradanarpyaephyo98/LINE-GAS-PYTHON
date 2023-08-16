from flask import Flask, render_template,request,jsonify
import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
# Embeddings
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain import HuggingFaceHub



app = Flask(__name__)
 
@app.route('/',methods=['GET'])
def home():
   
   return render_template('home.html')

@app.route('/reply',methods=['POST','GET'])
def reply():
   output = request.form.to_dict()
   query = output["question"]
   print( query)

   documents = []
   for file in os.listdir('docs'):
      if file.endswith('.pdf'):
         pdf_path = './docs/' + file
         loader = PyPDFLoader(pdf_path)
         documents.extend(loader.load())

   print("Number of documents :",len(documents))


   text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=10)
   documents = text_splitter.split_documents(documents)

   embeddings = HuggingFaceEmbeddings()
   db = FAISS.from_documents(documents, embeddings)

   os.environ["HUGGINGFACEHUB_API_TOKEN"] ="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"
   llm=HuggingFaceHub(repo_id="google/flan-t5-large", model_kwargs={"temperature":0, "max_length":512})
   chain = load_qa_chain(llm, chain_type="stuff")

   
   docs = db.similarity_search(query)
   print("Answer :",chain.run(input_documents=docs, question=query),"\n")
   answer=chain.run(input_documents=docs, question=query)
   return render_template('home.html',answer=answer,question=query)

    
   

@app.route('/result',methods=['POST','GET'])
def result():
   output = request.form.to_dict()
   question = output["question"]
   print(question)
   return render_template('home.html',question=question)

@app.route('/line',methods=['GET'])
def line():
   
   data = {
        'message': 'This is the message from the API route!'
    }
   return jsonify(data)
   

@app.route('/receive')
def display_message():
    message = "Hello, this is the message from the /receive route!"
    return render_template('home.html', message=message)


@app.route('/receive_frm_line', methods=['POST'])
def receive_message():
    data = request.get_json()
    line_msg = data.get('message')
    print(line_msg,"line msg ")
    return render_template('home.html', line_msg=line_msg)



if __name__ == '__main__':
   app.run()