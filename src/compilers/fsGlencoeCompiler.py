from fsBaseCompiler import BaseCompiler
import json


class GlencoeCompiler(BaseCompiler):
    """"""

    schema = json.load(open("../schema/GlencoeCompiler.schema.json"))
    protectedKeys = ["extra_params", "name_prepend", "name_append", "filetype"]
    argMap = {
        "max_processes": "--max_workers=",
        "pyramid_downsample_type": "--downsample_type=",
        "pyramid_resolutions": "-r=",
        "series": "-s=",
        "tile_size_x": "-w=",
        "tile_size_y": "-h=",
    }
    argMapTiff = {"rgb": "--rgb", "max_processes": "--max_workers="}

    def _wrap_args(self) -> "tuple[list[str],list[str]]":
        output = ([], [])  # bf2raw, raw2ome
        zarr = self.argMap
        tiff = self.argMapTiff
        for arg in self.json:
            # if has an argMap entry, wrap the arg
            if zarr.get(arg) is not None:
                output[0].append(str(zarr[arg]) + str(self.json[arg]))
            if tiff.get(arg) is not None:
                output[1].append(str(tiff[arg]) + str(self.json[arg]))

    def compile(self, file):
        """Compiles self.json into glencoe calls then outputs to self.build"""
        bf2raw = {"input": "", "output": "", "args": []}
        raw2ome = {"output": "", "args": []}
        ft = self.json["filetype"]

        bf2raw["args"], raw2ome["args"] = self._wrap_args()

        bf2raw["input"] = file

        # TODO
        name = "need to properly steal this"
        path = "/path"
        outdir = path
        output = outdir + name

        if ft == "zarr":
            bf2raw["output"] = output
        else:
            bf2raw["output"] = "/tempdir/"  # also input of raw2ome
            raw2ome["output"] = output

        zarrCmd = [bf2raw["input"], bf2raw["output"], bf2raw["args"]]

        if ft != "zarr":
            tiffCmd = [bf2raw["output"], raw2ome["output"], raw2ome["args"]]

        self.build = [zarrCmd, tiffCmd] if tiffCmd else [zarrCmd]
