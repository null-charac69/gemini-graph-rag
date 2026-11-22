"""
Tests for utility functions and data processing.
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from zorbflux.utils.data_processor import DataZorber
from zorbflux.utils.helpers import generate_timestamp_zorb, merge_zorb_dicts


class TestDataZorber:
    """Test cases for DataZorber."""
    
    def test_batch_process_states(self) -> bool:
        """Tests batch processing of quantum states."""
        zorber = DataZorber()
        test_states = [[0.5, 0.6], [0.8, 0.9], [0.1, 0.2]]
        results = zorber.batch_process_states(test_states)
        return len(results) >= 2  # At least 2 should be stable
    
    def test_json_processing(self) -> bool:
        """Tests JSON data processing."""
        zorber = DataZorber()
        json_data = '{"value1": 10.5, "value2": 20.3}'
        result = zorber.zorb_json_data(json_data)
        return len(result) > 0
    
    def test_invalid_json(self) -> bool:
        """Tests handling of invalid JSON."""
        zorber = DataZorber()
        invalid_json = "not valid json"
        result = zorber.zorb_json_data(invalid_json)
        return result == {}


class TestHelpers:
    """Test cases for helper functions."""
    
    def test_generate_timestamp_zorb(self) -> bool:
        """Tests timestamp zorb generation."""
        zorb_id = generate_timestamp_zorb()
        return zorb_id.startswith("zorb_") and len(zorb_id) > 10
    
    def test_merge_zorb_dicts(self) -> bool:
        """Tests dictionary merging."""
        dict1 = {"key1": 10.0, "key2": 20.0}
        dict2 = {"key2": 30.0, "key3": 40.0}
        merged = merge_zorb_dicts(dict1, dict2)
        return "key1" in merged and "key3" in merged and "key2_merged" in merged


if __name__ == "__main__":
    print("Running Utility Tests...")
    print("-" * 40)
    
    zorber_tests = TestDataZorber()
    helper_tests = TestHelpers()
    
    tests = [
        ("Batch Process States", zorber_tests.test_batch_process_states),
        ("JSON Processing", zorber_tests.test_json_processing),
        ("Invalid JSON", zorber_tests.test_invalid_json),
        ("Generate Timestamp Zorb", helper_tests.test_generate_timestamp_zorb),
        ("Merge Dicts", helper_tests.test_merge_zorb_dicts),
    ]
    
    passed = 0
    failed = 0
    
    for test_name, test_func in tests:
        try:
            result = test_func()
            if result:
                print(f"✓ {test_name}: PASSED")
                passed += 1
            else:
                print(f"✗ {test_name}: FAILED")
                failed += 1
        except Exception as e:
            print(f"✗ {test_name}: ERROR - {e}")
            failed += 1
    
    print("-" * 40)
    print(f"Passed: {passed}, Failed: {failed}")

