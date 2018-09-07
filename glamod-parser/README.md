# The GLAMOD Parser

A utility for managing deliveries of data sets in the agreed interface format
(pipe-separated values, or `.psv`).

The parser contains the following functionality:

 1. Read the input files:
  - Header Table
  - Observations Table
  - Source Configuration 
  - Station Configuration

 2. Check the contents of the files against a set of rules agreed within the project:
  - type-checking
  - look-ups to external (code) tables
  - look-ups to other content provided in the data delivery files 
 
 3. Map the contents to the database structure based on:
  - simple one-to-one mappings
  - and complex mappings described in the mapping rules 

 4. Load the Django database interface:
  - to allow reading and writing to production DB

 5. Write the records to the DB

 6. Generate reports about the process:
  - log all successes and failues
  - generate a summary report 
  - send report to relevant people 
