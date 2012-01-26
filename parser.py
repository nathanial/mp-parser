import codecs, struct, sys, re, itertools as it, os, math
import matplotlib.pyplot as plt
from matplotlib.backends.backend_pdf import PdfPages

def parse_header(bytes):
    txt = []
    for b in bytes:
        try:
            txt.append(b.decode('EBCDIC-CP-BE').encode('ascii'))
        except: 
            break
    return txt

def partition(n, xs):
    i = 0
    r = []
    while i < len(xs) - n:
        r.append(xs[i:i+n])
        i += n
    return r

def parse_floats(bytes):
    def parse_float(f):
        s, = struct.unpack('f',f)
        return s
    return [parse_float(f) for f in partition(4,bytes)]

def parse_traces(start, bytes):
    bytes = bytes[start:]
    floats = parse_floats(bytes)
    traces = partition(30000, floats)
    return traces

fname = sys.argv[1]
print "parsing %s" % fname
with open("data/" + fname, 'rb') as f:
    bytes = f.read()
    header = "".join(parse_header(bytes))
    i = header.index('END EBCDIC')
    i += len('END EBCDIC')
    while header[i] == ' ':
        i += 1
    i += 16 + 11904
    i = 1
    rem = len(bytes) - i
    print "%s,%s,%s,%s" % (i, len(bytes), rem, rem / 48. / 4.)
    
    traces = parse_traces(i, bytes)
    os.mkdir(fname[:-4] + "_imgs")
    i = 0
    for t in traces:
        i += 1
        plt.figure()
        plt.plot(t)
        plt.savefig('%s_imgs/output%s.png' % (fname[:-4],i))
        print i
