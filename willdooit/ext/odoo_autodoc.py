import os
import sys
from sphinx.application import Sphinx

VERSION='14.0'


def setup(app: Sphinx) -> dict:
    """
    Setup function used by Sphinx, when loading willdooit-odoo-autodoc as a Sphinx extension,

    :param app: Sphinx instance.
    :type app: Sphinx
    :return: Dictionary to report extension details back to Sphinx.
    :rtype: dict
    """
    app.add_config_value('odoo_root_path', '', True)
    app.add_config_value('odoo_addons_path', [], True)
    app.add_config_value('odoo_config_path', '', True)
    app.connect('builder-inited', load_modules)

    return {'version': VERSION}


def load_modules(app: Sphinx) -> None:
    """
    Parse config values and initialise Odoo modules.

    :param app: Sphinx instance.
    :type app: Sphinx
    """
    odoo_config_args = []

    if app.env.config.odoo_config_path:
        odoo_config_args.append('-c')
        odoo_config_args.append(app.env.config.odoo_config_path)

    addons_path = ','.join(app.env.config.odoo_addons_path)
    if not addons_path:
        addons_path = os.environ.get('ODOO_ADDONS_PATH', '')

    if addons_path:
        odoo_config_args.append('--addons-path')
        odoo_config_args.append(addons_path)

    if app.env.config.odoo_root_path:
        sys.path.append(app.env.config.odoo_root_path)

    import odoo

    # Initialise Odoo sys path overrides
    odoo.tools.config._parse_config(odoo_config_args)
    odoo.modules.initialize_sys_path()
