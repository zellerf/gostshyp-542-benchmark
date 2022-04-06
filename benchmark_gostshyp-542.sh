#!/bin/bash

# script to submit calculations for benchmark of the improved gostshyp method as implemented in Qchem 5.4.2

# usage: script geoms

# geoms: file with all geometries to calculate

#The script needs two different installed versions of Qchem: Qchem 5.4.2 and an older version with old gostshyp implementation

# Qchem path variables
# Qchem path variable to qchem 5.4.2 with new gostshyp
QCnew='/home/zellerf/qchem/qc542'
# Qchem path variable to qchem 5.4.1 or older with old gostshyp implementation
QCold='/opt/qchem-5.4'

#number of threads to use
nthreads=12

#number of scfcycles
cycles=50

#Assign geometries
geoms="$1"

# variable for crashed files
crashed_file=false
#error for none specified filename
if [ -z "$geoms" ]; then
	echo "ERROR: no directory for geometries specified"	
	exit 1
fi

#error for not filename
if [ ! -d "$geoms" ]; then
        echo "ERROR: directory $geoms does not exist"  
        exit 1
fi

#set execution dir
dir=$(pwd)
cd "$dir"

#create logfile
if [ -f "benchmark.log" ]; then
        echo "Warning: logfile already exists, appending to exsting log"
fi

touch 'benchmark.log'

#
# loop through geometries put in geoms directory
#

for filename in "$dir"/"$geoms"*.xyz ; do
	
	#
	# create input
	#

	name="$(basename "$filename" .xyz)"
	touch "$name.in"
	printf '%s\n' '$molecule' '0 1'  >> "$name.in" 
	
	#read geometry
	i=0 #counter
	while read line; do
	if (( $i > 1 )); then 
		echo "$line" >> "$name.in"
	fi
	let i++
	done < "$filename"	

	printf '%s\n' '$end' ''  >> "$name.in"
	printf '%s\n' '$rem' 'method hf' 'basis cc-pvdz' 'jobtype opt' 'mem_total 30000' "max_scf_cycles $cycles" 'geom_opt_max_cycles 300' 'sym_ignore true' 'distort 1' '$end' '' >> "$name.in"
	printf '%s\n' '$distort' 'model gostshyp' 'pressure' 'scaling' '$end' >> "$name.in"

	mkdir "$name"
	cd "$name"
	
	# loop pressures
        # for p in {p_start .. p_end .. p_increment}
        for p in {10000..110000..25000} # p in MPa
        do
 		# loop scaling factors
		for s in $(LANG=en seq 1.0 0.5 2.0) # scaling factor
		do	
		       	#check if dir exists
       		        if [ ! -d "$p""_scal-$s" ]; then
                        	mkdir "$p""_scal-$s"
                	fi

                	cd  "$p""_scal-$s"
                	cp $dir/"$name.in" "$name""_$p""_scal-$s.in"

                	#replace pressure in file
                	sed -i "s/pressure/pressure $p/" "$name""_$p""_scal-$s.in"

			#replace scaling in file
                        sed -i "s/scaling/scaling $s/" "$name""_$p""_scal-$s.in"


                	#calc reference file
			export QC="$QCold"
                	qchem -nt "$nthreads" "$name""_$p""_scal-$s.in" "$name""_$p""_scal-$s.ref"

			#calc 
			export QC="$QCnew"
                	qchem -nt "$nthreads" "$name""_$p""_scal-$s.in" "$name""_$p""_scal-$s.out"

                	# Check outputs for crashs
                	if ! grep -q "Thank you very much for using Q-Chem.  Have a nice day." "$name""_$p""_scal-$s.ref"; then
                	        echo  "$name""_$p"_scal-$s".ref file crashed" >> "$dir""/benchmark.log"
                	        crashed_file=true
                	fi

			if ! grep -q "Thank you very much for using Q-Chem.  Have a nice day." "$name""_$p""_scal-$s.out"; then
                       	 	echo  "$name""_$p"_scal-$s".out file crashed" >> "$dir""/benchmark.log"
                        	crashed_file=true
                	fi
		
			cd ..	
		done
        done
	
	#cleanup
	cd "$dir"
	rm "$name.in" 
done

#print Warning if crashs were detected during benchmark
if [ $crashed_file = true ]; then
        echo "Warning: crashed calculations during benchmark. check logfile for additional information"
fi
