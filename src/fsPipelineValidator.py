import shutil

class PipelineValidator:
    """ Looks at json pipeline, then dies and/or complains if bad settings are given """
    
    
    def validateGlencoe(preimport):
        """ Check options for glencoe converters """
        fail=[]
        warn=[]
        
        # find glencoe tools
        bfToRaw = shutil.which('bioformats2raw')
        if bfToRaw == None:
            fail.append("Glencoe bioformats2raw command not found on PATH") 
            
        rawToOme = shutil.which('raw2ometiff')
        if rawToOme == None:
            warn.append("Glencoe raw2ometiff command not found on PATH") 
            
        # validate filetype before loop
        try:
            with str(preimport["file_type"]).lower() as ft:
                values=("ome.tiff","zarr")
                
                if ft == None:
                    warn.append("Filetype not defined, using default (ome.tiff)")
                    preimport["file_type"] = "ome.tiff"
                    
                elif ft not in values:
                    fail.append(f"'{ft}' is not a supported file format") 
                    
                elif ft == "ome.tiff" and rawToOme == None:
                    warn=[] # only possible warning so far is one we want to upgrade to fail
                    fail.append("The glencoe ome.tiff script (raw2ometiff) is missing, either switch to bioformats or add raw2ometiff to your PATH")
        
        except KeyError:
            warn.append("Filetype not defined, using default (ome.tiff)")
        except:
            warn.append(f"file_type:{ft} - caused unknown issues")
            
        # check rest of keys
        for key in preimport.keys():
            # check supported compression formats
            with key.lower() as k:    
                if k == "file_type" or k ==~ '.*comment':
                    continue
                
                elif k == "compression":
                    with str(preimport[key]).lower() as cf:#
                        tiffFormats=("lzw", "uncompressed", "jpeg-2000 lossy", "jpeg-2000", "jpeg", "zlib")
                        zarrFormats=("null", "raw", "zlib", "blosc")
                    
                        values = zarrFormats if ft == "zarr" else tiffFormats
                        if cf not in values:
                            fail.append(f"'{cf}' is not a supported compression format") 
                
                elif k == "tile_size_x":
                    try: 
                        int(preimport[key])
                    except: 
                        fail.append(f"tile_size_x:{preimport[key]} - is not an integer") 
                
                elif k == "tile_size_y":
                    try: 
                        int(preimport[key])
                    except: 
                        fail.append(f"tile_size_y:{preimport[key]} - is not an integer") 
                        
                elif k == "channel":
                    try: 
                        int(preimport[key])
                    except: 
                        fail.append(f"channel:{preimport[key]} - is not an integer") 
                
                elif k == "z_index":
                    try: 
                        int(preimport[key])
                    except: 
                        fail.append(f"z_index:{preimport[key]} - is not an integer") 
                
                elif k == "series":
                    try: 
                        if len(list(preimport[key])) < 1: 
                            fail.append(f"Why did you give an empty list to series? Not allowed.")
                    except: 
                        fail.append(f"tile_size_y:{preimport[key]} - is not a list") 
                
                elif k == "pyramid_resolutions":
                    try: 
                        int(preimport[key])
                    except: 
                        fail.append(f"pyramid_resolutions:{preimport[key]} - is not an integer") 
            
                elif k == "pyramid_downsample_type":
                    with str(preimport[key]).upper() as pdt:
                        values=("SIMPLE","GAUSSIAN","AREA","LINEAR","CUBIC","LANCZOS")
                        if pdt not in values:
                            fail.append(f"pyramid_downsample_type:{preimport[key]} - is not a supported downsample technique")
                
                elif k == "rgb":
                    try:
                        if bool(preimport[key]) == False:
                            warn.append("Are you sure you don't want to mark this as rgb?")
                    except:
                        warn.append("Defaulting to rgb mode")
        
                elif k == "extra_params":
                    warn.append("extra parameters have no protections, bugs are almost guaranteed")
                    try:
                        list(preimport[key])    
                    except:
                        warn.append("even if only one set of extra params are provided, put it in an array to be safe")
                        preimport[key] = [preimport[key]]
                
                elif k == "pyramid_scale":
                    warn.append(f"pyramid_scale param is Bioformats exclusive and has no effect on Glencoe tools")
                
                elif k == "noflat":
                    warn.append("Noflat param is Bioformats exclusive and has no effect on Glencoe tools")

                elif k == "bigtiff":
                    warn.append("bigtiff param is Bioformats exclusive and has no effect on Glencoe tools")
                
                elif k == "timepoint":
                    warn.append("timepoint param is Bioformats exclusive and has no effect on Glencoe tools")
                    
                else: 
                    warn.append(f"Unrecognized param:{key}")
                
        return fail, warn
        
        
    def validateBioformats(preimport):
        """ Check options for bfconvert """
        fail=[]
        warn=[]
        
        # find bioformats tool
        bfToRaw = shutil.which('bfconvert')
        if bfToRaw == None:
            fail.append("OME bfconvert command not found on PATH") 

        # need a file_type val; ome.tiff default
        try:
            if preimport['file_type'] == None:
                warn.append("Filetype not defined, using default (ome.tiff)")
                preimport['file_type'] = "ome.tiff"
        except KeyError:
            warn.append("Filetype not defined, using default (ome.tiff)")
            preimport["file_type"] = "ome.tiff"
            
        # check supported file formats    
        ft = str(preimport['file_type']).lower()
        tiffs=("ome.tiff","ome.tif","ome.btf","ome.tf2","ome.tf8","tiff","tif","btf","tf2","tf8")
        values=("png","avi","ch5","dcm","eps","epsi","ids","ics","jpeg","jpg",
                "jpe","jp2","java","ome","ome.xml","mov","v3draw","wlz")
        
        if ft not in values and ft not in tiffs:
            fail.append(f"'{ft}' is not a supported file format") 
            
        # check rest of keys
        for key in preimport.keys():
            # check supported compression formats
            with key.lower() as k:
                if k == "file_type" or k ==~ '.*comment':
                    continue
                
                elif k == "compression":
                    with str(preimport[key]).lower() as cf:
                        tiffFormats=("lzw", "uncompressed", "jpeg-2000 lossy", "jpeg-2000", "jpeg", "zlib")
                        dicomFormats=("uncompressed", "jpeg", "jpeg-2000")
                        jpegFormats=("jpeg-2000 lossy", "jpeg-2000")
                        xmlFormats=("uncompressed","zlib")

                        if ft in tiffs:
                            values=tiffFormats
                        elif ft == "dcm":
                            values=dicomFormats
                        elif ft == "jp2":
                            values=jpegFormats
                        elif ft == "ome" or "ome.xml":
                            values=xmlFormats
                        else:
                            warn.append(f"Cannot confirm compression is compatible with desired file type")
                            values=tiffFormats

                        if cf not in values:
                            fail.append(f"'{cf}' is not a supported compression format") 
                
                elif k == "tile_size_x":
                    try: 
                        int(preimport[key])
                    except: 
                        fail.append(f"tile_size_x:{preimport[key]} - is not an integer") 
                
                elif k == "tile_size_y":
                    try: 
                        int(preimport[key])
                    except: 
                        fail.append(f"tile_size_y:{preimport[key]} - is not an integer") 
                        
                elif k == "channel":
                    try: 
                        int(preimport[key])
                    except: 
                        fail.append(f"channel:{preimport[key]} - is not an integer") 
                
                elif k == "z_index":
                    try: 
                        int(preimport[key])
                    except: 
                        fail.append(f"z_index:{preimport[key]} - is not an integer") 
                
                elif k == "series":
                    try: 
                        if len(list(preimport[key])) != 2: 
                            fail.append(f"Only allowed to given an inclusive range to bfconvert's series param")
                    except: 
                        fail.append(f"tile_size_y:{preimport[key]} - is not a list") 
                
                elif k == "timepoint":
                    try: 
                        int(preimport[key])
                    except: 
                        fail.append(f"timepoint:{preimport[key]} - is not an integer") 
                
                elif k == "pyramid_resolutions":
                    try: 
                        int(preimport[key])
                    except: 
                        fail.append(f"pyramid_resolutions:{preimport[key]} - is not an integer") 
                
                elif k == "pyramid_scale":
                    try:
                        float(preimport[key])
                    except:
                        fail.append(f"pyramid_scale:{preimport[key]} - is not a floating point number")
                
                elif k == "noflat":
                    try:
                        bool(preimport[key])
                    except:
                        fail.append(f"noflat:{preimport[key]} - is not a boolean")

                elif k == "bigtiff":
                    try:
                        if bool(preimport[key]) == False:
                            warn.append("Are you sure you want to completely disable bigtiff?")
                    except:
                        fail.append(f"bigtiff:{preimport[key]} - is not a boolean")
        
                elif k == "extra_params":
                    warn.append("extra parameters have no protections, bugs are almost guaranteed")
                    try:
                        if len(list(preimport[key])) < 1:
                            fail.append("Don't define an empty list >:(")
                    except:
                        warn.append("even if only one set of extra params are provided, put it in an array to be safe")
                        preimport[key] = [preimport[key]]
            
                elif k == "pyramid_downsample_type":
                    warn.append("pyramid_downsample_type is a Glencoe exclusive and will have no effects on Bioformats tools")
                    
                else:
                    warn.append(f"Unrecognized param:{key}")
                
        return fail, warn
        
        
    def validate(json):
        """Checks required inputs and reports bad settings"""
        fail = []
        warn = []
        
        if json.preimport == None and json.postimport == None: 
            fail.append("No meaningful pipeline defined, just use dropbox or make sure your json is written correct") #TODO
        #####
        # preimport
        #####
        if json.preimport:
            # if converter undefined, bioformats is default
            if json.preimport.converter == None:
                json.preimport.converter = "bioformats"
                
            # check supported converters
            with str(json.preimport.converter).lower() as converter:
                if converter == "glencoe":
                    result = PipelineValidator.validateGlencoe(json.preimport)
                else:
                    if converter != "bioformats":
                        warn.append("converter not recognized, using default converter (bioformats)") #TODO 
                    result = PipelineValidator.validateBioformats(json.preimport)
                fail.extend(result[0])
                warn.extend(result[1])
        
        #####
        # import args
        ##### TODO
        
        #####
        # postimport
        #####
        if type(json.postimport) == list:
            reqVars = []
            for script in json.postimport:
                varQueue = []
                for key in script.keys():
                    if key == "script_id":
                        check # TODO script existence check
                    elif key == "imageVarName":
                        check # TODO param existence check
                    else:
                        # request to send to a variable later
                        if script[key] != "PIPE_OUT":
                            varQueue.append(key)
                            
                for key in reqVars:
                    check # TODO param existence check
                
                if script.script_id == None or script.imageVarName == None:
                    fail.append("") # TODO
                    
                reqVars = varQueue
                
        elif json.postimport:
            fail.append("postimport formatted improperly, post import should be an array of OMERO.script runs") # TODO
            
        # report warnings
        if len(warn) > 0:
            report # TODO
        
        # report failures and die
        if len(fail) > 0:
            die # TODO
        
            