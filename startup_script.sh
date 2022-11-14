# hello! this script checks whether pygame is installed and prompts to install if not already installed
# it then proceeds to run Invaders

#!/bin/bash

python -m pygame 2>&1 | grep "No module named" > /dev/null
if [[ $? -eq 0 ]];
then
echo "You need to install pygame in order to run this game\n"
echo "Pygame can be installed with the terminal command 'pip install pygame'\n"
fi
