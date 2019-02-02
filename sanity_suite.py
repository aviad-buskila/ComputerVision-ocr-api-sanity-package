import requests
from api import ApiKey, ApiGetUrl, ApiResponse, ValidJpeg, InvalidInput
import json
import datetime
import getpass


# get api keys (valid and invalid)
def api_key_initialize():
    with open("./ocrTestFiles/resources/validApiKey.txt", "r") as valid, \
            open("./ocrTestFiles/resources/invalidApiKey.txt") as invalid:
        valid_key = valid.readline()
        invalid_key = invalid.readline()
        keys = ApiKey(valid_key, invalid_key)
        return keys


# test key validation by the api for valid and invalid keys
def api_status_test(state):
    if state == "valid":
        key = api_key_initialize().validApiKey
    else:
        key = api_key_initialize().invalidApiKey
    endpoint_url = ApiGetUrl().getUrl
    payload = {'apikey': key}
    r = requests.get(endpoint_url, data=payload)
    status_code = r.status_code
    return status_code


# test api response with valid image file from a url
def test_valid_input_url(url):
    key = api_key_initialize().validApiKey
    endpoint_url = ApiGetUrl().getUrl
    payload = {'apikey': key,
               'url': url}
    r = requests.get(endpoint_url, data=payload)
    return r.content.decode('utf-8')


# test api response with local invalid input
def test_invalid_input_file(input_file):
    key = api_key_initialize().validApiKey
    payload = {'apikey': key}
    with open(input_file, 'rb') as f:
        r = requests.post('https://api.ocr.space/parse/image',
                          files={input_file: f},
                          data=payload,
                          )
    return r.content.decode('utf-8')


# readable date and time for logs and result
def prettify_now():
    return datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")


# sanity suite implementation
def sanity():
    time_stamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    results_file_name = time_stamp + "_sanity_results.txt"
    log_file_name = time_stamp + "_sanity_log.txt"
    initiator = getpass.getuser()

    with open("./ocrTestFiles/results/" + results_file_name, "w") as results, \
            open("./ocrTestFiles/results/" + log_file_name, "w") as log:

        log.writelines("Sanity test initiated at " + prettify_now() + " by " + initiator + '\n')
        results.writelines("Sanity test initiated at " + prettify_now() + " by " + initiator + '\n')
        # initiate all flags to false, a True attribute would be assigned in case of pass scenario
        status = False
        valid = False
        invalid = False

        #Test API status
        log.writelines("Testing API status " + prettify_now() + '\n')
        results.writelines("Testing API status " + prettify_now() + '\n')
        try:
            api_status = [api_status_test("valid"), api_status_test("invalid")]
            log.writelines("Finished testing API status at " + prettify_now() + '\n')
            # expected statuses of 200 for valid and 403 for invalid key
            if api_status == [200, 403]:
                results.writelines("API status test passed " + prettify_now() + '\n')
                status = True
            else:
                results.writelines("API status test failed " + prettify_now() + '\n')
        except:
            log.writelines("API status testing crashed at " + prettify_now() + '\n')

        #Test valid input processing via get
        results.writelines("Testing valid input processing via url GET API call " + prettify_now() + '\n')
        log.writelines("Testing valid input processing via url GET API call " + prettify_now() + '\n')
        try:
            # initialize an instance of valid input for url get call
            valid_input = ValidJpeg()
            response = test_valid_input_url(valid_input.Url)
            valid_input_url_result = ApiResponse(json.loads(response.replace('\r\n', '')))
            log.writelines("Finished testing valid input processing at " + prettify_now() + '\n')
            # in case of exit code 1 and the correct expected result, scenario passes
            if valid_input_url_result.OcrExitCode == 1 and \
                    valid_input_url_result.ParsedResults.ParsedText == valid_input.ExpectedResult:
                results.writelines("Valid input test passed at " + prettify_now() + '\n')
                valid = True
            else:
                results.writelines("Valid input test failed at " + prettify_now() + '\n')
        except Exception as e:
            # an exception to cover crashed cases (i.e. local connection lost, etc.)
            results.writelines(str(e) + '/n')
            log.writelines("Valid input processing via url get API call crashed " + prettify_now() + '\n')

        #Test invalid input processing via post
        results.writelines("Testing invalid input processing via POST API call " + prettify_now() + '\n')
        log.writelines("Testing invalid input processing via POST API call " + prettify_now() + '\n')
        try:
            # initialize an instance of invalid input for file post call
            invalid_input = InvalidInput()
            response = test_invalid_input_file(invalid_input.FilePath)
            invalid_input_result = ApiResponse(json.loads(response.replace('\r\n', '')))
            log.writelines("Finished testing invalid input processing at " + prettify_now() + '\n')
            # in case of exit code 3 and the correct expected result, scenario passes
            if invalid_input_result.OcrExitCode == 3 and \
                    invalid_input_result.ErrorMessage == invalid_input.ExpextedResult:
                results.writelines("Invalid input test passed at " + prettify_now() + '\n')
                invalid = True
            else:
                results.writelines("Invalid input test failed at " + prettify_now() + '\n')
        # an exception to cover crashed cases (i.e. local connection lost, etc.)
        except Exception as e:
            results.writelines(str(e) + '/n')
            log.writelines("Invalid input processing via POST API call crashed " + prettify_now() + '\n')
        log.close()
        results.close()
        # destruct instances
        del valid_input
        del invalid_input
    # preparation of function return value - result file path and boolean value for pass or fail, all scenarios must
    # pass in order for sanity to pass
    sanity_results = (results_file_name, (status and valid and invalid))
    return sanity_results


def main():
    results = sanity()
    if results[1]:
        print "Sanity passed"
    else:
        print "Sanity failed"
    print "Sanity suite finished at " + prettify_now() + " results are at " + results[0] + '\n'


main()
