import utils.data_loader as data_loader

from app_instance import app
from components.layout import layout
from components import figures

app.layout = layout

if __name__ == '__main__':
    app.run(debug=True)