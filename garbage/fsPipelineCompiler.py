""" Compiles JSON into various commands """
from tempfile import gettempdir

preimportFields = (
    "bigtiff",
    "channel",
    "compression",
    "converter",
    "extra_params",
    "file_type",
    "name_append",
    "name_prepend",
    "noflat",
    "num_processes",
    "padded_pattern",
    "pyramid_downsample_type",
    "pyramid_resolutions",
    "pyramid_scale",
    "series",
    "tile_size_x",
    "tile_size_y",
    "timepoint",
    "z_index",
)


def _glencoe_format_zarr_args(preimport, bf2raw):
    for field in preimport.keys():
        setting = preimport[field]
        if field == "compression":
            bf2raw["args"].append(f"--compression {setting}")

        elif field == "extra_params":
            bf2raw["unsafe_args"] = setting[0]

        elif field == "num_processes":
            bf2raw["args"].append(f"--max_workers={setting}")

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


def _glencoe_format_tiff_args(preimport, bf2raw, raw2ome):
    for field in preimport.keys():
        setting = preimport[field]
        if field == "compression":
            bf2raw["args"].append("--compression raw")
            raw2ome["args"].append(f"--compression {setting}")

        elif field == "extra_params":
            bf2raw["unsafe_args"] = setting[0]
            if len(setting) > 1:
                raw2ome["unsafe_args"] = setting[1]

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


def compile_glencoe(preimport, filename):
    """Compiles bash commands for Glencoe tools"""
    build = []
    bf2raw = {"input": "", "output": "", "args": [], "unsafe_args": ""}
    raw2ome = {"output": "", "args": [], "unsafe_args": ""}
    file_type = preimport["file_type"]

    # TODO get real data from somewhere
    name = "fake"
    out_path = "/fake/path"

    # first stop, infile to zarr
    bf2raw["input"] = filename

    #
    if file_type == "zarr":
        # out_base
        bf2raw["output"] = name
        # out_append/prepend
        bf2raw["output"] += preimport["name_append"]
        bf2raw["output"] = preimport["name_prepend"] + bf2raw["output"]
        # out_path
        bf2raw["output"] = f"{out_path}/{bf2raw['output']}"
    else:
        # out_base
        raw2ome["output"] = name

        raw2ome["output"] += preimport["name_append"]
        raw2ome["output"] = preimport["name_prepend"] + raw2ome["output"]

        bf2raw["output"] = gettempdir()
        raw2ome["output"] = f"{out_path}/{raw2ome['output']}.{file_type}"

    # TODO move to validator
    if bool(preimport["rgb"]) or preimport["rgb"] is None:
        raw2ome["args"].append("--rgb")

    # compile bioformats2raw command
    bioformats2raw = ["bioformats2raw"]
    bioformats2raw.append(bf2raw["input"])
    bioformats2raw.append(bf2raw["output"])
    for arg in bf2raw["args"]:
        bioformats2raw.append(arg)
    bioformats2raw.append(bf2raw["unsafe_args"])
    build.append(bioformats2raw)

    # compile raw2ometiff
    if file_type != "zarr":
        raw2ometiff = ["raw2ometiff"]
        raw2ometiff.append(bf2raw["output"])  # input
        raw2ometiff.append(raw2ome["output"])
        for arg in raw2ome["args"]:
            raw2ometiff.append(arg)
        raw2ometiff.append(raw2ome["unsafe_args"])
        build.append(raw2ometiff)
    return build


def compileBioformats(preimport, filename):
    """Extracts Bioformats bfconvert commands from json obj"""
    build = []
    bfconvert = {"input": "", "output": "", "args": ""}


def compile(json, filename):
    """Calls all compilers and returns a full build to be used by ?PipelineClient? TODO"""
    build = {}
    # build preimport
    try:
        with str(json["preimport"]).lower() as pi:
            if pi["converter"] == "glencoe":
                build["preimport"] = PipelineCompiler.compileGlencoe(pi, filename)
            else:
                build["preimport"] = PipelineCompiler.compileBioformats(pi, filename)
    except:
        build = {}
    return build
