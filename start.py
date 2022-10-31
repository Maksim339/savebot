import os 

exist = os.system("sudo systemctl status savebot.service | grep 'active (running)'")

print(exist)

if exist == 0:
	os.system("sudo systemctl restart savebot.service")
	print('Done!')
else:
	try:
		os.system("sudo systemctl start savebot.service")
		#os.system("cd /var/www/savebot && source venv/bin/activate && uwsgi --ini 123.ini")123123
	except Exception as e:
		print(e)


