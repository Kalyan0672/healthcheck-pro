import unittest
from unittest.mock import patch, MagicMock

from healthcheck import check_website


class TestHealthCheck(unittest.TestCase):

    @patch("healthcheck.urllib.request.urlopen")
    def test_website_is_up(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_urlopen.return_value.__enter__.return_value = mock_response

        result = check_website("https://test.com")

        self.assertEqual(result["status"], "UP")
        self.assertEqual(result["status_code"], 200)

    @patch("healthcheck.urllib.request.urlopen")
    def test_website_is_down(self, mock_urlopen):
        mock_urlopen.side_effect = Exception("Connection failed")

        result = check_website("https://test.com")

        self.assertEqual(result["status"], "DOWN")

    @patch("healthcheck.urllib.request.urlopen")
    def test_response_time_is_recorded(self, mock_urlopen):
        mock_response = MagicMock()
        mock_response.status = 200
        mock_urlopen.return_value.__enter__.return_value = mock_response

        result = check_website("https://test.com")

        self.assertIn("response_time", result)
        self.assertGreaterEqual(result["response_time"], 0)


if __name__ == "__main__":
    unittest.main()