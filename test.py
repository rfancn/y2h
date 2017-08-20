import sys
from y2h import Yaml2Html

if len(sys.argv)<2:
    print('Please input test yaml file path')
    sys.exit(0)

ytoh = Yaml2Html()
yaml_file = sys.argv[1]
ytoh.read(yaml_file)
ytoh.convert()