import PIL.Image,json
from google import genai

client = genai.Client(api_key="AIzaSyAXsXien4tk2w4H79_aLhNCYoDlY9vmZfs")


def img_cmp(expected_img_path, taken_img_path):
    print("Entered comp")
    
    try:
        expected_img = PIL.Image.open(expected_img_path)
        taken_img = PIL.Image.open(taken_img_path)
        
        prompt = """
        Analyze the LED light in both images.
        1. Identify the color of the LED in the 'Expected' image.
        2. Identify the color of the LED in the 'Taken' image.
        3. Compare them.

        Return the result in this exact format:
        RESULT: [PASS/FAIL]
        COLOR: [Name of the color found]
        DETAILS: [Brief explanation if they don't match]
        """

        response = client.models.generate_content(
            model="gemini-2.5-flash", # Latest fast model
            contents=[prompt, expected_img, taken_img],
            config={
                'response_mime_type': 'application/json',
            }
        )

        data = json.loads(response.text)
        print(type(data))
        print(data)
        
        return False if data["RESULT"] == "FAIL" else True
        
    except Exception as e:
        print(f"An error occured: {e}")
       

    
