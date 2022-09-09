class PipelineCompiler:
    def compileGlencoe(preimport, filename):
        """ Extracts Glencoe bioformats2raw and raw2ometiff commands from json obj """
        build = []
        for key in preimport.keys():
            """"""
            
    def compileBioformats(preimport, filename):
        """ Extracts Bioformats bfconvert commands from json obj"""
            
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