__author__ = "Manjunath Babu"
__version__ = "1.0"
__email__ = "mababu@syr.edu"
__doc__ = """ test_planet.py: All tests included using pytest package """

import planet, random, requests, pytest, sys, json

planet.assetStore = []
API_URL = "http://127.0.0.1:5000"

def server_up(f, *args, **kwargs):
    def wraperFunc():
        try:
            requests.get(API_URL)
            return f(*args, **kwargs)
        except requests.ConnectionError:
            assert True, f"{API_URL} is down! Check the server."
    return wraperFunc

@server_up
def test_PlanetApplication():
	response = requests.get(f'{API_URL}/',headers={'Content-Type':'application/json'})
	assert response.ok, f"Error! {response.json()}"
	return response


@server_up
def test_GetAssetInvalidURL():
	response = requests.get(f'{API_URL}/plan',headers={'Content-Type':'application/json'})
	assert response.ok, f"Error! {response.json()}"
	return response

@server_up
def test_PostAssetInvalidURL():
	response = requests.post(f'{API_URL}/plan',
		headers={'Content-Type':'application/json','X-User':'admin'},
		json={"asset name":"Star100","asset type":"satellite","asset class":"dove"})
	assert response.ok, f"Error! {response.json()}"
	return response

sampleAssets = [{"asset name": "MarsLander", 	 "asset type": "satellite", "asset class": "dove"},
				{"asset name": "Earth2-0", 		 "asset type": "satellite", "asset class": "rapideye"},
				{"asset name": "PoleStarViewer", "asset type": "antenna",   "asset class": "dish", "asset details": {"diameter":"34.21", "radome":"False"}},
				{"asset name": "SkyScanner99", 	 "asset type": "antenna",   "asset class": "yagi", "asset details": {"gain":"1.21"}}]

@server_up
def test_post4SampleAssets():
	for someAsset in sampleAssets:
		response = requests.post(f'{API_URL}/planet',
			headers={'Content-Type':'application/json','X-User':'admin'}, 
			json=someAsset)
	assert response.ok, f"Error! {response.json()}"
	return response	

@server_up
def test_PostAssetWrongFormat():
	response = requests.post(f'{API_URL}/planet',
		headers={'Content-Type':'application/json','X-User':'admin'},
		json={"asset name":123,"asset type":"antenna","asset class":"yagi","asset details":{"gain":100.12}})
	assert response.ok, f"Error! {response.json()}"
	return response

@server_up
def test_GetAllAssets():
	response = requests.get(f'{API_URL}/planet',headers={'Content-Type':'application/json'})
	assert response.ok, f"Error! {response.json()}"
	return response

@server_up
def test_GetOneAvailableAsset():
	response = requests.get(f'{API_URL}/planet/MarsLander',headers={'Content-Type':'application/json'})
	assert response.ok, f"Error! {response.json()}"
	return response

@server_up
def test_GetOneUnavailableAsset():
	response = requests.get(f'{API_URL}/planet/SPY101',headers={'Content-Type':'application/json'})
	assert response.ok, f"Error! {response.json()}"
	return response

@server_up
def test_PostInvalidUser():
	response = requests.post(f'{API_URL}/planet',
		headers={'Content-Type':'application/json','X-User':'WhoIsIt'},
		json={"asset name":"SF-SAT","asset type":"satellite","asset class":"dove"})
	assert response.ok, f"Error! {response.json()}"
	return response

@server_up
def test_PostOneValidAsset():
	response = requests.post(f'{API_URL}/planet',
		headers={'Content-Type':'application/json','X-User':'admin'},
		json={"asset name":"SF-SAT","asset type":"satellite","asset class":"dove"})
	assert response.ok, f"Error! {response.json()}"
	return response

@server_up
def test_PostOneDuplicateAsset():
	response = requests.post(f'{API_URL}/planet',
		headers={'Content-Type':'application/json','X-User':'admin'},
		json={"asset name":"SF-SAT","asset type":"satellite","asset class":"dove"})
	assert response.ok, f"Error! {response.json()}"
	return response

