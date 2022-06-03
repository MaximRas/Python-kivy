from modules import archive_interface
import json
import uuid
login = "admin@domain.com"
password = "1234aA"
url = "http://xde-dev-im1:6006"


object_archive = archive_interface.ArchiveInterface(url, password, login)
token = object_archive.authorization()
url = "http://xde-dev-im1:6006/archive/"
print(token)
files = json.dumps({'FileName':'test2323', 'AttachmentType': 3, "DocumentId": str(uuid.uuid4())})
print(files)
response = object_archive.save_files_to_archive(url, '5123252322', token, files)
print(response)

response = object_archive.load_files_from_archive(url, response, token)
print(response)