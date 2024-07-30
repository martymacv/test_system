import subprocess

import clsTestSystem

actual_json_config = subprocess.Popen(['bash', '../Shell/return_current_config.sh', 'test_config'], stdout=subprocess.PIPE).communicate()[:~0]

# test_config = clsTestSystem.TestSystemConf(f"..CFG/test_config.json")
test_config = clsTestSystem.TestSystemConf(actual_json_config)
new_test_config = clsTestSystem.TestSystemConf()

# return dict() from class clsTestSystem
config = test_config.get_actual_test_config()

new_config = new_test_config.create_test_system_image()

new_test_config.write_to_json_config(new_config)
new_config = test_config.get_actual_test_config()
