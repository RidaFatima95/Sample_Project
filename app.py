
# coding: utf-8

# In[ ]:


from flask import Flask, jsonify, send_file, request
from random import randint
from pickle import load
from keras.models import load_model
from keras.preprocessing.sequence import pad_sequences
from werkzeug.exceptions import BadRequest
from werkzeug.utils import secure_filename

app = Flask(__name__)

def load_doc(filename):
    # open the file as read only
    #file = open(filename, 'r')
    file= request.files.get('file')
    filename1 = secure_filename(file.filename)
    # read all text
    text = filename1.read()
    input_filepath = os.path.join('./images/', filename)  
    output_filepath = os.path.join('/output/', filename)
    file.save(input_filepath)
    # close the file
    #file.close()
    return text

#def load_model():
  #  """Load and return the model"""
    # TODO: INSERT CODE
    # return model

#model = load_model('model.h5')



# The request method is POST (this method enables your to send arbitrary data to the endpoint in the 
#request body, including images, JSON, encoded-data, etc.)
@app.route('/')
def running():
    return "Flask is running"

@app.route('/', methods=["POST"])    
#def evaluate():
 #   """"Preprocessing the data and evaluate the model""""
    # TODO: data/input preprocessing
    # load cleaned text sequences
    
    
def generate_seq(model, tokenizer, seq_length, seed_text, n_words):
    result = list()
    in_text = seed_text
    # generate a fixed number of words
    for _ in range(n_words):
        # encode the text as integer
        encoded = tokenizer.texts_to_sequences([in_text])[0]
        # truncate sequences to a fixed length
        encoded = pad_sequences([encoded], maxlen=seq_length, truncating='pre')
        # predict probabilities for each word
        yhat = model.predict_classes(encoded, verbose=0)
        # map predicted word index to word
        out_word = ''
        for word, index in tokenizer.word_index.items():
            if index == yhat:
                out_word = word
                break
            # append to input
        in_text += ' ' + out_word
        result.append(out_word)
    return ' '.join(result)

    # eg: request.files.get('file')
    # eg: request.args.get('style')
    # eg: request.form.get('model_name')

    # TODO: model evaluation
    # eg: prediction = model.eval()

    # TODO: return prediction
    # eg: return jsonify({'score': 0.95})



in_filename = 'republic_sequences.txt'
doc = load_doc(in_filename)
lines = doc.split('\n')
seq_length = len(lines[0].split()) - 1   

# you can then reference this model object in evaluate function/handler
model = load_model('model.h5')
 
# load the tokenizer
#tokenizer = load(open('tokenizer.pkl', 'rb'))
fname='tokenizer.pkl'
t=request.files.get('file')
filename2 = secure_filename(t.fname)
tokenizer = load(filename2)

 
# select a seed text
seed_text = lines[randint(0,len(lines))]
print(seed_text + '\n')
 
# generate new text
generated = generate_seq(model, tokenizer, seq_length, seed_text, 50)
print(generated)

# In[ ]:



# The following is for running command `python app.py` in local development, not required for serving on FloydHub.
if __name__ == "__main__":
    print("* Starting web server... please wait until server has fully started")
    app.run(host='0.0.0.0', threaded=False)

