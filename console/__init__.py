from time import sleep
import logging
import curses
import locale

def init(stdscr, initmsg = 'openning...',
        logfile = 'log.log'):

    curses.use_default_colors()
    curses.init_pair(1, curses.COLOR_GREEN, -1) # italic
    curses.init_pair(2, curses.COLOR_WHITE, curses.COLOR_CYAN) # underline
    curses.init_pair(3, curses.COLOR_GREEN, curses.COLOR_CYAN) # italic and underline
    stdscr.addstr(initmsg)
    stdscr.refresh()

    from .logger import logger

    logging.basicConfig(filename = logfile,
            level=logging.DEBUG,
            format='%(asctime)s %(levelname)s %(name)-4s %(message)s')

def run(func, argv):
    locale.setlocale(locale.LC_ALL, '')
    curses.wrapper(func, argv)

def default_bindings():
    from .bindings import load_basic_key_bindings, load_default_key_bindings
    from .core.keybinding import Registry, MergedRegistry
    from .ui.confirm_window import load_confirm_prompt_bindings
    from .search import load_search_n_replace_bindings
    from .ui.menu_window import load_menu_bindings
    from .ui.textinput_window import load_textinput_bindings
    from .ui.message_window import load_message_prompt_bindings
    from .ui.selectfile_window import load_select_file_prompt_bindings

    return MergedRegistry([
        load_default_key_bindings(),
        load_basic_key_bindings(),
        load_confirm_prompt_bindings(),
        load_search_n_replace_bindings(),
        load_menu_bindings(),
        load_textinput_bindings(),
        load_message_prompt_bindings(),
        load_select_file_prompt_bindings()
        ])
