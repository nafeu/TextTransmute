#!/bin/bash
# Be aware that you are currently testing in python 2 for a plugin written in python 3
cd ..
echo "TESTING CORE\n"
python -m SublimeTransmute.tests.core_test
echo "\nTESTING COMMAND: COUNT\n"
python -m SublimeTransmute.tests.count_command_test