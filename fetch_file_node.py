import requests
import os

class FetchFileNode:
    """
    A node that fetches a file from a URL and saves it to a specified output path.

    Class methods
    -------------
    INPUT_TYPES (dict): 
        Tell the main program input parameters of nodes.
    IS_CHANGED:
        optional method to control when the node is re executed.

    Attributes
    ----------
    RETURN_TYPES (`tuple`): 
        The type of each element in the output tuple.
    RETURN_NAMES (`tuple`):
        Optional: The name of each output in the output tuple.
    FUNCTION (`str`):
        The name of the entry-point method. For example, if `FUNCTION = "execute"` then it will run FetchFileNode().execute()
    OUTPUT_NODE ([`bool`]):
        If this node is an output node that outputs a result/image from the graph. The SaveImage node is an example.
        Assumed to be False if not present.
    CATEGORY (`str`):
        The category the node should appear in the UI.
    execute(s) -> tuple || None:
        The entry point method. The name of this method must be the same as the value of property `FUNCTION`.
        For example, if `FUNCTION = "execute"` then this method's name must be `execute`, if `FUNCTION = "foo"` then it must be `foo`.
    """
    def __init__(self):
        pass
    
    @classmethod
    def INPUT_TYPES(s):
        """
            Return a dictionary which contains config for all input fields.
            Some types (string): "MODEL", "VAE", "CLIP", "CONDITIONING", "LATENT", "IMAGE", "INT", "STRING", "FLOAT".
            Input types "INT", "STRING" or "FLOAT" are special values for fields on the node.
            The type can be a list for selection.

            Returns: `dict`:
                - Key input_fields_group (`string`): Can be either required, hidden or optional. A node class must have property `required`
                - Value input_fields (`dict`): Contains input fields config:
                    * Key field_name (`string`): Name of a entry-point method's argument
                    * Value field_config (`tuple`):
                        + First value is a string indicate the type of field or a list for selection.
                        + Second value is a config for type "INT", "STRING" or "FLOAT".
        """
        return {
            "required": {
                "url": ("STRING", {
                    "multiline": False,
                    "default": "https://example.com/file.txt"
                }),
                "output_path": ("STRING", {
                    "multiline": False,
                    "default": "output/file.txt"
                }),
            },
            "optional": {
                "overwrite_local_file_if_exists": ("BOOL", {
                    "default": False
                }),
            },
        }

    RETURN_TYPES = ("STRING",)
    RETURN_NAMES = ("status",)

    FUNCTION = "execute"

    OUTPUT_NODE = True

    CATEGORY = "File Operations"

    def execute(self, url, output_path, overwrite_local_file_if_exists=False):
        try:
             # Get the absolute path of the script's directory
            script_dir = os.path.dirname(os.path.abspath(__file__))
            # Change the current working directory to the script's directory
            os.chdir(script_dir)

            # go up 2 directories
            os.chdir(os.path.join(os.getcwd(), "../../")) # now we are in the root directory

            final_output_path = os.path.join(os.getcwd(), output_path)

            if os.path.exists(final_output_path) and not overwrite_local_file_if_exists:
                return ("File already exists")

            # print that you are fetching the url
            print(f"Fetching file from {url} and saving to {final_output_path}")

            response = requests.get(url)
            response.raise_for_status()
            with open(output_path, 'wb') as file:
                file.write(response.content)
            return ("File fetched and saved successfully",)
        except Exception as e:
            return (f"Error: {e}",)


# Set the web directory, any .js file in that directory will be loaded by the frontend as a frontend extension
# WEB_DIRECTORY = "./somejs"

# Add custom API routes, using router
from aiohttp import web
from server import PromptServer

@PromptServer.instance.routes.get("/hello")
async def get_hello(request):
    return web.json_response("hello")

# A dictionary that contains all nodes you want to export with their names
# NOTE: names should be globally unique
NODE_CLASS_MAPPINGS = {
    "FetchFileNode": FetchFileNode,
}

# A dictionary that contains the friendly/humanly readable titles for the nodes
NODE_DISPLAY_NAME_MAPPINGS = {
    "FetchFileNode": "Fetch File Node",
    "PrintStatusNode": "Print Status Node",
}
