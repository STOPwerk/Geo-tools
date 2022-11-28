@echo off

if "A%1" == "A" goto MijnVoorbeelden
call %~dp0voer_tools_uit.bat --meldingen %~dp0logs %1 %2 %3 %4 %5 %6 %7
goto End
:MijnVoorbeelden
call %~dp0voer_tools_uit.bat --meldingen %~dp0logs --alle "mijn voorbeelden"

:End
