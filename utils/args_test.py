import os

xdg_config_home = os.getenv('XDG_CONFIG_HOME', '~/.config')
print xdg_config_home