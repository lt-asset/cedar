#!/bin/bash

# home='/home'
# usage: bash statistics/prepair_bug_list.sh /..../workdir expect_exception_constr

subpath=$1
workdir=$(dirname $subpath)
# subdir=$2


# subpath=$workdir/$subdir
pushd $subpath > /dev/null
tmp_api=$workdir/tmp_api
tmp_type=$workdir/tmp_type
tmp_input=$workdir/tmp_input
echo "Extracting API names"
# find . -regex '\.\/\(Floating_Point_Exception\|Abort\|Segmentation_Fault\)_script_record'  | sort -k 1 | cut -d"/" -f2 | sed 's/.yaml_workdir//g' > $tmp_api  #extract API name
find . -name '*_script_record' -not -iname 'failure*' -not -iname 'timeout*' -not -iname 'kill*' -not -iname 'nan*' -not -iname 'division_by_zero*' | sort -k 1 | cut -d"/" -f2 | sed 's/.yaml_workdir//g' > $tmp_api  #extract API name
echo "Extracting bug types"
# find . -regex '\.\/\(Floating_Point_Exception\|Abort\|Segmentation_Fault\)_script_record' | sort -k 1 | cut -d"/" -f3 | sed 's/_script_record//g' > $tmp_type #extract bug tpye
find . -name '*_script_record' -not -iname 'failure*' -not -iname 'timeout*' -not -iname 'kill*' -not -iname 'nan*' -not -iname 'division_by_zero*' | sort -k 1 | cut -d"/" -f3 | sed 's/_script_record//g' > $tmp_type #extract bug tpye
echo "Extracting input count and input script path"
# find . -regex '\.\/\(Floating_Point_Exception\|Abort\|Segmentation_Fault\)_script_record' -type f -print0 | wc -l --files0-from=- | sort -k 2 | sed '$ d' | sed "s~ \.~,$subpath~g" > $tmp_input #extract input count and input script
find . -name '*_script_record' -not -iname 'failure*' -not -iname 'timeout*' -not -iname 'kill*' -not -iname 'nan*' -not -iname 'division_by_zero*' -type f -print0 | wc -l --files0-from=- | sort -k 2 | sed '$ d' | sed "s~ \.~,$subpath~g" > $tmp_input #extract input count and input script
popd > /dev/null
tmp_1=$workdir/tmp_1
tmp_2=$workdir/tmp_2
# append columns
echo "Creating bug list"
bug_list=$subpath/bug_list
paste -d "," $tmp_api <(awk '{print $0}' $tmp_type) > $tmp_1 
paste -d "," $tmp_1 <(awk '{print $0}' $tmp_input) > $tmp_2
echo "API,Type,Count,Input" | cat - $tmp_2 > $bug_list #add header
rm -f $tmp_api $tmp_type $tmp_input $tmp_1 $tmp_2
