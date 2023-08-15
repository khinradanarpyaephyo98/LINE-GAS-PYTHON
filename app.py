from flask import Flask, render_template,request
app = Flask(__name__)
 
@app.route('/',methods=['GET'])
def home():
   print("linwwe")
   message="limb"
   return render_template('home.html',message=message)

@app.route('/result',methods=['POST','GET'])
def result():
   output = request.form.to_dict()
   question = output["question"]
   print(question)
   return render_template('home.html',message=question)

@app.route('/line',methods=['GET'])
def line():
   print("line")
   return render_template('home.html')

if __name__ == '__main__':
   app.run()