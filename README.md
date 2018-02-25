# Network_security_audit
Audits the security configuration on the devices
import paramiko,time,getpass
RECV_BUFFER=1000000


prefix_limit_enabled=[]
ipv6_vty_enabled=[]
prefix_limit_not_enabled=[]
ipv6_vty_not_enabled=[]

# different vendor will provide us different login types based on the vendor
def check_trailing_prompt(device, out_current):
    if ("#" in out_current[-3:] or ">" in out_current[-3:]): 
            return True 
    return False

#This will login in to the device, it will ask for username and password.
def SSHAccess(username, password, device, config): 
    output = "" 
    remote_conn_pre = paramiko.SSHClient() 
    remote_conn_pre.set_missing_host_key_policy(paramiko.AutoAddPolicy()) 
    try: 
        remote_conn_pre.connect(hostname=device, username=username, 
                                password=password, look_for_keys=False, allow_agent=False, timeout=40) 
        remote_conn = remote_conn_pre.invoke_shell()  
        out_current = remote_conn.recv(RECV_BUFFER) 
        status = False 
        for command in config: 
            timeout = 0 
            remote_conn.send(command + "\n") 
            while True: 
                if remote_conn.recv_ready(): 
                    out_current = remote_conn.recv(RECV_BUFFER) 
                    output += out_current 
                    status = True 
                    if len(out_current) == 0: 
                        output += "--Channel stream closed by remote device.\n" 
                        break 
                    if check_trailing_prompt(device, out_current): 
                        break 
                else: 
                    time.sleep(1) 
                    timeout += 1 
                    # time out delay 5 mins 
                    if timeout > 30: 
                        output += "\n--Not responding - Timed out by Bulkconfig tool" 
                        status = False 
                        break 
 
        remote_conn_pre.close() 
    except Exception as e: 
        output += "Unable to access " + str(device) + ":" + str(e) 
        status = False 
        print "Unexpected error:"+str(e)
    return {device:output} 

#This module executed for CISCO devices
def check_cisco(devicelist,username,password):
    commands = ['your commands here','next_command']
    for device in devicelist:
        output = SSHAccess(username,password,device,commands)
    if 'prefix_limit_required_out' in output[device]:
        prefix_limit_enabled.append(device)
    else:
        prefix_limit_not_enabled.append(device)
    if 'vty_output required' in output[device]:
        ipv6_vty_enabled.(device)
    else:
        ipv6_vty_not_enabled(device)

#Module for Juniper devices
def check_juniper(devicelist,username,password):
    commands = ['your commands here','next_command']
    for device in devicelist:
        output = SSHAccess(username,password,device,commands)
    if 'prefix_limit_required_out' in output[device]:
        prefix_limit_enabled.append(device)
    else:
        prefix_limit_not_enabled.append(device)
    if 'vty_output required' in output[device]:
        ipv6_vty_enabled.(device)
    else:
        ipv6_vty_not_enabled(device)

def main():
    cisco_list = open("ciscodevices","r")
    jun_list = open("juniperdevices","r")
    username = raw_input('Username:')
    password = getpass.getpass()
    check_juniper(jun_list,username,password)
    check_cisco(cisco_list,username,password)

if __name__ == '__main__': 
    main()
