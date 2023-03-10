from flask import Flask, render_template, request, jsonify, make_response
from dbsetup import create_connection, select_all_items, update_item
from flask_cors import CORS, cross_origin
from pusher import Pusher
import simplejson
import qrcode
from PIL import Image

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'

# configure pusher object
pusher = Pusher(
app_id='1565939',
key='12ea89a2e687c7d8aa06',
secret='d01f3dfe2bf8e9dcf303',
cluster='us2',
ssl=True)

database = "./pythonsqlite.db"
conn = create_connection(database)
c = conn.cursor()

# Image in center of QR Code
Logo_link = './static/assets/nfl256.png'
logo = Image.open(Logo_link)

# Taking base width
basewidth = 50

# adjust image size
wpercent = (basewidth/float(logo.size[0]))
hsize = int((float(logo.size[1])*float(wpercent)))
logo = logo.resize((basewidth, hsize), Image.ANTIALIAS)
QRcode = qrcode.QRCode(
    error_correction=qrcode.constants.ERROR_CORRECT_H
)

# taking url or text
# url = 'https://www.nfl.com/plus/'
url = 'https://www.figma.com/proto/ltx1jEM82pTnmPqdRwUPKc/BOTB_2023'
# adding URL or text to QRcode
QRcode.add_data(url)
 
# generating QR code
QRcode.make()
 
# taking color name from user
QRcolor = 'Blue'
 
# adding color to QR code
QRimg = QRcode.make_image(
    fill_color=QRcolor, back_color="black").convert('RGB')
 
# set size of QR code
pos = ((QRimg.size[0] - logo.size[0]) // 2,
       (QRimg.size[1] - logo.size[1]) // 2)
QRimg.paste(logo, pos)
 
# save the QR code generated
QRimg.save('./static/assets/nfl_QR.png')
 
# print('QR code generated!')

def main():
    global conn, c

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/admin')
def admin():
    return render_template('admin.html')

@app.route('/vote', methods=['POST'])
def vote():
    data = simplejson.loads(request.data)
    update_item(c, [data['member']])
    output = select_all_items(c, [data['member']])
    pusher.trigger(u'poll', u'vote', output)
    return request.data

if __name__ == '__main__':
    main()
    app.run(debug=True)