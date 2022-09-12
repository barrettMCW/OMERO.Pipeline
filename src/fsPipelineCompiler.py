from tempfile import gettempdir


class PipelineCompiler:
    preimportFields = ("bigtiff","channel","compression","converter","extra_params","file_type","name_append",
                       "name_prepend","noflat","num_processes","padded_pattern","pyramid_downsample_type",
                       "pyramid_resolutions","pyramid_scale","series","tile_size_x","tile_size_y","timepoint","z_index")
    
    def compileGlencoe(preimport, filename):
        """ Extracts Glencoe bioformats2raw and raw2ometiff commands from json obj """
        build = []
        bf2raw = {
            "input":f"",
            "output":f"",
            "args":[],
            "unsafe_args":""
        }
        raw2ome = {
            "output":f"",
            "args":[],
            "unsafe_args":""
        }
        ft = preimport["file_type"]
        
        #TODO get real data from somewhere
        name = "fake"
        outputPath="/fake/path"

        bf2raw["input"] = filename
            
        if ft == "zarr":
            bf2raw["output"] = name
        else:
            raw2ome["output"] = name
            
        try: 
            if bool(preimport["rgb"]):
                raw2ome["args"].append("--rgb")
        except:
            raw2ome["args"].append("--rgb")
        
        # convert pipe settings to glencoe tool settings
        for field in preimport.keys():
            try: 
                setting = preimport[field]
                if field == "compression":
                    if ft == "zarr":
                        bf2raw["args"].append(f"--compression {setting}")
                    else:
                        bf2raw["args"].append(f"--compression raw")
                        raw2ome["args"].append(f"--compression {setting}")
                        
                elif field == "extra_params" :
                    bf2raw["unsafe_args"] = setting[0]
                    if len(setting) > 1:
                        raw2ome["unsafe_args"] = setting[1]
                        
                elif field == "name_append":
                    if ft == "zarr":
                        bf2raw["output"] = setting + bf2raw["output"]
                    else:
                        raw2ome["output"] = setting + raw2ome["output"]
                
                elif field == "name_prepend":
                    if ft == "zarr":
                        bf2raw["output"] += setting
                    else:
                        raw2ome["output"] += setting
                
                elif field == "num_processes":
                    bf2raw["args"].append(f"--max_workers={setting}")
                    raw2ome["args"].append(f"--max_workers={setting}")
                    
                elif field == "pyramid_downsample_type":
                    bf2raw["args"].append(f"--downsample_type={setting}")
                    
                elif field == "pyramid_resolutions":
                    bf2raw["args"].append(f"-r={setting}")
                
                elif field == "series":
                    bf2raw["args"].append(f"-s={setting}")
                    
                elif field == "tile_size_x":
                    bf2raw["args"].append(f"-w={setting}")
                
                elif field == "tile_size_y":
                    bf2raw["args"].append(f"-h={setting}")
                
                elif field == "z_index":
                    bf2raw["args"].append(f"-z={setting}")
            except Exception as e:
                print(e)
                continue
            
        if ft == "zarr":
            bf2raw["output"] = f"{outputPath}/{bf2raw['output']}"
        else:
            bf2raw["output"] = gettempdir()
            raw2ome["output"] = f"{outputPath}/{raw2ome['output']}.{ft}"
        
        #compile bioformats2raw command
        bioformats2raw=["bioformats2raw"]
        bioformats2raw.append(bf2raw["input"])
        bioformats2raw.append(bf2raw["output"])
        for arg in bf2raw["args"]:
            bioformats2raw.append(arg)
        bioformats2raw.append(bf2raw["unsafe_args"])
        build.append(bioformats2raw)
        
        # compile raw2ometiff
        if ft != "zarr":
            raw2ometiff=["raw2ometiff"]
            raw2ometiff.append(bf2raw["output"]) # input
            raw2ometiff.append(raw2ome["output"])
            for arg in raw2ome["args"]:
                raw2ometiff.append(arg)
            raw2ometiff.append(raw2ome["unsafe_args"])
            build.append(raw2ometiff)

        return build
                    
    def compileBioformats(preimport, filename):
        """ Extracts Bioformats bfconvert commands from json obj"""
        build = []
        bfconvert = {
            "input":"",
            "output":"",
            "args":""
        }
            
    def compile(json, filename):
        """ Calls all compilers and returns a full build to be used by ?PipelineClient? TODO"""
        build = {}
        # build preimport
        try:
            with str(json['preimport']).lower() as pi:
                if pi['converter'] == "glencoe":
                    build["preimport"] = PipelineCompiler.compileGlencoe(pi, filename)
                else:
                    build["preimport"] = PipelineCompiler.compileBioformats(pi, filename)
        except:
            build = {}
        return build