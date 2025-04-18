# main.py
import pytest

if __name__ == "__main__":
	# Run pytest programmatically
	result = pytest.main(["-v", "test_thruster.py"])
	if result == 0:
		print("All tests passed.")
	else:
		print("Some tests failed.")
