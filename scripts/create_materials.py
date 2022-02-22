import ezomero
import os


def create_all(conn, user_list):
    return


if __name__ == "__main__":
    fpath = os.path.join(
        os.path.dirname(os.path.realpath(__file__)), "user_list.txt")
    with open(fpath, 'r') as fp:
        user_list = fp.readlines()
    conn = ezomero.connect()
    create_all(conn, user_list)
    conn.close()