@server_up
def test_PostOneInvalidAssetName():
	response = requests.post(f'{API_URL}/planet',headers={'Content-Type':'application/json','X-User':'admin'},
		json={"asset name":"123","asset type":"satellite","asset class":"dove"})
	assert response.ok, f"Error! {response.json()}"
	return response

@server_up
def test_PostOneInvalidAssetType():
	response = requests.post(f'{API_URL}/planet',headers={'Content-Type':'application/json','X-User':'admin'},
		json={"asset name":"SF-SD","asset type":"rocket","asset class":"dove"})
	assert response.ok, f"Error! {response.json()}"
	return response

@server_up
def test_PostOneInvalidAssetClass():
	response = requests.post(f'{API_URL}/planet',
		headers={'Content-Type':'application/json','X-User':'admin'},
		json={"asset name":"car101","asset type":"satellite","asset class":"car"})
	assert response.ok, f"Error! {response.json()}"
	return response

@server_up
def test_PostOneInvalidAssetDetailsDiameter():
	response = requests.post(f'{API_URL}/planet',
		headers={'Content-Type':'application/json','X-User':'admin'},
		json={"asset name":"EclipseChaser","asset type":"antenna","asset class":"dish","asset details":{"diameter":"a32.11a","radome":"true"}})
	assert response.ok, f"Error! {response.json()}"
	return response

@server_up
def test_PostOneInvalidAssetDetailsRadome():
	response = requests.post(f'{API_URL}/planet',
		headers={'Content-Type':'application/json','X-User':'admin'},
		json={"asset name":"Moon101","asset type":"antenna","asset class":"dish","asset details":{"diameter":"100.78","radome":"001trueFalsezz9"}})
	assert response.ok, f"Error! {response.json()}"
	return response



@server_up
def test_PostOneInvalidAssetDetailsGain():
	response = requests.post(f'{API_URL}/planet',
		headers={'Content-Type':'application/json','X-User':'admin'},
		json={"asset name":"NeptuneLander","asset type":"antenna","asset class":"yagi","asset details":{"gain":"zz300.2zz"}})
	assert response.ok, f"Error! {response.json()}"
	return response


@server_up
def test_PostOneInvalidAssetDetailsSatellite():
	response = requests.post(f'{API_URL}/planet',
		headers={'Content-Type':'application/json','X-User':'admin'},
		json={"asset name":"MarsTester","asset type":"satellite","asset class":"dove","asset details":{"diameter":"100.78","radome":"true"}})
	assert response.ok, f"Error! {response.json()}"
	return response

# ASSET_TYPE_CLASS = {"satellite":["dove", "rapideye"],
# 					  "antenna"  :["dish", "yagi"]}

@server_up
def test_post20RandomValidAssets():
	for i in range(1,21):
		assetType = random.choice(list(planet.ASSET_TYPE_CLASS.keys()))
		assetClass = random.choice(planet.ASSET_TYPE_CLASS[assetType])
		jsonVar = {"asset name":f'{assetType}_{i}',"asset type":assetType,"asset class":assetClass}
		
		if(assetType == "antenna"):
			if(assetClass == "dish"):
				jsonVar['asset details'] = {"diameter":random.random()*100.0 , "radome":random.choice(["True","False"])}
			if(assetClass == "yagi"):
				jsonVar['asset details'] = {"gain":random.random()*10.0}

		response = requests.post(f'{API_URL}/planet',
			headers={'Content-Type':'application/json','X-User':'admin'}, 
			json=jsonVar)
		jsonVar = []
	assert response.ok, f"Error! {response.json()}"
	return response	

@server_up
def test_GetFilteredDoves():
	response = requests.get(f'{API_URL}/planet/filter/dove',
		headers={'Content-Type':'application/json'})
	assert response.ok, f"Error! {response.json()}"
	return response

@server_up
def test_GetFilteredRapideyes():
	response = requests.get(f'{API_URL}/planet/filter/rapideye',
		headers={'Content-Type':'application/json'})
	assert response.ok, f"Error! {response.json()}"
	return response

@server_up
def test_GetInvalidFilter():
	response = requests.get(f'{API_URL}/planet/filter/nothing',
		headers={'Content-Type':'application/json'})
	assert response.ok, f"Error! {response.json()}"
	return response

