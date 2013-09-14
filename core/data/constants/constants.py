''' 
Esta classe armazena constantes de uso geral ao sistema.

'''

class Constants():

   # este método armazena listas de diretórios comuns para um determinado sistema operacional
   def getCommonDirectories(os=None):
      directories = []

      if os == 'linux' or os is None:
         directories.append("/bin/")
         directories.append("/boot/")
         directories.append("/cdrom/")
         directories.append("/dev/")
         directories.append("/etc/")
         directories.append("/home/")
         directories.append("/initrd/")
         directories.append("/lib/")
         directories.append("/media/")
         directories.append("/mnt/")
         directories.append("/opt/")
         directories.append("/proc/")
         directories.append("/root/")
         directories.append("/sbin/")
         directories.append("/sys/")
         directories.append("/srv/")
         directories.append("/tmp/")
         directories.append("/usr/")
         directories.append("/var/")
         directories.append("/htdocs/")
      
      if os == 'windows' or os is None:
         directories.append(r"C:\\")
         directories.append(r"D:\\")
         directories.append(r"E:\\")
         directories.append(r"Z:\\")
         directories.append(r"C:\\windows\\")
         directories.append(r"C:\\winnt\\")
         directories.append(r"C:\\win32\\")
         directories.append(r"C:\\win\\system\\")
         directories.append(r"C:\\windows\\system\\")
         directories.append(r"C:\\winnt\\system\\")
         directories.append(r"C:\\win32\\system\\")
         directories.append(r"C:\\Program Files\\")
         directories.append(r"C:\\Documents and Settings\\")

      return directories
