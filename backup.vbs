
Set Wshell = CreateObject("WScript.Shell")

Dim scriptPath

' 获取当前脚本的完整路径
strPath = Wshell.CurrentDirectory

Length = Len(strPath)

Dim operate

he = """"

operate = "source " + strPath + "\SqlFIle\backup.sql"

Wshell.run "mysql -uroot -pawsl"

WScript.Sleep 1000


Wshell.SendKeys operate 
Wshell.SendKeys "{ENTER}"

WScript.Sleep 500
Wshell.SendKeys "^Z{ENTER}"






