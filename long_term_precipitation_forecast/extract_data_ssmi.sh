#export PANSAT_ON_THE_FLY=1 # Uncomment this to discard raw satellite data.
export OUTPUT_FOLDER=/path/to/training_data
chimp extract_data ssmi 1987 ? $OUTPUT_FOLDER --domain merra --time_step 1440 --n_processes 8
chimp extract_data ssmi 1988 ? $OUTPUT_FOLDER --domain merra --time_step 1440 --n_processes 8
chimp extract_data ssmi 1989 ? $OUTPUT_FOLDER --domain merra --time_step 1440 --n_processes 8
chimp extract_data ssmi 1990 ? $OUTPUT_FOLDER --domain merra --time_step 1440 --n_processes 8
chimp extract_data ssmi 1991 ? $OUTPUT_FOLDER --domain merra --time_step 1440 --n_processes 8
chimp extract_data ssmi 1992 ? $OUTPUT_FOLDER --domain merra --time_step 1440 --n_processes 8
chimp extract_data ssmi 1993 ? $OUTPUT_FOLDER --domain merra --time_step 1440 --n_processes 8
chimp extract_data ssmi 1994 ? $OUTPUT_FOLDER --domain merra --time_step 1440 --n_processes 8
chimp extract_data ssmi 1995 ? $OUTPUT_FOLDER --domain merra --time_step 1440 --n_processes 8
chimp extract_data ssmi 1996 ? $OUTPUT_FOLDER --domain merra --time_step 1440 --n_processes 8
chimp extract_data ssmi 1997 ? $OUTPUT_FOLDER --domain merra --time_step 1440 --n_processes 8
chimp extract_data ssmi 1998 ? $OUTPUT_FOLDER --domain merra --time_step 1440 --n_processes 8
chimp extract_data ssmi 1999 ? $OUTPUT_FOLDER --domain merra --time_step 1440 --n_processes 8
chimp extract_data ssmi 2000 ? $OUTPUT_FOLDER --domain merra --time_step 1440 --n_processes 8
chimp extract_data ssmi 2001 ? $OUTPUT_FOLDER --domain merra --time_step 1440 --n_processes 8
chimp extract_data ssmi 2002 ? $OUTPUT_FOLDER --domain merra --time_step 1440 --n_processes 8
chimp extract_data ssmi 2003 ? $OUTPUT_FOLDER --domain merra --time_step 1440 --n_processes 8
chimp extract_data ssmi 2004 ? $OUTPUT_FOLDER --domain merra --time_step 1440 --n_processes 8
chimp extract_data ssmi 2005 ? $OUTPUT_FOLDER --domain merra --time_step 1440 --n_processes 8
chimp extract_data ssmi 2006 ? $OUTPUT_FOLDER --domain merra --time_step 1440 --n_processes 8
chimp extract_data ssmi 2007 ? $OUTPUT_FOLDER --domain merra --time_step 1440 --n_processes 8
chimp extract_data ssmi 2008 ? $OUTPUT_FOLDER --domain merra --time_step 1440 --n_processes 8
chimp extract_data ssmi 2009 ? $OUTPUT_FOLDER --domain merra --time_step 1440 --n_processes 8
chimp extract_data ssmi 2010 ? $OUTPUT_FOLDER --domain merra --time_step 1440 --n_processes 8
chimp extract_data ssmi 2011 ? $OUTPUT_FOLDER --domain merra --time_step 1440 --n_processes 8
chimp extract_data ssmi 2012 ? $OUTPUT_FOLDER --domain merra --time_step 1440 --n_processes 8
chimp extract_data ssmi 2013 ? $OUTPUT_FOLDER --domain merra --time_step 1440 --n_processes 8
chimp extract_data ssmi 2014 ? $OUTPUT_FOLDER --domain merra --time_step 1440 --n_processes 8
chimp extract_data ssmi 2015 ? $OUTPUT_FOLDER --domain merra --time_step 1440 --n_processes 8
chimp extract_data ssmi 2016 ? $OUTPUT_FOLDER --domain merra --time_step 1440 --n_processes 8
chimp extract_data ssmi 2017 ? $OUTPUT_FOLDER --domain merra --time_step 1440 --n_processes 8
chimp extract_data ssmi 2018 ? $OUTPUT_FOLDER --domain merra --time_step 1440 --n_processes 8
chimp extract_data ssmi 2019 ? $OUTPUT_FOLDER --domain merra --time_step 1440 --n_processes 8

export OUTPUT_FOLDER=/path/to/test_data
chimp extract_data ssmi 2019 ? $OUTPUT_FOLDER --domain merra --time_step 1440 --n_processes 4
chimp extract_data ssmi 2020 ? $OUTPUT_FOLDER --domain merra --time_step 1440 --n_processes 4
chimp extract_data ssmi 2021 ? $OUTPUT_FOLDER --domain merra --time_step 1440 --n_processes 4
chimp extract_data ssmi 2022 ? $OUTPUT_FOLDER --domain merra --time_step 1440 --n_processes 4
chimp extract_data ssmi 2023 ? $OUTPUT_FOLDER --domain merra --time_step 1440 --n_processes 4
