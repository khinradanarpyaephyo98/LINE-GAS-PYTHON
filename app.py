from flask import Flask, render_template,request
app = Flask(__name__)
 
@app.route('/')
def home():
   return render_template('home.html')

@app.route('/result',methods=['POST','GET'])
def result():
   output = request.form.to_dict()
   question = output["question"]
   print(question)
   return render_template('home.html')

if __name__ == '__main__':
   app.run()