import os
from fabric import Connection


class ComEx(object):
    """
    Command Executor. Wrapper class for fabric connection which remembers the working directory and other states
    """

    def __init__(self, remote, user):
        self._c = Connection(remote, user)

        self.dir = None
        self.venv = None

        self.hide = True  # hide mode for commands which are called implicitly

    def chdir(self, path):
        """
        The following works on uberspace:

        c.chdir("etc")
        c.chdir("~")
        c.chdir("$HOME")

        :param path:
        :return:
        """

        if path is None:
            self.dir = None
            return

        cmd = "cd {} && pwd".format(path)
        res = self.run(cmd, hide=self.hide, warn=True)

        if res.exited != 0:
            print("Could not change directory. Error message: {}".format(res.stderr))
        else:
            # store the result of pwd in the variable
            self.dir = res.stdout.strip()

    def activate_venv(self, path):
        """
        Activate a virtual environment
        :param path:    path to activate script (relative or absolute)
        :return:
        """

        dir_path, script_name = os.path.split(path)
        res0 = self.run("cd {} && pwd".format(dir_path), hide=self.hide)
        if not res0.exited == 0:
            print("There was some problem with the path of the virtual env. Error message:\n {}".format(res0.stderr))
            return
        abspath = os.path.join(res0.stdout.strip(), script_name)
        cmd = "source {}".format(abspath)

        res = self.run(cmd, hide=self.hide, warn=True)

        if res.exited != 0:
            print("Could not activate virtual environment. Error message:\n {}".format(res.stderr))
        else:
            # store the result of pwd in the variable
            self.venv = abspath

        return res.exited

    def deactivate_venv(self):
        self.venv = None

    def run(self, cmd, use_dir=True, hide=True, warn=False, printonly=False, use_venv=True):
        """

        :param cmd:
        :param use_dir:
        :param hide:        see docs of invoke
        :param warn:        see docs of invoke
        :param printonly:   only print the command but do not execute
        :return:
        """

        if use_dir and self.dir is not None:
            cmd = "cd {}; {}".format(self.dir, cmd)

        if use_venv and self.venv is not None:
            cmd = "source {}; {}".format(self.venv, cmd)

        if not printonly:
            res = self._c.run(cmd, hide=hide, warn=warn)
        else:
            print("->:", cmd)
            res = None
        return res

    def get_stdout(self, cmd, **kwargs):
        res = self.run(cmd, **kwargs)
        if hasattr(res, "stdout"):
            return res.stdout.strip()
        else:
            return res

