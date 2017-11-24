import sys
import os
from urllib2 import urlopen
import tarfile
import zipfile


def report_download_progress(count, block_size, total_size):
    pct_complete = float(count * block_size) / total_size
    msg = "\r {0:.1%} already downloaded".format(pct_complete)
    sys.stdout.write(msg)
    sys.stdout.flush()


def download_data_url(url, download_dir):
    filename = url.split('/')[-1]
    file_path = os.path.join(download_dir, filename)

    #print "url ", url
    #print "filename ", filename
    #print "filepath ", file_path
    #print "download_dir ", download_dir

    if not os.path.exists(file_path):
        #os.makedirs(download_dir)

        print("Download %s to %s" % (url, file_path))

        u = urlopen(url)
        f = open(file_path, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (filename, file_size)

        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break

            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            print status,

        f.close()

        # page = urlopen(url).read()
        # write_file = open(filename, 'wb')
        # write_file.write(page)
        # write_file.close()

        print("\nExtracting files")
        if file_path.endswith(".zip"):
            zipfile.ZipFile(file=file_path, mode="r").extractall(download_dir)
        elif file_path.endswith((".tar.gz", ".tgz")):
            tarfile.open(name=file_path, mode="r:gz").extractall(download_dir)
