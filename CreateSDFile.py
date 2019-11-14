import arcpy
import json

def CreateSDFile(configFile):
    try:
        with open(configFile) as json_config:
            config = json.load(json_config)
    except Exception as e:
        arcpy.AddMessage("Failed to load config.")
        return
    
    try:
        toolbox = config["toolbox"]
        alias = config["alias"]
        toolName = config["toolName"]
        toolArgs = config["toolArgs"]
        sddraft = config["sdDraft"]
        sd = config["sd"]
        portalurl = config["portalURL"]
        portalusername = config["portalUsername"]
        portalpassword = config["portalPassword"]
        serverURL = config["serverURL"]
        serviceName = config["serviceName"]
        serverType = config["serverType"]
        connectionFilePath = config["connectionFilePath"]
        copyDataToServer = config["copyDataToServer"]
        folderName = config["folderName"]
        summary = config["summary"]
        tags = config["tags"]
        executionType = config["executionType"]
        resultMapServer = config["resultMapServer"]
        showMessages = config["showMessages"]
        maximumRecords = config["maximumRecords"]
        minInstances = config["minInstances"]
        maxInstances = config["maxInstances"]
        maxUsageTime = config["maxUsageTime"]
        maxWaitTime = config["maxWaitTime"]
        maxIdleTime = config["maxIdleTime"]
        constantValues = config["constantValues"]
    except KeyError as keyErr:
        arcpy.AddMessage(f"Config file missing value: {keyErr}")
        return
    except Exception as e:
        arcpy.AddMessage(f"Error occured in retreiving config values: {e}")
        return

    arcpy.AddMessage("Successfuly read all configuration values.")
    arcpy.ImportToolbox(toolbox, alias)
    arcpy.AddMessage(arcpy.GetMessages(0))
    customToolMethod = getattr(arcpy, f"{toolName}_{alias}")
    result = customToolMethod(*toolArgs)
    arcpy.AddMessage(arcpy.GetMessages(0))
    arcpy.SignInToPortal(portalurl, portalusername, portalpassword)
    arcpy.AddMessage(arcpy.GetMessages(0))

    analyzeMessages = arcpy.CreateGPSDDraft(
        result, sddraft, serviceName, server_type=serverType,
        connection_file_path=connectionFilePath,
        copy_data_to_server=copyDataToServer, folder_name=folderName,
        summary=summary, tags=tags, executionType=executionType,
        resultMapServer=resultMapServer, showMessages=showMessages, maximumRecords=maximumRecords,
        minInstances=minInstances, maxInstances=maxInstances, maxUsageTime=maxUsageTime, maxWaitTime=maxWaitTime,
        maxIdleTime=maxIdleTime, constantValues=constantValues
    )
    arcpy.AddMessage(arcpy.GetMessages(0))

    # Stage and upload the service if the sddraft analysis did not
    # contain errors
    if analyzeMessages['errors'] == {}:
        # Execute StageService
        arcpy.StageService_server(sddraft, sd)
        arcpy.AddMessage(arcpy.GetMessages(0))
        # Execute UploadServiceDefinition
        # Use URL to a federated server
        arcpy.UploadServiceDefinition_server(sd, serverURL)
        arcpy.AddMessage(arcpy.GetMessages(0))
    else:
        # If the sddraft analysis contained errors, display them
        print(analyzeMessages['errors'])

if __name__ == "__main__":
    configFile = arcpy.GetParameterAsText(0)
    CreateSDFile(configFile)
