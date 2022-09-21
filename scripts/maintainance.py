import ezomero
from omero.cli import CLI
import os


def maintenance(user_list):
    cli = CLI()
    cli.loadplugins()
    for user in user_list:
        user = user.rstrip()
        print(f"deleting contents from user {user}")
        delete_contents(cli, user)
        print(f"reimporting data from user {user}")
        reimport(cli, user)
    return

def delete_contents(cli, user):
    conn = ezomero.connect(user, "omero", host="localhost", port=4064, group="", secure=True)
    uuid = conn.getSession().getUuid().val
    cli.invoke(['sessions', 'login', '-u', user,
                       '-k', uuid, '-s', "localhost"])
    my_exp_id = conn.getUser().getId()
    proj_id = None
    for proj in conn.getObjects("Project", opts={'owner': my_exp_id}):
        proj_id = proj.id
    if proj_id:
        cli.invoke(['delete', 'Project:'+str(proj_id), '--include', 'Dataset,Image,Annotation'])
    conn.close()


def reimport(cli, user):
    conn = ezomero.connect(user, "omero", host="localhost", port=4064, group="", secure=True)
    data = os.path.dirname("/hyperfile/omerodata/training_data/")
    uuid = conn.getSession().getUuid().val
    cli.invoke(['sessions', 'login', '-u', user,
                    '-k', uuid, '-s', "localhost"])
    cli.invoke(['-k', uuid, '-s', "localhost",
                        '-u', "localhost", 'transfer', 'unpack',
                        '--folder', data,
                        '--ln_s',
                        '--metadata', 'none']
                        )
    conn.close()


if __name__ == "__main__":
    fpath = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "user_list.txt")
    with open(fpath, 'r') as fp:
        user_list = fp.readlines()
    maintenance(user_list)
