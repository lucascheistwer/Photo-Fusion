from flask import Flask, request, render_template
import replicate

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('index.html')

@app.route('/image', methods=['GET', 'POST'])
def generate_image():
    text = request.form['text']
    model = replicate.models.get("stability-ai/stable-diffusion")
    version = model.versions.get("f178fa7a1ae43a9a9af01b833b9d2ecf97b1bcb0acfd2dc5dd04895e042863f1")
    image_url = version.predict(prompt=text)
    return render_template('image.html', image_url=image_url[0])

if __name__ == '__main__':
    app.run()