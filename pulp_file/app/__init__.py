from pulpcore.plugin import PulpPluginAppConfig


class PulpFilePluginAppConfig(PulpPluginAppConfig):
    name = 'pulp_file.app'
    label = 'pulp_file'
