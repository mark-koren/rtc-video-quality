while getopts ":p:" opt; do
  case "$opt" in
    p) preset=$OPTARG ;;
  esac
done
shift $(( OPTIND - 1 ))
echo "$preset"

case "$preset" in
	all) 

for run_name in "$@"; do
	echo "$run_name"
done