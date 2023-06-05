from flask import Flask, render_template, request, send_file
from weblogo import *
from PIL import Image
app = Flask(__name__)


def convert_jpg_to_svg(infile, outfile):
    # 打开 JPG 图像文件
    image = Image.open(infile).convert('RGBA')
    data = image.load()
    width, height = image.size
    out = open(outfile, "w")
    out.write('<?xml version="1.0" encoding="UTF-8" standalone="no"?>\n')
    out.write('<svg id="svg2" xmlns="http://www.w3.org/2000/svg" version="1.1" \
                width="%(x)i" height="%(y)i" viewBox="0 0 %(x)i %(y)i">\n' % \
              {'x': width, 'y': height})
    
    for y in range(height):
        for x in range(width):
            rgba = data[x, y]
            rgb = '#%02x%02x%02x' % rgba[:3]
            if rgba[3] > 0:
                out.write('<rect width="1" height="1" x="%i" y="%i" fill="%s" \
                    fill-opacity="%.2f" />\n' % (x, y, rgb, rgba[3]/255.0))
    out.write('</svg>\n')
    out.close()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/result', methods=['POST'])
def result():
    user_input = request.form['user_input']
    file_upload = request.files['file_upload']
    data_type = request.form['data_type']
    if user_input != '':
        
        with open('upload.fas', 'w') as f:
            f.write(user_input)
        file = open('upload.fas')
        print('text completelty')
    if file_upload.filename != '':
        file_upload.save('upload.fas')
        file = open('upload.fas')
        print('file completelty')
    image_file = 'result.jpg'
    if(data_type == 'amino_acid'):
        seqs = read_seq_data(file, alphabet=unambiguous_protein_alphabet)
    else:
        seqs = read_seq_data(file)
    file.close()
    print(seqs)
    data = LogoData.from_seqs(seqs)


    options = LogoOptions()
    options.unit_name = 'bits'
    options.number_interval = 1
    options.show_fineprint = False



    format = LogoFormat(data, options)

    jpg = jpeg_formatter(data, format)
    png = png_formatter(data, format)
    #svg = svg_formatter(data, format)
    with open('static/result.jpg', 'wb') as f:
        f.write(jpg)
    with open('static/result.png', 'wb') as f:
        f.write(png)
    #with open('static/result.svg', 'wb') as f:
        #f.write(svg)
    convert_jpg_to_svg('static/result.jpg', 'static/result.svg')
    
    return render_template('result.html', user_input=user_input, image_file=image_file)

@app.route('/download', methods=['POST'])
def download():
    filename = 'static/result.jpg'
    extension = request.form['extension']

    print(extension)
    if extension == '下載為PNG':
        filename = 'static/result.png'

    elif extension == '下載為JPEG':
        filename = 'static/result.jpg'

    elif extension == '下載為SVG':
        filename = 'static/result.svg'


    return send_file(filename, as_attachment=True)

if __name__ == '__main__':
    app.run()
