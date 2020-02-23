from unittest import TestCase
import os

import sarce

"""
Note these tests will probably not run on other computers out of the box. Reasons:
- you need your sshkey activated (e.g. `eval $(ssh-agent); ssh-add -t 5m`)
- the remote (localhost) needs to accept your ssh key (try in shell e.g. ssh localhost)
- the path `test_env_path` must point to a valid virtual environment

"""

remote = "localhost"
user = os.environ["USER"]

test_env_path = os.path.expanduser("~/z_local_data/venvs/sarca_test_env/bin/activate")


# noinspection PyMethodMayBeStatic
class GeneralTests(TestCase):

    def test_simple_command(self):
        ce = sarce.ComEx(remote, user)
        res = ce.run("whoami", hide=True)
        self.assertEqual(res.stdout.strip(), user)

        un = ce.get_stdout("whoami")
        self.assertEqual(un, user)

    def test_chdir(self):
        ce = sarce.ComEx(remote, user)
        res1 = ce.run("ls")
        ce.chdir("tmp")
        res2 = ce.run("ls")
        res3 = ce.run("ls")
        self.assertNotEqual(res1.stdout, res2.stdout)
        self.assertEqual(res2.stdout, res3.stdout)

    def test_venv(self):
        ce = sarce.ComEx(remote, user)

        test_env_path_base = test_env_path.replace("/bin/activate", "")

        get_pypath = 'python -c "import sys; print(sys.path)"'

        res1 = ce.run(get_pypath)

        self.assertTrue(ce.venv is None)
        ce.activate_venv(test_env_path)
        self.assertFalse(ce.venv is None)

        res2 = ce.run(get_pypath)
        ce.deactivate_venv()
        res3 = ce.run(get_pypath)

        self.assertFalse(test_env_path_base in res1.stdout)
        self.assertTrue(test_env_path_base in res2.stdout)
        self.assertFalse(test_env_path_base in res3.stdout)
