from flask import Flask, render_template,request,jsonify

app = Flask(__name__)
 
@app.route('/',methods=['GET'])
def home():
   mhm= " mhm"
   mo="88"
   return render_template('home.html',mhm=mhm, mo=mo)
   

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


@app.route('/receive_frm_line', methods=['GET'])
def receive_message():
    data = request.get_json()
    line_msg = data.get('message')
    
    return render_template('home.html', line_msg=line_msg)


if __name__ == '__main__':
   app.run()