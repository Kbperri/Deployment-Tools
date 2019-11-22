import arcpy

class Toolbox(object):
    def __init__(self):
        """Define the toolbox (the name of the toolbox is the name of the
        .pyt file)."""
        self.label = "Deployment Tools"
        self.alias = "deploy"

        # List of tool classes associated with this toolbox
        self.tools = [CreateSDFileTool]


class CreateSDFileTool(object):
    def __init__(self):
        """Define the tool (tool name is the name of the class)."""
        self.label = "Create SD File"
        self.description = "Creates an SD file to a GP service"
        self.canRunInBackground = False

    def getParameterInfo(self):
        """Define parameter definitions"""
        params = None

        configFile = arcpy.Parameter(
            name="configFile",
            displayName="Config File",
            direction="Input",
            datatype="DEFile",
            parameterType="Required",
        )

        configFile.value = r"C:\Users\kyle9645\Documents\GitHub\Deployment-Tools\CreateSDFile Config.json"

        params = [configFile]
        return params

    def isLicensed(self):
        """Set whether tool is licensed to execute."""
        return True

    def updateParameters(self, parameters):
        """Modify the values and properties of parameters before internal
        validation is performed.  This method is called whenever a parameter
        has been changed."""
        return

    def updateMessages(self, parameters):
        """Modify the messages created by internal validation for each tool
        parameter.  This method is called after internal validation."""
        return

    def execute(self, parameters, messages):
        """The source code of the tool."""
        import CreateSDFile
        CreateSDFile.CreateSDFile(parameters[0].valueAsText)
        return
