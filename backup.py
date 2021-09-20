import paramiko
import time
from rich import print,box
from datetime import datetime
from rich.layout import Layout
from rich.panel import Panel
from rich.table import Table
from rich.style import Style
from rich.console import Console
from rich.live import Live

console = Console()

grid = Table.grid(expand=True)
grid.add_column(justify="center", ratio=1)
grid.add_column(justify="right")
grid.add_row(
    "Backup Remote Config",
    datetime.now().ctime().replace(":", "[blink]:[/]"),
)
print(Panel(grid, style="white on blue"))


ssh_client = paramiko.SSHClient()
ssh_client.set_missing_host_key_policy(paramiko.AutoAddPolicy())

def connect(hname,port,uname,pswd):
    ssh_client.connect(hostname=hname,port=port,username=uname,password=pswd)

def disconnect():
    if ssh_client.get_transport().is_active() == True:
        ssh_client.close()
        
timestamp = str(datetime.now().timestamp()).split(".")[0]

def create_backup():
    console.print("\nCompressing[blink]..........",style="bright_red")
    live_compression()
    console.print("\ncompression successfull\n",style="blue")

def ftp(r_path,l_path):
    console.print("Downloading[blink]..........",style="bright_red")
    ftp_client = ssh_client.open_sftp() 
    ftp_client.get(remotepath=r_path,localpath=l_path+timestamp+".bz2")
    console.print("\nSuccessfully Downloaded",style="blue")
    ftp_client.close()

def live_compression():
    table = Table(border_style="bright_red")
    table.add_column("FILES",style="bright_cyan")
    with Live(table, refresh_per_second=1):
        stdin, stdout, stderr = ssh_client.exec_command("tar -cvf backup.bz2 backup_test/*")
        for res in stdout.read().decode().split("\n"):
            table.add_row(str(res))
            time.sleep(1.0)


connect("127.0.0.1","22","wgz","wgz")
create_backup()
ftp("/home/wgz/backup.bz2","/home/wgz/confbackups/backup")
disconnect()