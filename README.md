Utility to add a possibility to send queries to claude sonnet from terminal, get relevant commands, and access them from history by using arrow keys.

usage:

add this to your .bash_aliases , replace $PATH_TO_SCRIPT_DIR with the folder you cloned this repo into

```
cq(){
	(cd /$PATH_TO_SCRIPT_DIR && uv run main.py query $@)
	history -n

}

ca(){
	(cd /$PATH_TO_SCRIPT_DIR && "$@" 2>&1 | uv run main.py assist)
	history -n

}
```

