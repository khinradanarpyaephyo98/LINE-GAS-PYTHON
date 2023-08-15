from flask import Flask, render_template,request,jsonify

app = Flask(__name__)
 
@app.route('/',methods=['GET'])
def home():
   return render_template('home.html')
   

@app.route('/result',methods=['POST','GET'])
def result():
   output = request.form.to_dict()
   question = output["question"]
   print(question)
   return render_template('home.html',message=question)

@app.route('/line',methods=['GET'])
def line():
   data = {
        'message': 'This is the message from the API route!'
    }
   return jsonify(data)
   

if __name__ == '__main__':
   app.run()