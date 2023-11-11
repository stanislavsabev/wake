# wake
Build tool for windows, similar to `make`

![alt text](https://github.com/stanislavsabev/wake/blob/main/wake.jpg?raw=true)

**NOTE:** Still in progress

## installation

```powershell
> git clone https://github.com/stanislavsabev/wake
> pip install .
```

## Usage

- Create file named `wakefile` in root directory
- Add labels (see sample [wakefile](#sample-wake))
- Run
  ```wake <label-name>```


## Sample *wakefile*

**NOTE: Still in progress**

```powershell
# This is a comment

# Choose between cmd or powershell, default is cmd
@shell: cmd


# This is a variable and it is used like this - $(VAR_NAME)
VAR_NAME=myvar


# This is a label. The syntax is actually
# label - colon - <options-list> - colon
# label: @flags: --o/opt @params: --k/key=val @deps: another-label @doc: ... :
label::
    # this is a shell command
    echo hello

# i/install is a label with shortcut.
# Shortcuts work with flags and params too, but there
# the short form must be called with single - and long form with --.
# @params is a build-in and expects
#   --key=value pairs, --key=* means any value
# --e/venv is restricted to the values in the tuple
# Example call:
#   wake venv -e env
venv: @params: e/venv=(env venv .venv) @doc: Create virtual environment :
    # Set variable using params shortcut for venv
    venv_name=@params.e
    # Multiple shell commands
    python -m venv $(venv_name)
    $(venv_name)/Scripts/activate
    python -m pip install --upgrade pip

# Multi-line label definitions are allowed
# @deps means that the `venv` label will be executed first with provided flags and params
# @flags is a build-in, flags are `true` if defined and `false` if omitted
i/install:
    @deps: venv -d --venv=env
    @flags: d/dev
    @doc: Install requirementsvenv
    :
    pip install pip-tools
    # Call another label like this
    @update --dev

    if @flags.dev:
        pip install -r requirements-dev.txt
    else:
        pip install -r requirements.txt
    pip install --editable my-package

# Param --run can be any value
# Param --mode is restricted to the values listed in the tuple, and default is DEBUG
# @doc, The colon after usage needs to be escaped with \, alternatively,
#       string can be wrapped in "" - "Usage: my-package [foo | bar]"
r/run:
    @params: run=* m/mode=DEBUG(DEBUG,RELEASE)
    @doc: Usage\: my-package [foo | bar]
    :
    # If-elseif statement
    if @params.run == "foo":
        # @* will pass all not captured flags/params to the shell command
        python -m my-package.foo --log_level @params.mode @args
    elif @params.run == "bar":
        python -m my-package.bar --log_level @params.m @args
    else:
        echo Unknown command to run
        # Print a label doc
        echo @run.doc
        # Or call the help label
        @help

u/update: @flags: --d/dev @doc: Update requirements :
    pip-compile requirements.in
    pip-compile requirements-dev.in

# h/help is a build-in, that prints each label and it's @doc + all options
# But help can be extended
h/help::
    echo Add extended help here
    @help # Call the build-in help

# --any can be any value or list of values.
# If a value contains spaces, it needs to be wrapped in quotes
# --single is restricted to one value
# --one-three is between one and three values
# Tuples are space delimited, if a value contains spaces, it needs to be wrapped in quotes
other: @flags: a b c
    @params:
        foos=(foo bar "foo bar")
        a/any=*
        s/single=*1
        one-three=*1,3
    :
    # Environment variables
    echo %MY_ENV_VAR% # cmd
    echo $env:MY_ENV_VAR% # powershell

    # foos is a tuple
    echo @params.foos
    echo @len.params.foos

    # @len is a build-in
    # check the length flags or params
    if @len.flags:
        echo @len.flags

    echo @len.params
    echo @len.deps

    # Print all non-captured args
    echo @args
    echo @len.args

    # Check of --any is provided (Optional)
    if @params.a:
        echo @params.any
    echo @params.s
    if @len.params.one-three > 1:
        echo @params.one-three

```
