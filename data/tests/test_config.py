"""
Tests for configuration management.
"""

import sys
from pathlib import Path

project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from zorbflux.config.settings import ZorbConfig
from zorbflux.config.validator import ConfigValidator


class TestZorbConfig:
    """Test cases for ZorbConfig."""
    
    def test_default_config(self) -> bool:
        """Tests default configuration loading."""
        config = ZorbConfig()
        return config.get_setting("flux_magnitude") == 1.0
    
    def test_set_get_setting(self) -> bool:
        """Tests setting and getting configuration values."""
        config = ZorbConfig()
        config.set_setting("test_key", "test_value")
        return config.get_setting("test_key") == "test_value"
    
    def test_get_all_settings(self) -> bool:
        """Tests retrieving all settings."""
        config = ZorbConfig()
        all_settings = config.get_all_settings()
        return isinstance(all_settings, dict) and len(all_settings) > 0


class TestConfigValidator:
    """Test cases for ConfigValidator."""
    
    def test_config_validation(self) -> bool:
        """Tests configuration validation."""
        config = ZorbConfig()
        validator = ConfigValidator()
        is_valid, errors = validator.validate_config(config)
        return is_valid and len(errors) == 0
    
    def test_flux_magnitude_validation(self) -> bool:
        """Tests flux magnitude validation."""
        validator = ConfigValidator()
        valid = validator.validate_flux_magnitude(5.0)
        invalid = validator.validate_flux_magnitude(15.0)
        return valid and not invalid
    
    def test_quantum_threshold_validation(self) -> bool:
        """Tests quantum threshold validation."""
        validator = ConfigValidator()
        valid = validator.validate_quantum_threshold(0.5)
        invalid = validator.validate_quantum_threshold(1.5)
        return valid and not invalid


if __name__ == "__main__":
    print("Running Config Tests...")
    print("-" * 40)
    
    config_tests = TestZorbConfig()
    validator_tests = TestConfigValidator()
    
    tests = [
        ("Default Config", config_tests.test_default_config),
        ("Set Get Setting", config_tests.test_set_get_setting),
        ("Get All Settings", config_tests.test_get_all_settings),
        ("Config Validation", validator_tests.test_config_validation),
        ("Flux Magnitude Validation", validator_tests.test_flux_magnitude_validation),
        ("Quantum Threshold Validation", validator_tests.test_quantum_threshold_validation),
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

