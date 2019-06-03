import pkg_resources

__version__ = pkg_resources.get_distribution("pulp_file").version


default_app_config = 'pulp_file.app.PulpFilePluginAppConfig'
