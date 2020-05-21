import os
import json
import jinja2

import pdfkit
from sass import compile

# Access jinja2 enviroment with the PUG plugin
ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(['template']),
    extensions=['pypugjs.ext.jinja.PyPugJSExtension'],
)

# Path to compile directory and template directory
COMPILED_DIR = f'.{os.path.sep}compiled{os.path.sep}'
TEMPLATE_DIR = f'.{os.path.sep}template{os.path.sep}'

def compile_sass(input_file, output_file):
    """Compile all found Sass/SCSS files to CSS files"""
    dir_name = os.path.dirname(output_file)
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
    with open(output_file, 'w+') as file:
        css = compile(
            filename=input_file,
            output_style='compressed',
            include_paths=input_file
        )
        file.write(css)


if __name__ == '__main__':
    
    # Read settings from json file.
    with open('./cv.json','r+') as setting_file:
        settings = json.load(setting_file)

    # Compile SASS files to CSS.
    compile_sass(TEMPLATE_DIR + 'style.sass', COMPILED_DIR + 'style.css')
    
    # Convert pug files to one html file
    with open(COMPILED_DIR + 'cv.html', 'w+') as file:
        template = ENV.get_template('cv.pug')
        file.write(template.render(**settings))

    # Convert html file to pdf
    pdfkit.from_file(COMPILED_DIR + 'cv.html', 'cv.pdf')
