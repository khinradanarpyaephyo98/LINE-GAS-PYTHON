from flask import Flask, render_template,request,jsonify
import os
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
# Embeddings
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains.question_answering import load_qa_chain
from langchain import HuggingFaceHub


documents = []
for file in os.listdir('docs'):
   if file.endswith('.pdf'):
      pdf_path = './docs/' + file
      loader = PyPDFLoader(pdf_path)
      documents.extend(loader.load())

print("Number of documents :",len(documents))

text_splitter = CharacterTextSplitter(chunk_size=500, chunk_overlap=10)
documents = text_splitter.split_documents(documents)

embeddings = HuggingFaceEmbeddings()
db = FAISS.from_documents(documents, embeddings)

os.environ["HUGGINGFACEHUB_API_TOKEN"] ="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"
llm=HuggingFaceHub(repo_id="google/flan-t5-large", model_kwargs={"temperature":0, "max_length":512})
chain = load_qa_chain(llm, chain_type="stuff")


app = Flask(__name__)
 
@app.route('/',methods=['GET'])
def home():  
   return render_template('home.html')

#for line api test
@app.route('/reply', methods=['POST','GET'])
def reply():
    data = request.get_json() # msg from the GAS
    msg_from_gas = data.get('message')
    print(" Received msg from the GAS : ",msg_from_gas)
    docs = db.similarity_search(msg_from_gas)  # call AI model
    print("Answer :",chain.run(input_documents=docs, question=msg_from_gas),"\n")
    global answer1
    answer1=chain.run(input_documents=docs, question=msg_from_gas)
    return answer1

#for browser test
@app.route('/result',methods=['POST','GET'])
def result():
   output = request.form.to_dict()
   query = output["question"]
   print( query)
   docs = db.similarity_search(query)
   print("Answer :",chain.run(input_documents=docs, question=query),"\n")
   global answer2
   answer2=chain.run(input_documents=docs, question=query)
   return render_template('home.html',answer=answer2,question=query)


@app.route('/check_reply',methods=['GET','POST'])
def check_reply():
   data = {
        'answer1': answer1
    }
   return jsonify(data)


@app.route('/check_result',methods=['GET','POST'])
def check_result():
   data = {
        'answer2': answer2
    }
   return jsonify(data)  


if __name__ == '__main__':
   app.run()
   
