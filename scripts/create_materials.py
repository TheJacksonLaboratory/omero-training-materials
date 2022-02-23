import ezomero
import os
import argparse
from omero.cli import CLI
from omero.plugins.sessions import SessionsControl
from omero.plugins.user import UserControl
from omero.plugins.group import GroupControl


def create_group(cli, gname, session_uuid, hostname):
    cli.invoke(['group', 'add',
                gname,
                '--type', 'read-only',
                '-k', session_uuid,
                '-s', hostname
                ])
    gid = ezomero.get_group_id(conn, gname)
    return gid


def create_users(cli, gid, user_list, session_uuid, hostname):
    for user in user_list:
        user = user.rstrip()
        print(user)
        cli.invoke(['user', 'add',
                    user,
                    'Training',
                    f'User {user}',
                    '--group-id', str(gid),
                    '-e', 'useremail@jax.org',
                    '-P', 'omero',
                    '-k', session_uuid,
                    '-s', hostname
                    ])


def unpack_data(conn, user_list, groupname, hostname, ln_s, output):
    data = os.path.join(
            os.path.dirname(os.path.realpath(__file__)),
            "../data/training_pack.zip")
    for user in user_list:
        user = user.rstrip()
        newconn = conn.suConn(user, groupname, 999999999)
        newcli = CLI()
        newcli.loadplugins()
        new_uuid = newconn.getSession().getUuid().val
        newcli.invoke(['sessions', 'login', '-u', user,
                       '-k', new_uuid, '-s', hostname])
        if ln_s:
            newcli.invoke(['-k', new_uuid, '-s', hostname,
                           '-u', user, 'transfer', 'unpack',
                           data,
                           '--output', output,
                           '--ln_s_import']
                          )
        else:
            newcli.invoke(['-k', new_uuid, '-s', hostname,
                           '-u', user, 'transfer', 'unpack',
                           data,
                           '--output', output]
                          )
        newconn.close()


def create_all(conn, user_list, hostname, ln_s, output):
    training_group_name = "training"
    cli = CLI()
    cli.loadplugins()
    cli.register('sessions', SessionsControl, 'test')
    cli.register('user', UserControl, 'test')
    cli.register('group', GroupControl, 'test')
    session_uuid = conn.getSession().getUuid().val
    cli.invoke(['sessions', 'login', '-k', session_uuid, '-s', hostname])
    group_id = create_group(cli, training_group_name, session_uuid, hostname)
    create_users(cli, group_id, user_list, session_uuid, hostname)
    unpack_data(conn, user_list, training_group_name, hostname, ln_s, output)
    return


if __name__ == "__main__":
    description = "One-command training data creation script"
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument(
        '--output',
        type=str,
        help='Output folder for the training data',
        default=os.path.join(os.path.dirname(os.path.realpath(__file__)),
                             "../data/training_data"))
    parser.add_argument("--ln_s",
                        default=False,
                        action="store_true",
                        help='Use in-place imports for training data')
    args = parser.parse_args()
    fpath = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "user_list.txt")
    with open(fpath, 'r') as fp:
        user_list = fp.readlines()
    hostname = input("Enter hostname:")
    conn = ezomero.connect(host=hostname)
    conn.c.enableKeepAlive(60)
    create_all(conn, user_list, hostname, args.ln_s, args.output)
    conn.close()
