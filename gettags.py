from clarifai.client import ClarifaiApi
import pprint
pp = pprint.PrettyPrinter(indent=2)

clarifai_api = ClarifaiApi('_IKyhCSHnFAqoJ-UdXc1fm0K7q4nXWiIpysjKl2F',
                           'rIJ3yNCKQyunlrx6AIRvu7XJIZ4-oTXgCMiH1-7A')
# result = clarifai_api.tag_images(open("0.jpeg", "rb"))
with open('0.jpeg', 'rb') as image_file:
    response = clarifai_api.tag_images(image_file)

tags = response["results"][0]["result"]
pp.pprint(tags["tag"]["classes"])
# print tags['tags']['classes']
