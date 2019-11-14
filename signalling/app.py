import dash
import dash_table as dt
import dash_html_components as html

app = dash.Dash(__name__)

server = app.server

app.title = "Transportation Engineer"
app.layout = html.Div(
    [
        html.H2("Signalling"),
        dt.DataTable(
            id="table",
            columns=[{"name": i, "id": i} for i in df.columns],
            data=df.to_dict("records"),
        ),
    ]
)

if __name__ == "__main__":
    app.run_server(debug=True, port=8888)
