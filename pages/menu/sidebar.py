from dash import page_registry
import dash_mantine_components as dmc
from dash_iconify import DashIconify

CATEGORIES = {
    'Triggers': {'icon': 'streamline:database-setting'},
    'Plan d\'exécution': {'icon': 'material-symbols:format-list-numbered'}
}

def get_icon(icon: str, height: int=20, color: str='#343a40') -> DashIconify:
    return DashIconify(icon=icon, height=height, color=color)

def get_nav_link(label: str, path: str, icon: str) -> dmc.NavLink:
    return dmc.NavLink(
        label=label,
        icon=None if icon is None else get_icon(icon),
        href=path,
        style={'whiteSpace': 'nowrap'}
    )

def get_category(label: str, children: list[dmc.NavLink]) -> dmc.NavLink:
    return dmc.NavLink(
        label=label,
        icon=None if CATEGORIES.get(label) is None else get_icon(CATEGORIES.get(label).get('icon')),
        style={'whiteSpace': 'nowrap'},
        childrenOffset=28,
        children=children
    )

def get_sidebar(base_width: int) -> dmc.Navbar:
    nav_links: dict[int, dmc.NavLink] = {}
    categories: dict[str, list[tuple[dmc.NavLink, int]]] = {}

    for page in page_registry.values():
        if page.get('category_name') is not None:

            if categories.get(page.get('category_name')) is None:
                categories[page.get('category_name')] = []
            
            categories[page.get('category_name')].append(
                (get_nav_link(page.get('name'), page.get('path'), page.get('icon')), page.get('order'))
            )
            continue

        nav_links[page.get('order')] = get_nav_link(page.get('name'), page.get('path'), page.get('icon'))

    
    for category_name, values in categories.items():
        categorie_links = [value[0] for value in values]
        orders_links = [value[1] for value in values]
        nav_links[min(orders_links)] = get_category(category_name, categorie_links)

    children = [nav_link[1] for nav_link in sorted(nav_links.items())]

    return dmc.Navbar(
        children=children,
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