# client Id : _IKyhCSHnFAqoJ-UdXc1fm0K7q4nXWiIpysjKl2F
# client secret : rIJ3yNCKQyunlrx6AIRvu7XJIZ4-oTXgCMiH1-7A
# access token : Q2gcWhP1S3dDGs9umXM5lGSiUcx60H
# http://words.bighugelabs.com/api/2/your-api-key/love/json

from clarifai.client import ClarifaiApi
import pprint, requests

pp = pprint.PrettyPrinter(indent=2)

clarifai_api = ClarifaiApi()

result = clarifai_api.tag_images(open("/Users/ashish/Downloads/IMG_20160819_185528.jpg", "rb"))
tags = result["results"][0]["result"]

pp.pprint(tags["tag"]["classes"])

word = "laptop"
apiKey = "f7b4e46cec678cc5c3a75a13c394605e"
url = "http://words.bighugelabs.com/api/2/"+apiKey+"/"+word+"/json"

req = requests.get(url)

if(req.status_code == requests.codes.ok):
	resp = req.text;
	pp.pprint(resp)
