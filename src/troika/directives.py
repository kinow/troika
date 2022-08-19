"""Directive handling"""

import logging

from .hooks.base import Hook

_logger = logging.getLogger(__name__)

#: Directive aliases. A directive named `dir` found in the script will be
#: converted to `ALIASES[dir]`, if present
ALIASES = {
    "error": "error_file",
    "job_name": "name",
    "output": "output_file",
    "time": "walltime",
}


class Translator(Hook):
    """Directive translation hook manager

    See `troika.hooks.base.Hook`. The only change is the behaviour of the
    `__call__` method::

        def __call__(self, script_data, *args, **kwargs):
            for func in self.enabled_hooks:
                script_data = func(script_data, *args, **kwargs)
            return script_data
    """

    _namespace = "troika"

    def __call__(self, data, *args, **kwargs):
        if self._impl is None:
            raise ValueError("Attempt to call a non-instantiated hook registry")
        _logger.debug("Translating directives")
        for funcname, func in self._impl:
            _logger.debug("Calling translator function %s", funcname)
            data = func(data, *args, **kwargs)
        return data


@Translator.declare
def translators(script_data, global_config, site):
    """Directive translation hook

    Parameters
    ----------
    script_data: dict[str, Any]
        Data parsed from the input script
    global_config: `troika.config.Config`
        Global configuration
    site: `troika.sites.base.Site`
        Target site

    Returns
    -------
    dict[str, Any]
        Updated `script_data`
    """


def join_output_error(script_data, global_config, site):
    """Add the 'join_output_error' directive when needed"""
    if 'error_file' not in script_data['directives']:
        script_data['directives']['join_output_error'] = ()
    return script_data