import os
import sys
import shlex
import subprocess
import string


def get_javahome():
    '''
    Locate JAVA_HOME directory. First by looking at ENV:JAVA_HOME then by examining return value from
    call to which
    '''
    java_home = os.getenv("JAVA_HOME")
    try:
        java_bin = subprocess.check_output(["which", "java"]).rstrip('\n')
    except Exception, e:
        raise e
    if java_home:
        return java_home
    elif java_bin:
        if java_bin is not None:
            if java_bin.find("bin"):
                return ""
            else:
                return os.path.dirname(java_bin)
    else:
        return False


def check_jdk(e_maj, e_min, e_rev, java_home):
    '''
    Gets the version number of the java installed on the arg path
    Sets the check_JDK boolean to true if the java version is equal or greater than the recommended version
    '''

    if java_home:
        cmd = os.path.join(java_home, "/bin/java")
        try:
            result = subprocess.check_output([java_home + cmd, "-version"], stderr=subprocess.STDOUT)
        except Exception, e:
            raise e
        (maj, minor, rev) = shlex.split(result)[2].split('.')
        revision = int(rev[2:])
        e_rev_fixed = int(e_rev[2:])
        if (int(e_maj) == int(maj) and int(e_min) == int(minor) and int(revision) >= int(e_rev_fixed)):
            return True
        else:
            return False
    else:
        return False


def get_cpu_count():
    '''
    Darwin and Linux support for retrieving core count.
    '''
    #TODO check NUMA#
    # resources = self.config["resources"]

    if 'linux' in sys.platform:
        cmd = ["lscpu"]
        body = subprocess.check_output(cmd)
        lex = body.translate(string.maketrans('\t\,', "   ")).split('\n')
        del(lex[len(lex) - 1])
        res_dir = dict(map(str, x.split(':')) for x in lex)
        return int(res_dir["CPU(s)"])
    elif 'darwin' in sys.platform:
        cmd = ["sysctl", "hw"]
        lex = shlex.split(subprocess.check_output(cmd))
        res_dir = dict(zip(*[iter(lex)] * 2))
        return int(res_dir["hw.ncpu"])


def get_cpu_speed():
    '''
    Get cpu-speed count in MHz. Works for both Darwin and Linux
    '''
    #TODO check NUMA#
    if 'linux' in sys.platform:
        cmd = ["lscpu"]
        body = subprocess.check_output(cmd)
        lex = body.translate(string.maketrans('\t\,', "   ")).split('\n')
        del(lex[len(lex) - 1])
        res_dir = dict(map(str, x.split(':')) for x in lex)
        return float(res_dir["CPU MHz"])
    elif 'darwin' in sys.platform:
        cmd = ["sysctl", "hw"]
        lex = shlex.split(subprocess.check_output(cmd))
        res_dir = dict(zip(*[iter(lex)] * 2))
        norm_cpu_speed = int(res_dir["hw.cpufrequency:"]) * 1024 / 1000000000
        return norm_cpu_speed
    else:
        return None


def get_memory():
    if 'linux' in sys.platform:
        body = open("/proc/meminfo").read()
        lex = body.split('\n')
        del(lex[len(lex) - 1])
        res_dir = dict(map(str, x.split(':')) for x in lex)
        mem_total = filter(lambda x: x.isdigit(), res_dir["MemTotal"])
        return mem_total
    elif 'darwin' in sys.platform:
        cmd = ["sysctl", "machdep.memmap"]
        lex = shlex.split(subprocess.check_output(cmd))
        res_dir = dict(zip(*[iter(lex)] * 2))
        return int(res_dir["machdep.memmap.Conventional:"])
    else:
        return None


def get_pci_net():
    if 'linux' in sys.platform:
        cmd = subprocess.check_output(["which", "lspci"]).rstrip('\n')
        if cmd is not None:
            try:
                body = subprocess.check_output([cmd, "-n"], universal_newlines=False).split("\n")
            except Exception, e:
                raise e
            for line in body:
                str = line[8:12]
                if (str == "0200"):
                    print line
            return True


def get_cpu_flags():
    if 'linux' in sys.platform:
        body = open("/proc/cpuinfo").read()
        lex = body.split('\n')
        del(lex[len(lex) - 1])
        newlex = lex[:24]
        res_dir = dict(map(str, x.split(':')) for x in newlex)
        return res_dir["flags\t\t"]
    else:
        return None



