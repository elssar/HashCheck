HashCheck is a simple Python script that searches the internet for md5 & sha1 hashes of your passwords.
If you get a hit, then your password exists in a rainbow table that has been shared online & it's time to change that password.
Though getting no hits does not guarantee that your password is safe, it still is reassuring.

HashCheck uses the hashlib library to generage md5 & sha1 hashes.

You can either enter passwords when you run the program, passing -t or --text as argument, followed by any number of passwords you want checked.
Or you can save the password hashes in a YAML file(pwd.yaml) in the format 'service name' : [hash1, hash2], where hash1 & hash2 are the
md5 & sha1(no particular order required) hashes of your password.
Alternately, you can use the -m or --makefile option to make your pwd.yaml file. You can append to(-a|--append), delete a password(-d|--delete), change a password(-c|change) or even purge the entire file(-p|--purge)

External Libraries used - PyYAML3.10 - http://pyyaml.org/wiki/PyYAML
                        - Google's apilib - http://code.google.com/p/google-api-python-client/wiki/Installation

You will need to use Googles custom search API, and will require an API key for that - https://code.google.com/apis/console/
Also, keep in mind that Google only allows 100 free searches per day.

Licence - GPL v3 - http://www.gnu.org/copyleft/gpl.html
