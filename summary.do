clear all
set mem 2g

gl subs _ACCOUNTING _ECONOMICS _ENTREPRENEURSHIP _FINANCE _INFORMATION _INTERNATIONAL _MANAGEMENT _MARKETING _PRACTITIONER

// master files
cd "C:\\Users\\yling\\WOS\\JOURNAL\\csv2"
foreach sub in $subs {
	di "`sub'"
	local files: dir "C:\\Users\\yling\\WOS\\JOURNAL\\csv2\\`sub'" files "*.csv"
	clear
	set obs 1
	foreach file in `files' {
		di "`file'"
		preserve
		di "`file'"
		insheet using "`sub'\\`file'", comma clear names
		drop reprintaddress
		tempfile 1
		save "`1'"
		restore
		append using "`1'", force
	}
	drop in 1
	duplicates drop
	save "`sub'.dta", replace
}

// address files
cd "C:\\Users\\yling\\WOS\\JOURNAL\\addresses"
foreach sub in $subs {
	di "`sub'"
	local files: dir "C:\\Users\\yling\\WOS\\JOURNAL\\addresses\\`sub'" files "*.csv"
	clear
	set obs 1
	g title=""
	g issn=""
	g doi=""
	g author=""
	g address=""
	foreach file in `files' {
		di "`file'"
		preserve
		di "`file'"
		insheet using "`sub'\\`file'", comma clear names
		tempfile 1
		save "`1'"
		restore
		append using "`1'", force
	}
	duplicates drop
	drop in 1
	save "address`sub'.dta", replace
}

// reprint address files
cd "C:\\Users\\yling\\WOS\\JOURNAL\\reprint address"
foreach sub in $subs {
	di "`sub'"
	local files: dir "C:\\Users\\yling\\WOS\\JOURNAL\\reprint address\\`sub'" files "*.csv"
	clear
	set obs 1
	g title=""
	g issn=""
	g doi=""
	g author=""
	g reprintaddress=""
	foreach file in `files' {
		di "`file'"
		preserve
		di "`file'"
		insheet using "`sub'\\`file'", comma clear names
		tempfile 1
		save "`1'"
		restore
		append using "`1'", force
	}
	duplicates drop
	drop in 1
	save "reprint address`sub'.dta", replace
}
foreach sub in $subs {
	di "`sub'"
	use "reprint address`sub'", clear
	split reprintaddress, parse("(reprint author),")
	replace reprintaddress1 = trim(reprintaddress1)
	replace reprintaddress2 = trim(reprintaddress2)
	g reprint_author = reprintaddress1 if reprintaddress2~=""
	replace reprint_author = "" if reprintaddress2==""
	g reprint_address = reprintaddress2 if reprintaddress2~=""
	replace reprint_address = reprintaddress1 if reprintaddress2==""
	drop reprintaddress*
	save "reprint address`sub'", replace
}
// multiple reprint authors same reprint address case
foreach sub in $subs {
	di "`sub'"
	use "reprint address`sub'", clear
	split reprint_author, parse(";")
	g n = _n
	drop reprint_author
	reshape long reprint_author, i(n title issn doi reprint_address) j(j)
	drop if reprint_author==""
	sort n j
	drop n j
	keep title issn doi reprint_author reprint_address
	order title issn doi reprint_author reprint_address
	save "reprint address`sub'", replace
}


// cut->dta
cd "C:\\Users\\yling\\WOS\\JOURNAL\\dta"
foreach sub in $subs {
	di "`sub'"
	use "`sub'", clear
	merge m:m title issn doi using "address`sub'"
	ren _merge address_indicator
	merge m:m title issn doi using "reprint address`sub'"
	ren _merge reprint_address_indicator
	keep title issn doi address_indicator reprint_address_indicator
	duplicates drop
	g address=1 if (address_indicator==3 | reprint_address_indicator==3)
	replace address=0 if address==.
	save "summary`sub'", replace
}




