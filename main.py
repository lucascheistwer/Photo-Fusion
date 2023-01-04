from flask import Flask, request, render_template
import secrets
import replicate

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/txttoimg', methods=['GET', 'POST'])
def generate_txt2img():
    text = request.form['text']
    model = replicate.models.get("stability-ai/stable-diffusion")
    version = model.versions.get("f178fa7a1ae43a9a9af01b833b9d2ecf97b1bcb0acfd2dc5dd04895e042863f1")
    image_url = version.predict(prompt=text, num_outputs=3, num_interference_steps=50)
    return render_template('image.html', image1=image_url[0], image2=image_url[1], image3=image_url[2])

@app.route('/imgtoimg', methods=['GET', 'POST'])
def generate_img2img():
    neutral = request.form['neutral']
    target = request.form['target']
    file = request.files['file']
    file_url = 'static/' + secrets.token_hex(16) + '.jpg'
    file.save(file_url)
    model = replicate.models.get("orpatashnik/styleclip")
    version = model.versions.get("7af9a66f36f97fee2fece7dcc927551a951f0022cbdd23747b9212f23fc17021")
    image_url = version.predict(input=open(file_url, "rb"), neutral=neutral, target=target)
    return render_template('image.html', image_url=image_url)

if __name__ == '__main__':
    app.run()