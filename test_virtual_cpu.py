import requests
import json

def test_virtual_cpu(bytecode, expected_output):
    url = "http://127.0.0.1:5000/execute"  # Update if hosted elsewhere
    payload = json.dumps({"bytecode": bytecode})
    headers = {"Content-Type": "application/json"}
    
    response = requests.post(url, data=payload, headers=headers)
    result = response.json()
    
    print("Test Bytecode:", bytecode)
    print("Expected Output:", expected_output)
    print("Actual Output:", result["output"])
    print("Registers:", result["registers"])
    print("Execution Steps:", result["execution_steps"])
    print("Success:", result["success"])
    print("Error:", result.get("error"))
    print("---" * 10)
    
    assert result["output"] == expected_output, "Output mismatch!"
    assert result["success"] == True, "Execution failed!"

# Test Cases
test_cases = [
    {"bytecode": "01000501010703000001030200010F000E", "expected_output": "12"},
    {"bytecode": "01000A010101040000010A000F09060F000E", "expected_output": "0"},
    {"bytecode": "0100050C080F000E010102050000010D", "expected_output": "10"},
]

for test in test_cases:
    test_virtual_cpu(test["bytecode"], test["expected_output"])
