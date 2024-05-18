from .menu import _menu_show_loading_initial, _menu_show_loading_splash, _menu_show_main_menu, _menu_show_exit

menu_show_loading_initial = _menu_show_loading_initial
menu_show_loading_splash = _menu_show_loading_splash
menu_show_main_menu = _menu_show_main_menu
menu_show_exit = _menu_show_exit

from .ui_battle import _menu_show_battle

menu_show_battle = _menu_show_battle

from .ui_debug import _menu_show_debug_test, _menu_show_debug_battle

menu_show_debug_test = _menu_show_debug_test
menu_show_debug_battle = _menu_show_debug_battle

from .ui_user import _menu_show_login, _menu_show_register, _menu_show_logout

menu_show_login = _menu_show_login
menu_show_register = _menu_show_register
menu_show_logout = _menu_show_logout
