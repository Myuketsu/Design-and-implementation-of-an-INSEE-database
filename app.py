from dash import Dash, html, page_container
from dash_bootstrap_components import themes, icons
import dash_mantine_components as dmc

from pages.menu.sidebar import get_sidebar

app = Dash(
    __name__,
    use_pages=True,
    prevent_initial_callbacks=True,
    external_stylesheets=[themes.PULSE, icons.BOOTSTRAP],
    suppress_callback_exceptions=True
)

app.title = 'BDA'
app._favicon = './pictures/database.svg'

def get_header(height: int) -> dmc.Header:
    return dmc.Header(
        dmc.Text(
            'Bases de Données Avancées : Mini-Projet SQL',
            variant='gradient',
            gradient={'from': '#343a40', 'to': 'red', 'deg': 45}
        ),
        id='app_title',
        fixed=True,
        height=height,
        p=25
    )

header_height: int = 70
sidebar_base_width: int = 72

app.layout = html.Div(
    [
        get_header(header_height),
        get_sidebar(sidebar_base_width),
        html.Div(
            page_container.children,
            id='page_content',
            style={
                'margin-top': header_height,
                'margin-left': sidebar_base_width,
                'max-width': f'calc(100% - {sidebar_base_width}px)'
            }
        )
    ],
    id='layout'
)

if __name__ == '__main__':
    app.run(debug=True)