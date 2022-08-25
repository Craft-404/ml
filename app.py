from urllib import request
import flask
import requests # to get image from the web
import shutil 
import read


app = flask.Flask(__name__)

def download_img(url):
	r = requests.get(url, stream = True)

# Check if the image was retrieved successfully
	if r.status_code == 200:
		# Set decode_content value to True, otherwise the downloaded image file's size will be zero.
		r.raw.decode_content = True
		# img = Image.open(r.raw)
		# img.save('greenland_02a.png')
		# Open a local file with wb ( write binary ) permission.
		with open("scan123.jpg",'wb') as f:
			f.write(r.content)
			
		print('Image sucessfully Downloaded')
	else:
		print('Image Couldn\'t be retreived')


@app.route('/tenMS' , methods=['POST'])
def read_ten_ms():
	data = flask.request.json
	download_img(data['url'])
	res = read.reader("scan123.jpg")
	if(res==-1):
		res = {"status : error reading the doc"}
		return flask.jsonify.status_code(404)
	return flask.jsonify(res).status_code(200)


if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')