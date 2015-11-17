#!/bin/bash

cd ..
echo "TESTING CORE\n"
python -m SublimeTransmute.tests.core_test
echo "\nTESTING COMMAND: COUNT\n"
python -m SublimeTransmute.tests.count_command_test