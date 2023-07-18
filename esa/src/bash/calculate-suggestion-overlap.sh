#!/bin/bash

if [ $# -lt 2 ];then
  echo "$0 <suggestions.csv> <method1> <method2> [<method3> [...]]"
  echo "$0 <suggestions.csv> '*'"
  exit 1
fi

suggestions_file=$1
shift

if [ "$1" == "*" ];then
  methods=$(tail -n +2 $suggestions_file | cut -d, -f3 | sort | uniq)
  $0 $suggestions_file $methods
  exit 0
fi

tmp_dir=/tmp/suggestion-overlap-$$
mkdir -p $tmp_dir

for method in $@;do
  cat $suggestions_file | grep ",$method," | cut -d, -f1-2 | sort > $tmp_dir/$method.txt
done

method1=$1
shift

while [ ! \( -z "$1" \) ];do
  for method2 in $@;do
    echo -n "$method1 $method2 "
    num_common=$(comm -12 $tmp_dir/$method1.txt $tmp_dir/$method2.txt | wc -l)
    num_total=$(comm $tmp_dir/$method1.txt $tmp_dir/$method2.txt | wc -l)
    echo "$num_common $num_total" | awk '{printf "%d/%d = %.2f\n", $1, $2, $1/$2}'
  done
  method1=$1
  shift
done

rm -rf $tmp_dir

