from create_materials import create_all
import ezomero
import os


def maintenance(conn, user_list):
    delete_contents(conn, user_list)
    create_all(conn, user_list)
    return


def delete_contents(conn, user_list):
    for user in user_list:
        user = user.rstrip() 
    return


if __name__ == "__main__":
    fpath = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "user_list.txt")
    with open(fpath, 'r') as fp:
        user_list = fp.readlines()
    conn = ezomero.connect()
    maintenance(conn)
    conn.close()
