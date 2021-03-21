@echo off

:: Calls DOSBOX to launch Star Trek 25th Anniversary

:: Written by Rebecca Ann Heineman
:: Olde Skuul

cd "%~dp0DOSBOX"

DOSBox.exe -conf "..\dosbox_st25.conf" -conf "..\dosbox_st25_single.conf" -noconsole -c exit
