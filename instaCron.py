import pickle
from urlparse import urlparse

iterations = 50

# WHAT IS OUR PATH
path = ''

# API Setup
client_id = 'YOUR ID'
client_secret = 'YOUR KEY'
from instagram.client import InstagramAPI
api = InstagramAPI(client_id=client_id, client_secret=client_secret)

# figure out the max ID
try:
	max_tag_id = pickle.load(open(path + 'last_max_id.p', 'rb')) - 1
except:
	max_tag_id = 0

# Tag setup
used_tag = 'music'

# instantiate all_media
all_media = []

# run one query which we will also use to initialize params['max_tag_id']
ans = api.tag_recent_media(33, max_tag_id, used_tag)
for m in ans[0]:
	all_media.append(m)

# parse the url to get a new max_tag_id
parsed = urlparse(ans[1])
params = {a:b for a,b in [x.split('=') for x in parsed.query.split('&')]}

for i in range(iterations):
	max_tag_id = int(params['max_tag_id'])
	ans = api.tag_recent_media(200, max_tag_id-1, used_tag)
	for m in ans[0]:
		all_media.append(m)

	# get next max_tag_id
	parsed = urlparse(ans[1])
	params = {a:b for a,b in [x.split('=') for x in parsed.query.split('&')]}
	print 'max tag id: ' + str(max_tag_id)

# save a pickle with all_media
pickle.dump(all_media, open(path+used_tag+'%s_.p' % str(max_tag_id),'wb'))

# save a pickle with max_tag_id
pickle.dump(max_tag_id, open(path+'last_max_id.p','wb'))