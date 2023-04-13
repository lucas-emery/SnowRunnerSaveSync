import argparse
import re
import shutil
import time
import json

parser = argparse.ArgumentParser()
parser.add_argument('account', help='Steam account number', type=str)
args = parser.parse_args()

source_path = './CompleteSave.cfg'
target_path = 'C:/Program Files (x86)/Steam/userdata/{}/1465360/remote/CompleteSave.cfg'.format(args.account)

print('Loading source save:', source_path)
with open(source_path, 'r') as file:
    data = file.read()
    source = json.loads(data.rstrip('\0'))

print('Loading target save:', target_path)
with open(target_path, 'r') as file:
    data = file.read()
    target = json.loads(data.rstrip('\0'))

backup_path = '{}.{}.bck'.format(target_path, str(round(time.time() * 1000)))
print('Backing up target save to:', backup_path)
shutil.copy2(target_path, backup_path)

print('Transfering unlocks')
target['CompleteSave']['SslValue']['upgradesGiverData'] = source['CompleteSave']['SslValue']['upgradesGiverData']
target['CompleteSave']['SslValue']['persistentProfileData']['discoveredUpgrades'] = source['CompleteSave']['SslValue']['persistentProfileData']['discoveredUpgrades']
target['CompleteSave']['SslValue']['persistentProfileData']['unlockedItemNames'] = source['CompleteSave']['SslValue']['persistentProfileData']['unlockedItemNames']

print('Writing updated save')
with open(target_path, 'w') as file:
    data = json.dumps(target) + '\0'
    file.write(data)

print('Save file updated successfully')
