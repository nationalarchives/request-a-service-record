import unittest
from unittest.mock import patch
from app.lib.content import prepare_country_options


class TestPrepareCountryOptions(unittest.TestCase):

    def setUp(self):
        # Test content with valid country data
        self.test_content = {
            "request_form": {
                "fields": {
                    "forenames": {
                        "label": "Forenames (including middle names)",
                        "messages": {
                            "required": "The service person's first name is required"
                        }
                    },
                    "last_name": {
                        "label": "Last name",
                        "messages": {
                            "required": "The service person's last name is required"
                        }
                    },
                    "requester_country": {
                        "label": "Country",
                        "prompt_to_select": "Please select a country",
                        "countries": ["United Kingdom", "United States", "Canada"]
                    }
                }
            }
        }

    def test_valid_country_options(self):
        """Test with valid country data"""
        expected = [
            ("", "Please select a country"),
            ("United Kingdom", "United Kingdom"),
            ("United States", "United States"),
            ("Canada", "Canada")
        ]
        result = prepare_country_options(self.test_content)
        self.assertEqual(result, expected)

    def test_missing_prompt(self):
        """Test when prompt_to_select is missing"""
        incomplete_content = {
            "request_form": {
                "fields": {
                    "requester_country": {
                        "label": "Country",
                        "countries": ["United Kingdom", "United States", "Canada"]
                    }
                }
            }
        }
        with patch('builtins.print') as mock_print:
            result = prepare_country_options(incomplete_content)
            mock_print.assert_called_once()
            self.assertEqual(result, [])

    def test_missing_country_field(self):
        """Test when requester_country field is missing"""
        content_without_country = {
            "request_form": {
                "fields": {
                    "forenames": {
                        "label": "Forenames (including middle names)"
                    },
                    "last_name": {
                        "label": "Last name"
                    }
                }
            }
        }
        with patch('builtins.print') as mock_print:
            result = prepare_country_options(content_without_country)
            # Check that print was called at least once with an error message
            self.assertGreaterEqual(mock_print.call_count, 1)
            self.assertEqual(result, [])

    def test_missing_countries(self):
        """Test when countries list is missing"""
        incomplete_content = {
            "request_form": {
                "fields": {
                    "requester_country": {
                        "label": "Country",
                        "prompt_to_select": "Please select a country"
                    }
                }
            }
        }
        with patch('builtins.print') as mock_print:
            result = prepare_country_options(incomplete_content)
            mock_print.assert_called_once()
            self.assertEqual(result, [])

    def test_invalid_prompt_type(self):
        """Test when prompt is not a string"""
        invalid_content = {
            "request_form": {
                "fields": {
                    "requester_country": {
                        "prompt_to_select": ["Not a string"],
                        "countries": ["United Kingdom", "United States", "Canada"]
                    }
                }
            }
        }
        with patch('builtins.print') as mock_print:
            result = prepare_country_options(invalid_content)
            mock_print.assert_called_once()
            self.assertEqual(result, [])

    def test_invalid_countries_type(self):
        """Test when countries is not a list"""
        invalid_content = {
            "request_form": {
                "fields": {
                    "requester_country": {
                        "prompt_to_select": "Please select a country",
                        "countries": "Not a list"
                    }
                }
            }
        }
        with patch('builtins.print') as mock_print:
            result = prepare_country_options(invalid_content)
            mock_print.assert_called_once()
            self.assertEqual(result, [])


if __name__ == '__main__':
    unittest.main()
