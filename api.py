class ApiKey:
    def __init__(self, valid_api_key, invalid_api_key):
        self.validApiKey = valid_api_key
        self.invalidApiKey = invalid_api_key


class ApiGetUrl:
    def __init__(self):
        self.getUrl = "https://api.ocr.space/parse/imageurl?"


class ApiResponse:
    def __init__(self, response_text):
        self.OcrExitCode = response_text['OCRExitCode']
        if self.OcrExitCode == 1:
            self.IsErroredOnProcessing = response_text['IsErroredOnProcessing']
            self.ProcessingTimeInMilliseconds = response_text['ProcessingTimeInMilliseconds']
            self.SearchablePDFURL = response_text['SearchablePDFURL']
            self.ParsedResults = ParsedResults(response_text['ParsedResults'])
            self.ErrorDetails = None
            self.ErrorMessage = None
        else:
            self.IsErroredOnProcessing = response_text['IsErroredOnProcessing']
            self.ProcessingTimeInMilliseconds = response_text['ProcessingTimeInMilliseconds']
            # self.ErrorDetails = response_text['ErrorDetails']
            self.ErrorMessage = response_text['ErrorMessage'][0]
            self.ErrorDetails = None
            self.SearchablePDFURL = None
            self.ParsedResults = ParsedResults(None)


class ParsedResults:
    def __init__(self, parsed_results):
        if parsed_results is not None:
            self.ParsedText = parsed_results[0]['ParsedText']
            self.TextOrientation = parsed_results[0]['TextOrientation']
            self.ErrorDetails = parsed_results[0]['ErrorDetails']
            self.ErrorMessage = parsed_results[0]['ErrorMessage']
            self.FileParseExitCode = parsed_results[0]['FileParseExitCode']
            self.TextOverlay = TextOverlay(parsed_results[0]['TextOverlay'])
        else:
            self.ParsedText = None
            self.TextOrientation = None
            self.ErrorDetails = None
            self.ErrorMessage = None
            self.FileParseExitCode = None
            self.TextOverlay = None


class TextOverlay:
    def __init__(self, text_overlay):
        self.Message = text_overlay['Message']
        self.HasOverlay = text_overlay['HasOverlay']
        self.Lines = text_overlay['Lines']


class ValidJpeg:
    def __init__(self):
        self.Url = "https://www.pyimagesearch.com/wp-content/uploads/2017/06/example_01.png"
        self.ExpectedResult = "Noisy image to test Tesseract OCR"


class InvalidInput:
    def __init__(self):
        self.FilePath = "./ocrTestFiles/resources/invalid.txt"
        self.ExpextedResult = "File failed validation. File does not have a valid extension. " \
                              "Allowed file extensions: .pdf,.jpg,.png,.jpeg,.bmp,.gif,.tif,.tiff"
