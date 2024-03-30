from dash import page_registry
import dash_mantine_components as dmc
from dash_iconify import DashIconify

CATEGORIES = {
    'Requêtes': {'icon': 'bi:database-down'}
}

def get_icon(icon: str, height: int=20, color: str='#343a40') -> DashIconify:
    return DashIconify(icon=icon, height=height, color=color)

def get_nav_link(label: str, path: str, icon: str) -> dmc.NavLink:
    return dmc.NavLink(
        label=label,
        icon=None if icon is None else get_icon(icon),
        href=path,
        style={'white-space': 'nowrap'}
    )

def get_category(label: str, children: list[dmc.NavLink]) -> dmc.NavLink:
    return dmc.NavLink(
        label=label,
        icon=None if CATEGORIES.get(label) is None else get_icon(CATEGORIES.get(label).get('icon')),
        style={'white-space': 'nowrap'},
        childrenOffset=28,
        children=children
    )

def get_sidebar(base_width: int) -> dmc.Navbar:
    nav_links: list[dmc.NavLink] = []
    categories: dict[str, list[dmc.NavLink]] = {}

    for page in page_registry.values():
        if page.get('category_name') is not None:

            if categories.get(page.get('category_name')) is None:
                categories[page.get('category_name')] = []
            
            categories[page.get('category_name')].append(
                get_nav_link(page.get('name'), page.get('path'), page.get('icon'))
            )
            continue

        nav_links.append(
            get_nav_link(page.get('name'), page.get('path'), page.get('icon'))
        )
    
    for category_name, values in categories.items():
        nav_links.append(get_category(category_name, values))

    return dmc.Navbar(
        children=nav_links,
        id='sidebar',
        fixed=True,
        width={'base': base_width},
        height='100vh',
        p='sm',
        style={
            'overflow': 'hidden',
            'transition': 'width 0.2s ease-in-out'
        }
    )