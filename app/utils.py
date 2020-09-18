import json
import subprocess

conf = "/app/config/config"

def getclusterinfo():
    output = dict()
    output["NodeStatus"], output["NodeEvents"] = getnodestatusevents()
    output["Namespaces"], output["PodsStatus"] = getnamespacespods()
    return json.loads(json.dumps(output))


def subprocess_cmd(command):
    process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
    stdout, stderr = process.communicate()
    if stderr == None:
        return stdout.decode()


def getevents(nodes):
    nodeevents = dict()
    for i in nodes:
        nodeevents[i] = subprocess_cmd("kubectl --kubeconfig=%s get events --no-headers | grep %s " % (conf, i))
    return nodeevents


def getpodsstatus(ns):
    nspodsstatus = dict()
    for i in ns:
        pstatus = subprocess_cmd("kubectl --kubeconfig=%s get pod -n %s --no-headers | awk '{print $1,$3}'" % (conf, i))
        for j in pstatus.splitlines():
            if 'No resources' in j:
                break
            nspodsstatus[i + "-----" + j.split()[0]] = j.split()[1]
    return nspodsstatus


def getnodestatusevents():
    nodeout = subprocess_cmd("kubectl --kubeconfig=%s get nodes --no-headers | awk '{print $1,$2}' " % conf)
    nodestatus = dict()
    for i in nodeout.splitlines():
        nodestatus[i.split()[0]] = i.split()[1]
    return nodestatus, getevents(nodestatus.keys())


def getnamespacespods():
    ns = subprocess_cmd("kubectl --kubeconfig=%s get namespaces --no-headers | awk '{print $1,$2}' " % conf)
    nsstatus = dict()
    for i in ns.splitlines():
        if i.split()[0] == "No":
            pass
        nsstatus[i.split()[0]] = i.split()[1]
    return nsstatus, getpodsstatus(nsstatus.keys())


def customcommand(cmd):
    if cmd == "":
        return ""
    if "|" in cmd:
        subcmd , arg = cmd.split("|",1)
        return subprocess_cmd(subcmd + " --kubeconfig=%s | " % conf + arg).splitlines()
    return subprocess_cmd(cmd + " --kubeconfig=%s" % conf).splitlines()
