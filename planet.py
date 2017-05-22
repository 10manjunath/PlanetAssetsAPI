__author__ = "Manjunath Babu"
__version__ = "1.0"
__email__ = "mababu@syr.edu"
__doc__ = """ planet.py: This is the Flask server code """

import re
from flask import Flask, jsonify, request
app = Flask(__name__)

# Sample Asset Store to test data and functionality
assetStore = []

# This list holds all required keys needed in an asset
ASSET_REQ_KEYS = ["asset name","asset type", "asset class"]

#This dictionary holds the asset type key associated with its acceptable asset class
ASSET_TYPE_CLASS = {"satellite":["dove","rapideye"],
				"antenna":["dish","yagi"]}

# Post data only if the parameters are valid
def parmsValidityCheck(data):
	assetName  = data['asset name']
	assetType  = data['asset type']
	assetClass = data['asset class']

# Check if all required parameters are present in the POST request
	for key in data.keys():
		if key not in ASSET_REQ_KEYS and key != 'asset details':
			return False, "Required Parameters Missing"  

# Checking for correct name format
	if not re.findall('^[a-z0-9A-Z][a-z0-9A-Z\_\-]{3,64}',assetName):
		return False, f"{assetName}: Asset name format is incorrect"

# Checking for duplicate asset name
	if assetName in [ele['asset name'] for ele in assetStore]:
		return False, f"{assetName}: Asset already exists. Cannot insert duplicates"

# Checking for valid asset class
	if assetType not in ASSET_TYPE_CLASS.keys(): 
		return False, f"{assetType}: Invalid Asset Type. Enter satellite or antenna only."

# Checking for valid asset type
	if assetClass not in ASSET_TYPE_CLASS[assetType]:
		return False, f"{assetClass}: Invalid Asset Class. Enter dove, rapideye, dish or yagi only"

# Checking for valid asset details. Only antennas can have details
	if(data.get('asset details')!=None):
		assetDetails = data['asset details']

# Check if there is a value in the asset details key
		if(len(assetDetails) > 0):
			if(assetType != "antenna"): #Check if asset type is antenna only
				return False, "Asset Details found. It is not for Satellites. Error"

# For dish class, there will be 2 attributes in a dictionary
			if(assetClass == "dish" ):
				if len(assetDetails)!=2 or "diameter" not in assetDetails.keys() or "radome" not in assetDetails.keys():
					return False, "Invalid entry found in Asset Details. Post only diameter and radome variables"
					#Dish assets have diameter and radome keys. Float and Bool respectively
				
# Radome attribute needs to be either true or false.
				if assetDetails['radome'].lower() not in ("true","false"):
					return False, f"{assetDetails['radome']}: Radome value is invalid. Needs to be a boolean. True or False only"

# Diameter attribute has to be a float only value
				try:
					float(assetDetails['diameter'])
				except:
					return False, f"{assetDetails['diameter']}: Diameter datatype is invalid. Needs to be float only"
					
# Gain attribute for yagi class has to be float only value
			if(assetClass == "yagi"):
				if len(assetDetails)!=1 or "gain" not in assetDetails.keys():
					return False, "Invalid entry found in Asset Details. Post only gain variable"
				try:
					float(assetDetails['gain'])
				except:
					return False, f"{assetDetails['gain']}: Gain datatype is invalid. Needs to be float only"
					
	return True, "POST SUCCESSFUL"

# POST request can only be done with header X-User set as admin.
def authenticationCheck():

	if(request.headers['X-User']!="admin"):
		return False
	else:
		return True


# Invalid URL results in Error 404.
@app.errorhandler(404)
def page_not_found(e):
    return jsonify({'Error Message':"Invalid URL. Try Again"})

# Handling for Error 500
@app.errorhandler(500)
def post_data_error(e):
    return jsonify({'Error Message':"POST json data format mismatch. Please review specifications"}) 


# Check if server is up and running
@app.route('/',methods=['GET'])
def checkAPI():
	return jsonify({'message': "Everything is up and running. Welcome to Planet Labs Coding Test. Code Written by Manjunath Babu. Find me on Github https://github.com/10manjunath"})


# Get all assets
@app.route('/planet', methods=['GET'])
@app.route('/planet/', methods=['GET'])
def returnAll():
	return jsonify({'assetStore':assetStore})

# Get sprcific asset name
@app.route('/planet/<string:name>', methods=['GET'])
def returnOne(name):
	asset = [someAsset for someAsset in assetStore if someAsset['asset name']==name]
	if asset:
		return jsonify({'Found Asset':asset[0]})
	else:
		return jsonify({'Error Message':f"{name} not found"})  

# Filtering for asset type or asset class
@app.route('/planet/filter/<string:classORtype>', methods=['GET'])
def returnFew(classORtype):
	if classORtype in ASSET_TYPE_CLASS:
		return jsonify({f'filtered {classORtype}\'s':list(filter(lambda asset:asset['asset type']==classORtype,assetStore))})
		
	for val in ASSET_TYPE_CLASS.values():
		if classORtype in val:
			return jsonify({f'filtered {classORtype}\'s':list(filter(lambda asset:asset['asset class']==classORtype,assetStore))})
			
	return jsonify({'Error Message':"Invalid Asset Type or Asset Class. Unable to Filter. Filter with words satellite, antenna, dove, rapideye, dish or yagi only"})



#Post one asset
@app.route('/planet', methods=['POST'])
def addOneAsset():
	# if(request.headers['X-User']!="admin"):
	# 	return "Invalid User. Try again"

	if not authenticationCheck():
		return jsonify({'Error Message':'Invalid Credentials. Please try again'})

	postData = request.get_json()

	ret = parmsValidityCheck(postData)
	if(ret[0]==False):
		return jsonify({'Error Message':ret[1]})

	asset = {"asset name": request.json['asset name'],
			   "asset type": request.json['asset type'],
			   "asset class": request.json['asset class']}

	if(request.json.get('asset details')!=None):
		asset['asset details'] = request.json['asset details']

	assetStore.append(asset)
	return jsonify({'assetStore':assetStore})


if __name__ == '__main__':
	app.run(debug=False)

