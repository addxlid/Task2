import datetime
import getopt
import hashlib
import os
import shutil
import sys
import time

DEBUGGING = True


def cmp(odir, cdir):
    ohashes = checksums(odir)
    chashes = checksums(cdir)
    result = {}
    for f in ohashes:
        if f not in chashes:
            result[f] = 'add: '
    for f in sorted(result):
        yield (f, result[f])


def checksums(targetdir):
    result = {}
    for root, dirs, files in os.walk(targetdir):
        if DEBUGGING:
            print(root, dirs, files)
        for f in files:
            fpath = os.path.join(root, f)
            frelpath = os.path.relpath(fpath, targetdir)
            result[frelpath] = md5(fpath)
    return result


def md5(fname):
    hash_md5 = hashlib.md5()
    with open(fname, "rb") as f:
        for chunk in iter(lambda: f.read(4096), b""):
            hash_md5.update(chunk)
    return hash_md5.hexdigest()


def main(argv):
    origindir = ''
    clonedir = ''
    Logfile = ''
    Log_timeout = 0
    try:
        opts, args = getopt.getopt(argv, "o:c:l:h:", ["odir=", "cdir=", "Logfile", "Log_timeout"])
    except getopt.GetoptError:
        print('Error with options -o origindir -c clonedir -l')
        sys.exit(2)
    for opt, arg in opts:
        if opt in ("-h", "--Log_timeout"):
            Log_timeout = int(arg)
        elif opt in ("-l", "--Logfile"):
            Logfile = arg
        elif opt in ("-o", "--odir"):
            origindir = arg
        elif opt in ("-c", "--cdir"):
            clonedir = arg
    if DEBUGGING:
        print('Origin dir is "{}"'.format(origindir))
        print('Clone dir is "{}"'.format(clonedir))
        print('Log file is "{}"'.format(Logfile))
        print('Log timeout is "{}"'.format(Log_timeout))

    while True:

        for path, status in cmp(origindir, clonedir):
            t = "{} {}".format(status, path)
            print(t)
            shutil.copy2(origindir + "\\" + path, clonedir + "\\" + path, follow_symlinks=True)
            f = open(Logfile, 'a')
            now = datetime.datetime.now()
            f.write("{0} : {1}\n".format(now.strftime("%d-%m-%Y %H:%M"), t))
            f.close()
        time.sleep(Log_timeout)


if __name__ == "__main__":
    main(sys.argv[1:])
