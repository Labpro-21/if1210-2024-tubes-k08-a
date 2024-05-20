from .menu import _menu_show_loading_initial, _menu_show_loading_splash, _menu_show_main_menu, _menu_show_exit

menu_show_loading_initial = _menu_show_loading_initial
menu_show_loading_splash = _menu_show_loading_splash
menu_show_main_menu = _menu_show_main_menu
menu_show_exit = _menu_show_exit

from .ui_arena import _menu_show_arena

menu_show_arena = _menu_show_arena

from .ui_battle import _menu_show_battle

menu_show_battle = _menu_show_battle

from .ui_debug import _menu_show_debug_test, _menu_toggle_coroutines_stats, _menu_show_debug_battle, _menu_show_debug_arena, _menu_show_debug_shop, _menu_show_debug_laboratory

menu_show_debug_test = _menu_show_debug_test
menu_toggle_coroutines_stats = _menu_toggle_coroutines_stats
menu_show_debug_battle = _menu_show_debug_battle
menu_show_debug_arena = _menu_show_debug_arena
menu_show_debug_shop = _menu_show_debug_shop
menu_show_debug_laboratory = _menu_show_debug_laboratory

from .ui_laboratory import _menu_show_laboratory

menu_show_laboratory = _menu_show_laboratory

from .ui_shop import _menu_show_shop

menu_show_shop = _menu_show_shop

from .ui_user import _menu_show_login, _menu_show_register, _menu_show_logout

menu_show_login = _menu_show_login
menu_show_register = _menu_show_register
menu_show_logout = _menu_show_logout