@server_up
def test_GetFilteredSatellites():
	response = requests.get(f'{API_URL}/planet/filter/satellite',
		headers={'Content-Type':'application/json'})
	assert response.ok, f"Error! {response.json()}"
	return response

@server_up
def test_GetFilteredAntennas():
	response = requests.get(f'{API_URL}/planet/filter/antenna',
		headers={'Content-Type':'application/json'})
	assert response.ok, f"Error! {response.json()}"
	return response

#Execute specific test cases that's passed from the main function
def call_Test_Case(f,title):
	if not hasattr(call_Test_Case, "counter"):
		call_Test_Case.counter = 1
	print("\n"*5)
	print("*"*len(title))
	print(f"\tTest Case Number: {call_Test_Case.counter}")
	print(title)
	print("*"*len(title))
	response = f
	print(f"Testing_Response: {json.dumps(response.json(),indent=5)}")
	call_Test_Case.counter += 1

def main():

	print("Welcome to Planet Labs Asset Store Testing")

	call_Test_Case(test_PlanetApplication(), "GET Request:\n Check server if its up and running")

	call_Test_Case(test_GetAssetInvalidURL(), "GET Request:\n Get request from a malformed URL")

	call_Test_Case(test_PostAssetInvalidURL(), "POST Request:\n Post request to a malformed URL")

	call_Test_Case(test_post4SampleAssets(), "POST Request:\n Post 4 sample assets of all valid combinations of types and classes")

	call_Test_Case(test_PostAssetWrongFormat(), "POST Request:\n Post an asset with wrong json format")

	call_Test_Case(test_GetAllAssets(), "GET Request:\n Get all available assets")

	call_Test_Case(test_GetOneAvailableAsset(), "GET Request:\n Get one available asset")

	call_Test_Case(test_GetOneUnavailableAsset(), "GET Request:\n Get one unavailable asset")

	call_Test_Case(test_PostInvalidUser(), "POST Request:\n Post an asset with invalid X-User")

	call_Test_Case(test_PostOneValidAsset(),"POST Request:\n Post one valid asset")

	call_Test_Case(test_PostOneDuplicateAsset(),"POST Request:\n Post one duplicate asset")

	call_Test_Case(test_PostOneInvalidAssetName(), "POST Request:\n Post one asset with invalid asset name")

	call_Test_Case(test_PostOneInvalidAssetType(), "POST Request:\n Post one asset with invalid asset type")

	call_Test_Case(test_PostOneInvalidAssetClass(), "POST Request:\n Post one asset with invalid asset class")

	call_Test_Case(test_PostOneInvalidAssetDetailsDiameter(), "POST Request:\n Post one antenna asset with invalid diameter float value")

	call_Test_Case(test_PostOneInvalidAssetDetailsRadome(), "POST Request:\n Post one antenna asset with invalid radome bool value")

	call_Test_Case(test_PostOneInvalidAssetDetailsGain(), "POST Request:\n Post one antenna asset with invalid gain float value")

	call_Test_Case(test_PostOneInvalidAssetDetailsSatellite(), "POST Request:\n Post one satellite asset with invalid details that belongs to antenna type")

	call_Test_Case(test_post20RandomValidAssets(), "POST Request:\n Post 20 Randomly generated valid assets")

	call_Test_Case(test_GetFilteredDoves(),"GET Request:\n Filter all assets with only dove class")

	call_Test_Case(test_GetFilteredRapideyes() ,"GET Request:\n Filter all assets with only rapideye class")

	call_Test_Case(test_GetInvalidFilter() ,"GET Request:\n Try to filter with wrong class or type")

	call_Test_Case(test_GetFilteredSatellites(),"GET Request:\n Filter all assets with only type satellite")

	call_Test_Case(test_GetFilteredAntennas(),"GET Request:\n Filter all assets with only type antenna")

	print("\nSUCCESSFULLY COMPLETED ALL TESTS. \nTHANK YOU")


if(__name__ == '__main__'):
	print("Running all test cases")
	mainRet = main()
	sys.exit(mainRet)

