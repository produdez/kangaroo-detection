# DVC NOTES

- Only write needed things to output if the output is dependency for next stage
- Do not use explicit name as key for `dag.yaml`'s stage.params
- Use external file as params for stage with

```[yaml]
params:
 - external_file.yaml: # this means include all
 - another_file.yaml: # this means only get some keys
  - key1
  - key2
```

- user `-u` tag so that python output is not buffered (which leads to delayed terminal output) when used with pipe `|` and `tee`
- Do not put `config.yaml` file as dependency for a stage cause we only need some keys from it, put it in `params` instead
- Yes you can use explicit name as key for `dvc.yaml` multiline

```[yaml]
outs:
 - ${train.model.output}:
  persist: true
```

- Use `persist` for outputs you dont wanna get deleted instantly when `dvc repro` runs
- Must use `always_change` flags for stages you want to rerun all the time (this wont trigger others unless the output changes)
