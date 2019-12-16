import dash
from signalling.app.setup import app_init as signalling_app_init

app = dash.Dash(__name__)
server = app.server

app.title = "Transportation Engineer"

signalling_app_init(app)

if __name__ == "__main__":
    app.run_server(debug=True, port=8888)
