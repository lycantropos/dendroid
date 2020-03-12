import os

from hypothesis import (HealthCheck,
                        Verbosity,
                        settings)

on_travis_ci = bool(os.getenv('CI', False))
on_azure_pipelines = bool(os.getenv('TF_BUILD', False))
settings.register_profile('default',
                          max_examples=(settings.default.max_examples // 2
                                        if on_travis_ci or on_azure_pipelines
                                        else settings.default.max_examples),
                          deadline=None,
                          suppress_health_check=[HealthCheck.filter_too_much,
                                                 HealthCheck.too_slow],
                          verbosity=Verbosity(settings.default.verbosity
                                              + on_travis_ci))
