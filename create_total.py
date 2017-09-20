from glob import glob as g
from json import load
from json import dumps

def main(path):
	lst=g(path+"*json")
	d={}
	for i in lst:
		with open(i) as in_put:
			data=load(in_put)
		d[i.split('/')[-1].split('.')[0]]=data
	save_json(d,path)
	return d

def save_json(d,path):
	d = dumps(d, sort_keys=True, indent=4, separators=(',', ': '))
	with open(path+"total.json","w") as out_put:
		out_put.write(d)
