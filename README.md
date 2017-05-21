# ffxiv_status


	./ffxiv_status.py --help
	usage: ffxiv_status.py [-h] [--server -s] [--url -u] [--smtp_server -m]
						   [--smtp_port -p] [--username -n] [--password -w]
						   [--recipient -r]

	Check if FFXIV Server is accepting new character creation

	optional arguments:
	  -h, --help        show this help message and exit
	  --server -s       Server name (ie. Excalibur)
	  --url -u          URL of FFXIV Lodestone news page showing character
						creation status
	  --smtp_server -m  SMTP Server (ie. smtp.gmail.com)
	  --smtp_port -p    SMTP Server Port (ie. 587)
	  --username -n     SMTP Username login
	  --password -w     SMTP Password login
	  --recipient -r    Who is getting the email?



example:

	# ./ffxiv_status.py --server Gilgamesh
	Server 'Gilgamesh' is closed for character creation ;(
