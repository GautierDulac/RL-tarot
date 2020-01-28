import importlib

from rlcard.envs.env import Env


class EnvSpec(object):
    """
    A specification for a particular instance of the environment.
    """

    def __init__(self, env_id: str, entry_point: str = None):
        """
        Initialize
        :param env_id: (string): the name of the environent
        :param entry_point: (string): a string the indicates the location of the envronment class
        """
        self.env_id = env_id
        mod_name, class_name = entry_point.split(':')
        self._entry_point = getattr(importlib.import_module(mod_name), class_name)

    def make(self) -> Env:
        """
        Instantiates an instance of the environment
        :return: (Env): an instance of the environemnt
        """
        env = self._entry_point()
        return env


class EnvRegistry(object):
    """
    Register an environment (game) by ID
    """

    def __init__(self):
        """
        Initilize
        """
        self.env_specs = {}

    def register(self, env_id: str, entry_point: str) -> None:
        """
        Register an environment
        :param env_id: (string): the name of the environent
        :param entry_point: (string): a string the indicates the location of the envronment class
        :return:
        """
        if env_id in self.env_specs:
            raise ValueError('Cannot re-register env_id: {}'.format(env_id))
        self.env_specs[env_id] = EnvSpec(env_id, entry_point)

    def make(self, env_id: str) -> Env:
        """
        Create an environment instance
        :param env_id: (string): the name of the environment
        :return: Env instance
        """
        if env_id not in self.env_specs:
            raise ValueError('Cannot find env_id: {}'.format(env_id))
        return self.env_specs[env_id].make()


# Have a global registry
registry = EnvRegistry()


def register(env_id: str, entry_point: str) -> None:
    """
    Register an environment
    :param env_id: (string): the name of the environent
    :param entry_point: (string): a string the indicates the location of the envronment class
    :return:
    """
    return registry.register(env_id, entry_point)


def make(env_id: str) -> Env:
    """
    Create an environment instance
    :param env_id: (string): the name of the environment
    :return: Env instance
    """
    return registry.make(env_id)
