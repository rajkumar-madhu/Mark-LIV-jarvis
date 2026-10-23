import unittest

from dashboard.status import K8S_STATUS_MESSAGE


class DashboardStatusTests(unittest.TestCase):
    def test_kubernetes_status_explains_desktop_bridge_requirement(self):
        status = K8S_STATUS_MESSAGE.lower()
        self.assertIn("desktop jarvis bridge is not attached", status)
        self.assertIn("commands will queue", status)


if __name__ == "__main__":
    unittest.main()
