#!/usr/local/CyberCP/bin/python
import sys
import os.path
import django

sys.path.append('/usr/local/CyberCP')
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "CyberCP.settings")
try:
    django.setup()
except:
    pass
from loginSystem.models import Administrator, ACL
import argparse
import pwd
import json
from CLScript.CLMain import CLMain


class CloudLinuxAdmins(CLMain):

    def __init__(self):
        CLMain.__init__(self)

    def listAll(self, owner=None):
        users = []
        acl = ACL.objects.get(name='admin')
        for items in Administrator.objects.filter(acl=acl):

            if items.userName == 'admin':
                isMain = True
            else:
                isMain = False


            user = {'name': items.userName,
                    "locale_code": "EN_us",
                    "unix_user": None,
                     "email": items.email,
                     "is_main": isMain
                    }

            users.append(user)

        final = {'data': users, 'metadata': self.initialMeta}
        print(json.dumps(final))


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='CyberPanel CloudLinux Manager')
    parser.add_argument('--owner', help='Owner')

    args = parser.parse_args()

    pi = CloudLinuxAdmins()
    try:
        pi.listAll(args.owner)
    except:
        pi.listAll()